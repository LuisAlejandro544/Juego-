# AI Context & Technical Domain Knowledge 🧠🤖

Este archivo proporciona contexto técnico, restricciones de arquitectura y conocimiento del dominio para modelos de inteligencia artificial (LLMs como Gemini, Claude o GPT) que asistan en el desarrollo de este repositorio.

---

## 🎯 Identidad del Dominio

El proyecto es un **juego de mesa de estrategia inmobiliaria por turnos**, basado en la mecánica matemática del arquetipo clásico de circuito cerrado (40 casillas), compra de propiedades, cobro de alquileres y bancarrota.

### Restricciones Críticas de Marca y Propiedad Intelectual
- **No usar marcas registradas en el código fuente ni nombres de archivos**: No utilizar nombres comerciales protegidos (como "Monopoly", marcas comerciales de Hasbro, o mascotas oficiales con copyright).
- **Nombre oficial del proyecto en el repositorio**: `Capital Tycoon`.
- **Nombres de archivos permitidos**: `generar_tablero.py`, `tablero_datos.db`, `tablero_espana_color.png`, etc.
- **Legalidad de las mecánicas**: Las mecánicas de juego abstractas (tirar dados, avanzar casillas, comprar y pagar alquiler) son de dominio público. Las calles de las ciudades son bienes públicos geográficos.

---

## 📐 Reglas Matemáticas y Modelo Económico

1. **Circuito**: 40 casillas numeradas del 0 al 39 en sentido horario.
   - Esquinas: 0 (Salida), 10 (Cárcel), 20 (Parking Gratuito), 30 (Vaya a la Cárcel).
2. **Dinero y Salario**:
   - Saldo inicial por jugador: 1500 €.
   - Salario al pasar o caer en la Salida (0): 200 €.
3. **Casillas de Pago y Sanciones**:
   - Impuesto sobre el Capital (Casilla 4): 200 €.
   - Tasa de Lujo (Casilla 38): 100 €.
   - Fianza de salida de prisión: 50 € o sacar dados dobles en máximo 3 intentos.
4. **Alquileres**:
   - Calles normales: Renta base progresiva multiplicada con 1, 2, 3, 4 casas y hotel.
   - Estaciones (4 en total): 25 € con 1 estación, 50 € con 2, 100 € con 3, 200 € con las 4.
   - Servicios (Electricidad y Aguas): 4x la tirada de dados con 1 servicio; 10x la tirada con ambos servicios.

---

## 📱 Restricciones Técnicas del Entorno y Usuario

- **Dispositivo del Usuario**: El usuario opera **exclusivamente desde un teléfono móvil**, sin acceso a PC ni terminal de escritorio.
  - Toda la interacción con GitHub Actions debe admitir activación táctil sencilla (`workflow_dispatch`).
  - Las salidas gráficas y datos deben ser descargables en formatos universales (PNG, ZIP, JSON, SQLite).
- **Entorno de Distribución**: La aplicación Android se distribuirá mediante APKs en tiendas libres o de terceros (Uptodown, etc.). No debe depender de Google Play Services ni bibliotecas propietarias cerradas.
- **Arquitectura Móvil**: Soporte para procesadores de 32 bits (`armeabi-v7a`) y 64 bits (`arm64-v8a`).
- **Idioma del Proyecto**: Tanto la interfaz de usuario, los mensajes de confirmación, los commits y la documentación deben estar en **español**.

---

## ⚙️ Pipeline de GitHub Actions

El archivo `.github/workflows/generar_tablero.yml` opera con el siguiente flujo:
1. `on: workflow_dispatch` (Activación exclusivamente manual bajo demanda).
2. Runner: `ubuntu-latest`.
3. Pasos: Checkout -> Setup Python 3.11 -> Pip install Pillow -> Ejecución de `python scripts/generar_tablero.py` -> Upload de artefactos (`actions/upload-artifact@v4`).
4. Artefacto de salida: `tablero-espana-completo` (contiene ambos PNGs, el archivo `.db` y el `.json`).
