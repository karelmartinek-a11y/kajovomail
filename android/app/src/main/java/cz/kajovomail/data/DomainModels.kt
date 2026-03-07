package cz.kajovomail.data

data class MailAccount(val id: String, val email: String, val provider: String)
data class MailFolder(val id: String, val name: String)
data class MailMessage(val id: String, val subject: String, val sender: String, val snippet: String)
data class OfferItem(val id: String, val title: String, val state: String)
data class AIResponse(val summary: String, val htmlPreview: String, val policy: String)
data class ComposeState(val recipient: String = "", val subject: String = "", val body: String = "")
data class AISettings(
    val hasOpenAIApiKey: Boolean = false,
    val openAIApiKeyMasked: String = "",
    val responseStyle: String = "balanced",
    val model: String = ""
)
