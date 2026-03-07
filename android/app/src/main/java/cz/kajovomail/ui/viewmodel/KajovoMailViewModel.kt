package cz.kajovomail.ui.viewmodel

import android.app.Application
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateListOf
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.setValue
import androidx.lifecycle.AndroidViewModel
import androidx.lifecycle.viewModelScope
import cz.kajovomail.data.ApiRepository
import cz.kajovomail.data.ComposeState
import cz.kajovomail.data.MailAccount
import cz.kajovomail.data.MailMessage
import cz.kajovomail.data.OfferItem
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch

class KajovoMailViewModel(application: Application) : AndroidViewModel(application) {
    private val repository = ApiRepository(application)

    val loginState = mutableStateOf(LoginForm())
    var composeState by mutableStateOf(ComposeState())

    private val _accounts = MutableStateFlow<List<MailAccount>>(emptyList())
    val accounts: StateFlow<List<MailAccount>> = _accounts.asStateFlow()

    private val _messages = MutableStateFlow<List<MailMessage>>(emptyList())
    val messages: StateFlow<List<MailMessage>> = _messages.asStateFlow()

    val offers = mutableStateListOf<OfferItem>()
    var aiPrompt by mutableStateOf("")
    var aiResponse by mutableStateOf("")
    var aiApiKey by mutableStateOf("")
    var aiApiKeyMasked by mutableStateOf("")
    var aiResponseStyle by mutableStateOf("balanced")
    var aiSelectedModel by mutableStateOf("")
    val aiModels = mutableStateListOf<String>()
    var aiSettingsStatus by mutableStateOf("AI nastavení zatím nebylo načteno.")
    private var _selectedMessage: MailMessage? = null
    val selectedMessage get() = _selectedMessage

    fun onEmailChanged(value: String) {
        loginState.value = loginState.value.copy(email = value)
    }

    fun onPasswordChanged(value: String) {
        loginState.value = loginState.value.copy(password = value)
    }

    fun login(onSuccess: () -> Unit) {
        viewModelScope.launch {
            try {
                repository.login(loginState.value.email, loginState.value.password)
                loadAccounts()
                loadOffers()
                onSuccess()
            } catch (e: Exception) {
                aiSettingsStatus = e.message ?: "Přihlášení selhalo."
            }
        }
    }

    private fun loadAccounts() {
        viewModelScope.launch {
            _accounts.value = repository.fetchAccounts()
        }
    }

    private fun loadOffers() {
        viewModelScope.launch {
            offers.clear()
            offers.addAll(repository.fetchOffers())
        }
    }

    fun selectVirtualView(view: String) {}

    fun onRecipientChanged(value: String) {
        composeState = composeState.copy(recipient = value)
    }

    fun onSubjectChanged(value: String) {
        composeState = composeState.copy(subject = value)
    }

    fun onBodyChanged(value: String) {
        composeState = composeState.copy(body = value)
    }

    fun sendDraft() {
        viewModelScope.launch {
            repository.sendDraft(composeState)
        }
    }

    fun logout() {
        loginState.value = LoginForm()
        composeState = ComposeState()
        _accounts.value = emptyList()
        _messages.value = emptyList()
        offers.clear()
        aiPrompt = ""
        aiResponse = ""
    }

    fun loadAISettings() {
        viewModelScope.launch {
            try {
                val settings = repository.fetchAISettings()
                aiApiKeyMasked = settings.openAIApiKeyMasked
                aiResponseStyle = settings.responseStyle
                aiSelectedModel = settings.model
                aiSettingsStatus = if (settings.hasOpenAIApiKey) {
                    "Uložený klíč: ${settings.openAIApiKeyMasked}"
                } else {
                    "API klíč zatím není nastaven."
                }
            } catch (e: Exception) {
                aiSettingsStatus = e.message ?: "Načtení AI nastavení selhalo."
            }
        }
    }

    fun saveAISettings() {
        viewModelScope.launch {
            val ok = repository.updateAISettings(
                apiKey = aiApiKey.takeIf { it.isNotBlank() },
                responseStyle = aiResponseStyle,
                model = aiSelectedModel.takeIf { it.isNotBlank() }
            )
            aiSettingsStatus = if (ok) {
                aiApiKey = ""
                "AI nastavení bylo uloženo."
            } else {
                "Uložení AI nastavení selhalo."
            }
        }
    }

    fun testAIKey() {
        viewModelScope.launch {
            try {
                val (message, models) = repository.testAIKey(aiApiKey.takeIf { it.isNotBlank() })
                aiSettingsStatus = message
                aiModels.clear()
                aiModels.addAll(models)
                if (aiSelectedModel.isBlank() && models.isNotEmpty()) {
                    aiSelectedModel = models.first()
                }
            } catch (e: Exception) {
                aiSettingsStatus = e.message ?: "Test API klíče selhal."
            }
        }
    }

    fun loadAIModels() {
        viewModelScope.launch {
            try {
                val models = repository.loadAIModels()
                aiModels.clear()
                aiModels.addAll(models)
                if (aiSelectedModel.isBlank() && models.isNotEmpty()) {
                    aiSelectedModel = models.first()
                }
                aiSettingsStatus = "Načteno modelů: ${models.size}."
            } catch (e: Exception) {
                aiSettingsStatus = e.message ?: "Načtení modelů selhalo."
            }
        }
    }

    fun onAiApiKeyChanged(value: String) {
        aiApiKey = value
    }

    fun onAiResponseStyleChanged(value: String) {
        aiResponseStyle = value
    }

    fun onAiModelChanged(value: String) {
        aiSelectedModel = value
    }

    fun orchestrateAI() {
        viewModelScope.launch {
            val response = repository.requestAI(aiPrompt)
            aiResponse = response.summary
        }
    }
}

data class LoginForm(val email: String = "", val password: String = "")
