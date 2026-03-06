package cz.kajovomail.data

import android.content.Context
import androidx.security.crypto.EncryptedSharedPreferences
import androidx.security.crypto.MasterKey
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import okhttp3.OkHttpClient
import okhttp3.Request
import org.json.JSONObject

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

    suspend fun login(email: String, password: String): Boolean = withContext(Dispatchers.IO) {
        val request = Request.Builder()
            .url("$baseUrl/session/login")
            .post(okhttp3.FormBody.Builder().add("email", email).add("password", password).build())
            .build()
        val response = client.newCall(request).execute()
        if (!response.isSuccessful) throw Exception("Failed to login")
        val payload = JSONObject(response.body?.string().orEmpty())
        prefs.edit().putString("csrf", payload.optString("csrfToken")).apply()
        prefs.edit().putString("currentUser", email).apply()
        true
    }

    suspend fun fetchAccounts(): List<MailAccount> = withContext(Dispatchers.IO) {
        val request = Request.Builder().url("$baseUrl/accounts").build()
        val response = client.newCall(request).execute()
        if (!response.isSuccessful) return@withContext emptyList()
        emptyList()
    }

    suspend fun fetchMessages(folderId: String): List<MailMessage> = withContext(Dispatchers.IO) {
        val request = Request.Builder().url("$baseUrl/folders/$folderId/messages").build()
        val response = client.newCall(request).execute()
        if (!response.isSuccessful) return@withContext emptyList()
        emptyList()
    }

    suspend fun fetchOffers(): List<OfferItem> = withContext(Dispatchers.IO) {
        val request = Request.Builder().url("$baseUrl/offers").build()
        val response = client.newCall(request).execute()
        if (!response.isSuccessful) return@withContext emptyList()
        emptyList()
    }

    suspend fun sendDraft(composeState: ComposeState) {
        withContext(Dispatchers.IO) {
            val request = Request.Builder()
                .url("$baseUrl/drafts/send")
                .post(okhttp3.FormBody.Builder()
                    .add("to", composeState.recipient)
                    .add("subject", composeState.subject)
                    .add("body", composeState.body)
                    .build())
                .build()
            client.newCall(request).execute()
        }
    }

    suspend fun requestAI(prompt: String): AIResponse = withContext(Dispatchers.IO) {
        AIResponse(
            summary = "AI summary placeholder",
            htmlPreview = "<p>Preview</p>",
            policy = "store: false"
        )
    }
}
