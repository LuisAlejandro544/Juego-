package com.example.viewmodel

import androidx.compose.ui.graphics.Color
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.example.model.BoardData
import com.example.model.BoardTile
import com.example.model.ChanceCard
import com.example.model.GameLogEntry
import com.example.model.Player
import com.example.model.TileType
import com.example.model.TurnPhase
import kotlinx.coroutines.delay
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch
import kotlin.random.Random

/**
 * ============================================================================
 * VIEWMODEL PRINCIPAL DEL JUEGO "CAPITAL TYCOON"
 * ============================================================================
 * Gestiona toda la lógica de negocio, reglas de las casillas, economía de
 * los jugadores, inteligencia artificial (Bot) rival y turnos.
 *
 * Contiene comentarios explicativos en español para cada función principal.
 */
class GameViewModel : ViewModel() {

    // Lista de casillas del tablero
    private val _boardTiles = MutableStateFlow<List<BoardTile>>(BoardData.createDefaultBoard())
    val boardTiles: StateFlow<List<BoardTile>> = _boardTiles.asStateFlow()

    // Jugadores de la partida (Jugador 1 Humano vs Jugador 2 / Bot)
    private val _players = MutableStateFlow<List<Player>>(
        listOf(
            Player(
                id = 0,
                name = "Tú (Inversor)",
                isBot = false,
                avatar = "🎩",
                color = Color(0xFF1E88E5), // Azul corporativo
                cash = 1500,
                position = 0
            ),
            Player(
                id = 1,
                name = "Bot Magnate",
                isBot = true,
                avatar = "🚗",
                color = Color(0xFFE53935), // Rojo rival
                cash = 1500,
                position = 0
            )
        )
    )
    val players: StateFlow<List<Player>> = _players.asStateFlow()

    // Índice del jugador activo (0 o 1)
    private val _currentPlayerIndex = MutableStateFlow(0)
    val currentPlayerIndex: StateFlow<Int> = _currentPlayerIndex.asStateFlow()

    // Valores de los dos dados
    private val _diceValues = MutableStateFlow(Pair(1, 1))
    val diceValues: StateFlow<Pair<Int, Int>> = _diceValues.asStateFlow()

    // Fase actual del turno
    private val _turnPhase = MutableStateFlow(TurnPhase.WAITING_ROLL)
    val turnPhase: StateFlow<TurnPhase> = _turnPhase.asStateFlow()

    // Bote acumulado de impuestos en el Parque Central
    private val _parkingPot = MutableStateFlow(100)
    val parkingPot: StateFlow<Int> = _parkingPot.asStateFlow()

    // Carta de Suerte activa mostrada al jugador
    private val _activeChanceCard = MutableStateFlow<ChanceCard?>(null)
    val activeChanceCard: StateFlow<ChanceCard?> = _activeChanceCard.asStateFlow()

    // Casilla seleccionada para ver detalles en el modal
    private val _selectedTile = MutableStateFlow<BoardTile?>(null)
    val selectedTile: StateFlow<BoardTile?> = _selectedTile.asStateFlow()

    // Historial de eventos y transacciones
    private val _gameLogs = MutableStateFlow<List<GameLogEntry>>(
        listOf(
            GameLogEntry(message = "¡Bienvenidos a Capital Tycoon! Inician con $1,500 cada uno.", isHighlight = true)
        )
    )
    val gameLogs: StateFlow<List<GameLogEntry>> = _gameLogs.asStateFlow()

    // Jugador ganador si termina la partida
    private val _winner = MutableStateFlow<Player?>(null)
    val winner: StateFlow<Player?> = _winner.asStateFlow()

    // Modo de juego: Contra la IA o Pasa y Juega (2 jugadores humanos)
    private val _isVsAiMode = MutableStateFlow(true)
    val isVsAiMode: StateFlow<Boolean> = _isVsAiMode.asStateFlow()

    // Mazo de cartas de oportunidad
    private var chanceDeck = BoardData.createChanceDeck().shuffled()
    private var chanceIndex = 0

    val currentPlayer: Player
        get() = _players.value[_currentPlayerIndex.value]

    val currentTile: BoardTile
        get() = _boardTiles.value[currentPlayer.position]

    /**
     * Alterna entre modo contra IA o dos jugadores humanos locales.
     */
    fun toggleGameMode() {
        val newVsAi = !_isVsAiMode.value
        _isVsAiMode.value = newVsAi
        _players.update { list ->
            list.mapIndexed { index, player ->
                if (index == 1) {
                    player.copy(
                        name = if (newVsAi) "Bot Magnate" else "Jugador 2",
                        isBot = newVsAi
                    )
                } else player
            }
        }
        addLog(
            message = if (newVsAi) "Modo cambiado a: vs Inteligencia Artificial" else "Modo cambiado a: Pasa y Juega (2 Jugadores)",
            isHighlight = true
        )
    }

