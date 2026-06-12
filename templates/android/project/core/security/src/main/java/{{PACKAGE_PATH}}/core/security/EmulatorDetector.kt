package {{PACKAGE}}.core.security

import android.os.Build

object EmulatorDetector {
    fun isEmulator(): Boolean =
        Build.FINGERPRINT.startsWith("generic") ||
            Build.FINGERPRINT.contains("vbox") ||
            Build.MODEL.contains("Emulator") ||
            Build.MANUFACTURER.contains("Genymotion")
}
