package {{PACKAGE}}.core.i18n

import android.content.Context
import org.json.JSONObject

object LocaleManager {
    private var cache: Map<String, String> = emptyMap()

    fun load(context: Context, locale: String = "tr") {
        val json = context.assets.open("locales/$locale.json")
            .bufferedReader().use { it.readText() }
        val obj = JSONObject(json)
        cache = obj.keys().asSequence().associateWith { obj.getString(it) }
    }

    fun getString(key: String): String = cache[key] ?: key
}
