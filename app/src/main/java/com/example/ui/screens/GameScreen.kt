package com.example.ui.screens

import androidx.compose.animation.AnimatedVisibility
import androidx.compose.animation.fadeIn
import androidx.compose.animation.fadeOut
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Casino
import androidx.compose.material.icons.filled.Check
import androidx.compose.material.icons.filled.Close
import androidx.compose.material.icons.filled.HelpOutline
import androidx.compose.material.icons.filled.Home
import androidx.compose.material.icons.filled.Lock
import androidx.compose.material.icons.filled.Refresh
import androidx.compose.material.icons.filled.SmartToy
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedButton
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.material3.TopAppBar
import androidx.compose.material3.TopAppBarDefaults
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.testTag
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import com.example.model.Player
import com.example.model.TileType
import com.example.model.TurnPhase
import com.example.ui.components.CapitalBoardLayout
import com.example.ui.components.ChanceCardDialog
import com.example.ui.components.DiceRollView
import com.example.ui.components.GameOverDialog
import com.example.ui.components.GameRulesDialog
import com.example.ui.components.MyPropertiesDialog
import com.example.ui.components.PlayerBadgeView
import com.example.ui.components.TileDetailsDialog
import com.example.viewmodel.GameViewModel

/**
 * ============================================================================
 * PANTALLA PRINCIPAL DEL JUEGO (CAPITAL TYCOON)
 * ============================================================================
 * Diseñada específicamente para teléfonos móviles en orientación vertical.
 * Integra el tablero perimetral, dados interactivos, botones de acción
 * rápida, estadísticas de los jugadores e historial de eventos.
 */
