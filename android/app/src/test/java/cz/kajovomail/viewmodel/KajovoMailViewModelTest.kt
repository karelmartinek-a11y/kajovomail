package cz.kajovomail.viewmodel

import android.app.Application
import androidx.test.core.app.ApplicationProvider
import org.junit.Assert.assertEquals
import org.junit.Test

class KajovoMailViewModelTest {
    private val viewModel = KajovoMailViewModel(ApplicationProvider.getApplicationContext())

    @Test
    fun `login form starts empty`() {
        assertEquals("", viewModel.loginState.value.email)
        assertEquals("", viewModel.loginState.value.password)
    }
}
