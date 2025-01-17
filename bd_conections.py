import mysql.connector

def conexion_bd():
    return mysql.connector.connect(
        user="demouser",
        password="Admin123",
        host="demoserverl.mysql.database.azure.com",
        port=3306,
        database="bd_emaus")

def insertar_datos(tabla, valores_tabla,datos):
    position_values = list()
    for i in valores_tabla:
        position_values.append(f"%({i})s")

    insert_string = (
        "INSERT INTO " + tabla + " "
        "(" + ",".join(valores_tabla) + ") "
        "VALUES (" + ",".join(position_values) + ")"
    )
    cnx = conexion_bd()
    cursor = cnx.cursor()
    cursor.execute(insert_string, datos)
    cnx.commit()
    cnx.close()

def actualizar_datos(tabla, valores_tabla, condicion, datos_actualizar):
    position_values = list()
    for i in valores_tabla:
        position_values.append(f"{i}=%({i})s")
    
    update_string = ("UPDATE " + tabla +
                    " SET " + ",".join(position_values) +
                    " WHERE "+ condicion)
    
    cnx = conexion_bd()
    cnx.cursor().execute(update_string, datos_actualizar)
    cnx.commit()
    cnx.close()

def eliminar_datos(tabla, condicion):
    delete_string = "DELETE FROM " + tabla + " WHERE " + condicion
    cnx = conexion_bd()
    cnx.cursor().execute(delete_string)
    cnx.commit()
    cnx.close()

def visualizar_datos(tabla, columnas=None, condicion=None, grupo=None, cond_grupo=None):
    select_col = ""
    if(columnas == None):
        select_col = "SELECT *"
    else:
        select_col = f"SELECT {columnas} "
    
    select_tb = f"FROM {tabla}"

    select_cond = ""
    if(condicion != None):
        select_cond = f" WHERE {condicion}"
    
    select_gr = ""
    if(grupo != None):
        select_gr = f"GROUP BY {grupo}"

    select_cond_gr = ""
    if(cond_grupo != None):
        select_cond_gr = f"HAVING {condicion}"
    
    select = select_col + select_tb + select_cond + select_gr + select_cond_gr
    
    cnx = conexion_bd()
    cursor = cnx.cursor()
    cursor.execute(select)

    seleccion = list()
    for fila in cursor:
        seleccion.append(fila)
    cnx.close()

    return seleccion

# Utilizar este metodo para insertar/actualizar/eliminar de cualquier tabla

def llamar_procedimiento(nombre: str, parametros: tuple) -> str:
    try:
        cnx = conexion_bd()
        cnx.autocommit = True
        cnx.cursor().callproc(nombre, parametros)
        cnx.close()
        return "Proceso Exitoso"
    except mysql.connector.Error as err:
        return err.msg
    

# Utilizar este metodo para verificar un id en una tabla
# El procedimiento tiene que tener el prefijo: VerificarID
# Cada palabra del nombre de la tabla tiene que comenzar con mayuscula
def verificar_id(tabla: str, nombre: str, apellido: str):
    try:
        cnx = conexion_bd()
        cursor = cnx.cursor()
        result = cursor.callproc("VerificarID" + tabla , (nombre,apellido, 0))
        return result[2]
    except mysql.connector.Error as err:
        return f"Error al verificar el ID {id} de la tabla {tabla}"