package {{PACKAGE}}.core.i18n

import androidx.compose.runtime.Composable
import androidx.compose.runtime.remember

@Composable
fun localized(key: String): String = remember(key) { LocaleManager.getString(key) }
