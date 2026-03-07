package cz.kajovomail.ui.screens

import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material3.AssistChip
import androidx.compose.material3.Button
import androidx.compose.material3.Card
import androidx.compose.material3.Divider
import androidx.compose.material3.ListItem
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.input.PasswordVisualTransformation
import androidx.compose.ui.unit.dp
import androidx.navigation.NavController
import cz.kajovomail.ui.viewmodel.KajovoMailViewModel

@Composable
fun LoginScreen(navController: NavController, viewModel: KajovoMailViewModel) {
    val state = viewModel.loginState
    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(16.dp)
            .padding(bottom = 80.dp),
        verticalArrangement = Arrangement.Center
    ) {
        Text("Bezpečné přihlášení", style = MaterialTheme.typography.headlineSmall)
        Spacer(modifier = Modifier.height(12.dp))
        OutlinedTextField(
            value = state.email,
            onValueChange = viewModel::onEmailChanged,
            label = { Text("E-mail") },
            singleLine = true,
            modifier = Modifier.fillMaxWidth()
        )
        Spacer(modifier = Modifier.height(8.dp))
        OutlinedTextField(
            value = state.password,
            onValueChange = viewModel::onPasswordChanged,
            label = { Text("Heslo") },
            singleLine = true,
            visualTransformation = PasswordVisualTransformation(),
            modifier = Modifier.fillMaxWidth()
        )
        Spacer(modifier = Modifier.height(16.dp))
        Button(
            onClick = {
                viewModel.login {
                    navController.navigate(Screens.Accounts.route)
                }
            }
        ) {
            Text("Přihlásit")
        }
    }
}

@Composable
fun AccountsScreen(navController: NavController, viewModel: KajovoMailViewModel) {
    val accounts by viewModel.accounts.collectAsState()
    Column(modifier = Modifier.fillMaxSize().padding(16.dp).padding(bottom = 80.dp)) {
        Text("Účty a složky", fontWeight = FontWeight.Bold)
        Spacer(modifier = Modifier.height(8.dp))
        Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
            AssistChip(onClick = { navController.navigate(Screens.Messages.route) }, label = { Text("Zprávy") })
            AssistChip(onClick = { navController.navigate(Screens.Compose.route) }, label = { Text("Napsat") })
            AssistChip(onClick = { navController.navigate(Screens.Settings.route) }, label = { Text("Nastavení") })
        }
        Spacer(modifier = Modifier.height(8.dp))
        LazyColumn {
            items(accounts) { account ->
                Card(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(vertical = 4.dp)
                        .clickable { navController.navigate(Screens.Messages.route) }
                ) {
                    Column(modifier = Modifier.padding(12.dp)) {
                        Text(account.email, fontWeight = FontWeight.Medium)
                        Text(account.provider, style = MaterialTheme.typography.bodySmall)
                    }
                }
            }
        }
    }
}

@Composable
fun MessageListScreen(navController: NavController, viewModel: KajovoMailViewModel) {
    val virtualViews = listOf("Nepřečtené", "Označené", "S přílohami")
    val messages by viewModel.messages.collectAsState()
    Column(modifier = Modifier.fillMaxSize().padding(16.dp).padding(bottom = 80.dp)) {
        Text("Zprávy", fontWeight = FontWeight.Bold)
        Spacer(modifier = Modifier.height(8.dp))
        Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
            virtualViews.forEach { view ->
                AssistChip(onClick = { viewModel.selectVirtualView(view) }, label = { Text(view) })
            }
        }
        Spacer(modifier = Modifier.height(12.dp))
        LazyColumn {
            items(messages) { message ->
                ListItem(
                    modifier = Modifier.clickable { navController.navigate(Screens.MessageDetail.route) },
                    headlineText = { Text(message.subject) },
                    supportingText = { Text(message.sender) }
                )
                Divider()
            }
        }
    }
}

@Composable
fun MessageDetailScreen(viewModel: KajovoMailViewModel) {
    val message = viewModel.selectedMessage ?: return
    Column(modifier = Modifier.fillMaxSize().padding(16.dp).padding(bottom = 80.dp)) {
        Text(message.subject, style = MaterialTheme.typography.headlineSmall)
        Spacer(modifier = Modifier.height(8.dp))
        Text("Od: ${message.sender}")
        Spacer(modifier = Modifier.height(12.dp))
        Text(message.snippet)
    }
}

