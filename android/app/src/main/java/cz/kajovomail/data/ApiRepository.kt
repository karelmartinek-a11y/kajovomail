package cz.kajovomail.data

import android.content.Context
import androidx.security.crypto.EncryptedSharedPreferences
import androidx.security.crypto.MasterKey
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import okhttp3.OkHttpClient
import okhttp3.MediaType.Companion.toMediaType
import okhttp3.RequestBody.Companion.toRequestBody
import okhttp3.Request
import okhttp3.FormBody
import org.json.JSONObject
import org.json.JSONArray

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

    private fun authRequest(url: String): Request.Builder {
        val builder = Request.Builder().url(url)
        prefs.getString("sessionCookie", null)?.let { builder.addHeader("Cookie", it) }
        prefs.getString("csrf", null)?.takeIf { it.isNotBlank() }?.let { builder.addHeader("x-csrf-token", it) }
        return builder
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
        val payload = JSONObject(response.body?.string().orEmpty())
        val setCookie = response.header("Set-Cookie").orEmpty()
        val sessionPair = setCookie.split(";").firstOrNull { it.contains("kajovo_session=") } ?: ""
        if (sessionPair.isNotBlank()) {
            prefs.edit().putString("sessionCookie", sessionPair).apply()
        }
        prefs.edit().putString("csrf", payload.optString("csrfToken")).apply()
        prefs.edit().putString("currentUser", email).apply()
        true
    }

    suspend fun fetchAccounts(): List<MailAccount> = withContext(Dispatchers.IO) {
        val request = authRequest("$baseUrl/accounts").build()
        val response = client.newCall(request).execute()
        if (!response.isSuccessful) return@withContext emptyList()
        emptyList()
    }

    suspend fun fetchMessages(folderId: String): List<MailMessage> = withContext(Dispatchers.IO) {
        val request = authRequest("$baseUrl/folders/$folderId/messages").build()
        val response = client.newCall(request).execute()
        if (!response.isSuccessful) return@withContext emptyList()
        emptyList()
    }

    suspend fun fetchOffers(): List<OfferItem> = withContext(Dispatchers.IO) {
        val request = authRequest("$baseUrl/offers").build()
        val response = client.newCall(request).execute()
        if (!response.isSuccessful) return@withContext emptyList()
        emptyList()
    }

    suspend fun sendDraft(composeState: ComposeState) {
        withContext(Dispatchers.IO) {
            val request = Request.Builder()
                .url("$baseUrl/drafts/send")
                .post(FormBody.Builder()
                    .add("to", composeState.recipient)
                    .add("subject", composeState.subject)
                    .add("body", composeState.body)
                    .build())
                .build()
            client.newCall(request).execute()
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

    suspend fun requestAI(prompt: String): AIResponse = withContext(Dispatchers.IO) {
        AIResponse(
            summary = "Zástupný AI souhrn",
            htmlPreview = "<p>Náhled</p>",
            policy = "ukládání: ne"
        )
    }
}
