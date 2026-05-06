# Sistema de Registro de Notas

> Una aplicación Django completa para que un maestro pueda gestionar a sus
> estudiantes y sus calificaciones

## DESCRIPCION GENERAL DEL SISTEMA

**Sistema de Registro de Notas** es una aplicación web desarrollada con Django que permite:
-  Gestionar estudiantes (crear, leer, actualizar, eliminar)
-  Registrar y administrar calificaciones por estudiante
-  Calcular promedios automáticamente
-  Generar reportes individuales y generales
-  Visualizar estado de aprobación/reprobación

##  Estructura del Proyecto

```
sistema_notas/
├── estudiantes/                # App para gestión de estudiantes
│   ├── models.py               # Modelo: Estudiante
│   ├── views.py                # Vista: lista_estudiantes
│   ├── forms.py                # Formulario: EstudianteForm
│   ├── admin.py                # Panel de administración
│   ├── migrations/             # Migraciones de BD
│   └── tests.py                # Tests 
│
├── notas/                       # App para gestión de notas
│   ├── models.py               # Modelos: RegistroNotas, DetalleNota
│   ├── views.py                # Vistas: dashboard, reportes
│   ├── forms.py                # Formulario: NotaForm
│   ├── admin.py                # Panel de administración
│   ├── signals.py              # Señales Django
│   ├── migrations/             # Migraciones de BD
│   └── tests.py                # Tests unitarios
│
├── sistema_notas/              # Configuración del proyecto
│   ├── settings.py             # Configuración Django
│   ├── urls.py                 # URLs principales
│   ├── wsgi.py                 # WSGI para producción
│   └── asgi.py                 # ASGI para websockets
│
├── templates/                  # Plantillas HTML
│   ├── base.html              # Base template (herencia)
│   ├── dashboard.html         # Dashboard principal
│   ├── componentes/           # Componentes reutilizables
│   │   ├── estudiantes.html   # CRUD de estudiantes
│   │   ├── notas.html         # CRUD de notas
│   │   └── resumen.html       # Resumen de notas
│   ├── reportes/              # Reportes
│   │   ├── individual.html    # Reporte por estudiante
│   │   └── general.html       # Reporte general
│   └── estudiantes/
│       └── lista.html         # Lista de estudiantes
│
├── static/                     # Archivos estáticos
│   ├── css/
│   │   └── base.css           # Estilos principales
│   └── js/
│       └── base.js            # JavaScript interactivo
│
├── db.sqlite3                 # Base de datos
├── manage.py                  # Utilidad de Django
├── requirements.txt           # Dependencias Python
└── .gitignore                # Archivos ignorados por Git
```

## Modelo de Base de Datos

### Diagrama de Relaciones

```
┌──────────────────────────────┐
│       Estudiante             │
├──────────────────────────────┤
│ id (PK)                      │
│ id_estudiante (UNIQUE)       │
│ nombre (VARCHAR)             │
│ apellido (VARCHAR)           │
└──────────────────────────────┘
           │
           │ OneToOne
           ▼
┌──────────────────────────────┐
│      RegistroNotas           │
├──────────────────────────────┤
│ id (PK)                      │
│ estudiante_id (FK, UNIQUE)   │
└──────────────────────────────┘
           │
           │ OneToMany
           ▼
┌──────────────────────────────┐
│       DetalleNota            │
├──────────────────────────────┤
│ id (PK)                      │
│ registro_id (FK)             │
│ tipo (VARCHAR)               │
│ valor (DECIMAL: 0-100)       │
└──────────────────────────────┘
```

### Descripción de Modelos

#### 1. **Estudiante**
Almacena información básica del estudiante.

| Campo           | Tipo      | Restricciones |         Descripción        |
|-----------------|-----------|---------------|----------------------------|
| `id`            | AutoField | PK            | ID único autogenerado      |
| `id_estudiante` | CharField | UNIQUE, max=10| Cédula o ID del estudiante |
| `nombre`        | CharField | max=20        | Nombre del estudiante      |
| `apellido`      | CharField | max=20        | Apellido del estudiante    |

**Métodos:**
```python
def __str__(self):
    return f"{self.nombre} {self.apellido}"
```

#### 2. **RegistroNotas**
Agrupa todas las notas de un estudiante. Relación OneToOne.

| Campo        | Tipo          | Restricciones   | Descripción            |
|--------------|---------------|-----------------|------------------------|
| `id`         | AutoField     | PK              | ID único autogenerado  |
| `estudiante` | OneToOneField | FK a Estudiante | Estudiante propietario |

**Métodos:**
```python
def promedio(self) -> float
    # Retorna el promedio de todas las notas del estudiante
    # Ej: 85.50

def estado(self) -> str
    # Retorna "Aprobado" si promedio >= 60, sino "Reprobado"

def __str__(self) -> str
    # Retorna el nombre del estudiante
```

