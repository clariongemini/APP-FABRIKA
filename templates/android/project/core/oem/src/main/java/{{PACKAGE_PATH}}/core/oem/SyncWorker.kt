package {{PACKAGE}}.core.oem

import android.content.Context
import androidx.hilt.work.HiltWorker
import androidx.work.CoroutineWorker
import androidx.work.WorkerParameters
import dagger.assisted.Assisted
import dagger.assisted.AssistedInject

/**
 * Arka plan sync worker — OEM hazırlığı zorunlu.
 * @see docs/03-STANDARDS/BACKGROUND_PROCESSING.md
 */
@HiltWorker
class SyncWorker @AssistedInject constructor(
    @Assisted context: Context,
    @Assisted params: WorkerParameters,
    private val oemCompat: OemCompatFacade,
    // private val syncRepository: SyncRepository,
) : CoroutineWorker(context, params) {

    override suspend fun doWork(): Result {
        return try {
            oemCompat.prepareForBackgroundWork()
            // syncRepository.syncPending()
            Result.success()
        } catch (e: Exception) {
            if (runAttemptCount < 3) Result.retry() else Result.failure()
        }
    }
}
