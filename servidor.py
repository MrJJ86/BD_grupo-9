import utils
import bd_conections
import pandas as pd
from datetime import date
import time

def servidor():
    es_volver = False
    while not es_volver:
        utils.borrarPantalla()
        print("\nMenu Servidores")
        print("1. Registrar")
        print("2. Actualizar")
        print("3. eliminar")
        print("4. Lista de Servidores")
        print("5. Regresar")
        print("Seleccione una opcion:")
        opcion = int(input())
        match opcion:
            case 1:
                ingresar_servidor()
            case 2:
                actualizar_servidor()
            case 3:
                eliminar_servidor()
            case 4:
                lista_servidor()
            case 5:
                es_volver =  True
            case _:
                print("\nIngrese una opcion valida")

def ingresar_servidor():
    utils.borrarPantalla()
    print("\nIngresar a los Servidores")
    nombres = input("\nNombres: ")
    apellidos = input("Apellidos: ")

    email = "null"
    if(input("Tiene email? (y/n): ") == "y"):
        email = input("Email: ")
    celular = "null"
    if input("Tiene numero celular? (y/n): ") == "y":
        celular = input("Celular: ")

    ciudad = input("Ciudad correspondiente del Servidor: ")
    ronca = 1 if (input("El participante Ronca? (y/n): ") == "y") else 0
    es_guia = 1 if (input("El Servidor es Guia? (y/n): ") == "y") else 0
    es_subguia = 1 if (input("El Servidor es sub Guia? (y/n): ") == "y") else 0
    

    utils.borrarPantalla()
    time.sleep(2)
    print("\nRegistrando Servidor...\n")
    utils.borrarPantalla()
    time.sleep(2)

    #Seccion de SQL
    try:
        cond_servidor = f"nombre='{nombres}' AND apellido='{apellidos}'"
        servidor_existente = bd_conections.visualizar_datos("servidor", "id_servidor", cond_servidor)
        
        if len(servidor_existente) > 0:
            print("Este Servidor ya está registrado en la base de datos.")
            time.sleep(2)
            return None
        
        # Registrar el servidor
        campos_servidor = ("nombre", "apellido", "email", "celular", "ciudad", "ronca", "es_guia", "es_subguia")
        datos_servidor = {
            "nombre": nombres,
            "apellido": apellidos,
            "email": email,
            "celular": celular,
            "ciudad": ciudad,
            "ronca": ronca,
            "es_guia": es_guia,
            "es_subguia": es_subguia
        }
        resultado_servidor = bd_conections.llamar_procedimiento("InsertarServidor", datos_servidor)
        if resultado_servidor == "Proceso Exitoso":
            print("\nRetiro registrado exitosamente.")
        else:
            print(f"\n{resultado_servidor}")
            time.sleep(5)
            return None
             
    except Exception as e:
        print(f"Ocurrió un error al registrar el retiro: {e}")
    time.sleep(2)

def actualizar():
    while True:
        utils.borrarPantalla()
        print("\nActualizar Registro")
        print("1. Servidor")
        print("2. Regresar")
        opc = int(input("Seleccione una opcion: "))
        match opc:
            case 1:
                utils.borrarPantalla()
                lista_servidor_id()
                id_servidor = int(input("\nIngrese el ID del Servidor a actualizar: "))
                try:
                    resultado = bd_conections.visualizar_datos("Servidor","nombre",f"id_servidor={id_servidor}")
                    if(len(resultado) != 0):
                        actualizar_servidor(id_servidor)
                    else:
                        servidor_existe = bd_conections.verificar_id("Servidor", id=id_servidor)
                        if isinstance(servidor_existe, str):
                            print(f"\n{servidor_existe}")
                            time.sleep(5)
                            return None
                        
                except Exception as e:
                    print(f"Error al comprobar si existe el servidor en actualizar datos: {e}")

                time.sleep(3)

            case 2:
                break
            case _:
                print("Seleccione una opcion valida")
                time.sleep(3)