    /**
     * Acción principal: Lanzar los dados y mover la ficha del jugador activo.
     */
    fun rollDice() {
        if (_turnPhase.value != TurnPhase.WAITING_ROLL || _winner.value != null) return

        val player = currentPlayer

        // Si el jugador está en prisión, verificar si debe pagar o esperar
        if (player.inJail) {
            handleJailTurn(player)
            return
        }

        viewModelScope.launch {
            _turnPhase.value = TurnPhase.ROLLING_ANIMATION

            // Simulación visual rápida de dados rodando
            var d1 = 1
            var d2 = 1
            repeat(6) {
                d1 = Random.nextInt(1, 7)
                d2 = Random.nextInt(1, 7)
                _diceValues.value = Pair(d1, d2)
                delay(70)
            }

            val totalSteps = d1 + d2
            val isDouble = d1 == d2
            val bonusText = if (isDouble) " (¡Dobles!)" else ""
            addLog("${player.name} sacó un $totalSteps ($d1 y $d2)$bonusText.", playerColor = player.color)

            // Movimiento paso a paso alrededor del circuito de 20 casillas
            val oldPos = player.position
            val newPos = (oldPos + totalSteps) % 20
            val passedStart = (oldPos + totalSteps) >= 20

            // Recompensa por pasar por la Salida ($200)
            if (passedStart) {
                _players.update { currentList ->
                    currentList.map { p ->
                        if (p.id == player.id) p.copy(cash = p.cash + 200) else p
                    }
                }
                addLog("🏁 ${player.name} pasó por la Salida y cobró $200 de salario.", isHighlight = true, playerColor = player.color)
            }

            // Actualizar posición del jugador
            _players.update { currentList ->
                currentList.map { p ->
                    if (p.id == player.id) p.copy(position = newPos) else p
                }
            }

            delay(350)
            resolveLandedTile(newPos)
        }
    }

    /**
     * Evalúa la casilla en la que aterrizó el jugador y aplica sus reglas.
     */
    private fun resolveLandedTile(tileIndex: Int) {
        val tile = _boardTiles.value[tileIndex]
        val player = currentPlayer
        _turnPhase.value = TurnPhase.RESOLVING_TILE

        when (tile.type) {
            TileType.START -> {
                addLog("${player.name} descansó en la Salida.", playerColor = player.color)
                _turnPhase.value = TurnPhase.DECISION_UPGRADE
                checkBotAutoTurn()
            }

            TileType.PROPERTY -> {
                if (tile.ownerId == null) {
                    // Propiedad libre para compra
                    if (player.cash >= tile.price) {
                        addLog("🏢 ${player.name} cayó en ${tile.name}. Disponible por $${tile.price}.", playerColor = player.color)
                        _turnPhase.value = TurnPhase.DECISION_BUY
                        if (player.isBot) {
                            handleBotBuyDecision(tile)
                        }
                    } else {
                        addLog("${player.name} cayó en ${tile.name}, pero no tiene fondos suficientes ($${tile.price}).", playerColor = player.color)
                        _turnPhase.value = TurnPhase.DECISION_UPGRADE
                        checkBotAutoTurn()
                    }
                } else if (tile.ownerId == player.id) {
                    // Propiedad del mismo jugador (posibilidad de construir)
                    addLog("🏡 ${player.name} visitó su propia propiedad: ${tile.name}.", playerColor = player.color)
                    _turnPhase.value = TurnPhase.DECISION_UPGRADE
                    if (player.isBot) {
                        handleBotUpgradeDecision(tile)
                    }
                } else {
                    // Propiedad de un rival: Cobrar alquiler
                    val owner = _players.value.first { it.id == tile.ownerId }
                    val rent = tile.currentRent
                    addLog("💸 ¡Alquiler! ${player.name} cayó en propiedad de ${owner.name} (${tile.name}). Paga $rent.", playerColor = player.color)

                    transferCash(fromPlayerId = player.id, toPlayerId = owner.id, amount = rent)
                    _turnPhase.value = TurnPhase.DECISION_UPGRADE
                    checkBotAutoTurn()
                }
            }

            TileType.CHANCE -> {
                drawChanceCard(player)
            }

            TileType.TAX -> {
                val taxAmount = tile.price
                addLog("🏛️ Impuesto: ${player.name} pagó $$taxAmount que van al bote municipal.", playerColor = player.color)
                _parkingPot.update { it + taxAmount }
                deductCash(player.id, taxAmount)
                _turnPhase.value = TurnPhase.DECISION_UPGRADE
                checkBotAutoTurn()
            }

            TileType.JAIL -> {
                addLog("${player.name} está de visita pacífica en la Cárcel.", playerColor = player.color)
                _turnPhase.value = TurnPhase.DECISION_UPGRADE
                checkBotAutoTurn()
            }

            TileType.FREE_PARKING -> {
                val pot = _parkingPot.value
                if (pot > 0) {
                    addLog("💰 ¡Bote de Parque Central! ${player.name} recolectó el premio acumulado de $$pot.", isHighlight = true, playerColor = player.color)
                    _players.update { currentList ->
                        currentList.map { p ->
                            if (p.id == player.id) p.copy(cash = p.cash + pot) else p
                        }
                    }
                    _parkingPot.value = 50 // Se reinicia con un fondo base
                } else {
                    addLog("${player.name} se relajó en el Parque Central.", playerColor = player.color)
                }
                _turnPhase.value = TurnPhase.DECISION_UPGRADE
                checkBotAutoTurn()
            }

            TileType.GO_TO_JAIL -> {
                addLog("👮 ¡A la cárcel! ${player.name} fue arrestado por evasión fiscal.", isHighlight = true, playerColor = player.color)
                _players.update { currentList ->
                    currentList.map { p ->
                        if (p.id == player.id) p.copy(position = 5, inJail = true, jailTurns = 2) else p
                    }
                }
                _turnPhase.value = TurnPhase.TURN_ENDED
                checkBotAutoTurn()
            }
        }
    }

