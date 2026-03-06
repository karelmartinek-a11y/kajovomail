package cz.kajovomail.ui.viewmodel

import android.app.Application
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateListOf
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.setValue
import androidx.lifecycle.AndroidViewModel
import androidx.lifecycle.viewModelScope
import cz.kajovomail.data.*
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
            repository.login(loginState.value.email, loginState.value.password)
            onSuccess()
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

    fun logout() {}

    fun orchestrateAI() {
        viewModelScope.launch {
            val response = repository.requestAI(aiPrompt)
            aiResponse = response.summary
        }
    }
}

data class LoginForm(val email: String = "", val password: String = "")
