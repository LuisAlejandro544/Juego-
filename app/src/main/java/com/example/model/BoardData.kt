package com.example.model

/**
 * ============================================================================
 * DATOS INICIALES DEL TABLERO Y CARTAS DE SUERTE
 * ============================================================================
 * Contiene la definición predeterminada de las 20 casillas del circuito
 * de "Capital Tycoon" y la baraja de eventos sorpresivos.
 */
object BoardData {

    /**
     * Lista completa de las 20 casillas que componen el tablero perimeter.
     * Diseñado en un bucle cerrado ordenado en sentido horario.
     */
    fun createDefaultBoard(): List<BoardTile> = listOf(
        // CASILLA 0: SALIDA
        BoardTile(
            id = 0,
            name = "Salida",
            type = TileType.START,
            icon = "🏁"
        ),
        // CASILLA 1: DISTRITO ANTIGUO
        BoardTile(
            id = 1,
            name = "Paseo Flores",
            type = TileType.PROPERTY,
            group = PropertyGroup.BROWN,
            price = 60,
            baseRent = 10,
            houseCost = 50,
            icon = "🏡"
        ),
        // CASILLA 2: SUERTE
        BoardTile(
            id = 2,
            name = "Oportunidad",
            type = TileType.CHANCE,
            icon = "🎁"
        ),
        // CASILLA 3: DISTRITO ANTIGUO
        BoardTile(
            id = 3,
            name = "Av. del Puerto",
            type = TileType.PROPERTY,
            group = PropertyGroup.BROWN,
            price = 80,
            baseRent = 15,
            houseCost = 50,
            icon = "⚓"
        ),
        // CASILLA 4: IMPUESTO URBANO
        BoardTile(
            id = 4,
            name = "Impuesto Urbano",
            type = TileType.TAX,
            price = 100, // Monto a pagar
            icon = "🏛️"
        ),
        // CASILLA 5: CÁRCEL / DE VISITA
        BoardTile(
            id = 5,
            name = "Cárcel",
            type = TileType.JAIL,
            icon = "⚖️"
        ),
        // CASILLA 6: DISTRITO COSTERO
        BoardTile(
            id = 6,
            name = "Calle Mayor",
            type = TileType.PROPERTY,
            group = PropertyGroup.CYAN,
            price = 100,
            baseRent = 20,
            houseCost = 60,
            icon = "🏖️"
        ),
        // CASILLA 7: ESTACIÓN DE TREN
        BoardTile(
            id = 7,
            name = "Estación Norte",
            type = TileType.PROPERTY,
            group = PropertyGroup.STATION,
            price = 150,
            baseRent = 30,
            houseCost = 75,
            icon = "🚆"
        ),
        // CASILLA 8: DISTRITO COSTERO
        BoardTile(
            id = 8,
            name = "Av. Costanera",
            type = TileType.PROPERTY,
            group = PropertyGroup.CYAN,
            price = 120,
            baseRent = 25,
            houseCost = 60,
            icon = "⛵"
        ),
        // CASILLA 9: SUERTE
        BoardTile(
            id = 9,
            name = "Suerte",
            type = TileType.CHANCE,
            icon = "🍀"
        ),
        // CASILLA 10: ESTACIONAMIENTO GRATUITO / BOTE
        BoardTile(
            id = 10,
            name = "Parque Bote",
            type = TileType.FREE_PARKING,
            icon = "💰"
        ),
        // CASILLA 11: DISTRITO TECNOLÓGICO
        BoardTile(
            id = 11,
            name = "Plaza del Sol",
            type = TileType.PROPERTY,
            group = PropertyGroup.ORANGE,
            price = 160,
            baseRent = 35,
            houseCost = 80,
            icon = "☀️"
        ),
        // CASILLA 12: COMPAÑÍA DE ENERGÍA
        BoardTile(
            id = 12,
            name = "Compañía Eléctrica",
            type = TileType.PROPERTY,
            group = PropertyGroup.SERVICES,
            price = 140,
            baseRent = 28,
            houseCost = 70,
            icon = "⚡"
        ),
        // CASILLA 13: DISTRITO TECNOLÓGICO
        BoardTile(
            id = 13,
            name = "Gran Vía Tech",
            type = TileType.PROPERTY,
            group = PropertyGroup.ORANGE,
            price = 180,
            baseRent = 40,
            houseCost = 80,
            icon = "💻"
        ),
        // CASILLA 14: COMUNIDAD
        BoardTile(
            id = 14,
            name = "Caja Sorpresa",
            type = TileType.CHANCE,
            icon = "⭐"
        ),
        // CASILLA 15: ¡VE A LA CÁRCEL!
        BoardTile(
            id = 15,
            name = "A la Cárcel",
            type = TileType.GO_TO_JAIL,
            icon = "👮"
        ),
        // CASILLA 16: ZONA FINANCIERA
        BoardTile(
            id = 16,
            name = "Paseo del Prado",
            type = TileType.PROPERTY,
            group = PropertyGroup.RED,
            price = 220,
            baseRent = 50,
            houseCost = 100,
            icon = "🏦"
        ),
        // CASILLA 17: ZONA FINANCIERA
        BoardTile(
            id = 17,
            name = "Distrito Bolsa",
            type = TileType.PROPERTY,
            group = PropertyGroup.RED,
            price = 240,
            baseRent = 55,
            houseCost = 100,
            icon = "📈"
        ),
        // CASILLA 18: TASA DE LUJO
        BoardTile(
            id = 18,
            name = "Tasa de Lujo",
            type = TileType.TAX,
            price = 75,
            icon = "💎"
        ),
        // CASILLA 19: MILLA DE ORO
        BoardTile(
            id = 19,
            name = "Torre Imperial",
            type = TileType.PROPERTY,
            group = PropertyGroup.BLUE,
            price = 350,
            baseRent = 85,
            houseCost = 150,
            icon = "👑"
        )
    )

    /**
     * Mazo de cartas de Suerte y Oportunidad.
     */
    fun createChanceDeck(): List<ChanceCard> = listOf(
        ChanceCard(
            id = 1,
            title = "¡Premio de la Lotería!",
            description = "Has ganado el segundo premio de la lotería de la ciudad. ¡Cobra $150!",
            cashReward = 150
        ),
        ChanceCard(
            id = 2,
            title = "Reparación en tus Inmuebles",
            description = "Tuviste que pagar mantenimiento urgente de fontanería. Paga $50.",
            cashReward = -50
        ),
        ChanceCard(
            id = 3,
            title = "Reintegro de Impuestos",
            description = "Hacienda te devuelve fondos tributarios. Recibes $80.",
            cashReward = 80
        ),
        ChanceCard(
            id = 4,
            title = "Exceso de Velocidad",
            description = "La policía de tráfico te multa con $40 por acelerar en tu auto.",
            cashReward = -40
        ),
        ChanceCard(
            id = 5,
            title = "¡Vuelo Directo a la Salida!",
            description = "Avanzas directamente a la Salida y cobras tus $200 de salario.",
            teleportToTile = 0
        ),
        ChanceCard(
            id = 6,
            title = "Dividendo de Acciones",
            description = "Tus inversiones en el banco rinden grandes frutos. Cobra $100.",
            cashReward = 100
        ),
        ChanceCard(
            id = 7,
            title = "Paseo Turístico",
            description = "Avanzas 3 casillas explorando la metrópoli.",
            moveSteps = 3
        ),
        ChanceCard(
            id = 8,
            title = "Cena de Negocios VIP",
            description = "Invitaste a inversionistas a un restaurante de 5 estrellas. Paga $60.",
            cashReward = -60
        )
    )
}