@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun GameScreen(
    viewModel: GameViewModel,
    modifier: Modifier = Modifier
) {
    val boardTiles by viewModel.boardTiles.collectAsStateWithLifecycle()
    val players by viewModel.players.collectAsStateWithLifecycle()
    val currentPlayerIndex by viewModel.currentPlayerIndex.collectAsStateWithLifecycle()
    val diceValues by viewModel.diceValues.collectAsStateWithLifecycle()
    val turnPhase by viewModel.turnPhase.collectAsStateWithLifecycle()
    val parkingPot by viewModel.parkingPot.collectAsStateWithLifecycle()
    val activeChanceCard by viewModel.activeChanceCard.collectAsStateWithLifecycle()
    val selectedTile by viewModel.selectedTile.collectAsStateWithLifecycle()
    val gameLogs by viewModel.gameLogs.collectAsStateWithLifecycle()
    val winner by viewModel.winner.collectAsStateWithLifecycle()
    val isVsAiMode by viewModel.isVsAiMode.collectAsStateWithLifecycle()

    var showPropertiesDialog by remember { mutableStateOf(false) }
    var showRulesDialog by remember { mutableStateOf(false) }

    val activePlayer = players.getOrElse(currentPlayerIndex) { players.first() }
    val p1 = players.getOrElse(0) { players.first() }
    val p2 = players.getOrElse(1) { players.last() }

    // Cálculo de patrimonio neto para cada jugador (Efectivo + Valor de compra de inmuebles)
    val p1Properties = boardTiles.filter { it.ownerId == p1.id }
    val p2Properties = boardTiles.filter { it.ownerId == p2.id }
    val p1NetWorth = p1.cash + p1Properties.sumOf { it.price + (it.houses * it.houseCost) }
    val p2NetWorth = p2.cash + p2Properties.sumOf { it.price + (it.houses * it.houseCost) }

    Scaffold(
        modifier = modifier.fillMaxSize(),
        topBar = {
            TopAppBar(
                title = {
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        Text(
                            text = "Capital Tycoon",
                            fontSize = 17.sp,
                            fontWeight = FontWeight.Bold
                        )
                        Spacer(modifier = Modifier.width(6.dp))
                        Text(text = "🎲", fontSize = 16.sp)
                    }
                },
                actions = {
                    // Botón para alternar modo vs IA o 2 Jugadores
                    OutlinedButton(
                        onClick = { viewModel.toggleGameMode() },
                        shape = RoundedCornerShape(20.dp),
                        modifier = Modifier
                            .height(32.dp)
                            .testTag("btn_toggle_mode")
                    ) {
                        Icon(
                            if (isVsAiMode) Icons.Default.SmartToy else Icons.Default.Casino,
                            contentDescription = null,
                            modifier = Modifier.size(14.dp)
                        )
                        Spacer(modifier = Modifier.width(4.dp))
                        Text(
                            text = if (isVsAiMode) "vs IA" else "2 Jugadores",
                            fontSize = 10.sp
                        )
                    }

                    // Botón de Reglas
                    IconButton(
                        onClick = { showRulesDialog = true },
                        modifier = Modifier.testTag("btn_rules")
                    ) {
                        Icon(Icons.Default.HelpOutline, contentDescription = "Reglas del juego")
                    }

                    // Botón de Reiniciar
                    IconButton(
                        onClick = { viewModel.restartGame() },
                        modifier = Modifier.testTag("btn_restart")
                    ) {
                        Icon(Icons.Default.Refresh, contentDescription = "Reiniciar partida")
                    }
                },
                colors = TopAppBarDefaults.topAppBarColors(
                    containerColor = MaterialTheme.colorScheme.surface
                )
            )
        }
    ) { innerPadding ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(innerPadding)
                .padding(horizontal = 10.dp)
                .verticalScroll(rememberScrollState()),
            horizontalAlignment = Alignment.CenterHorizontally,
            verticalArrangement = Arrangement.spacedBy(8.dp)
        ) {
            // ================================================================
            // TARJETAS DE ESTADO ECONÓMICO DE LOS JUGADORES
            // ================================================================
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.spacedBy(8.dp)
            ) {
                PlayerBadgeView(
                    player = p1,
                    isActive = currentPlayerIndex == 0,
                    propertiesCount = p1Properties.size,
                    netWorth = p1NetWorth,
                    modifier = Modifier
                        .weight(1f)
                        .testTag("player_card_0")
                )
                PlayerBadgeView(
                    player = p2,
                    isActive = currentPlayerIndex == 1,
                    propertiesCount = p2Properties.size,
                    netWorth = p2NetWorth,
                    modifier = Modifier
                        .weight(1f)
                        .testTag("player_card_1")
                )
            }

            // Barra rápida de utilidades: Bote del Parque y Acceso a Cartera de Inmuebles
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(horizontal = 4.dp),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                // Indicador de Bote del Parque Central
                Surface(
                    shape = RoundedCornerShape(12.dp),
                    color = Color(0xFFFFF8E1),
                    border = androidx.compose.foundation.BorderStroke(1.dp, Color(0xFFFFB300))
                ) {
                    Row(
                        modifier = Modifier.padding(horizontal = 8.dp, vertical = 4.dp),
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Text(text = "💰 Bote Parque:", fontSize = 10.sp, fontWeight = FontWeight.SemiBold, color = Color(0xFF795548))
                        Spacer(modifier = Modifier.width(4.dp))
                        Text(text = "$$parkingPot", fontSize = 11.sp, fontWeight = FontWeight.Bold, color = Color(0xFFE65100))
                    }
                }

                // Botón para ver y mejorar propiedades
                OutlinedButton(
                    onClick = { showPropertiesDialog = true },
                    shape = RoundedCornerShape(12.dp),
                    modifier = Modifier
                        .height(30.dp)
                        .testTag("btn_my_properties")
                ) {
                    Icon(Icons.Default.Home, contentDescription = null, modifier = Modifier.size(13.dp))
                    Spacer(modifier = Modifier.width(4.dp))
                    Text(text = "Mis Inmuebles (${p1Properties.size})", fontSize = 10.sp)
                }
            }

            // ================================================================
            // TABLERO PERIMETRAL Y PATIO CENTRAL DE ACCIÓN
            // ================================================================
            CapitalBoardLayout(
                boardTiles = boardTiles,
                players = players,
                parkingPot = parkingPot,
                onTileClick = { tile -> viewModel.selectTile(tile) },
                centerContent = {
                    CentralActionHub(
                        viewModel = viewModel,
                        activePlayer = activePlayer,
                        diceValues = diceValues,
                        turnPhase = turnPhase
                    )
                },
                modifier = Modifier
                    .fillMaxWidth()
                    .testTag("capital_board")
            )

            // ================================================================
            // HISTORIAL DE EVENTOS Y JUGADAS RECIENTES
            // ================================================================
            Card(
                modifier = Modifier
                    .fillMaxWidth()
                    .testTag("game_logs_card"),
                shape = RoundedCornerShape(12.dp),
                colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.35f))
            ) {
                Column(modifier = Modifier.padding(10.dp)) {
                    Text(
                        text = "Actividad de la Ciudad 📰",
                        fontSize = 11.sp,
                        fontWeight = FontWeight.Bold,
                        color = MaterialTheme.colorScheme.onSurfaceVariant
                    )
                    Spacer(modifier = Modifier.height(6.dp))

                    Column(verticalArrangement = Arrangement.spacedBy(4.dp)) {
                        gameLogs.take(4).forEach { log ->
                            Row(
                                modifier = Modifier.fillMaxWidth(),
                                verticalAlignment = Alignment.CenterVertically
                            ) {
                                if (log.playerColor != null) {
                                    Box(
                                        modifier = Modifier
                                            .size(7.dp)
                                            .clip(CircleShape)
                                            .background(log.playerColor)
                                    )
                                    Spacer(modifier = Modifier.width(6.dp))
                                }
                                Text(
                                    text = log.message,
                                    fontSize = 11.sp,
                                    fontWeight = if (log.isHighlight) FontWeight.Bold else FontWeight.Normal,
                                    color = if (log.isHighlight) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.onSurface,
                                    maxLines = 2,
                                    overflow = TextOverflow.Ellipsis
                                )
                            }
                        }
                    }
                }
            }

            Spacer(modifier = Modifier.height(16.dp))
        }
    }

    // ========================================================================
    // MODALES Y DIÁLOGOS
    // ========================================================================

    // Detalle de escritura al pulsar cualquier casilla
    selectedTile?.let { tile ->
        TileDetailsDialog(
            tile = tile,
            players = players,
            currentPlayer = activePlayer,
            onUpgrade = { tileId -> viewModel.upgradeProperty(tileId) },
            onDismiss = { viewModel.selectTile(null) }
        )
    }

    // Carta de oportunidad sacada
    activeChanceCard?.let { card ->
        ChanceCardDialog(
            card = card,
            onDismiss = { viewModel.dismissChanceCard() }
        )
    }

    // Diálogo de mis propiedades para construir mejoras
    if (showPropertiesDialog) {
        MyPropertiesDialog(
            player = p1,
            properties = p1Properties,
            onUpgrade = { tileId -> viewModel.upgradeProperty(tileId) },
            onDismiss = { showPropertiesDialog = false }
        )
    }

    // Diálogo con las reglas
    if (showRulesDialog) {
        GameRulesDialog(onDismiss = { showRulesDialog = false })
    }

    // Fin de partida por bancarrota
    winner?.let { winPlayer ->
        GameOverDialog(
            winner = winPlayer,
            onRestart = { viewModel.restartGame() }
        )
    }
}

