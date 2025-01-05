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
    es_guia = 1 if (input("El Servidor es Guia? (y/n): ") == "y") else 0
    es_subguia = 1 if (input("El Servidor es sub Guia? (y/n): ") == "y") else 0

    utils.borrarPantalla()
    time.sleep(2)
    print("\nRegistrando Servidor...\n")
    utils.borrarPantalla()
    time.sleep(2)

    #Seccion de SQL



def actualizar_servidor():
    pass

def eliminar_servidor():
    pass

def lista_servidor():
    tabla = "servidor"
    columnas = "nombre,apellido,ciudad,email,celular"
    df = pd.DataFrame(bd_conections.visualizar_datos(tabla,columnas), columns=["Nombre","Apellido","Ciudad","Email","Celular"])
    print()
    print(df)