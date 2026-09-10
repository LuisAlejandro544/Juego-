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

2. **Generador Automatizado de Tableros (Python + SQLite)**:
   - Generación de tableros de 2048 x 2048 px con las 40 casillas oficiales de la edición España.
   - Exportación dual:
     - `tablero_espana_color.png`: A todo color con distritos oficiales y decoración clásica.
     - `tablero_espana_byn.png`: Monocromático de alto contraste para impresión en blanco y negro.
   - Base de datos relacional SQLite (`tablero_datos.db`) y copia editable en JSON (`tablero_datos.json`) para modificar precios, rentas y reglas económicas.

3. **Workflow de GitHub Actions (Activación 100% Manual)**:
   - Permite ejecutar el generador en la nube directamente desde el navegador de un teléfono móvil sin necesidad de ordenador.
   - Genera y empaqueta automáticamente los archivos en un `.zip` descargable.

---

## 🚀 Inicio Rápido desde el Teléfono Móvil

### Opción A: Generar y descargar los tableros con GitHub Actions
1. Abre tu repositorio en GitHub desde el navegador de tu teléfono móvil.
2. Pulsa en la pestaña superior **Actions**.
3. En la lista lateral izquierda, selecciona el flujo **"Generar Tableros de España"**.
4. Pulsa en el botón azul **"Run workflow"** y confirma la ejecución.
5. Espera unos 20 segundos a que finalice la ejecución.
6. Entra en la ejecución completada y en la sección inferior **Artifacts** descarga el archivo `tablero-espana-completo.zip`.
   * Contiene los dos PNGs (`color` y `blanco y negro`), la base de datos `tablero_datos.db` y el archivo `tablero_datos.json`.

### Opción B: Ejecución local en terminal / entorno Python
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
- **Compatibilidad**: Compatible con dispositivos de 32 bits y 64 bits (armeabi-v7a, arm64-v8a, x86, x86_64).
- **Distribución**: Lista para exportar en APK e instalar mediante tiendas de terceros (Uptodown, F-Droid, APKPure) sin dependencia obligatoria de Google Play Services.

```bash
# Compilar la aplicación en modo Debug
gradle :app:assembleDebug
```
