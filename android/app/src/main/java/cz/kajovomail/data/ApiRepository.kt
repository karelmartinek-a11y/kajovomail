package cz.kajovomail.data

import android.content.Context
import androidx.security.crypto.EncryptedSharedPreferences
import androidx.security.crypto.MasterKey
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import okhttp3.MediaType.Companion.toMediaType
import okhttp3.OkHttpClient
import okhttp3.Request
import okhttp3.RequestBody.Companion.toRequestBody
import org.json.JSONArray
import org.json.JSONObject
import java.net.URLEncoder

class ApiRepository(private val context: Context) {
    private val client = OkHttpClient()
    private val prefs by lazy {
        val masterKey = MasterKey.Builder(context).setKeyScheme(MasterKey.KeyScheme.AES256_GCM).build()
        EncryptedSharedPreferences.create(
            context,
            "kajovomail_session",
            masterKey,
            EncryptedSharedPreferences.PrefKeyEncryptionScheme.AES256_SIV,
            EncryptedSharedPreferences.PrefValueEncryptionScheme.AES256_GCM
        )
    }

    private val baseUrl = BuildConfig.BACKEND_URL

    private fun encode(value: String): String = URLEncoder.encode(value, "UTF-8")

    private fun authRequest(url: String): Request.Builder {
        val builder = Request.Builder().url(url)
        prefs.getString("sessionCookie", null)?.let { builder.addHeader("Cookie", it) }
        prefs.getString("csrf", null)?.takeIf { it.isNotBlank() }?.let { builder.addHeader("x-csrf-token", it) }
        return builder
    }

    private fun currentUserId(): Int? {
        val userId = prefs.getInt("userId", -1)
        return if (userId >= 0) userId else null
    }

    suspend fun login(email: String, password: String): Boolean = withContext(Dispatchers.IO) {
        val payload = JSONObject().apply {
            put("email", email)
            put("password", password)
        }
        val request = Request.Builder()
            .url("$baseUrl/session/login")
            .post(payload.toString().toRequestBody("application/json; charset=utf-8".toMediaType()))
            .build()
        val response = client.newCall(request).execute()
        if (!response.isSuccessful) throw Exception("Přihlášení selhalo")
        val body = response.body?.string().orEmpty()
        val json = JSONObject(body)
        val setCookie = response.header("Set-Cookie").orEmpty()
        val sessionPair = setCookie.split(";").firstOrNull { it.contains("kajovo_session=") } ?: ""
        if (sessionPair.isNotBlank()) {
            prefs.edit().putString("sessionCookie", sessionPair).apply()
        }
        val csrf = json.optString("csrfToken")
        prefs.edit().putString("csrf", csrf).apply()
        val userId = json.optJSONObject("user")?.optInt("id", -1) ?: -1
        if (userId >= 0) {
            prefs.edit().putInt("userId", userId).apply()
        }
        prefs.edit().putString("currentUser", email).apply()
        true
    }

    suspend fun fetchAccounts(): List<MailAccount> = withContext(Dispatchers.IO) {
        val request = authRequest("$baseUrl/accounts").build()
        val response = client.newCall(request).execute()
        if (!response.isSuccessful) return@withContext emptyList()
        val array = JSONArray(response.body?.string().orEmpty().ifBlank { "[]" })
        val list = mutableListOf<MailAccount>()
        for (i in 0 until array.length()) {
            val item = array.optJSONObject(i) ?: continue
            val capabilities = item.optJSONArray("capability_flags") ?: JSONArray()
            val flags = mutableListOf<String>()
            for (j in 0 until capabilities.length()) {
                capabilities.optString(j).takeIf { it.isNotBlank() }?.let { flags.add(it) }
            }
            list.add(
                MailAccount(
                    id = item.optString("id"),
                    email = item.optString("email"),
                    provider = item.optString("provider"),
                    providerType = item.optString("provider_type"),
                    displayName = item.optString("display_name").takeIf { it.isNotBlank() },
                    capabilityFlags = flags
                )
            )
        }
        list
    }

    suspend fun fetchMessages(accountId: String): List<MailMessage> = withContext(Dispatchers.IO) {
        val encodedAccount = encode(accountId)
        val request = authRequest("$baseUrl/messages?account_id=$encodedAccount").build()
        val response = client.newCall(request).execute()
        if (!response.isSuccessful) return@withContext emptyList()
        parseMessageArray(response.body?.string().orEmpty())
    }

    suspend fun searchMessages(accountId: String, query: String, folderId: String? = null): List<MailMessage> =
        withContext(Dispatchers.IO) {
            val encodedAccount = encode(accountId)
            val encodedQuery = encode(query)
        val params = StringBuilder("?account_id=$encodedAccount&q=$encodedQuery")
            folderId?.takeIf { it.isNotBlank() }?.let {
                params.append("&folder_id=${encode(it)}")
            }
            val request = authRequest("$baseUrl/search$params").build()
            val response = client.newCall(request).execute()
            if (!response.isSuccessful) return@withContext emptyList()
            parseMessageArray(response.body?.string().orEmpty())
        }

