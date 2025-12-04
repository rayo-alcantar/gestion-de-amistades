# DOCUMENTACIÓN TÉCNICA - GESTIÓN DE AMISTADES

## 1. ESTRUCTURA DEL PROYECTO
El proyecto ha sido refactorizado para mejorar la organización y mantenibilidad.

```
/
├── main.py                 # Punto de entrada de la aplicación.
├── amigo.py                # Clase Amigo (Modelo).
├── circulo_amistad.py      # Clase CirculoAmistad (Controlador de datos).
├── criterios.txt           # Archivo de configuración de criterios.
├── amigos.txt              # Base de datos (CSV).
├── ui/                     # Paquete de Interfaz de Usuario.
│   ├── __init__.py
│   ├── amigo_dialog.py           # Diálogo para agregar.
│   ├── reevaluar_amigo_dialog.py # Diálogo para editar (con lógica de validación).
│   ├── eliminar_amigo_dialog.py  # Diálogo para eliminar.
│   └── estadisticas_dialog.py    # Nuevo diálogo de estadísticas.
└── manuales/
    ├── MANUAL_USUARIO.md
    └── DOCUMENTACION_TECNICA.md
```

## 2. CLASES PRINCIPALES

### 2.1. `Amigo` (`amigo.py`)
Representa a una entidad "Amigo".
- **Atributos**: `nombre` (str), `puntuaciones` (dict), `genero` (str), `categoria` (str).
- **Métodos**:
  - `clasificar_amigo()`: Determina la categoría según el puntaje total.
  - `to_line()`: Serializa a formato CSV.
  - `from_line()`: Deserializa desde formato CSV.

### 2.2. `CirculoAmistad` (`circulo_amistad.py`)
Gestiona la colección de amigos y la persistencia.
- **Manejo de Archivos**: Usa `utf-8` con fallback a `latin-1` para migración.
- **Backups**: Crea `amigos.txt.bak` antes de sobrescribir.
- **Persistencia**: Utiliza el módulo `csv` de Python para robustez.

### 2.3. Diálogos (`ui/*.py`)
Clases que heredan de `wx.Dialog` para la interacción con el usuario.
- **`ReevaluarAmigoDialog`**: Contiene lógica crítica para detectar cambios sin guardar (`has_unsaved_changes`). Se ha corregido un bug de tipos (int vs str) en esta validación.

## 3. FORMATO DE DATOS (`amigos.txt`)
El archivo utiliza formato CSV estándar.
`Nombre,Score1,Score2,...,Score10,Género,Categoría`

Ejemplo:
`Juan Pérez,10,9,10,8,9,10,9,10,8,9,M,Súper Amigo`

## 4. REQUERIMIENTOS
- Python 3.6+
- wxPython (`pip install wxPython`)

## 5. HISTORIAL DE CAMBIOS
- **Refactorización UI**: Movida a carpeta `ui/`.
- **Bug Fix**: Solucionado error de "cambios sin guardar" en reevaluación.
- **Feature**: Añadido módulo de estadísticas.
- **Robustez**: Implementado manejo de CSV y UTF-8.
