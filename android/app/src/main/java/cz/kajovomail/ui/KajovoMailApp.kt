package cz.kajovomail.ui

import androidx.compose.foundation.Image
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.material3.CenterAlignedTopAppBar
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.lifecycle.viewmodel.compose.viewModel
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.rememberNavController
import cz.kajovomail.R
import cz.kajovomail.ui.screens.AccountsScreen
import cz.kajovomail.ui.screens.AIPanelScreen
import cz.kajovomail.ui.screens.ComposeScreen
import cz.kajovomail.ui.screens.LoginScreen
import cz.kajovomail.ui.screens.MessageDetailScreen
import cz.kajovomail.ui.screens.MessageListScreen
import cz.kajovomail.ui.screens.OffersScreen
import cz.kajovomail.ui.screens.Screens
import cz.kajovomail.ui.screens.SettingsScreen
import cz.kajovomail.ui.viewmodel.KajovoMailViewModel
import kotlinx.coroutines.delay

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun KajovoMailApp() {
    val navController = rememberNavController()
    val viewModel: KajovoMailViewModel = viewModel()
    var showIntro by remember { mutableStateOf(true) }

    LaunchedEffect(Unit) {
        delay(1400)
        showIntro = false
    }

    Box(modifier = Modifier.fillMaxSize()) {
        Scaffold(
            topBar = {
                CenterAlignedTopAppBar(
                    title = {
                        Row(
                            verticalAlignment = Alignment.CenterVertically,
                            horizontalArrangement = Arrangement.spacedBy(8.dp)
                        ) {
                            Image(
                                painter = painterResource(id = R.drawable.kajovo_signace),
                                contentDescription = "KÁJOVO signace",
                                modifier = Modifier.height(42.dp),
                                contentScale = ContentScale.Fit
                            )
                            Image(
                                painter = painterResource(id = R.drawable.kajovo_mark),
                                contentDescription = "KajovoMail mark",
                                modifier = Modifier.size(28.dp),
                                contentScale = ContentScale.Fit
                            )
                            Text("KajovoMail", fontWeight = FontWeight.Bold)
                        }
                    }
                )
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

        Image(
            painter = painterResource(id = R.drawable.kajovo_signace),
            contentDescription = "KÁJOVO signace",
            modifier = Modifier
                .align(Alignment.BottomStart)
                .padding(start = 10.dp, bottom = 10.dp)
                .height(64.dp),
            contentScale = ContentScale.Fit
        )

        if (showIntro) {
            Box(
                modifier = Modifier
                    .fillMaxSize()
                    .background(MaterialTheme.colorScheme.background.copy(alpha = 0.97f)),
                contentAlignment = Alignment.Center
            ) {
                Image(
                    painter = painterResource(id = R.drawable.kajovo_logo_full),
                    contentDescription = "KajovoMail plné logo",
                    modifier = Modifier
                        .padding(24.dp)
                        .size(260.dp),
                    contentScale = ContentScale.Fit
                )
            }
        }
    }
}
