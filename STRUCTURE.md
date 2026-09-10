# Estructura del Proyecto (Architecture & File Tree) 🏗️

Este documento describe la organización de carpetas, módulos de código y modelos de datos del proyecto **Capital Tycoon**.

---

## 🌳 Árbol de Directorios del Repositorio

```text
.
├── .github/
│   └── workflows/
│       ├── generar_tablero.yml            # Generación de tableros (manual: workflow_dispatch)
│       └── propuestas_iconos.yml          # Catálogo de propuestas de iconos (manual)
├── app/                                   # Módulo de la aplicación Android
│   ├── build.gradle.kts                   # Configuración de compilación de la app
│   └── src/
│       ├── main/
│       │   ├── AndroidManifest.xml
│       │   ├── java/com/example/
│       │   │   ├── MainActivity.kt         # Actividad principal y pantalla de Compose
│       │   │   ├── GameModels.kt           # Entidades (Casilla, Jugador, Carta, ModoJuego)
│       │   │   ├── GameViewModel.kt        # Máquina de estados del juego (StateFlow)
│       │   │   └── ui/theme/               # Sistema de diseño Material 3 (Color, Type, Theme)
│       │   └── res/
│       │       ├── values/
│       │       │   ├── strings.xml         # Recursos de cadenas de texto
│       │       │   └── colors.xml          # Paleta de colores del sistema
│       │       └── mipmap-*/               # Iconos adaptativos del lanzador
│       └── test/                           # Pruebas unitarias en JVM
├── scripts/                               # Generador de tableros y herramientas de datos
│   ├── requirements.txt                   # Dependencias de Python (Pillow>=10.0.0)
│   ├── gestor_db.py                       # Creación y administración del esquema SQLite
│   ├── generar_tablero.py                 # Generador maestro de tableros gráficos
│   ├── generar_propuestas_iconos.py       # Generador de variantes y catálogo de iconos
│   └── modificar_db.py                    # Utilidad CLI para editar precios o sincronizar JSON
├── output/                                # Directorio de artefactos generados
│   ├── tablero_datos.db                   # Base de datos SQLite modificable
│   ├── tablero_datos.json                 # Copia editable en JSON
│   ├── tablero_espana_color.png           # Tablero oficial de España en alta definición (Color)
│   ├── tablero_espana_byn.png             # Tablero oficial en escala de grises (Blanco y Negro)
│   ├── catalogo_propuestas_iconos.png     # Lámina comparativa de variantes de iconos para móvil
│   └── iconos_propuestas/                 # Iconos individuales PNG de 256x256 con canal alfa
├── metadata.json                 # Metadatos de la plataforma Google AI Studio
├── build.gradle.kts              # Configuración raíz de Gradle
├── settings.gradle.kts           # Módulos y configuración del proyecto
├── README.md                     # Documentación general y guía de inicio rápido
├── ROADMAP.md                    # Plan de desarrollo y fases futuras
├── STRUCTURE.md                  # Arquitectura del sistema y estructura de archivos
├── AI_CONTEXT.md                 # Contexto de dominio para modelos de lenguaje (LLM)
└── AGENTS.md                     # Directrices y normas operativas para agentes de IA
```

---

## 🏛️ Componentes y Arquitectura

### 1. Módulo Android (`app/`)
* **Patrón Arquitectónico**: MVVM (Model-View-ViewModel) con arquitectura reactiva unificada.
* **Flujo de Estado**:
  - `GameViewModel` expone un único `StateFlow<GameState>` inmutable.
  - La interfaz de usuario en `MainActivity.kt` observa el estado mediante `collectAsStateWithLifecycle()` recomponiendo únicamente los componentes afectados.
* **Componentes de UI clave**:
  - `BoardView`: Renderizado perimetral en cuadrícula responsiva optimizada para pantalla vertical de smartphone.
  - `DiceView`: Animación de lanzamiento con rotación física de dados 3D en 2D.
  - `CenterCourtyard`: Patio central táctil con información del turno, fondos, mensajes de evento y botones de acción rápida.
  - `PropertyDetailDialog`: Modal flotante con tabla de rentas e información catastral de cualquier casilla.

### 2. Generador Gráfico y de Datos (`scripts/`)
* **`gestor_db.py`**: Administra el schema relacional de SQLite. Si la base de datos no existe, la crea con las 40 casillas de España, las 32 cartas oficiales y las reglas de partida.
* **`generar_tablero.py`**:
  - Proceso de renderizado:
    1. Lee las casillas desde `tablero_datos.db`.
    2. Dibuja cada casilla estándar verticalmente con auto-ajuste tipográfico.
    3. Rota cada lado en su ángulo perimetral correspondiente (0°, 90°, 180°, 270°) orientando textos hacia el centro.
    4. Ensambla esquinas, marcos, cartas centrales e iconografía vectorial.
    5. Exporta los archivos finales a `output/`.
* **`modificar_db.py`**: Permite cambiar valores individuales o hacer importación masiva desde `tablero_datos.json`.

---

## 💾 Esquema de la Base de Datos (`tablero_datos.db`)

### Tabla `casillas`
| Campo | Tipo | Descripción |
| :--- | :--- | :--- |
| `id` | INTEGER PK | Identificador único |
| `posicion` | INTEGER | Posición perimetral en el circuito (0 a 39) |
| `nombre` | TEXT | Nombre visible de la calle o casilla |
| `tipo` | TEXT | `CALLE`, `ESTACION`, `SERVICIO`, `SUERTE`, `COMUNIDAD`, `IMPUESTO`, `CARCEL`, etc. |
| `grupo` | TEXT | Código de color del distrito (`MARRON`, `CELESTE`, `AZUL`, etc.) |
| `precio_compra` | INTEGER | Precio de adquisición |
| `alquiler_base` | INTEGER | Renta sin edificaciones |
| `alquiler_1_casa`..`hotel` | INTEGER | Rentas progresivas con edificaciones |
| `coste_casa` | INTEGER | Coste de edificar cada casa |
| `hipoteca` | INTEGER | Valor de hipoteca del banco |
| `icono` | TEXT | Clave de icono o representación |
| `descripcion` | TEXT | Texto informativo |

### Tabla `cartas_suerte` y `cartas_comunidad`
| Campo | Tipo | Descripción |
| :--- | :--- | :--- |
| `id` | INTEGER PK | Identificador único |
| `titulo` | TEXT | Título o encabezado de la carta |
| `tipo_accion` | TEXT | `COBRAR`, `PAGAR`, `AVANZAR`, `CARCEL`, `REPARAR`, etc. |
| `valor` | INTEGER | Cantidad económica o índice de casilla destino |
| `descripcion` | TEXT | Texto detallado de la acción |
