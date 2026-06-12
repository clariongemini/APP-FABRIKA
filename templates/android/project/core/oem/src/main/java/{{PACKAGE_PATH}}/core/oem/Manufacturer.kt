package {{PACKAGE}}.core.oem

enum class Manufacturer {
    SAMSUNG,
    XIAOMI,
    OPPO,
    VIVO,
    HUAWEI,
    GOOGLE,
    MOTOROLA,
    ONEPLUS,
    UNKNOWN;

    val requiresAutostartGuide: Boolean
        get() = this in setOf(XIAOMI, OPPO, VIVO)

    val requiresBatteryUnrestrict: Boolean
        get() = this in setOf(SAMSUNG, XIAOMI, OPPO, HUAWEI)
}
