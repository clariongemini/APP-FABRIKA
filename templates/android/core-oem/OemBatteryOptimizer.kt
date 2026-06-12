package {{PACKAGE}}.core.oem

import android.content.Context
import android.content.Intent
import android.net.Uri
import android.os.PowerManager
import android.provider.Settings
import dagger.hilt.android.qualifiers.ApplicationContext
import javax.inject.Inject

interface OemBatteryOptimizer {
    fun isIgnoringBatteryOptimizations(): Boolean
    fun requestUnrestrictedIfNeeded()
    fun openSettings()
}

class DefaultOemBatteryOptimizer @Inject constructor(
    @ApplicationContext private val context: Context,
    private val detector: ManufacturerDetector,
) : OemBatteryOptimizer {

    private val powerManager: PowerManager
        get() = context.getSystemService(Context.POWER_SERVICE) as PowerManager

    override fun isIgnoringBatteryOptimizations(): Boolean =
        powerManager.isIgnoringBatteryOptimizations(context.packageName)

    override fun requestUnrestrictedIfNeeded() {
        if (!detector.current().requiresBatteryUnrestrict) return
        if (isIgnoringBatteryOptimizations()) return
        openSettings()
    }

    override fun openSettings() {
        val intent = Intent(Settings.ACTION_REQUEST_IGNORE_BATTERY_OPTIMIZATIONS).apply {
            data = Uri.parse("package:${context.packageName}")
            addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
        }
        runCatching { context.startActivity(intent) }
    }
}
