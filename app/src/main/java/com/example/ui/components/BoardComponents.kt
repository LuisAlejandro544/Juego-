package com.example.ui.components

import androidx.compose.animation.AnimatedVisibility
import androidx.compose.animation.core.animateFloatAsState
import androidx.compose.animation.core.tween
import androidx.compose.animation.fadeIn
import androidx.compose.animation.fadeOut
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.aspectRatio
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Casino
import androidx.compose.material.icons.filled.CheckCircle
import androidx.compose.material.icons.filled.Home
import androidx.compose.material.icons.filled.Lock
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedButton
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.draw.rotate
import androidx.compose.ui.draw.shadow
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.testTag
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.example.model.BoardTile
import com.example.model.Player
import com.example.model.TileType

/**
 * ============================================================================
 * COMPONENTES DEL TABLERO Y CASILLAS (CAPITAL TYCOON)
 * ============================================================================
 * Implementa la representación gráfica del circuito perimetral de 20 casillas,
 * fichas de los jugadores, dados animados y visualizadores de propiedad.
 */

/**
 * Casilla individual dentro de la cuadrícula perimetral del tablero.
 */
@Composable
fun BoardCellView(
    tile: BoardTile,
    playersOnTile: List<Player>,
    onClick: () -> Unit,
    modifier: Modifier = Modifier
) {
    val isCorner = tile.type in listOf(TileType.START, TileType.JAIL, TileType.FREE_PARKING, TileType.GO_TO_JAIL)
    val ownerColor = if (tile.ownerId == 0) Color(0xFF1E88E5) else if (tile.ownerId == 1) Color(0xFFE53935) else null

    Card(
        modifier = modifier
            .padding(1.dp)
            .clickable(onClick = onClick)
            .testTag("tile_${tile.id}"),
        shape = RoundedCornerShape(4.dp),
        colors = CardDefaults.cardColors(
            containerColor = when {
                ownerColor != null -> ownerColor.copy(alpha = 0.12f)
                isCorner -> MaterialTheme.colorScheme.surfaceVariant
                else -> MaterialTheme.colorScheme.surface
            }
        ),
        elevation = CardDefaults.cardElevation(defaultElevation = if (ownerColor != null) 2.dp else 1.dp)
    ) {
        Column(
            modifier = Modifier
                .fillMaxSize()
                .border(
                    width = if (ownerColor != null) 1.5.dp else 0.5.dp,
                    color = ownerColor ?: MaterialTheme.colorScheme.outlineVariant,
                    shape = RoundedCornerShape(4.dp)
                ),
            horizontalAlignment = Alignment.CenterHorizontally,
            verticalArrangement = Arrangement.SpaceBetween
        ) {
            // Franja superior de color de grupo si es propiedad
            if (tile.group != null) {
                Box(
                    modifier = Modifier
                        .fillMaxWidth()
                        .height(6.dp)
                        .background(tile.group.color)
                )
            } else {
                Spacer(modifier = Modifier.height(2.dp))
            }

            // Contenido central: Icono o Emoji y Nombre
            Column(
                horizontalAlignment = Alignment.CenterHorizontally,
                modifier = Modifier.padding(horizontal = 2.dp)
            ) {
                Text(
                    text = tile.icon,
                    fontSize = if (isCorner) 13.sp else 11.sp,
                    lineHeight = 13.sp
                )
                Text(
                    text = tile.name,
                    fontSize = 7.5.sp,
                    fontWeight = FontWeight.Bold,
                    maxLines = 1,
                    overflow = TextOverflow.Ellipsis,
                    textAlign = TextAlign.Center,
                    color = MaterialTheme.colorScheme.onSurface
                )
            }

            // Indicador inferior: Precio o Casas
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(horizontal = 2.dp, vertical = 1.dp),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                if (tile.type == TileType.PROPERTY) {
                    if (tile.houses > 0) {
                        // Muestra indicador de mejoras
                        Text(
                            text = if (tile.houses == 4) "🏨" else "🏡x${tile.houses}",
                            fontSize = 7.sp
                        )
                    } else {
                        Text(
                            text = "$${tile.price}",
                            fontSize = 7.sp,
                            fontWeight = FontWeight.SemiBold,
                            color = MaterialTheme.colorScheme.primary
                        )
                    }
                } else if (tile.type == TileType.TAX) {
                    Text(text = "$${tile.price}", fontSize = 7.sp, color = MaterialTheme.colorScheme.error)
                } else {
                    Spacer(modifier = Modifier.width(4.dp))
                }

                // Fichas de jugadores sobre esta casilla
                Row(horizontalArrangement = Arrangement.spacedBy((-4).dp)) {
                    playersOnTile.forEach { player ->
                        Box(
                            modifier = Modifier
                                .size(13.dp)
                                .clip(CircleShape)
                                .background(player.color)
                                .border(1.dp, Color.White, CircleShape),
                            contentAlignment = Alignment.Center
                        ) {
                            Text(text = player.avatar, fontSize = 7.sp)
                        }
                    }
                }
            }
        }
    }
}