/**
 * Patio central del tablero que contiene los dados 3D y los botones de
 * decisión del turno actual.
 */
@Composable
private fun CentralActionHub(
    viewModel: GameViewModel,
    activePlayer: Player,
    diceValues: Pair<Int, Int>,
    turnPhase: TurnPhase
) {
    val isRolling = turnPhase == TurnPhase.ROLLING_ANIMATION

    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(4.dp),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.SpaceEvenly
    ) {
        // Indicador del turno activo
        Row(
            verticalAlignment = Alignment.CenterVertically,
            horizontalArrangement = Arrangement.Center
        ) {
            Box(
                modifier = Modifier
                    .size(8.dp)
                    .clip(CircleShape)
                    .background(activePlayer.color)
            )
            Spacer(modifier = Modifier.width(4.dp))
            Text(
                text = "${activePlayer.avatar} Turno de ${activePlayer.name}",
                fontSize = 10.sp,
                fontWeight = FontWeight.Bold,
                color = activePlayer.color,
                maxLines = 1,
                overflow = TextOverflow.Ellipsis
            )
        }

        // Dados de juego con animación
        DiceRollView(
            d1 = diceValues.first,
            d2 = diceValues.second,
            isRolling = isRolling
        )

        // Botones de acción según la fase del turno
        when (turnPhase) {
            TurnPhase.WAITING_ROLL -> {
                if (activePlayer.isBot) {
                    Text(
                        text = "Pensando jugada...",
                        fontSize = 11.sp,
                        color = MaterialTheme.colorScheme.onSurfaceVariant
                    )
                } else {
                    if (activePlayer.inJail) {
                        Column(
                            horizontalAlignment = Alignment.CenterHorizontally,
                            verticalArrangement = Arrangement.spacedBy(4.dp)
                        ) {
                            if (activePlayer.cash >= 50) {
                                Button(
                                    onClick = { viewModel.payJailBail() },
                                    colors = ButtonDefaults.buttonColors(containerColor = Color(0xFFD32F2F)),
                                    modifier = Modifier
                                        .height(30.dp)
                                        .testTag("btn_pay_bail")
                                ) {
                                    Text("Pagar Fianza ($50)", fontSize = 9.sp)
                                }
                            }
                            Button(
                                onClick = { viewModel.rollDice() },
                                modifier = Modifier
                                    .height(30.dp)
                                    .testTag("btn_roll_jail")
                            ) {
                                Text("Tirar por Dobles", fontSize = 9.sp)
                            }
                        }
                    } else {
                        Button(
                            onClick = { viewModel.rollDice() },
                            modifier = Modifier
                                .fillMaxWidth(0.9f)
                                .height(38.dp)
                                .testTag("btn_roll_dice"),
                            colors = ButtonDefaults.buttonColors(containerColor = activePlayer.color)
                        ) {
                            Icon(Icons.Default.Casino, contentDescription = null, modifier = Modifier.size(16.dp))
                            Spacer(modifier = Modifier.width(6.dp))
                            Text("Lanzar Dados", fontSize = 12.sp, fontWeight = FontWeight.Bold)
                        }
                    }
                }
            }

            TurnPhase.ROLLING_ANIMATION -> {
                Text(
                    text = "¡Rodando dados! 🎲",
                    fontSize = 11.sp,
                    fontWeight = FontWeight.SemiBold,
                    color = MaterialTheme.colorScheme.primary
                )
            }

            TurnPhase.DECISION_BUY -> {
                val currentTile = viewModel.currentTile
                if (activePlayer.isBot) {
                    Text(
                        text = "Analizando compra...",
                        fontSize = 11.sp,
                        color = MaterialTheme.colorScheme.onSurfaceVariant
                    )
                } else {
                    Column(
                        horizontalAlignment = Alignment.CenterHorizontally,
                        modifier = Modifier.fillMaxWidth(0.95f)
                    ) {
                        Text(
                            text = "¿Comprar ${currentTile.name}?",
                            fontSize = 10.sp,
                            fontWeight = FontWeight.Bold,
                            maxLines = 1,
                            overflow = TextOverflow.Ellipsis
                        )
                        Spacer(modifier = Modifier.height(4.dp))
                        Row(
                            modifier = Modifier.fillMaxWidth(),
                            horizontalArrangement = Arrangement.spacedBy(4.dp)
                        ) {
                            Button(
                                onClick = { viewModel.buyCurrentProperty() },
                                modifier = Modifier
                                    .weight(1f)
                                    .height(32.dp)
                                    .testTag("btn_buy_property"),
                                colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF2E7D32))
                            ) {
                                Text("Comprar ($${currentTile.price})", fontSize = 9.sp)
                            }
                            OutlinedButton(
                                onClick = { viewModel.passProperty() },
                                modifier = Modifier
                                    .weight(0.7f)
                                    .height(32.dp)
                                    .testTag("btn_pass_property")
                            ) {
                                Text("Pasar", fontSize = 9.sp)
                            }
                        }
                    }
                }
            }

            TurnPhase.RESOLVING_TILE -> {
                Text(
                    text = "Avanzando...",
                    fontSize = 11.sp,
                    color = MaterialTheme.colorScheme.onSurfaceVariant
                )
            }

            TurnPhase.DECISION_UPGRADE, TurnPhase.TURN_ENDED -> {
                if (activePlayer.isBot) {
                    Text(
                        text = "Finalizando turno...",
                        fontSize = 11.sp,
                        color = MaterialTheme.colorScheme.onSurfaceVariant
                    )
                } else {
                    Button(
                        onClick = { viewModel.endTurn() },
                        modifier = Modifier
                            .fillMaxWidth(0.85f)
                            .height(36.dp)
                            .testTag("btn_end_turn")
                    ) {
                        Icon(Icons.Default.Check, contentDescription = null, modifier = Modifier.size(16.dp))
                        Spacer(modifier = Modifier.width(6.dp))
                        Text("Terminar Turno", fontSize = 11.sp, fontWeight = FontWeight.Bold)
                    }
                }
            }

            TurnPhase.GAME_OVER -> {
                Text(
                    text = "¡Partida Finalizada!",
                    fontSize = 11.sp,
                    fontWeight = FontWeight.Bold,
                    color = MaterialTheme.colorScheme.primary
                )
            }
        }
    }
}
