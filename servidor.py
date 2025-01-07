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
        
        if len(servidor_existente) == 0:
            campos_servidor = ["nombre", "apellido", "email", "celular", "ciudad", "ronca", "es_guia", "es_subguia"]
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
            bd_conections.insertar_datos("servidor", campos_servidor, datos_servidor)
            
            id_servidor = bd_conections.visualizar_datos("servidor", "id_servidor", cond_servidor).pop()
            print(f"Servidor registrado exitosamente con ID: {id_servidor}")
            time.sleep(2)
        else:
            print("El servidor ya está registrado en la base de datos.")
            time.sleep(2)
    except Exception as e:
        print(f"Ocurrió un error al registrar al servidor: {e}")
    time.sleep(3)

def actualizar():
    pass

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
                    bd_conections.actualizar_datos(tabla,["nombre","apellido"],condicion,{"nombre":nombre,"apellido":apellido})
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
                    bd_conections.actualizar_datos(tabla,["email","celular"],condicion,{"email":email,"celular":celular})
                except Exception as e:
                    print(f"Error al actualizar el Servidor: {e}")
                time.sleep(2)
            case 3:
                utils.borrarPantalla()
                print("\nActualizar Ciudad del Servidor")
                print(df_servidor)
                ciudad = input("Ciudad correspondiente: ")

                try:
                    bd_conections.actualizar_datos(tabla,["ciudad"],condicion,{"ciudad":ciudad})
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
                    bd_conections.actualizar_datos("servidor",["ronca","es_guia","es_subguia"],condicion,{"ronca":ronca,"es_guia":es_guia,"es_subguia":es_subguia})
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
                    bd_conections.eliminar_datos(tabla,condicion)
                    print("\nServidor Eliminado")
                except Exception as e:
                    print(f"Error al eliminar servidor por ID: {e}")
                    
                time.sleep(3)
            case 2:
                utils.borrarPantalla()
                lista_servidor_id()
                nombre = input("\nIngrese el nombre del servidor: ")
                apellido = input("Ingrese el apellido del servidor: ")
                condicion = f"nombre=\"{nombre}\" and apellido=\"{apellido}\""
                try:
                    bd_conections.eliminar_datos(tabla,condicion)
                    print("\nServidor Eliminado")
                except Exception as e:
                    print(f"Error al eliminar servidor por nombre y apellido: {e}")
                
                time.sleep(3)
            case 3:
                break
            case _:
                print("Seleccione una opcion valida")
                time.sleep(3)

def lista_servidor_id():
    tabla = "servidor"
    columnas = "id_servidor, nombre, apellido"
    df = pd.DataFrame(bd_conections.visualizar_datos(tabla,columnas),columns=["ID", "Nombre","Apellido"])
    print("\n**Lista de Servidores**")
    print(df.to_string(index=False))
    print()


def lista_servidor():
    tabla = "servidor"
    columnas = "nombre,apellido,ciudad,email,celular"
    df = pd.DataFrame(bd_conections.visualizar_datos(tabla,columnas), columns=["Nombre","Apellido","Ciudad","Email","Celular"])
    print()
    print(df)