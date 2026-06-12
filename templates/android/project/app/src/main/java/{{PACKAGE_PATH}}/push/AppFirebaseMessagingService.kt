package {{PACKAGE}}.push

import com.google.firebase.messaging.FirebaseMessagingService
import com.google.firebase.messaging.RemoteMessage
import dagger.hilt.android.AndroidEntryPoint
import {{PACKAGE}}.core.oem.OemCompatFacade
import javax.inject.Inject

/**
 * FCM push — Katman 11/20. OEM kill sonrası high-priority recovery.
 * @see docs/03-STANDARDS/FCM_PUSH.md
 */
@AndroidEntryPoint
class AppFirebaseMessagingService : FirebaseMessagingService() {

    @Inject lateinit var oemCompat: OemCompatFacade

    override fun onMessageReceived(message: RemoteMessage) {
        oemCompat.prepareForBackgroundWork()
        // Handle data payload → sync trigger
    }

    override fun onNewToken(token: String) {
        // V2: send to backend
    }
}
