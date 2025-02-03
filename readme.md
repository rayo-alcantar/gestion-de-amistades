# Gestión de Amistades

Este proyecto es una aplicación de escritorio (usando wxPython) que permite gestionar un círculo de amistades. La aplicación permite agregar, editar y eliminar amigos, además de mostrar una lista ordenada y filtrada. Se ha prestado especial atención a la accesibilidad (por ejemplo, navegación con Tab y manejo de atajos) y a la claridad en la presentación de la información (usando “toString” o métodos de formateo para detallar cada amigo).

## Estructura de Archivos

### 1. `amigo.py`

- **Funcionalidad:**  
  Define la clase `Amigo` que representa a un amigo en el sistema.  
  - Atributos principales:  
    - `nombre`: nombre del amigo (string).  
    - `puntuaciones`: diccionario con 10 parámetros de amistad (por ejemplo, “tiempo_compartido”, “apoyo_emocional”, etc.).  
    - `genero`: almacena "M" (Hombre) o "F" (Mujer).  
    - `categoria`: se asigna según la suma total de las puntuaciones (por ejemplo, "Súper Amigo", "Primario", "Secundario", etc.).
  - Métodos clave:  
    - `actualizar_puntuaciones()`: actualiza los valores y vuelve a clasificar la amistad.  
    - `clasificar_amigo()`: asigna la categoría basándose en la suma de las puntuaciones.  
    - `editar_nombre()` y `editar_genero()`: permiten actualizar estos atributos.  
    - `to_line()` y `from_line()`: métodos para convertir la información del amigo a una línea de texto (para guardar en archivo) y para crear un objeto a partir de una línea de texto, respectivamente.  
    - Se incluyen validaciones y normalización del campo género (por ejemplo, convertir "H" a "M").

### 2. `circulo_amistad.py`

- **Funcionalidad:**  
  Define la clase `CirculoAmistad`, la cual es responsable de gestionar la colección de objetos `Amigo`.  
  - Métodos principales:  
    - `cargar_amigos()`: lee un archivo de texto (usando la codificación "latin-1") y crea una lista de objetos `Amigo` a partir de cada línea.  
    - `guardar_amigos()`: escribe la información de cada amigo en el archivo en el formato adecuado.  
    - `agregar_amigo()`, `reevaluar_amigo()` y `eliminar_amigo()`: métodos para manipular la lista de amigos y luego guardar los cambios en el archivo.  
    - Métodos para listar y mostrar amigos ordenados según la suma de sus puntuaciones.

### 3. `amigo_dialog.py`

- **Funcionalidad:**  
  Proporciona la interfaz gráfica (un diálogo) para agregar un nuevo amigo.  
  - Se muestran campos para:  
    - Ingresar el nombre.  
    - Seleccionar el género mediante un combo box (con opciones “Hombre” y “Mujer”).  
    - Ingresar las 10 puntuaciones.  
  - Se realizan validaciones (por ejemplo, que el nombre no esté vacío y que las puntuaciones sean números entre 1 y 10).  
  - Se cierra el diálogo sólo si las validaciones son correctas.

### 4. `reevaluar_amigo_dialog.py`

- **Funcionalidad:**  
  Proporciona la interfaz gráfica para editar o reevaluar la información de un amigo existente.  
  - Contiene dos combo boxes:  
    - Uno para filtrar y seleccionar el amigo a editar (ordenados de mayor a menor según la suma de las puntuaciones).  
    - Otro para seleccionar el género del amigo.  
  - También incluye campos para editar el nombre y las puntuaciones.  
  - Se muestra un área de detalle (usando un método __str__ personalizado) para ver la información completa y formateada del amigo seleccionado.  
  - Permite actualizar la información del amigo y, tras la actualización, recarga la lista manteniendo la selección en el amigo actualizado.
  - Integra validación de cambios sin guardar y solicita confirmación antes de cerrar el diálogo.

### 5. `eliminar_amigo_dialog.py`

- **Funcionalidad:**  
  Proporciona la interfaz gráfica para eliminar un amigo.  
  - Muestra un combo box con los nombres de los amigos (extraído de la colección).  
  - Al confirmar, se elimina el amigo seleccionado y se actualiza la lista en el archivo de datos.

### 6. `main.py`

- **Funcionalidad:**  
  Es el archivo principal que arranca la aplicación.  
  - Crea la ventana principal con botones para cada una de las operaciones: agregar, editar, eliminar y mostrar amigos, y salir de la aplicación.  
  - El botón “Mostrar Amigos” abre un diálogo exclusivo donde se incluye un combo box para filtrar la lista de amigos (por género, categoría, o por puntuación) y se muestra la lista ordenada (de mayor a menor) en un área de texto.
  - Se han utilizado atajos (por ejemplo, usando "&" en las etiquetas de los botones) y se ha implementado navegación mediante Tab para mejorar la accesibilidad.

