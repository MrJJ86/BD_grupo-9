# Prototipo de Pantallas para la Base de Datos de Emaús

## Clonar repositorio
En la carpeta que desea clonar el repositorio ingrese el siguiente comando:
```
git clone git@github.com:MrJJ86/BD_grupo-9.git
```

## Librerías
1. MySQL-python
2. Pandas

## Instalación de librerias
En la consola ingrese los siguientes comandos
```
pip install MySQL-python
```
```
pip install Pandas
```
## Links para utilizar librerias
1. [Documentación de los DataFrames de Pandas](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html)
2. [Documentación de MySQL Connector/Python](https://dev.mysql.com/doc/connector-python/en/connector-python-examples.html)

## Archivo utils
En el archivo `utils.py` se encuentra una función para borrar las pantallas en la consola. Se debe utilizar en cada nueva pantalla.

## Conexión de la Base de Datos
En el archivo `bd_conections.py` se encuentran todas las funciones necesarias para conectarse con la base de datos

Uso de las diferentes funciones:

### `visualizar_datos(tabla, columnas=None, condicion=None, grupo=None, cond_grupo=None)`
Esta función recibe obligatoriamente la **tabla** a la que se va a referenciar en el SQL.
De ahí los demás parámetros son opcionales:

**Columnas**
  - Se pasan las columnas de la tabla como texto, ej: `columnas="nombre,apellido,celular"`
  - Si no pasan las columnas entonces se escogen todas las columnas de la tabla.
    
**Condicion**
- Se pasan las condiciones en el siguiente formato: `condicion="columna=valor"`
  
**Grupo**
- Se pasan los campos o columnas que por las que se quiere agrupar: `grupo="col1,col2"`
  
**Condición Grupo**
-Se pasan las condiciones para los grupos en el siguiente formato: `cond_grupo="columna=valor"`

### `insertar_datos(tabla, valores_tabla,datos)`
Esta función recibe obligatoriamento todos los parámentros.

**Tabla**
- Se pasa la tabla a la que se van a insertar los datos
  
**Valores Tabla**
- Se pasan las columnas de la tabla en formato de lista: `valores_tabla=["columna1","columna2","columna3"]`
  
**Datos**
- Se pasan los datos de las columnas en formato de diccionario: `datos={"columna1": valor, "columna2": valor, "columna3": valor}`

### `actualizar_datos(tabla, valores_tabla, condicion, datos_actualizar)`
Esta función recibe obligatoriamento todos los parámentros.

**Tabla**
- Se pasa la tabla a la que se van a insertar los datos
  
**Valores Tabla**
- Se pasan las columnas de la tabla en formato de lista: `valores_tabla=["columna1","columna2","columna3"]`
  
**Datos**
- Se pasan los datos de las columnas en formato de diccionario: `datos={"columna1": valor, "columna2": valor, "columna3": valor}`

### `eliminar_datos(tabla, condicion)`
Esta función recibe obligatoriamento todos los parámentros.

**Tabla**
- Se pasa la tabla a la que se van a insertar los datos
  
**Condicion**
- Se pasan las condiciones en el siguiente formato: `condicion="columna=valor"`