    private fun parseMessageArray(body: String): List<MailMessage> {
        val array = JSONArray(body.ifBlank { "[]" })
        val list = mutableListOf<MailMessage>()
        for (i in 0 until array.length()) {
            val item = array.optJSONObject(i) ?: continue
            val bodyText = item.optString("body", "").ifBlank { null }
            val snippet = item.optString("snippet").takeIf { it.isNotBlank() }
                ?: bodyText?.take(160) ?: ""
            list.add(
                MailMessage(
                    id = item.optString("id"),
                    subject = item.optString("subject"),
                    sender = item.optString("sender", "neznámý"),
                    snippet = snippet,
                    body = bodyText,
                    folderId = item.optString("folder_id"),
                    createdAt = item.optString("created_at").takeIf { it.isNotBlank() }
                )
            )
        }
        return list
    }

    suspend fun fetchOffers(): List<OfferItem> = withContext(Dispatchers.IO) {
        // Backend does not expose a global list currently
        emptyList()
    }

    suspend fun sendDraft(composeState: ComposeState) {
        withContext(Dispatchers.IO) {
            val accountId = composeState.accountId
            val userId = currentUserId() ?: throw Exception("Uživatel není přihlášen.")
            if (accountId.isNullOrBlank()) throw Exception("Zašlete účet")
            val payload = JSONObject().apply {
                put("user_id", userId)
                put("account_id", accountId.toIntOrNull() ?: accountId)
                put("plaintext", composeState.body)
                put("html", composeState.body)
            }
            val request = authRequest("$baseUrl/drafts/")
                .post(payload.toString().toRequestBody("application/json; charset=utf-8".toMediaType()))
                .build()
            val response = client.newCall(request).execute()
            if (!response.isSuccessful) throw Exception("Ukládání konceptu selhalo.")
        }
    }

    suspend fun fetchAISettings(): AISettings = withContext(Dispatchers.IO) {
        val request = authRequest("$baseUrl/settings/ai").build()
        val response = client.newCall(request).execute()
        if (!response.isSuccessful) throw Exception("Načtení AI nastavení selhalo")
        val payload = JSONObject(response.body?.string().orEmpty())
        AISettings(
            hasOpenAIApiKey = payload.optBoolean("has_openai_api_key"),
            openAIApiKeyMasked = payload.optString("openai_api_key_masked", ""),
            responseStyle = payload.optString("response_style", "balanced"),
            model = payload.optString("model", "")
        )
    }

    suspend fun updateAISettings(apiKey: String?, responseStyle: String, model: String?): Boolean =
        withContext(Dispatchers.IO) {
            val payload = JSONObject().apply {
                if (!apiKey.isNullOrBlank()) put("openai_api_key", apiKey)
                put("response_style", responseStyle)
                if (!model.isNullOrBlank()) put("model", model)
            }
            val request = authRequest("$baseUrl/settings/ai")
                .put(payload.toString().toRequestBody("application/json; charset=utf-8".toMediaType()))
                .build()
            val response = client.newCall(request).execute()
            response.isSuccessful
        }

    suspend fun testAIKey(apiKey: String?): Pair<String, List<String>> = withContext(Dispatchers.IO) {
        val payload = JSONObject().apply {
            if (!apiKey.isNullOrBlank()) put("openai_api_key", apiKey)
        }
        val request = authRequest("$baseUrl/settings/ai/test-key")
            .post(payload.toString().toRequestBody("application/json; charset=utf-8".toMediaType()))
            .build()
        val response = client.newCall(request).execute()
        val body = JSONObject(response.body?.string().orEmpty())
        val message = body.optString("message", "Test API klíče selhal")
        val modelsJson = body.optJSONArray("models") ?: JSONArray()
        val models = mutableListOf<String>()
        for (i in 0 until modelsJson.length()) {
            models.add(modelsJson.optString(i))
        }
        Pair(message, models)
    }

    suspend fun loadAIModels(): List<String> = withContext(Dispatchers.IO) {
        val request = authRequest("$baseUrl/settings/ai/models").build()
        val response = client.newCall(request).execute()
        if (!response.isSuccessful) throw Exception("Načtení modelů selhalo")
        val payload = JSONObject(response.body?.string().orEmpty())
        val modelsJson = payload.optJSONArray("models") ?: JSONArray()
        val models = mutableListOf<String>()
        for (i in 0 until modelsJson.length()) {
            models.add(modelsJson.optString(i))
        }
        models
    }

    suspend fun requestAI(prompt: String, accountId: String?): AIResponse = withContext(Dispatchers.IO) {
        val payload = JSONObject().apply {
            put("body", prompt)
            accountId?.takeIf { it.isNotBlank() }?.let { put("account_id", it) }
        }
        val request = authRequest("$baseUrl/ai/")
            .post(payload.toString().toRequestBody("application/json; charset=utf-8".toMediaType()))
            .build()
        val response = client.newCall(request).execute()
        if (!response.isSuccessful) throw Exception("AI orchestrace selhala.")
        val body = JSONObject(response.body?.string().orEmpty())
        val result = body.optJSONObject("result") ?: JSONObject()
        AIResponse(
            summary = result.optString("plaintext", ""),
            htmlPreview = result.optString("html", ""),
            policy = result.optString("status", "")
        )
    }
}
