package {{PACKAGE}}.core.designsystem.component

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.unit.dp
import {{PACKAGE}}.core.designsystem.theme.GlassTokens

@Composable
fun GlassCard(
    modifier: Modifier = Modifier,
    content: @Composable () -> Unit,
) {
    Box(
        modifier = modifier
            .clip(RoundedCornerShape(GlassTokens.CornerRadius))
            .background(Color.White.copy(alpha = GlassTokens.GlassAlpha))
            .padding(16.dp),
    ) {
        content()
    }
}
