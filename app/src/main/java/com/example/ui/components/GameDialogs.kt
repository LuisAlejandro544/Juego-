package com.example.ui.components

import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Close
import androidx.compose.material.icons.filled.EmojiEvents
import androidx.compose.material.icons.filled.Home
import androidx.compose.material.icons.filled.Info
import androidx.compose.material.icons.filled.Star
import androidx.compose.material3.AlertDialog
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.Divider
import androidx.compose.material3.HorizontalDivider
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedButton
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.testTag
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.compose.ui.window.Dialog
import com.example.model.BoardTile
import com.example.model.ChanceCard
import com.example.model.Player
import com.example.model.TileType

/**
 * ============================================================================
 * DIÁLOGOS Y VENTANAS EMERGENTES (CAPITAL TYCOON)
 * ============================================================================
 * Contiene los modales interactivos para visualización de escrituras de
 * propiedad, eventos de suerte, gestión de cartera inmobiliaria y fin de juego.
 */

/**
 * Modal que muestra la escritura formal de una propiedad con su tabla
 * de alquileres progresivos por número de casas.
 */
@Composable
fun TileDetailsDialog(
    tile: BoardTile,
    players: List<Player>,
    currentPlayer: Player,
    onUpgrade: (Int) -> Unit,
    onDismiss: () -> Unit
) {
    val owner = players.firstOrNull { it.id == tile.ownerId }
    val isOwnerCurrent = owner?.id == currentPlayer.id
    val canUpgrade = isOwnerCurrent && tile.houses < 4 && currentPlayer.cash >= tile.houseCost

    Dialog(onDismissRequest = onDismiss) {
        Card(
            modifier = Modifier
                .fillMaxWidth()
                .padding(8.dp)
                .testTag("dialog_tile_details"),
            shape = RoundedCornerShape(16.dp),
            colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surface),
            elevation = CardDefaults.cardElevation(defaultElevation = 8.dp)
        ) {
            Column(modifier = Modifier.fillMaxWidth()) {
                // Encabezado con color de grupo o tipo
                Box(
                    modifier = Modifier
                        .fillMaxWidth()
                        .background(tile.group?.color ?: MaterialTheme.colorScheme.primary)
                        .padding(vertical = 12.dp, horizontal = 16.dp)
                ) {
                    Column(horizontalAlignment = Alignment.CenterHorizontally, modifier = Modifier.fillMaxWidth()) {
                        Text(
                            text = "TÍTULO DE PROPIEDAD",
                            fontSize = 11.sp,
                            fontWeight = FontWeight.Bold,
                            color = Color.White.copy(alpha = 0.85f),
                            letterSpacing = 1.sp
                        )
                        Text(
                            text = "${tile.icon} ${tile.name}",
                            fontSize = 18.sp,
                            fontWeight = FontWeight.ExtraBold,
                            color = Color.White,
                            textAlign = TextAlign.Center
                        )
                    }
                }

                Column(modifier = Modifier.padding(16.dp)) {
                    if (tile.type == TileType.PROPERTY) {
                        // Estado del propietario
                        Row(
                            modifier = Modifier.fillMaxWidth(),
                            horizontalArrangement = Arrangement.SpaceBetween,
                            verticalAlignment = Alignment.CenterVertically
                        ) {
                            Text(text = "Propietario:", fontSize = 12.sp, color = MaterialTheme.colorScheme.onSurfaceVariant)
                            if (owner != null) {
                                Row(verticalAlignment = Alignment.CenterVertically) {
                                    Box(
                                        modifier = Modifier
                                            .size(16.dp)
                                            .clip(CircleShape)
                                            .background(owner.color)
                                    )
                                    Spacer(modifier = Modifier.width(4.dp))
                                    Text(
                                        text = "${owner.avatar} ${owner.name}",
                                        fontSize = 12.sp,
                                        fontWeight = FontWeight.Bold
                                    )
                                }
                            } else {
                                Text(
                                    text = "Sin dueño (Precio: $${tile.price})",
                                    fontSize = 12.sp,
                                    fontWeight = FontWeight.Bold,
                                    color = Color(0xFF2E7D32)
                                )
                            }
                        }

                        HorizontalDivider(modifier = Modifier.padding(vertical = 8.dp))

                        // Tabla de alquileres
                        Text(text = "Tabla de Alquiler:", fontSize = 12.sp, fontWeight = FontWeight.Bold)
                        Spacer(modifier = Modifier.height(4.dp))

                        RentRow("Alquiler base", "$${tile.baseRent}", tile.houses == 0)
                        RentRow("Con 1 Casa", "$${tile.baseRent * 2}", tile.houses == 1)
                        RentRow("Con 2 Casas", "$${tile.baseRent * 4}", tile.houses == 2)
                        RentRow("Con 3 Casas", "$${tile.baseRent * 7}", tile.houses == 3)
                        RentRow("Con Hotel 🏨", "$${tile.baseRent * 12}", tile.houses == 4)

                        HorizontalDivider(modifier = Modifier.padding(vertical = 8.dp))

                        Text(
                            text = "Costo por construcción: $${tile.houseCost}",
                            fontSize = 11.sp,
                            color = MaterialTheme.colorScheme.onSurfaceVariant
                        )

                        if (canUpgrade) {
                            Spacer(modifier = Modifier.height(8.dp))
                            Button(
                                onClick = {
                                    onUpgrade(tile.id)
                                    onDismiss()
                                },
                                modifier = Modifier
                                    .fillMaxWidth()
                                    .testTag("btn_upgrade_in_dialog"),
                                colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF2E7D32))
                            ) {
                                Icon(Icons.Default.Home, contentDescription = null, modifier = Modifier.size(16.dp))
                                Spacer(modifier = Modifier.width(6.dp))
                                Text("Construir Mejora ($${tile.houseCost})", fontSize = 12.sp)
                            }
                        }
                    } else {
                        // Casilla no adquirible (Salida, Impuesto, Suerte, Cárcel, etc.)
                        Text(
                            text = when (tile.type) {
                                TileType.START -> "Casilla de inicio. Cada vez que das una vuelta completa y pasas por aquí, cobras tu salario de $200."
                                TileType.TAX -> "Impuesto de la ciudad. El monto pagado ($${tile.price}) se acumula directamente en el bote del Parque Central."
                                TileType.CHANCE -> "Casilla de eventos sorpresivos. Robas una tarjeta que puede otorgar premios millonarios o inesperadas multas."
                                TileType.JAIL -> "Estancia penitenciaria. Si caes de paso estás solo de visita; si eres enviado como convicto deberás pagar $50 o sacar dobles para salir."
                                TileType.FREE_PARKING -> "Zona de descanso. ¡Quien aterrice en esta casilla se lleva todo el bote acumulado por impuestos!"
                                TileType.GO_TO_JAIL -> "¡Orden de arresto! Vas directo a la cárcel sin pasar por la salida ni cobrar salario."
                                else -> "Casilla del tablero."
                            },
                            fontSize = 13.sp,
                            lineHeight = 18.sp,
                            color = MaterialTheme.colorScheme.onSurface
                        )
                    }

                    Spacer(modifier = Modifier.height(12.dp))

                    OutlinedButton(
                        onClick = onDismiss,
                        modifier = Modifier.fillMaxWidth()
                    ) {
                        Text("Cerrar")
                    }
                }
            }
        }
    }
}

