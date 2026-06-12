package {{PACKAGE}}

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import dagger.hilt.android.AndroidEntryPoint
import {{PACKAGE}}.core.designsystem.theme.{{APP_CLASS}}Theme
import {{PACKAGE}}.feature.home.presentation.HomeScreen

@AndroidEntryPoint
class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContent {
            {{APP_CLASS}}Theme {
                HomeScreen()
            }
        }
    }
}
