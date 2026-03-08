package cz.kajovomail.data

data class MailAccount(
    val id: String,
    val email: String,
    val provider: String,
    val providerType: String,
    val displayName: String?,
    val capabilityFlags: List<String>
)
data class MailFolder(val id: String, val name: String, val accountId: String)
data class MailMessage(
    val id: String,
    val subject: String,
    val sender: String,
    val snippet: String,
    val body: String?,
    val folderId: String,
    val createdAt: String?
)
data class OfferItem(val id: String, val title: String, val state: String)
data class AIResponse(val summary: String, val htmlPreview: String, val policy: String)
data class ComposeState(
    val recipient: String = "",
    val subject: String = "",
    val body: String = "",
    val accountId: String? = null
)
data class AISettings(
    val hasOpenAIApiKey: Boolean = false,
    val openAIApiKeyMasked: String = "",
    val responseStyle: String = "balanced",
    val model: String = ""
)
