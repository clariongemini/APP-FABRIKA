package {{PACKAGE}}.feature.home.presentation

import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import {{PACKAGE}}.core.designsystem.component.GlassCard
import {{PACKAGE}}.core.i18n.localized

@Composable
fun HomeScreen() {
    Scaffold { padding ->
        GlassCard(modifier = Modifier.padding(padding).padding(16.dp).fillMaxSize()) {
            Text(text = localized("home_welcome"))
        }
    }
}
