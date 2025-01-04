import bd_conections
import utils
import pandas as pd

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
    pass

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