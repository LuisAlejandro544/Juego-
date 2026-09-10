# Capital Tycoon (Edición España) 🎲🏙️

Juego de mesa inmobiliario y generador automatizado de tableros estándar de 40 casillas para dispositivos móviles Android y pipelines de GitHub Actions.

---

## 📌 Descripción del Proyecto

**Capital Tycoon** es una aplicación y ecosistema de desarrollo enfocado en la simulación inmobiliaria, compraventa de propiedades, gestión de alquileres y bancarrota. Diseñado y optimizado específicamente para teléfonos móviles en orientación vertical, incluye:

1. **Juego Móvil Android (Jetpack Compose + Material Design 3)**:
   - Modos de juego: *Un Jugador contra Bot Magnate* y *Pasa y Juega local (2 Jugadores)*.
   - Tablero perimetral táctil adaptativo.
   - Dados animados con detección de tiradas dobles.
   - Sistema de compra de solares, construcción de casas y hoteles, cobro de alquileres, eventos de Suerte/Caja de Comunidad, cárcel y fianza.

2. **Generador Automatizado de Tableros y Catálogo de Iconos (Python + SQLite)**:
   - Generación de tableros de 2048 x 2048 px con las 40 casillas oficiales de la edición España e iconografía en alta definición (Supersampling 4x con filtro Lanczos).
   - Exportación dual de tableros:
     - `tablero_espana_color.png`: A todo color con distritos oficiales, decoración clásica e iconos nítidos.
     - `tablero_espana_byn.png`: Monocromático de alto contraste para impresión en blanco y negro.
   - Generador y catálogo de propuestas de iconos:
     - `catalogo_propuestas_iconos.png`: Lámina comparativa optimizada para pantalla de móvil con variantes numeradas de bolsas de impuestos, joyas de lujo, locomotoras, servicios y cofres.
     - Carpeta `output/iconos_propuestas/`: Iconos individuales en PNG transparente de 256x256 px.
   - Base de datos relacional SQLite (`tablero_datos.db`) y copia editable en JSON (`tablero_datos.json`) para modificar precios, rentas y reglas económicas.

3. **Workflows de GitHub Actions (Activación 100% Manual)**:
   - **"Generar Tableros de España"**: Genera y empaqueta los tableros PNG y la base de datos en un `.zip`.
   - **"Generar Propuestas de Iconos y Catálogo"**: Genera la lámina de catálogo y los iconos en PNG transparente para previsualizarlos y descargarlos con un solo toque desde el móvil.

---

## 🚀 Inicio Rápido desde el Teléfono Móvil

### Opción A: Generar propuestas de iconos y catálogo visual
1. Abre tu repositorio en GitHub desde el navegador de tu smartphone.
2. Pulsa en la pestaña superior **Actions**.
3. En la lista lateral izquierda, pulsa **"Generar Propuestas de Iconos y Catálogo"**.
4. Pulsa en el botón azul **"Run workflow"** y confirma la ejecución.
5. Al terminar, descarga el artefacto `catalogo-propuestas-iconos.zip` para ver la lámina `catalogo_propuestas_iconos.png` y comparar las variantes.

### Opción B: Generar y descargar los tableros de España completos
1. En la pestaña **Actions**, selecciona el flujo **"Generar Tableros de España"**.
2. Pulsa en **"Run workflow"** y confirma la ejecución.
3. Descarga el artefacto `tablero-espana-completo.zip` (contiene los PNGs a 2048x2048, la base de datos `tablero_datos.db` y `tablero_datos.json`).

### Opción C: Ejecución local en terminal / entorno Python
```bash
# 1. Instalar dependencias
pip install -r scripts/requirements.txt

# 2. Generar tableros PNG y base de datos SQLite
python scripts/generar_tablero.py

# Los archivos generados se ubicarán en la carpeta output/:
# - output/tablero_espana_color.png
# - output/tablero_espana_byn.png
# - output/tablero_datos.db
# - output/tablero_datos.json
```

---

## ✏️ Cómo modificar precios, alquileres y nombres

Todos los datos del tablero están desacoplados del código fuente:

1. Abre el archivo `output/tablero_datos.json` en cualquier editor de texto o visor JSON de tu teléfono.
2. Modifica los campos que desees (por ejemplo, cambiar el `precio_compra` de *Paseo del Prado* o la renta base).
3. Sincroniza los cambios con la base de datos SQLite ejecutando:
   ```bash
   python scripts/modificar_db.py --importar-json
   ```
4. Vuelve a ejecutar `python scripts/generar_tablero.py` o corre el GitHub Action para obtener los nuevos tableros dibujados con tus precios personalizados.

---

## 📱 Compilación de la Aplicación Android

La aplicación está construida con la arquitectura recomendada de Android:
- **Lenguaje**: Kotlin 2.x
- **UI Framework**: Jetpack Compose con Material Design 3
- **Persistencia**: Room Database / SQLite
- **Versión mínima de Android**: Android 8.0 Oreo (API 26) - Cobertura del ~94% de dispositivos.
- **Compatibilidad**: Compatible con dispositivos de 32 bits y 64 bits (armeabi-v7a, arm64-v8a, x86, x86_64).
- **Distribución**: Lista para exportar en APK e instalar mediante tiendas de terceros (Uptodown, F-Droid, APKPure) sin dependencia obligatoria de Google Play Services.

```bash
# Compilar la aplicación en modo Debug
gradle :app:assembleDebug
```