/**
 * Tablero completo organizado en una cuadrícula perimetral de 6x6 celdas
 * con un patio central informativo adaptado al teléfono.
 */
@Composable
fun CapitalBoardLayout(
    boardTiles: List<BoardTile>,
    players: List<Player>,
    parkingPot: Int,
    onTileClick: (BoardTile) -> Unit,
    centerContent: @Composable () -> Unit,
    modifier: Modifier = Modifier
) {
    // Matriz de 6x6 que mapea la posición en el perímetro (0..19)
    // Casillas perimetrales:
    // Fila 0 (arriba): [10, 11, 12, 13, 14, 15]
    // Columna 5 (derecha): [15, 16, 17, 18, 19, 0]
    // Fila 5 (abajo): [5, 4, 3, 2, 1, 0]
    // Columna 0 (izquierda): [10, 9, 8, 7, 6, 5]

    fun getTileAt(row: Int, col: Int): BoardTile? {
        val index = when {
            row == 0 -> 10 + col // 10, 11, 12, 13, 14, 15
            col == 5 && row in 1..4 -> 15 + row // 16, 17, 18, 19
            row == 5 -> when (col) {
                5 -> 0
                4 -> 1
                3 -> 2
                2 -> 3
                1 -> 4
                0 -> 5
                else -> null
            }
            col == 0 && row in 1..4 -> 10 - row // 9, 8, 7, 6
            else -> null // Zona central del tablero (1..4, 1..4)
        }
        return index?.let { boardTiles.getOrNull(it) }
    }

    Box(
        modifier = modifier
            .fillMaxWidth()
            .aspectRatio(1f)
            .clip(RoundedCornerShape(12.dp))
            .background(MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.5f))
            .border(2.dp, MaterialTheme.colorScheme.outlineVariant, RoundedCornerShape(12.dp))
            .padding(4.dp)
    ) {
        Column(modifier = Modifier.fillMaxSize()) {
            for (r in 0..5) {
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .weight(1f)
                ) {
                    for (c in 0..5) {
                        val tile = getTileAt(r, c)
                        if (tile != null) {
                            val playersOnTile = players.filter { it.position == tile.id }
                            BoardCellView(
                                tile = tile,
                                playersOnTile = playersOnTile,
                                onClick = { onTileClick(tile) },
                                modifier = Modifier.weight(1f)
                            )
                        } else if (r == 1 && c == 1) {
                            // Célula que inicia el área central de 4x4
                            Box(
                                modifier = Modifier
                                    .weight(4f)
                                    .fillMaxSize()
                                    .padding(2.dp),
                                contentAlignment = Alignment.Center
                            ) {
                                centerContent()
                            }
                        }
                        // Saltamos las demás columnas intermedias porque el Box central de 4x4 ya las cubre
                        if (r in 1..4 && c == 1) {
                            break
                        }
                    }
                }
            }
        }
    }
}

/**
 * Visualizador 3D de los dos dados con animación de lanzamiento.
 */
