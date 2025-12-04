# MANUAL DE USUARIO - GESTIÓN DE AMISTADES

## 1. INTRODUCCIÓN
Esta aplicación te permite gestionar tu círculo de amistades, evaluando a tus amigos en base a 10 criterios personalizados. Puedes añadir, editar, eliminar y analizar tus amistades para entender mejor tus relaciones.

## 2. INSTALACIÓN Y EJECUCIÓN
- **Requisitos**: Python 3.x instalado y la librería wxPython (`pip install wxPython`).
- **Ejecución**: Haz doble clic en `main.py` o ejecútalo desde la terminal con `python main.py`.

## 3. FUNCIONALIDADES PRINCIPALES

### 3.1. AGREGAR AMIGO
   - Haz clic en **"Agregar Amigo"**.
   - Ingresa el nombre y selecciona el género.
   - Puntúa del 1 al 10 cada uno de los 10 criterios (ej. Confianza, Empatía).
   - Haz clic en **"Aceptar"** para guardar.

### 3.2. REEVALUAR / EDITAR AMIGO
   - Haz clic en **"Reevaluar/Editar Amigo"**.
   - Selecciona un amigo de la lista desplegable. Puedes filtrar por género.
   - Modifica su nombre, género o puntuaciones.
   - Haz clic en **"Actualizar"**.
   - **NOTA**: Si intentas salir sin guardar cambios, el sistema te avisará. (Este comportamiento ha sido corregido para no dar falsos positivos).

### 3.3. ELIMINAR AMIGO
   - Haz clic en **"Eliminar Amigo"**.
   - Selecciona el amigo que deseas borrar.
   - Confirma la acción. ¡Cuidado, esto no se puede deshacer! (Aunque se crea una copia de seguridad automática).

### 3.4. MOSTRAR AMIGOS
   - Haz clic en **"Mostrar Amigos"**.
   - Verás una lista ordenada de tus mejores amigos.
   - Puedes filtrar por categoría (Súper Amigo, Primario, etc.) o género.
   - El sistema te muestra qué porcentaje de tus amigos cumple con el filtro.

### 3.5. VER ESTADÍSTICAS (NUEVO)
   - Haz clic en **"Ver Estadísticas"**.
   - Obtén un resumen rápido: total de amigos, distribución por género, promedio de puntuación y desglose por categorías.

## 4. CATEGORÍAS DE AMISTAD
El sistema clasifica automáticamente a tus amigos según la suma total de puntos (máx 100):
- **Súper Amigo**: > 90 puntos
- **Primario**: 80 - 90 puntos
- **Secundario**: 60 - 79 puntos
- **Terciario**: 40 - 59 puntos
- **Ocasional**: 20 - 39 puntos
- **Conocido**: < 20 puntos

## 5. PERSONALIZACIÓN
Puedes editar el archivo `criterios.txt` para cambiar las preguntas de evaluación. Asegúrate de mantener exactamente 10 líneas.

## 6. SOLUCIÓN DE PROBLEMAS
- **Acentos**: La aplicación ahora usa UTF-8 por defecto. Si tienes archivos antiguos, se convertirán automáticamente al guardar.
- **Copias de seguridad**: Cada vez que guardas, se crea un archivo `amigos.txt.bak` por si necesitas recuperar datos anteriores.
