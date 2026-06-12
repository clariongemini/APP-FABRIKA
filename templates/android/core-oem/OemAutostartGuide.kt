package {{PACKAGE}}.core.oem

import android.content.Context
import android.content.Intent
import dagger.hilt.android.qualifiers.ApplicationContext
import javax.inject.Inject

interface OemAutostartGuide {
    fun showIfNeeded()
    fun openSettings()
}

class DefaultOemAutostartGuide @Inject constructor(
    @ApplicationContext private val context: Context,
    private val detector: ManufacturerDetector,
) : OemAutostartGuide {

    override fun showIfNeeded() {
        if (!detector.current().requiresAutostartGuide) return
        // UI katmanı: localized dialog → openSettings()
    }

    override fun openSettings() {
        val intents = listOf(
            "miui.intent.action.OP_AUTO_START",
            "oppo.intent.action.OPPO_AUTO_START",
        )
        for (action in intents) {
            val intent = Intent(action).apply { addFlags(Intent.FLAG_ACTIVITY_NEW_TASK) }
            if (intent.resolveActivity(context.packageManager) != null) {
                runCatching { context.startActivity(intent) }
                return
            }
        }
        // Fallback: app details
        val fallback = Intent(android.provider.Settings.ACTION_APPLICATION_DETAILS_SETTINGS).apply {
            data = android.net.Uri.parse("package:${context.packageName}")
            addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
        }
        runCatching { context.startActivity(fallback) }
    }
}