@Composable
fun DiceRollView(
    d1: Int,
    d2: Int,
    isRolling: Boolean,
    modifier: Modifier = Modifier
) {
    val rotation by animateFloatAsState(
        targetValue = if (isRolling) 360f else 0f,
        animationSpec = tween(durationMillis = 300),
        label = "dice_rotation"
    )

    Row(
        modifier = modifier,
        horizontalArrangement = Arrangement.spacedBy(10.dp),
        verticalAlignment = Alignment.CenterVertically
    ) {
        SingleDiceCard(value = d1, rotation = rotation)
        SingleDiceCard(value = d2, rotation = -rotation)
    }
}

/**
 * Cara individual de un dado de juego.
 */
@Composable
private fun SingleDiceCard(value: Int, rotation: Float) {
    val diceGlyph = when (value) {
        1 -> "⚀"
        2 -> "⚁"
        3 -> "⚂"
        4 -> "⚃"
        5 -> "⚄"
        else -> "⚅"
    }

    Card(
        modifier = Modifier
            .size(44.dp)
            .rotate(rotation)
            .shadow(4.dp, RoundedCornerShape(8.dp)),
        shape = RoundedCornerShape(8.dp),
        colors = CardDefaults.cardColors(containerColor = Color.White)
    ) {
        Box(
            modifier = Modifier.fillMaxSize(),
            contentAlignment = Alignment.Center
        ) {
            Text(
                text = diceGlyph,
                fontSize = 32.sp,
                color = Color(0xFF1E293B),
                lineHeight = 32.sp
            )
        }
    }
}

/**
 * Tarjeta de información económica y estado de un jugador.
 */
@Composable
fun PlayerBadgeView(
    player: Player,
    isActive: Boolean,
    propertiesCount: Int,
    netWorth: Int,
    modifier: Modifier = Modifier
) {
    Card(
        modifier = modifier
            .border(
                width = if (isActive) 2.dp else 1.dp,
                color = if (isActive) player.color else MaterialTheme.colorScheme.outlineVariant,
                shape = RoundedCornerShape(10.dp)
            ),
        shape = RoundedCornerShape(10.dp),
        colors = CardDefaults.cardColors(
            containerColor = if (isActive) player.color.copy(alpha = 0.12f) else MaterialTheme.colorScheme.surface
        ),
        elevation = CardDefaults.cardElevation(defaultElevation = if (isActive) 4.dp else 1.dp)
    ) {
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(horizontal = 8.dp, vertical = 6.dp),
            verticalAlignment = Alignment.CenterVertically,
            horizontalArrangement = Arrangement.SpaceBetween
        ) {
            Row(verticalAlignment = Alignment.CenterVertically) {
                Box(
                    modifier = Modifier
                        .size(28.dp)
                        .clip(CircleShape)
                        .background(player.color),
                    contentAlignment = Alignment.Center
                ) {
                    Text(text = player.avatar, fontSize = 14.sp)
                }
                Spacer(modifier = Modifier.width(6.dp))
                Column {
                    Text(
                        text = player.name,
                        fontSize = 11.sp,
                        fontWeight = if (isActive) FontWeight.Bold else FontWeight.Medium,
                        color = MaterialTheme.colorScheme.onSurface,
                        maxLines = 1,
                        overflow = TextOverflow.Ellipsis
                    )
                    Text(
                        text = "$${player.cash}",
                        fontSize = 13.sp,
                        fontWeight = FontWeight.ExtraBold,
                        color = if (player.cash < 100) MaterialTheme.colorScheme.error else Color(0xFF2E7D32)
                    )
                }
            }

            Column(horizontalAlignment = Alignment.End) {
                Text(
                    text = "Patrimonio: $$netWorth",
                    fontSize = 9.sp,
                    color = MaterialTheme.colorScheme.onSurfaceVariant
                )
                Text(
                    text = "Propiedades: $propertiesCount",
                    fontSize = 9.sp,
                    fontWeight = FontWeight.SemiBold,
                    color = player.color
                )
                if (player.inJail) {
                    Text(
                        text = "🔒 En Cárcel",
                        fontSize = 8.sp,
                        color = MaterialTheme.colorScheme.error,
                        fontWeight = FontWeight.Bold
                    )
                }
            }
        }
    }
}
