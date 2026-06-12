package {{PACKAGE}}.core.security

import java.io.File

object RootDetector {
    fun isRooted(): Boolean {
        val paths = arrayOf(
            "/system/app/Superuser.apk",
            "/sbin/su", "/system/bin/su", "/system/xbin/su",
        )
        return paths.any { File(it).exists() }
    }
}
