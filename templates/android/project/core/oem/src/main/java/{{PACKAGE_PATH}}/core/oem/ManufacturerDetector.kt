package {{PACKAGE}}.core.oem

import android.os.Build

interface ManufacturerDetector {
    fun current(): Manufacturer
}

class DefaultManufacturerDetector : ManufacturerDetector {
    override fun current(): Manufacturer {
        val brand = Build.BRAND.lowercase()
        val manufacturer = Build.MANUFACTURER.lowercase()
        return when {
            manufacturer.contains("samsung") || brand.contains("samsung") -> Manufacturer.SAMSUNG
            manufacturer.contains("xiaomi") || brand.contains("redmi") || brand.contains("poco") -> Manufacturer.XIAOMI
            manufacturer.contains("oppo") || brand.contains("realme") -> Manufacturer.OPPO
            manufacturer.contains("vivo") -> Manufacturer.VIVO
            manufacturer.contains("huawei") || brand.contains("honor") -> Manufacturer.HUAWEI
            manufacturer.contains("google") -> Manufacturer.GOOGLE
            manufacturer.contains("motorola") -> Manufacturer.MOTOROLA
            manufacturer.contains("oneplus") -> Manufacturer.ONEPLUS
            else -> Manufacturer.UNKNOWN
        }
    }
}
