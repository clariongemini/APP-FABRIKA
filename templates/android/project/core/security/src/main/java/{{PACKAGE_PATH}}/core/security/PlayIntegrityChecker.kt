package {{PACKAGE}}.core.security

import android.content.Context
import dagger.hilt.android.qualifiers.ApplicationContext
import {{PACKAGE}}.core.common.result.AppResult
import javax.inject.Inject
import javax.inject.Singleton

/**
 * Play Integrity API facade — V2'de token backend'de doğrulanır.
 * @see docs/03-STANDARDS/PLAY_INTEGRITY.md
 */
interface PlayIntegrityChecker {
    suspend fun requestToken(nonce: String): AppResult<String>
}

@Singleton
class DefaultPlayIntegrityChecker @Inject constructor(
    @ApplicationContext private val context: Context,
) : PlayIntegrityChecker {
    override suspend fun requestToken(nonce: String): AppResult<String> {
        // V1 stub — V2: IntegrityManagerFactory.create(context)
        return AppResult.Success("integrity-stub-$nonce")
    }
}
