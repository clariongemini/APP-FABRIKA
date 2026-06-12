package {{PACKAGE}}.feature.premium.domain

import java.time.Instant

sealed class SubscriptionState {
    data object Free : SubscriptionState()
    data class Trial(val expiresAt: Instant) : SubscriptionState()
    data class Active(val planId: String) : SubscriptionState()
    data object Expired : SubscriptionState()
}
