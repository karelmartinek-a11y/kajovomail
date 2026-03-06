package cz.kajovomail.ui

import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.hilt.navigation.compose.hiltViewModel
import androidx.lifecycle.viewmodel.compose.viewModel
import androidx.navigation.NavHostController
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.rememberNavController
import cz.kajovomail.ui.screens.*
import cz.kajovomail.ui.viewmodel.KajovoMailViewModel

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun KajovoMailApp() {
    val navController = rememberNavController()
    val viewModel: KajovoMailViewModel = viewModel()

    Scaffold(
        topBar = {
            CenterAlignedTopAppBar(title = { Text("KajovoMail") })
        }
    ) { padding ->
        NavHost(
            navController = navController,
            startDestination = Screens.Login.route,
            modifier = Modifier.padding(padding)
        ) {
            composable(Screens.Login.route) {
                LoginScreen(navController = navController, viewModel = viewModel)
            }
            composable(Screens.Accounts.route) {
                AccountsScreen(navController = navController, viewModel = viewModel)
            }
            composable(Screens.Messages.route) {
                MessageListScreen(navController = navController, viewModel = viewModel)
            }
            composable(Screens.MessageDetail.route) {
                MessageDetailScreen(viewModel = viewModel)
            }
            composable(Screens.Compose.route) {
                ComposeScreen(viewModel = viewModel)
            }
            composable(Screens.Settings.route) {
                SettingsScreen(viewModel = viewModel)
            }
            composable(Screens.AIPanel.route) {
                AIPanelScreen(viewModel = viewModel)
            }
            composable(Screens.Offers.route) {
                OffersScreen(viewModel = viewModel)
            }
        }
    }
}
