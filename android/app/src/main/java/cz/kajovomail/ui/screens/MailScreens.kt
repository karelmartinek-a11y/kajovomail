package cz.kajovomail.ui.screens

import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalConfiguration
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.navigation.NavController
import cz.kajovomail.ui.viewmodel.KajovoMailViewModel
import androidx.compose.ui.text.input.PasswordVisualTransformation

@Composable
fun LoginScreen(navController: NavController, viewModel: KajovoMailViewModel) {
    val state = viewModel.loginState
    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(16.dp),
        verticalArrangement = Arrangement.Center
    ) {
        Text("Secure login", style = MaterialTheme.typography.headlineSmall)
        Spacer(modifier = Modifier.height(12.dp))
        OutlinedTextField(
            value = state.email,
            onValueChange = viewModel::onEmailChanged,
            label = { Text("Email") },
            singleLine = true
        )
        Spacer(modifier = Modifier.height(8.dp))
        OutlinedTextField(
            value = state.password,
            onValueChange = viewModel::onPasswordChanged,
            label = { Text("Password") },
            singleLine = true,
            visualTransformation = PasswordVisualTransformation()
        )
        Spacer(modifier = Modifier.height(16.dp))
        Button(
            onClick = {
                viewModel.login {
                    navController.navigate(Screens.Accounts.route)
                }
            }
        ) {
            Text("Sign in")
        }
    }
}

@Composable
fun AccountsScreen(navController: NavController, viewModel: KajovoMailViewModel) {
    val isTablet = LocalConfiguration.current.screenWidthDp > 720
    val accounts by viewModel.accounts.collectAsState()
    Column(modifier = Modifier.fillMaxSize().padding(16.dp)) {
        Text("Accounts & folders", fontWeight = FontWeight.Bold)
        Spacer(modifier = Modifier.height(8.dp))
        LazyColumn {
            items(accounts) { account ->
                Card(modifier = Modifier
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
    val virtualViews = listOf("Unread", "Flagged", "With attachments")
    val messages by viewModel.messages.collectAsState()
    Column(modifier = Modifier.fillMaxSize().padding(16.dp)) {
        Text("Messages", fontWeight = FontWeight.Bold)
        Spacer(modifier = Modifier.height(8.dp))
        Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
            virtualViews.forEach { view ->
                AssistChip(onClick = { viewModel.selectVirtualView(view) }, label = { Text(view) })
            }
        }
        Spacer(modifier = Modifier.height(12.dp))
        LazyColumn {
            items(viewModel.messages) { message ->
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
    Column(modifier = Modifier.fillMaxSize().padding(16.dp)) {
        Text(message.subject, style = MaterialTheme.typography.headlineSmall)
        Spacer(modifier = Modifier.height(8.dp))
        Text("From: ${message.sender}")
        Spacer(modifier = Modifier.height(12.dp))
        Text(message.snippet)
    }
}

@Composable
fun ComposeScreen(viewModel: KajovoMailViewModel) {
    Column(modifier = Modifier.fillMaxSize().padding(16.dp)) {
        Text("Compose", fontWeight = FontWeight.Bold)
        Spacer(Modifier.height(8.dp))
        OutlinedTextField(
            value = viewModel.composeState.recipient,
            onValueChange = viewModel::onRecipientChanged,
            label = { Text("To") },
            modifier = Modifier.fillMaxWidth()
        )
        Spacer(Modifier.height(8.dp))
        OutlinedTextField(
            value = viewModel.composeState.subject,
            onValueChange = viewModel::onSubjectChanged,
            label = { Text("Subject") },
            modifier = Modifier.fillMaxWidth()
        )
        Spacer(Modifier.height(8.dp))
        OutlinedTextField(
            value = viewModel.composeState.body,
            onValueChange = viewModel::onBodyChanged,
            label = { Text("Body") },
            modifier = Modifier
                .fillMaxWidth()
                .height(200.dp)
        )
        Spacer(Modifier.height(12.dp))
        Button(onClick = viewModel::sendDraft) {
            Text("Send draft")
        }
    }
}

@Composable
fun SettingsScreen(viewModel: KajovoMailViewModel) {
    LaunchedEffect(Unit) {
        viewModel.loadAISettings()
    }
    Column(modifier = Modifier.fillMaxSize().padding(16.dp)) {
        Text("Security & Sessions", fontWeight = FontWeight.Bold)
        Spacer(Modifier.height(12.dp))
        OutlinedTextField(
            value = viewModel.aiApiKey,
            onValueChange = viewModel::onAiApiKeyChanged,
            label = { Text("OpenAI API key") },
            visualTransformation = PasswordVisualTransformation(),
            modifier = Modifier.fillMaxWidth()
        )
        if (viewModel.aiApiKeyMasked.isNotBlank()) {
            Text("Stored key: ${viewModel.aiApiKeyMasked}", style = MaterialTheme.typography.bodySmall)
        }
        Spacer(Modifier.height(8.dp))
        Text("Response style", fontWeight = FontWeight.Medium)
        Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
            listOf("concise", "balanced", "detailed").forEach { style ->
                AssistChip(
                    onClick = { viewModel.onAiResponseStyleChanged(style) },
                    label = { Text(style) }
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
            Button(onClick = viewModel::testAIKey) { Text("Test API key") }
            Button(onClick = viewModel::loadAIModels) { Text("Load models") }
        }
        if (viewModel.aiModels.isNotEmpty()) {
            Spacer(Modifier.height(8.dp))
            Text("Available models", fontWeight = FontWeight.Medium)
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
            Text("Save AI settings")
        }
        Spacer(Modifier.height(8.dp))
        Text(viewModel.aiSettingsStatus, style = MaterialTheme.typography.bodySmall)
        Spacer(Modifier.height(12.dp))
        Button(onClick = viewModel::logout) {
            Text("Logout")
        }
    }
}

@Composable
fun AIPanelScreen(viewModel: KajovoMailViewModel) {
    Column(modifier = Modifier.fillMaxSize().padding(16.dp)) {
        Text("AI Console", fontWeight = FontWeight.Bold)
        Spacer(Modifier.height(8.dp))
        OutlinedTextField(
            value = viewModel.aiPrompt,
            onValueChange = viewModel::onPromptChanged,
            label = { Text("Prompt") },
            modifier = Modifier.fillMaxWidth()
        )
        Spacer(Modifier.height(8.dp))
        Button(onClick = viewModel::orchestrateAI) {
            Text("Run AI orchestration")
        }
        Spacer(Modifier.height(12.dp))
        Text(viewModel.aiResponse)
    }
}

@Composable
fun OffersScreen(viewModel: KajovoMailViewModel) {
    Column(modifier = Modifier.fillMaxSize().padding(16.dp)) {
        Text("Nabídky", fontWeight = FontWeight.Bold)
        Spacer(Modifier.height(8.dp))
        LazyColumn {
            items(viewModel.offers) { offer ->
                Card(modifier = Modifier.padding(vertical = 4.dp).fillMaxWidth()) {
                    Column(modifier = Modifier.padding(12.dp)) {
                        Text(offer.title, fontWeight = FontWeight.Medium)
                        Text("State: ${offer.state}")
                    }
                }
            }
        }
    }
}