@Composable
fun ComposeScreen(viewModel: KajovoMailViewModel) {
    Column(modifier = Modifier.fillMaxSize().padding(16.dp).padding(bottom = 80.dp)) {
        Text("Napsat zprávu", fontWeight = FontWeight.Bold)
        Spacer(Modifier.height(8.dp))
        OutlinedTextField(
            value = viewModel.composeState.recipient,
            onValueChange = viewModel::onRecipientChanged,
            label = { Text("Komu") },
            modifier = Modifier.fillMaxWidth()
        )
        Spacer(Modifier.height(8.dp))
        OutlinedTextField(
            value = viewModel.composeState.subject,
            onValueChange = viewModel::onSubjectChanged,
            label = { Text("Předmět") },
            modifier = Modifier.fillMaxWidth()
        )
        Spacer(Modifier.height(8.dp))
        OutlinedTextField(
            value = viewModel.composeState.body,
            onValueChange = viewModel::onBodyChanged,
            label = { Text("Text") },
            modifier = Modifier
                .fillMaxWidth()
                .height(200.dp)
        )
        Spacer(Modifier.height(12.dp))
        Button(onClick = viewModel::sendDraft) {
            Text("Odeslat koncept")
        }
    }
}

@Composable
fun SettingsScreen(viewModel: KajovoMailViewModel) {
    LaunchedEffect(Unit) {
        viewModel.loadAISettings()
    }
    Column(modifier = Modifier.fillMaxSize().padding(16.dp).padding(bottom = 80.dp)) {
        Text("Bezpečnost a relace", fontWeight = FontWeight.Bold)
        Spacer(Modifier.height(12.dp))
        OutlinedTextField(
            value = viewModel.aiApiKey,
            onValueChange = viewModel::onAiApiKeyChanged,
            label = { Text("OpenAI API klíč") },
            visualTransformation = PasswordVisualTransformation(),
            modifier = Modifier.fillMaxWidth()
        )
        if (viewModel.aiApiKeyMasked.isNotBlank()) {
            Text("Uložený klíč: ${viewModel.aiApiKeyMasked}", style = MaterialTheme.typography.bodySmall)
        }
        Spacer(Modifier.height(8.dp))
        Text("Styl odpovědi", fontWeight = FontWeight.Medium)
        Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
            listOf("concise" to "Stručný", "balanced" to "Vyvážený", "detailed" to "Detailní").forEach { (styleValue, styleLabel) ->
                AssistChip(
                    onClick = { viewModel.onAiResponseStyleChanged(styleValue) },
                    label = { Text(styleLabel) }
                )
            }
        }
        Spacer(Modifier.height(8.dp))
        OutlinedTextField(
            value = viewModel.aiSelectedModel,
            onValueChange = viewModel::onAiModelChanged,
            label = { Text("OpenAI model") },
            modifier = Modifier.fillMaxWidth()
        )
        Spacer(Modifier.height(8.dp))
        Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
            Button(onClick = viewModel::testAIKey) { Text("Otestovat API klíč") }
            Button(onClick = viewModel::loadAIModels) { Text("Načíst modely") }
        }
        if (viewModel.aiModels.isNotEmpty()) {
            Spacer(Modifier.height(8.dp))
            Text("Dostupné modely", fontWeight = FontWeight.Medium)
            LazyColumn(modifier = Modifier.height(140.dp)) {
                items(viewModel.aiModels) { model ->
                    Text(
                        text = model,
                        modifier = Modifier
                            .fillMaxWidth()
                            .clickable { viewModel.onAiModelChanged(model) }
                            .padding(vertical = 4.dp)
                    )
                }
            }
        }
        Spacer(Modifier.height(8.dp))
        Button(onClick = viewModel::saveAISettings) {
            Text("Uložit AI nastavení")
        }
        Spacer(Modifier.height(8.dp))
        Text(viewModel.aiSettingsStatus, style = MaterialTheme.typography.bodySmall)
        Spacer(Modifier.height(12.dp))
        Button(onClick = viewModel::logout) {
            Text("Odhlásit")
        }
    }
}

@Composable
fun AIPanelScreen(viewModel: KajovoMailViewModel) {
    Column(modifier = Modifier.fillMaxSize().padding(16.dp).padding(bottom = 80.dp)) {
        Text("AI panel", fontWeight = FontWeight.Bold)
        Spacer(Modifier.height(8.dp))
        OutlinedTextField(
            value = viewModel.aiPrompt,
            onValueChange = viewModel::onPromptChanged,
            label = { Text("Prompt") },
            modifier = Modifier.fillMaxWidth()
        )
        Spacer(Modifier.height(8.dp))
        Button(onClick = viewModel::orchestrateAI) {
            Text("Spustit AI orchestraci")
        }
        Spacer(Modifier.height(12.dp))
        Text(viewModel.aiResponse)
    }
}

@Composable
fun OffersScreen(viewModel: KajovoMailViewModel) {
    Column(modifier = Modifier.fillMaxSize().padding(16.dp).padding(bottom = 80.dp)) {
        Text("Nabídky", fontWeight = FontWeight.Bold)
        Spacer(Modifier.height(8.dp))
        LazyColumn {
            items(viewModel.offers) { offer ->
                Card(modifier = Modifier.padding(vertical = 4.dp).fillMaxWidth()) {
                    Column(modifier = Modifier.padding(12.dp)) {
                        Text(offer.title, fontWeight = FontWeight.Medium)
                        Text("Stav: ${offer.state}")
                    }
                }
            }
        }
    }
}