@Composable
private fun RentRow(label: String, amount: String, isCurrent: Boolean) {
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .background(if (isCurrent) MaterialTheme.colorScheme.primaryContainer.copy(alpha = 0.4f) else Color.Transparent)
            .padding(horizontal = 4.dp, vertical = 2.dp),
        horizontalArrangement = Arrangement.SpaceBetween
    ) {
        Text(
            text = if (isCurrent) "▶ $label" else label,
            fontSize = 11.sp,
            fontWeight = if (isCurrent) FontWeight.Bold else FontWeight.Normal,
            color = if (isCurrent) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.onSurface
        )
        Text(
            text = amount,
            fontSize = 11.sp,
            fontWeight = if (isCurrent) FontWeight.Bold else FontWeight.Normal,
            color = if (isCurrent) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.onSurface
        )
    }
}

/**
 * Diálogo de Carta de Oportunidad que muestra el evento recién sacado.
 */
@Composable
fun ChanceCardDialog(
    card: ChanceCard,
    onDismiss: () -> Unit
) {
    Dialog(onDismissRequest = onDismiss) {
        Card(
            modifier = Modifier
                .fillMaxWidth()
                .padding(12.dp)
                .testTag("dialog_chance_card"),
            shape = RoundedCornerShape(16.dp),
            colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surface),
            elevation = CardDefaults.cardElevation(defaultElevation = 8.dp)
        ) {
            Column(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(20.dp),
                horizontalAlignment = Alignment.CenterHorizontally
            ) {
                Text(text = "🎁", fontSize = 42.sp)
                Spacer(modifier = Modifier.height(8.dp))
                Text(
                    text = "OPORTUNIDAD",
                    fontSize = 11.sp,
                    fontWeight = FontWeight.Bold,
                    color = MaterialTheme.colorScheme.primary,
                    letterSpacing = 1.sp
                )
                Text(
                    text = card.title,
                    fontSize = 17.sp,
                    fontWeight = FontWeight.ExtraBold,
                    textAlign = TextAlign.Center
                )
                Spacer(modifier = Modifier.height(10.dp))
                Text(
                    text = card.description,
                    fontSize = 13.sp,
                    textAlign = TextAlign.Center,
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                    lineHeight = 18.sp
                )
                Spacer(modifier = Modifier.height(16.dp))

                if (card.cashReward > 0) {
                    Text(
                        text = "+$${card.cashReward}",
                        fontSize = 20.sp,
                        fontWeight = FontWeight.Bold,
                        color = Color(0xFF2E7D32)
                    )
                } else if (card.cashReward < 0) {
                    Text(
                        text = "-$${-card.cashReward}",
                        fontSize = 20.sp,
                        fontWeight = FontWeight.Bold,
                        color = MaterialTheme.colorScheme.error
                    )
                }

                Spacer(modifier = Modifier.height(16.dp))
                Button(
                    onClick = onDismiss,
                    modifier = Modifier.fillMaxWidth()
                ) {
                    Text("Aceptar")
                }
            }
        }
    }
}

