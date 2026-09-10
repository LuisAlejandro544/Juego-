# Directrices para Agentes de Inteligencia Artificial (AGENTS.md) 🤖📋

Este documento establece las reglas obligatorias de desarrollo, comportamiento y estilo para cualquier asistente de IA o agente autónomo que modifique o extienda este repositorio.

---

## 👤 Perfil y Restricciones del Usuario

1. **Dispositivo del Usuario (Móvil Únicamente)**:
   - El usuario **no tiene ordenador (PC)**; administra, prueba y ejecuta todo desde su **teléfono móvil**.
   - Toda herramienta, workflow o script debe poder usarse, descargarse y gestionarse cómodamente desde la interfaz táctil de un smartphone o mediante el navegador web del teléfono.
2. **Distribución en Tiendas Alternativas (Uptodown, APK Directo)**:
   - Las apps móviles de este repositorio se distribuirán en tiendas como Uptodown o mediante descarga de APK directa de terceros, no obligatoriamente en Google Play Store.
   - No forzar dependencias que requieran estrictamente los servicios de Google Play (Google Play Services) si impiden la ejecución en terminales libres o con microG.

---

## 🛡️ Propiedad Intelectual y Seguridad Legal

1. **Protección de Marcas Comerciales**:
   - **Queda estrictamente prohibido** utilizar nombres de marcas registradas o comerciales protegidas por derechos de autor (como nombres oficiales de marcas comerciales de Hasbro) en los nombres de archivos del repositorio, nombres de ramas o paquetes.
   - Usar siempre nombres descriptivos o el nombre del proyecto (`Capital Tycoon`, `generar_tablero.py`, `tablero_datos.db`).
2. **Licenciamiento de Librerías**:
   - No agregar dependencias con licencias restrictivas de tipo copyleft fuerte (como AGPL o GPL estricta) que obliguen a cambiar los términos de la aplicación o fuercen créditos no deseados. Preferir licencias permisivas (MIT, Apache 2.0, BSD).

---

## 💻 Normas de Código y Arquitectura

1. **Razonamiento Antes de la Acción**:
   - El agente debe razonar metódicamente antes de aplicar cambios a los archivos: evaluar qué herramientas usar, el impacto en la compilación y la coherencia del diseño.
2. **Comentarios Explicativos en Español**:
   - Cada archivo de código nuevo o modificado (Kotlin, Python, Gradle, etc.) debe contener comentarios claros y pedagógicos en **español** que expliquen la lógica, los parámetros y el propósito de las funciones para que el usuario pueda comprenderlas sin dificultad.
3. **Uso Pragmático de Dependencias**:
   - Al usuario no le preocupa el peso del APK final siempre que la solución sea 100% funcional y robusta. Priorizar el uso de librerías oficiales y estables en lugar de escribir soluciones artesanales frágiles desde cero.
4. **Soporte de Arquitecturas**:
   - Mantener compatibilidad tanto con arquitecturas de 32 bits (`armeabi-v7a`) como de 64 bits (`arm64-v8a`).
5. **No Tocar Archivos Innecesarios**:
   - No leer ni alterar archivos que no guarden relación directa con la solicitud activa del usuario.
   - Si existe un archivo `commit_message.txt`, mantener su información en español y no modificarlo a menos que el usuario lo pida expresamente.
6. **Políticas de Sistema Android**:
   - En caso de trabajar con optimizadores o utilidades del sistema, jamás usar propiedades del tipo `persist.sys.*`.

---

## 🚀 Flujo de Verificación y Compilación

- Siempre verificar el proyecto con `compile_applet` tras realizar cambios en el código de Android.
- No alterar la configuración de firma (`debug.keystore`), `applicationId` preexistente ni las versiones base de Kotlin/AGP a menos que sea indispensable y solicitado.