    /**
     * Compra la propiedad donde está parado el jugador activo.
     */
    fun buyCurrentProperty() {
        val player = currentPlayer
        val tile = currentTile

        if (tile.type != TileType.PROPERTY || tile.ownerId != null || player.cash < tile.price) return

        // Descontar dinero y asignar propiedad
        _players.update { list ->
            list.map { p ->
                if (p.id == player.id) p.copy(cash = p.cash - tile.price) else p
            }
        }

        _boardTiles.update { list ->
            list.map { t ->
                if (t.id == tile.id) t.copy(ownerId = player.id) else t
            }
        }

        addLog("🎉 ${player.name} compró ${tile.name} por $${tile.price}.", isHighlight = true, playerColor = player.color)
        _turnPhase.value = TurnPhase.DECISION_UPGRADE
        checkBotAutoTurn()
    }

    /**
     * Declina comprar la propiedad actual.
     */
    fun passProperty() {
        addLog("${currentPlayer.name} decidió no comprar ${currentTile.name}.", playerColor = currentPlayer.color)
        _turnPhase.value = TurnPhase.DECISION_UPGRADE
        checkBotAutoTurn()
    }

    /**
     * Construye una casa o mejora el inmueble para aumentar el alquiler.
     */
    fun upgradeProperty(tileId: Int) {
        val player = currentPlayer
        val tile = _boardTiles.value.firstOrNull { it.id == tileId } ?: return

        if (tile.ownerId != player.id || tile.houses >= 4 || player.cash < tile.houseCost) return

        _players.update { list ->
            list.map { p ->
                if (p.id == player.id) p.copy(cash = p.cash - tile.houseCost) else p
            }
        }

        val newHouses = tile.houses + 1
        _boardTiles.update { list ->
            list.map { t ->
                if (t.id == tile.id) t.copy(houses = newHouses) else t
            }
        }

        val levelName = if (newHouses == 4) "Hotel de Lujo 🏨" else "Casa #$newHouses 🏡"
        addLog("🔨 ${player.name} construyó $levelName en ${tile.name} (Alquiler ahora: $${tile.copy(houses = newHouses).currentRent}).", isHighlight = true, playerColor = player.color)
    }

    /**
     * Paga la fianza de $50 para salir de prisión inmediatamente.
     */
    fun payJailBail() {
        val player = currentPlayer
        if (!player.inJail || player.cash < 50) return

        _players.update { list ->
            list.map { p ->
                if (p.id == player.id) p.copy(cash = p.cash - 50, inJail = false, jailTurns = 0) else p
            }
        }
        _parkingPot.update { it + 50 }
        addLog("🔓 ${player.name} pagó $50 de fianza y salió de prisión.", isHighlight = true, playerColor = player.color)
        _turnPhase.value = TurnPhase.WAITING_ROLL
    }