def actualizar_servidor(id_servidor):
    tabla = "servidor"
    condicion = f"id_servidor={id_servidor}"
    df_servidor = pd.DataFrame(bd_conections.visualizar_datos(tabla,condicion=condicion)).to_string(index=False)
    while True:
        utils.borrarPantalla()
        print("\nActualizar Servidor")
        print("1. Nombres y Apellidos")
        print("2. Email y Celular")
        print("3. Ciudad")
        print("4. Informacion del servidor adicional")
        print("5. Regresar")
        opc = int(input("Seleccione una opcion: "))
        match opc:
            case 1:
                utils.borrarPantalla()
                print("\nActualizar Nombres y Apellidos del Servidor")
                print(df_servidor)
                nombre = input("Nombre: ")
                apellido = input("Apellido: ")
                try:
                    datos_actualizados = (id_servidor, nombre, apellido)
                    resultado_actualizacion = bd_conections.llamar_procedimiento("ActualizarServidor", datos_actualizados)
                    
                    if resultado_actualizacion == "Proceso Exitoso":
                        print(f"\nRetiro con ID {id_retiro} actualizado exitosamente.")
                    else:
                        print(f"\n{resultado_actualizacion}")
                        time.sleep(5)
                        return None
                except Exception as e:
                    print(f"Error al actualizar el Servidor: {e}")
                time.sleep(2)
            case 2:
                utils.borrarPantalla()
                print("\nActualizar Email y Celular del Servidor")
                print(df_servidor)
                celular = input("Celular: ")
                email=input("Email: ")

                try:
                    datos_actualizados = (id_servidor, celular, email)
                    resultado_actualizacion = bd_conections.llamar_procedimiento("ActualizarServidor", datos_actualizados)
                except Exception as e:
                    print(f"Error al actualizar el Servidor: {e}")
                time.sleep(2)
            case 3:
                utils.borrarPantalla()
                print("\nActualizar Ciudad del Servidor")
                print(df_servidor)
                ciudad = input("Ciudad correspondiente: ")

                try:
                    datos_actualizados = (id_servidor, ciudad)
                    resultado_actualizacion = bd_conections.llamar_procedimiento("ActualizarServidor", datos_actualizados)
                except Exception as e:
                    print(f"Error al actualizar ell Servidor: {e}")
                time.sleep(2)
            case 4:
                utils.borrarPantalla()
                print("\nActualizar informacion adicional del Servidor")
                print(df_servidor)
                ronca = 1 if (input("El participante Ronca? (y/n): ") == "y") else 0
                es_guia = 1 if (input("El Servidor es Guia? (y/n): ") == "y") else 0
                es_subguia = 1 if (input("El Servidor es sub Guia? (y/n): ") == "y") else 0
                try:
                    datos_actualizados = (id_servidor, ronca, es_guia,es_subguia)
                    resultado_actualizacion = bd_conections.llamar_procedimiento("ActualizarServidor", datos_actualizados)
                except Exception as e:
                    print(f"Error al actualizar el Servidor: {e}")
                time.sleep(2)
            case 5:
                break
            case _:
                print("Seleccione una opcion valida")
                time.sleep(2)


def eliminar_servidor():
    tabla="servidor"
    condicion = f"id_servidor={id}"
    while True:
        utils.borrarPantalla()
        print("\nEliminar Servidor por")
        print("1. ID")
        print("2. Nombre y Apellido")
        print("3. Regresar")
        opc = int(input("Seleccione una opcion: "))
        match opc:
            case 1:
                utils.borrarPantalla()
                lista_servidor_id()
                id = int(input("\nIngrese el id del servidor: "))
                try:
                    resultado = bd_conections.llamar_procedimiento("EliminarServidorPorID",tuple([id]))

                    if(resultado != "Proceso Exitoso"):
                        print(f"\n{resultado}")
                        time.sleep(5)
                    else:
                        print("Participante Eliminado")
                        time.sleep(3)
                except Exception as e:
                    print(f"Error al eliminar servidor por ID: {e}")
                    
                time.sleep(3)
            case 2:
                utils.borrarPantalla()
                lista_servidor_id()
                nombre = input("\nIngrese el nombre del servidor: ")
                apellido = input("Ingrese el apellido del servidor: ")
                try:

                    resultado = bd_conections.llamar_procedimiento("EliminarServidorPorNombreApellido",(nombre, apellido))

                    if(resultado != "Proceso Exitoso"):
                        print(f"\n{resultado}")
                        time.sleep(5)
                    else:
                        print("Participante Eliminado")
                        time.sleep(3)
                except Exception as e:
                    print(f"Error al eliminar servidor por nombre y apellido: {e}")
                
                time.sleep(3)
            case 3:
                break
            case _:
                print("Seleccione una opcion valida")
                time.sleep(3)

def lista_servidor_id():
    vista = "view_servidorID"
    df = pd.DataFrame(bd_conections.visualizar_datos(vista),columns=["ID", "nombre", "apellido"])
    print("\n**Lista de Servidores**")
    print(df.to_string(index=False))
    print()


def lista_servidor():
    tabla = "servidor"
    columnas_df = ["ID_Servidor","nombre","apellido","email","celular"]
    df = pd.DataFrame(bd_conections.visualizar_datos(tabla), columns=columnas_df).to_string(index=False)
    print(df)