#### 3. **DetalleNota**
Registra cada evaluación/nota de un estudiante.

| Campo      | Tipo         | Restricciones      | Descripción                                     |
|------------|--------------|--------------------|-------------------------------------------------|
| `id`       | AutoField    | PK                 | ID único autogenerado                           |
| `registro` | ForeignKey   | FK a RegistroNotas | Registro padre                                  |
| `tipo`     | CharField    | max=50             | Tipo de evaluación (quiz, parcial, final, etc.) |
| `valor`    | DecimalField | min=0, max=100     | Calificación numérica                           |

**Métodos:**
```python
def __str__(self) -> str
    # Retorna formato: "TIPO - VALOR"
    # Ej: "Quiz 1 - 85.50"
```

## URLs y Rutas

| Ruta                   | Método   | Vista               | Descripción                      |
|------------------------|----------|---------------------|----------------------------------|
| `/`                    | GET/POST | `dashboard`         | Dashboard principal con CRUD     |
| `/admin/`              | GET      | Django Admin        | Panel administrativo             |
| `/estudiantes/`        | GET      | `lista_estudiantes` | Lista de estudiantes             |
| `/reporte-individual/` | GET      | `reporte_individual`| Reporte de un estudiante         |
| `/reporte-general/`    | GET      | `reporte_general`   | Reporte de todos los estudiantes |

##  Vistas (Views)

### 1. Dashboard (`notas/views.py`)

**URL:** `/`  
**Métodos:** GET, POST

**Funcionalidad:**
- Muestra lista de estudiantes en el dashboard
- Permite CRUD de estudiantes
- Permite CRUD de notas para estudiantes seleccionados
- Muestra resumen de notas

**Parámetros GET:**
- `estudiante`: ID del estudiante a mostrar
- `edit_id`: ID del estudiante a editar
- `edit_nota`: ID de la nota a editar

**Operaciones POST:**

#### Crear Estudiante
```python
# Parámetros requeridos
guardar_estudiante: (hidden button)
id_estudiante: "12345678"    # Cédula única
nombre: "Juan"
apellido: "Pérez"
```

#### Editar Estudiante
```python
editar_estudiante: (hidden button)
id: <student_id>              # ID del estudiante
nombre: "Juan"
apellido: "Pérez"
```

#### Eliminar Estudiante
```python
eliminar_estudiante: (hidden button)
id: <student_id>              # ID del estudiante
```

#### Crear Nota
```python
guardar_nota: (hidden button)
estudiante_id: <student_id>
tipo: "Quiz 1"                # Tipo de evaluación
valor: "85.50"                # Nota 0-100
```

#### Editar Nota
```python
editar_nota: (hidden button)
nota_id: <note_id>
tipo: "Quiz 1"
valor: "90.00"
```

#### Eliminar Nota
```python
eliminar_nota: (hidden button)
nota_id: <note_id>
```

### 2. Lista de Estudiantes (`estudiantes/views.py`)

**URL:** `/estudiantes/`  
**Método:** GET

**Funcionalidad:**
- Muestra lista de todos los estudiantes

**Contexto de Template:**
```python
{
    'estudiantes': QuerySet[Estudiante]
}
```

### 3. Reporte Individual (`notas/views.py`)

**URL:** `/reporte-individual/`  
**Método:** GET

**Parámetros:**
- `estudiante`: ID del estudiante (obligatorio)

**Funcionalidad:**
- Muestra reporte detallado de un estudiante
- Muestra todas sus notas
- Muestra promedio y estado

**Contexto de Template:**
```python
{
    'registro': RegistroNotas,
    'notas': QuerySet[DetalleNota]
}
```

### 4. Reporte General (`notas/views.py`)

**URL:** `/reporte-general/`  
**Método:** GET

**Funcionalidad:**
- Muestra reporte de todos los estudiantes
- Calcula estadísticas globales

**Contexto de Template:**
```python
{
    'registros': QuerySet[RegistroNotas],
    'total': int,              # Total de estudiantes
    'aprobados': int,          # Estudiantes aprobados (prom >= 60)
    'reprobados': int,         # Estudiantes reprobados (prom < 60)
    'promedio_general': float  # Promedio de todos
}
```

## Configuración de Base de Datos

### Tipo: SQLite

**Archivo:** `db.sqlite3`  
**Engine:** `django.db.backends.sqlite3`  
**Ubicación:** Raíz del proyecto

### Archivos de Migración

```
estudiantes/migrations/
├── 0001_initial.py              # Modelo inicial
├── 0002_estudiante_apellido.py
├── 0003_alter_estudiante_apellido.py
├── 0004_alter_estudiante_apellido.py
└── 0005_alter_estudiante_apellido_and_more.py  # Última

notas/migrations/
├── 0001_initial.py              # Modelos: RegistroNotas, DetalleNota
├── 0002_alter_detallenota_registro.py
└── 0003_rename_nombre_nota_detallenota_tipo_and_more.py
```

