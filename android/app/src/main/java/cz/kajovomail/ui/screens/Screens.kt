package cz.kajovomail.ui.screens

sealed class Screens(val route: String) {
    object Login : Screens("login")
    object Accounts : Screens("accounts")
    object Messages : Screens("messages")
    object MessageDetail : Screens("messageDetail")
    object Compose : Screens("compose")
    object Settings : Screens("settings")
    object AIPanel : Screens("ai")
    object Offers : Screens("offers")
}
