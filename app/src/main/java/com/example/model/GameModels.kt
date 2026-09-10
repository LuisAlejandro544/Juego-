package com.example.model

import androidx.compose.ui.graphics.Color

/**
 * ============================================================================
 * MODELOS DE DATOS PARA EL JUEGO "CAPITAL TYCOON"
 * ============================================================================
 * Este archivo contiene todas las estructuras de datos que representan el
 * estado del tablero, casillas, jugadores, cartas de oportunidad y eventos.
 * Diseñado con explicaciones claras en español para facilitar su mantenimiento.
 */

/**
 * Tipos de casillas disponibles en el tablero del juego.
 */
enum class TileType {
    START,          // Casilla de Salida (Cobra salario al pasar o caer)
    PROPERTY,       // Propiedad adquirible (Genera alquiler)
    CHANCE,         // Casilla de Suerte / Oportunidad (Roba tarjeta de evento)
    TAX,            // Impuesto municipal (Pago que va al bote acumulado)
    JAIL,           // Cárcel / De visita
    FREE_PARKING,   // Estacionamiento gratuito / Bote de impuestos acumulados
    GO_TO_JAIL      // Casilla que envía directamente a prisión
}

/**
 * Grupos de color para las propiedades del tablero, similar a las zonas
 * clásicas de bienes raíces.
 */
enum class PropertyGroup(val groupName: String, val color: Color) {
    BROWN("Distrito Antiguo", Color(0xFF8D6E63)),
    CYAN("Distrito Costero", Color(0xFF26C6DA)),
    MAGENTA("Distrito Comercial", Color(0xFFEC407A)),
    ORANGE("Distrito Tecnológico", Color(0xFFFFA726)),
    RED("Avenida Principal", Color(0xFFEF5350)),
    YELLOW("Zona Financiera", Color(0xFFFFCA28)),
    GREEN("Parque Residencial", Color(0xFF66BB6A)),
    BLUE("Milla de Oro", Color(0xFF42A5F5)),
    SERVICES("Servicios Públicos", Color(0xFF78909C)),
    STATION("Estaciones", Color(0xFF8E24AA))
}

/**
 * Representación de una casilla individual dentro del tablero circular.
 *
 * @param id Identificador único y posición en el tablero (0 a 19).
 * @param name Nombre descriptivo de la casilla o calle.
 * @param type Tipo de casilla (Propiedad, Salida, Suerte, Cárcel, etc.).
 * @param group Grupo de color (solo aplica si es PROPERTY).
 * @param price Precio de compra de la propiedad.
 * @param baseRent Alquiler base cuando un rival cae en la casilla.
 * @param houseCost Costo por construir una casa o mejora de nivel.
 * @param houses Cantidad de casas construidas (0 a 3, nivel 4 = Hotel).
 * @param ownerId ID del jugador propietario (null si no tiene dueño).
 * @param icon Símbolo o emoji representativo de la casilla.
 */
data class BoardTile(
    val id: Int,
    val name: String,
    val type: TileType,
    val group: PropertyGroup? = null,
    val price: Int = 0,
    val baseRent: Int = 0,
    val houseCost: Int = 50,
    val houses: Int = 0,
    val ownerId: Int? = null,
    val icon: String = "🏢"
) {
    /**
     * Calcula el alquiler actual según las casas construidas.
     * Cada casa multiplica el valor del alquiler sustancialmente.
     */
    val currentRent: Int
        get() = when (houses) {
            0 -> baseRent
            1 -> baseRent * 2
            2 -> baseRent * 4
            3 -> baseRent * 7
            else -> baseRent * 12 // Hotel o nivel máximo
        }
}

/**
 * Representa a un jugador en la partida (humano o bot de IA).
 *
 * @param id Identificador del jugador (0 = Jugador 1 / Usuario, 1 = Jugador 2 / Bot).
 * @param name Nombre visible del jugador.
 * @param isBot Indica si este jugador es controlado por la computadora.
 * @param avatar Emoji representativo de la ficha del jugador (ej. 🎩, 🚗).
 * @param color Color temático del jugador para marcar casillas e interfaz.
 * @param cash Dinero en efectivo disponible para compras y pagos.
 * @param position Índice de la casilla actual en el tablero (0 a 19).
 * @param inJail Indica si el jugador se encuentra preso.
 * @param jailTurns Contador de turnos restantes en prisión.
 * @param isBankrupt Indica si el jugador ha quedado en bancarrota (saldo < 0 sin fondos).
 */
data class Player(
    val id: Int,
    val name: String,
    val isBot: Boolean,
    val avatar: String,
    val color: Color,
    val cash: Int = 1500,
    val position: Int = 0,
    val inJail: Boolean = false,
    val jailTurns: Int = 0,
    val isBankrupt: Boolean = false
)

/**
 * Tarjeta de Oportunidad / Suerte que genera giros inesperados en la partida.
 */
data class ChanceCard(
    val id: Int,
    val title: String,
    val description: String,
    val cashReward: Int = 0,     // Puede ser positivo (premio) o negativo (multa)
    val moveSteps: Int = 0,      // Pasos que avanza o retrocede
    val teleportToTile: Int? = null // Envía a casilla específica si no es nulo
)

/**
 * Registro de actividad para mostrar los acontecimientos en el historial del juego.
 */
data class GameLogEntry(
    val id: Long = System.currentTimeMillis(),
    val message: String,
    val isHighlight: Boolean = false,
    val playerColor: Color? = null
)

/**
 * Fases por las que pasa un turno en el juego.
 */
enum class TurnPhase {
    WAITING_ROLL,       // Esperando a que el jugador tire los dados
    ROLLING_ANIMATION,  // Dados rodando con animación
    RESOLVING_TILE,     // Jugador se mueve y se evalúa la casilla
    DECISION_BUY,       // Preguntando si desea comprar la propiedad
    DECISION_UPGRADE,   // Puede comprar casas o pasar turno
    TURN_ENDED,         // Turno concluido, listo para el siguiente jugador
    GAME_OVER           // Uno de los jugadores cayó en bancarrota
}