### Tabla: `estudiantes_estudiante`

```sql
CREATE TABLE "estudiantes_estudiante" (
  "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
  "id_estudiante" varchar(10) NOT NULL UNIQUE,
  "nombre" varchar(20) NOT NULL,
  "apellido" varchar(20) NOT NULL
);
```

### Tabla: `notas_registronotas`

```sql
CREATE TABLE "notas_registronotas" (
  "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
  "estudiante_id" integer NOT NULL UNIQUE,
  FOREIGN KEY("estudiante_id") REFERENCES "estudiantes_estudiante"("id")
    ON DELETE CASCADE
);
```

### Tabla: `notas_detallenota`

```sql
CREATE TABLE "notas_detallenota" (
  "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
  "registro_id" integer NOT NULL,
  "tipo" varchar(50) NOT NULL,
  "valor" numeric(5,2) NOT NULL CHECK (valor >= 0 AND valor <= 100),
  FOREIGN KEY("registro_id") REFERENCES "notas_registronotas"("id")
    ON DELETE CASCADE
);
```

##  INSTALACION Y CONFIGURACION

### 1. Clonar el repositorio 

```bash
git clone <repository-url>
cd "Registro de notas"
```

### 2. Crear entorno virtual

```bash
python3 -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Aplicar migraciones

```bash
cd sistema_notas
python manage.py migrate
```

### 5. Crear superusuario (opcional para admin)

```bash
python manage.py createsuperuser
```

### 6. Ejecutar servidor de desarrollo

```bash
python manage.py runserver
```

Accede a: `http://localhost:8000`

##  Dependencias

```
Django==6.0.4           # Framework web
asgiref==3.11.1         # ASGI support
sqlparse==0.5.5         # SQL parser
```

Ver `requirements.txt` para lista completa.

##  Tests

### Ejecutar todos los tests

```bash
python manage.py test
```

### Ejecutar tests de una app específica

```bash
python manage.py test estudiantes
python manage.py test notas
```

##  Seguridad

### Configuración Actual

-  CSRF Protection habilitado
-  SQL Injection prevention (ORM)
-  Validación de entrada en modelos
-  DEBUG = True (cambiar en producción)
-  SECRET_KEY hardcodeado (usar variables de entorno)


## Lógica de Negocio

### Cálculo de Promedio

```python
def promedio(self):
    notas = self.detallenota_set.all()
    if notas.exists():
        return round(sum(n.valor for n in notas) / notas.count(), 2)
    return 0
```

**Ejemplo:**
```
Notas: [85.5, 90.0, 78.25]
Promedio = (85.5 + 90.0 + 78.25) / 3 = 84.58
```

### Criterio de Aprobación

```python
def estado(self):
    return "Aprobado" if self.promedio() >= 60 else "Reprobado"
```

**Regla:** 
-  Aprobado si promedio >= 60
-  Reprobado si promedio < 60

### Validación de Notas

```python
# En modelo DetalleNota
valor = models.DecimalField(
    max_digits=5,
    decimal_places=2,
    validators=[MinValueValidator(0), MaxValueValidator(100)]
)
```

- Mínimo: 0
- Máximo: 100
- Decimales: 2 (hasta centésimas)

## Interfaz (Frontend)

### Base Template (`base.html`)

Estructura base de todas las páginas:
- Header con título y descripción
- Sidebar colapsable con navegación
- Area de contenido principal
- Sistema de mensajes (éxito/error)

### Dashboard (`dashboard.html`)

Página principal con:
- Componente de gestión de estudiantes
- Componente de gestión de notas
- Componente de resumen

### Estilos

**Archivo:** `static/css/base.css`

- Tema moderno con gradientes
- Colores: Azul (#2d7be5) y Magenta (#c81df2)
- Sidebar responsivo (colapsable)
- Cartas (cards) para secciones

### JavaScript

**Archivo:** `static/js/base.js`

Funciones interactivas:
- `toggleSidebar()`: Alternar sidebar
- `confirmDelete()`: Confirmación de eliminación
- `openModal(id)`: Abrir modal
- `closeModal(id)`: Cerrar modal
- Cerrar modal al hacer click afuera

## Mejoras propuestas para mejorar:

### Prioridad ALTA

- [ ] Implementar tests unitarios
- [ ] Usar variables de entorno para configuración sensible
- [ ] Cambiar LANGUAGE_CODE a 'es'
- [ ] Configurar TIME_ZONE correctamente

### Prioridad MEDIA

- [ ] Agregar paginación en reportes
- [ ] Agregar búsqueda de estudiantes
- [ ] Mejorar responsive design
- [ ] Agregar validaciones frontend

### Prioridad BAJA

- [ ] Exportar reportes a PDF/Excel
- [ ] Agregar autenticación de usuarios
- [ ] Agregar historial de cambios
- [ ] Agregar gráficos de desempeño