    /**
     * Maneja el turno de un jugador que está en prisión.
     */
    private fun handleJailTurn(player: Player) {
        viewModelScope.launch {
            _turnPhase.value = TurnPhase.ROLLING_ANIMATION
            val d1 = Random.nextInt(1, 7)
            val d2 = Random.nextInt(1, 7)
            _diceValues.value = Pair(d1, d2)
            delay(400)

            if (d1 == d2) {
                // Dobles: Salida libre
                _players.update { list ->
                    list.map { p ->
                        if (p.id == player.id) p.copy(inJail = false, jailTurns = 0) else p
                    }
                }
                addLog("🎲 ¡Dados dobles ($d1 y $d2)! ${player.name} quedó libre de prisión gratis.", isHighlight = true, playerColor = player.color)
                _turnPhase.value = TurnPhase.WAITING_ROLL
            } else {
                val newTurns = player.jailTurns - 1
                if (newTurns <= 0) {
                    // Cumplió condena, paga $50 de tasa administrativa y sale
                    _players.update { list ->
                        list.map { p ->
                            if (p.id == player.id) p.copy(cash = p.cash - 50, inJail = false, jailTurns = 0) else p
                        }
                    }
                    _parkingPot.update { it + 50 }
                    addLog("⚖️ ${player.name} cumplió su condena, pagó $50 de tasa y quedó libre.", playerColor = player.color)
                    _turnPhase.value = TurnPhase.TURN_ENDED
                } else {
                    _players.update { list ->
                        list.map { p ->
                            if (p.id == player.id) p.copy(jailTurns = newTurns) else p
                        }
                    }
                    addLog("${player.name} sacó $d1 y $d2. Sigue en prisión (Turnos restantes: $newTurns).", playerColor = player.color)
                    _turnPhase.value = TurnPhase.TURN_ENDED
                }
                checkBotAutoTurn()
            }
        }
    }

    /**
     * Roba una carta de suerte y aplica sus consecuencias.
     */
    private fun drawChanceCard(player: Player) {
        if (chanceIndex >= chanceDeck.size) {
            chanceDeck = chanceDeck.shuffled()
            chanceIndex = 0
        }
        val card = chanceDeck[chanceIndex++]
        _activeChanceCard.value = card

        addLog("🎁 Carta para ${player.name}: \"${card.title}\"", isHighlight = true, playerColor = player.color)

        // Aplicar efecto financiero
        if (card.cashReward > 0) {
            _players.update { list ->
                list.map { p ->
                    if (p.id == player.id) p.copy(cash = p.cash + card.cashReward) else p
                }
            }
        } else if (card.cashReward < 0) {
            deductCash(player.id, -card.cashReward)
        }

        // Aplicar teletransporte o avance si corresponde
        if (card.teleportToTile != null) {
            _players.update { list ->
                list.map { p ->
                    if (p.id == player.id) p.copy(position = card.teleportToTile, cash = p.cash + 200) else p
                }
            }
        } else if (card.moveSteps > 0) {
            val newPos = (player.position + card.moveSteps) % 20
            _players.update { list ->
                list.map { p ->
                    if (p.id == player.id) p.copy(position = newPos) else p
                }
            }
        }

        _turnPhase.value = TurnPhase.DECISION_UPGRADE
        checkBotAutoTurn()
    }

    /**
     * Cierra el modal de la carta de oportunidad.
     */
    fun dismissChanceCard() {
        _activeChanceCard.value = null
    }

    /**
     * Finaliza el turno actual y pasa al siguiente jugador.
     */
    fun endTurn() {
        if (_winner.value != null) return

        _activeChanceCard.value = null
        val nextIndex = (_currentPlayerIndex.value + 1) % _players.value.size
        _currentPlayerIndex.value = nextIndex
        _turnPhase.value = TurnPhase.WAITING_ROLL

        val nextPlayer = _players.value[nextIndex]
        addLog("👉 Turno de: ${nextPlayer.name}", playerColor = nextPlayer.color)

        // Si el siguiente jugador es la IA, ejecuta su turno automáticamente con pequeña pausa
        if (nextPlayer.isBot) {
            viewModelScope.launch {
                delay(700)
                if (_players.value[nextIndex].inJail && _players.value[nextIndex].cash >= 100) {
                    payJailBail()
                    delay(500)
                }
                rollDice()
            }
        }
    }

    /**
     * Decisión inteligente del bot para adquirir propiedades disponibles.
     */
    private fun handleBotBuyDecision(tile: BoardTile) {
        viewModelScope.launch {
            delay(900)
            val bot = currentPlayer
            // El bot compra si le queda un colchón seguro de al menos $100
            if (bot.cash - tile.price >= 100) {
                buyCurrentProperty()
            } else {
                passProperty()
            }
        }
    }