/**
 * Modal para gestionar y mejorar todas las propiedades del jugador.
 */
@Composable
fun MyPropertiesDialog(
    player: Player,
    properties: List<BoardTile>,
    onUpgrade: (Int) -> Unit,
    onDismiss: () -> Unit
) {
    Dialog(onDismissRequest = onDismiss) {
        Card(
            modifier = Modifier
                .fillMaxWidth()
                .padding(8.dp)
                .testTag("dialog_my_properties"),
            shape = RoundedCornerShape(16.dp),
            colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surface)
        ) {
            Column(modifier = Modifier.padding(16.dp)) {
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Column {
                        Text(
                            text = "Mis Inmuebles",
                            fontSize = 16.sp,
                            fontWeight = FontWeight.Bold
                        )
                        Text(
                            text = "Capital: $${player.cash} • Propiedades: ${properties.size}",
                            fontSize = 11.sp,
                            color = MaterialTheme.colorScheme.onSurfaceVariant
                        )
                    }
                    IconButton(onClick = onDismiss) {
                        Icon(Icons.Default.Close, contentDescription = "Cerrar")
                    }
                }

                HorizontalDivider(modifier = Modifier.padding(vertical = 8.dp))

                if (properties.isEmpty()) {
                    Box(
                        modifier = Modifier
                            .fillMaxWidth()
                            .height(120.dp),
                        contentAlignment = Alignment.Center
                    ) {
                        Text(
                            text = "Aún no posees ninguna propiedad.\n¡Cae en una casilla vacía para comprarla!",
                            textAlign = TextAlign.Center,
                            fontSize = 12.sp,
                            color = MaterialTheme.colorScheme.onSurfaceVariant
                        )
                    }
                } else {
                    LazyColumn(
                        modifier = Modifier
                            .fillMaxWidth()
                            .height(260.dp),
                        verticalArrangement = Arrangement.spacedBy(6.dp)
                    ) {
                        items(properties) { tile ->
                            Card(
                                modifier = Modifier.fillMaxWidth(),
                                colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.5f))
                            ) {
                                Row(
                                    modifier = Modifier
                                        .fillMaxWidth()
                                        .padding(8.dp),
                                    verticalAlignment = Alignment.CenterVertically,
                                    horizontalArrangement = Arrangement.SpaceBetween
                                ) {
                                    Row(verticalAlignment = Alignment.CenterVertically) {
                                        Box(
                                            modifier = Modifier
                                                .size(10.dp)
                                                .clip(CircleShape)
                                                .background(tile.group?.color ?: Color.Gray)
                                        )
                                        Spacer(modifier = Modifier.width(6.dp))
                                        Column {
                                            Text(
                                                text = "${tile.icon} ${tile.name}",
                                                fontSize = 12.sp,
                                                fontWeight = FontWeight.Bold
                                            )
                                            Text(
                                                text = "Alquiler: $${tile.currentRent} • ${if (tile.houses == 4) "Hotel" else "${tile.houses} casas"}",
                                                fontSize = 10.sp,
                                                color = MaterialTheme.colorScheme.onSurfaceVariant
                                            )
                                        }
                                    }

                                    if (tile.houses < 4) {
                                        val canAfford = player.cash >= tile.houseCost
                                        Button(
                                            onClick = { onUpgrade(tile.id) },
                                            enabled = canAfford,
                                            colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF2E7D32)),
                                            shape = RoundedCornerShape(6.dp),
                                            modifier = Modifier.height(32.dp)
                                        ) {
                                            Text(
                                                text = "+Casa ($${tile.houseCost})",
                                                fontSize = 9.5.sp
                                            )
                                        }
                                    } else {
                                        Text(text = "Nivel Máximo ⭐", fontSize = 10.sp, color = Color(0xFFF57F17), fontWeight = FontWeight.Bold)
                                    }
                                }
                            }
                        }
                    }
                }

                Spacer(modifier = Modifier.height(8.dp))
                Button(onClick = onDismiss, modifier = Modifier.fillMaxWidth()) {
                    Text("Listo")
                }
            }
        }
    }
}

