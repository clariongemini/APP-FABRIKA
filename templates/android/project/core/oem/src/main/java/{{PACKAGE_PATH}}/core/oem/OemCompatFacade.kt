package {{PACKAGE}}.core.oem

/**
 * OEM uyumluluk tek giriş noktası.
 * Arka plan işi planlamadan önce [prepareForBackgroundWork] çağrılmalı.
 * @see docs/03-STANDARDS/OEM_COMPATIBILITY.md
 */
interface OemCompatFacade {
    fun currentManufacturer(): Manufacturer
    fun prepareForBackgroundWork()
    fun openBatterySettings()
    fun openAutostartSettings()
}

class DefaultOemCompatFacade(
    private val detector: ManufacturerDetector,
    private val batteryOptimizer: OemBatteryOptimizer,
    private val autostartGuide: OemAutostartGuide,
) : OemCompatFacade {

    override fun currentManufacturer(): Manufacturer = detector.current()

    override fun prepareForBackgroundWork() {
        when (detector.current()) {
            Manufacturer.XIAOMI, Manufacturer.OPPO, Manufacturer.VIVO ->
                autostartGuide.showIfNeeded()
            Manufacturer.SAMSUNG ->
                batteryOptimizer.requestUnrestrictedIfNeeded()
            else -> Unit
        }
    }

    override fun openBatterySettings() = batteryOptimizer.openSettings()
    override fun openAutostartSettings() = autostartGuide.openSettings()
}
