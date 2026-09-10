# Mapa de Ruta (Roadmap) - Capital Tycoon 🗺️

Este documento define la planificación estratégica y técnica para la evolución del juego de mesa inmobiliario y su generador de datasets.

---

## 📍 Fase 1: Prototipo y Generador Base (Completada ✅)

- [x] **Motor de Juego Android Básico**:
  - [x] Circuito perimetral cerrado y conteo de casillas.
  - [x] Lanzamiento de dados aleatorios con animación y detección de dobles.
  - [x] Economía básica: dinero de jugadores, compra de terrenos y cobro de rentas.
  - [x] Oponente automatizado (Bot Magnate con toma de decisiones lógicas).
  - [x] Modo Pasa y Juega local en un solo dispositivo.
  - [x] Sistema de Cárcel con fianza de 50€ y turnos de condena.
- [x] **Generador de Tableros y Catálogo de Iconos Automático**:
  - [x] Base de datos SQLite (`tablero_datos.db`) con las 40 casillas de España.
  - [x] Generador de imágenes PNG en alta resolución (2048 x 2048 px).
  - [x] Dataset de iconos en alta resolución con Supersampling 4x y filtro Lanczos.
  - [x] Generador de propuestas y catálogo comparativo para móvil (`catalogo_propuestas_iconos.png`).
  - [x] Exportación dual: Color y Blanco/Negro para impresión con iconos integrados.
  - [x] Workflows de GitHub Actions manuales (`workflow_dispatch`) para tableros y catálogo de iconos.
  - [x] Corrección tipográfica con auto-ajuste (*auto-fit text*) para evitar desbordes.
  - [x] Rotación orientada hacia el centro del tablero y contraste dinámico.

---

## 📍 Fase 2: Profundización de Reglas y Jugabilidad (Próxima)

- [ ] **Tablas de Construcción Progresiva**:
  - [ ] Implementar la regla de posesión del grupo completo de color antes de poder edificar.
  - [ ] Construcción uniforme de casas (no se puede poner 2 casas si otra calle del grupo tiene 0).
  - [ ] Gráficos visuales de casitas verdes y hoteles rojos directamente sobre las casillas del tablero Android.
- [ ] **Sistema de Hipotecas y Bancarrota Formal**:
  - [ ] Opción de hipotecar propiedades cuando el dinero sea insuficiente para pagar una renta.
  - [ ] Transferencia automática de bienes al acreedor en caso de bancarrota total.
- [ ] **Negociaciones entre Jugadores (Subastas e Intercambios)**:
  - [ ] Subasta abierta de propiedades cuando el jugador que aterriza en ella decide no comprarla.
  - [ ] Pantalla de trueque entre jugadores para intercambiar calles y dinero.

---

## 📍 Fase 3: Integración de Datasets Internacionales y Temáticos

- [ ] **Soporte Multiciudad**:
  - [ ] Datasets de ciudades latinoamericanas (Ciudad de México, Buenos Aires, Bogotá, Santiago, Lima).
  - [ ] Tablero internacional en dólares ($), libras (£) y euros (€).
- [ ] **Generador de Tableros Personalizados desde la App**:
  - [ ] Permitir a los usuarios crear sus propios tableros con nombres de su barrio o grupo de amigos directamente desde el teléfono.
- [ ] **Lector dinámico de SQLite en Android**:
  - [ ] Cargar el archivo `tablero_datos.db` generado por el script directamente en Room dentro de la aplicación móvil.

---

## 📍 Fase 4: Optimización, Audio y Distribución Alternativa

- [ ] **Efectos de Sonido Hápticos y Visuales**:
  - [ ] Sonido de dados rodando, tintineo de monedas al cobrar y sirena al caer en la cárcel.
  - [ ] Animación de fichas desplazándose casilla por casilla.
- [ ] **Empaquetado para Tiendas Libres y Uptodown**:
  - [ ] Generación automatizada de APKs Release sin firma de Google Play.
  - [ ] Compatibilidad estricta con arquitecturas de 32 bits (`armeabi-v7a`) y 64 bits (`arm64-v8a`).
  - [ ] Modo 100% offline sin telemetría ni recopilación de datos privados.