/**
 * Diálogo de fin de partida cuando un jugador quiebra.
 */
@Composable
fun GameOverDialog(
    winner: Player,
    onRestart: () -> Unit
) {
    AlertDialog(
        onDismissRequest = { /* No cancelable */ },
        icon = {
            Icon(
                Icons.Default.EmojiEvents,
                contentDescription = null,
                tint = Color(0xFFFFB300),
                modifier = Modifier.size(48.dp)
            )
        },
        title = {
            Text(
                text = "¡VICTORIA INMOBILIARIA!",
                fontWeight = FontWeight.ExtraBold,
                textAlign = TextAlign.Center,
                fontSize = 18.sp
            )
        },
        text = {
            Column(
                horizontalAlignment = Alignment.CenterHorizontally,
                modifier = Modifier.fillMaxWidth()
            ) {
                Text(
                    text = "El rival se declaró en bancarrota.",
                    fontSize = 13.sp,
                    color = MaterialTheme.colorScheme.onSurfaceVariant
                )
                Spacer(modifier = Modifier.height(8.dp))
                Text(
                    text = "🏆 Ganador: ${winner.avatar} ${winner.name}",
                    fontSize = 16.sp,
                    fontWeight = FontWeight.Bold,
                    color = winner.color
                )
                Text(
                    text = "Dinero final: $${winner.cash}",
                    fontSize = 14.sp,
                    fontWeight = FontWeight.SemiBold,
                    color = Color(0xFF2E7D32)
                )
            }
        },
        confirmButton = {
            Button(
                onClick = onRestart,
                modifier = Modifier
                    .fillMaxWidth()
                    .testTag("btn_restart_game")
            ) {
                Text("Jugar Otra Partida")
            }
        }
    )
}

/**
 * Diálogo explicativo de las reglas del prototipo de Capital Tycoon.
 */
@Composable
fun GameRulesDialog(onDismiss: () -> Unit) {
    Dialog(onDismissRequest = onDismiss) {
        Card(
            modifier = Modifier
                .fillMaxWidth()
                .padding(12.dp)
                .testTag("dialog_game_rules"),
            shape = RoundedCornerShape(16.dp),
            colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surface)
        ) {
            Column(modifier = Modifier.padding(18.dp)) {
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        Icon(Icons.Default.Info, contentDescription = null, tint = MaterialTheme.colorScheme.primary)
                        Spacer(modifier = Modifier.width(6.dp))
                        Text(text = "Reglas de Capital Tycoon", fontSize = 15.sp, fontWeight = FontWeight.Bold)
                    }
                    IconButton(onClick = onDismiss) {
                        Icon(Icons.Default.Close, contentDescription = "Cerrar")
                    }
                }

                HorizontalDivider(modifier = Modifier.padding(vertical = 8.dp))

                LazyColumn(modifier = Modifier.height(240.dp)) {
                    item {
                        RuleItem("🏁 Salida", "Cada vez que completas una vuelta al tablero cobras $200 de salario.")
                        RuleItem("🏢 Comprar Calles", "Si caes en una casilla sin dueño, puedes comprarla para cobrar alquiler a tus rivales.")
                        RuleItem("🏡 Construir Casas", "En tus propiedades puedes construir hasta 3 casas y 1 hotel para multiplicar el alquiler.")
                        RuleItem("🎁 Cartas de Oportunidad", "Efectos especiales: premios en efectivo, multas o desplazamientos.")
                        RuleItem("🏛️ Bote de Parque Central", "Todos los impuestos van al Parque Central. ¡Quien aterrice allí se lleva todo el acumulado!")
                        RuleItem("⚖️ Prisión", "Puedes salir pagando $50 de fianza, sacando dobles en los dados o tras cumplir 2 turnos.")
                        RuleItem("💥 Bancarrota", "Si no puedes pagar tus deudas y tu saldo cae a cero, quedas eliminado y gana tu rival.")
                    }
                }

                Spacer(modifier = Modifier.height(10.dp))
                Button(onClick = onDismiss, modifier = Modifier.fillMaxWidth()) {
                    Text("¡Entendido!")
                }
            }
        }
    }
}

@Composable
private fun RuleItem(title: String, description: String) {
    Column(modifier = Modifier.padding(vertical = 4.dp)) {
        Text(text = title, fontSize = 12.sp, fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.primary)
        Text(text = description, fontSize = 11.sp, color = MaterialTheme.colorScheme.onSurfaceVariant, lineHeight = 15.sp)
    }
}