    /**
     * Decisión del bot para mejorar sus propiedades cuando tiene capital holgado.
     */
    private fun handleBotUpgradeDecision(tile: BoardTile) {
        viewModelScope.launch {
            delay(700)
            val bot = currentPlayer
            if (tile.houses < 4 && bot.cash - tile.houseCost >= 250) {
                upgradeProperty(tile.id)
            }
            delay(500)
            endTurn()
        }
    }

    /**
     * Si el bot está en fase de finalizar turno, lo concluye de forma autónoma.
     */
    private fun checkBotAutoTurn() {
        val player = currentPlayer
        if (player.isBot && _winner.value == null) {
            viewModelScope.launch {
                delay(1000)
                if (_turnPhase.value == TurnPhase.DECISION_UPGRADE || _turnPhase.value == TurnPhase.TURN_ENDED) {
                    endTurn()
                }
            }
        }
    }

    /**
     * Transfiere dinero de un jugador a otro por concepto de alquiler.
     */
    private fun transferCash(fromPlayerId: Int, toPlayerId: Int, amount: Int) {
        var isBankrupt = false

        _players.update { list ->
            list.map { p ->
                when (p.id) {
                    fromPlayerId -> {
                        val remaining = p.cash - amount
                        if (remaining < 0) {
                            isBankrupt = true
                            p.copy(cash = 0, isBankrupt = true)
                        } else {
                            p.copy(cash = remaining)
                        }
                    }
                    toPlayerId -> p.copy(cash = p.cash + amount)
                    else -> p
                }
            }
        }

        if (isBankrupt) {
            val loser = _players.value.first { it.id == fromPlayerId }
            val winner = _players.value.first { it.id == toPlayerId }
            _winner.value = winner
            _turnPhase.value = TurnPhase.GAME_OVER
            addLog("💥 ¡BANCARROTA! ${loser.name} se quedó sin fondos. ¡${winner.name} es el ganador!", isHighlight = true)
        }
    }

    /**
     * Deduce dinero a un jugador (para impuestos o multas).
     */
    private fun deductCash(playerId: Int, amount: Int) {
        var isBankrupt = false

        _players.update { list ->
            list.map { p ->
                if (p.id == playerId) {
                    val remaining = p.cash - amount
                    if (remaining < 0) {
                        isBankrupt = true
                        p.copy(cash = 0, isBankrupt = true)
                    } else {
                        p.copy(cash = remaining)
                    }
                } else p
            }
        }

        if (isBankrupt) {
            val loser = _players.value.first { it.id == playerId }
            val otherPlayer = _players.value.first { it.id != playerId }
            _winner.value = otherPlayer
            _turnPhase.value = TurnPhase.GAME_OVER
            addLog("💥 ¡BANCARROTA! ${loser.name} no pudo pagar sus obligaciones.", isHighlight = true)
        }
    }

    /**
     * Selecciona una casilla para ver sus detalles en el visor de escritura.
     */
    fun selectTile(tile: BoardTile?) {
        _selectedTile.value = tile
    }

    /**
     * Añade una entrada al historial de eventos.
     */
    private fun addLog(message: String, isHighlight: Boolean = false, playerColor: Color? = null) {
        _gameLogs.update { current ->
            listOf(GameLogEntry(message = message, isHighlight = isHighlight, playerColor = playerColor)) + current.take(25)
        }
    }

    /**
     * Reinicia la partida completa a los valores iniciales.
     */
    fun restartGame() {
        _boardTiles.value = BoardData.createDefaultBoard()
        _parkingPot.value = 100
        _activeChanceCard.value = null
        _selectedTile.value = null
        _winner.value = null
        _currentPlayerIndex.value = 0
        _turnPhase.value = TurnPhase.WAITING_ROLL
        _diceValues.value = Pair(1, 1)

        val vsAi = _isVsAiMode.value
        _players.value = listOf(
            Player(id = 0, name = "Tú (Inversor)", isBot = false, avatar = "🎩", color = Color(0xFF1E88E5), cash = 1500, position = 0),
            Player(id = 1, name = if (vsAi) "Bot Magnate" else "Jugador 2", isBot = vsAi, avatar = "🚗", color = Color(0xFFE53935), cash = 1500, position = 0)
        )
        chanceDeck = BoardData.createChanceDeck().shuffled()
        chanceIndex = 0

        _gameLogs.value = listOf(
            GameLogEntry(message = "¡Nueva partida iniciada! La ciudad espera al mejor magnate.", isHighlight = true)
        )
    }
}
