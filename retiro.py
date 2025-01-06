import utils
import bd_conections
import pandas as pd
from datetime import date
import time

def retiro():
    es_volver = False
    while not es_volver:
        utils.borrarPantalla()
        print("\nMenu Retiros")
        print("1. Registrar Retiro")
        print("2. Actualizar Retiro")
        print("3. Eliminar Retiro")
        print("4. Lista de Retiros")
        print("5. Ingresar Donaciones")
        print("6. Ingresar Pagos")
        print("7. Regresar")
        opcion = int(input("Seleccione una opcion:"))
        match opcion:
            case 1:
                ingresar_retiro()
            case 2:
                actualizar_retiro()
            case 3:
                eliminar_registro()
            case 4:
                listas_retiro()
            case 5:
                ingresar_donaciones()
            case 6:
                ingresar_pagos()
            case 7:
                es_volver =  True
            case _:
                print("\nIngrese una opcion valida")
                time.sleep(3)


def ingresar_retiro():
    utils.borrarPantalla()
    print("\nIngresar Retiro")
    parroquia= input("\nIngrese la parroquia donde se realizara el retiro: ")
    tipo= input("Indica para que personas es el retiro (Hombres/Mujeres/Jovenes):")
    
    utils.borrarPantalla()
    time.sleep(2)
    print("\nRegistrando Retiro...\n")
    utils.borrarPantalla()
    time.sleep(2)

    #Seccion de SQL
    try:
        cond_retiro = f"parroquia='{parroquia}' AND tipo='{tipo}'"
        retiro_existente = bd_conections.visualizar_datos("retiro", "id_retiro", cond_retiro)
        
        if len(retiro_existente) == 0:
            campos_retiro = ["parroquia", "tipo"]
            valores_retiro = {
                "parroquia": parroquia,
                "tipo": tipo}
            
            bd_conections.insertar_datos("retiro", campos_retiro, valores_retiro)
            
            id_retiro = bd_conections.visualizar_datos("retiro", "id_retiro", cond_retiro).pop()
            print(f"Retiro registrado exitosamente.")
        else:
            print("Este retiro ya está registrado en la base de datos.")
    except Exception as e:
        print(f"Ocurrió un error al registrar el retiro: {e}")
    time.sleep(3)


def actualizar_retiro():
    utils.borrarPantalla()
    print("\nActualizar Retiro")
    id_retiro = input("Ingrese el ID del retiro que desea actualizar: ")

    # Verifica si el retiro existe
    try:
        cond_retiro = f"id_retiro={id_retiro}"
        retiro_existente = bd_conections.visualizar_datos("retiro", "*", cond_retiro)

        if len(retiro_existente) == 0:
            print("No se encontró un retiro con ese ID.")
            time.sleep(2)
            return

        retiro = retiro_existente[0]
        print(f"\nDatos actuales del retiro con ID {id_retiro}:")
        print(f"Parroquia: {retiro['parroquia']}")
        print(f"Tipo: {retiro['tipo']}")

        nueva_parroquia = input(f"Nuevo valor para la parroquia (actual: {retiro['parroquia']}): ")
        nueva_tipo = input(f"Nuevo valor para el tipo (actual: {retiro['tipo']}): ")

        if not nueva_parroquia:
            nueva_parroquia = retiro['parroquia']
        if not nueva_tipo:
            nueva_tipo = retiro['tipo']

        valores_actualizados = {
            "parroquia": nueva_parroquia,
            "tipo": nueva_tipo
        }

        bd_conections.actualizar_datos("retiro", valores_actualizados, cond_retiro)

        print(f"\nRetiro con ID {id_retiro} actualizado exitosamente.")
        time.sleep(2)

    except Exception as e:
        print(f"Ocurrió un error al actualizar el retiro: {e}")
        time.sleep(3)

def eliminar_registro():
    while True:
        utils.borrarPantalla()
        print("\nEliminar Registro")
        print("1. Retiro")
        print("2. Pago")
        print("3. Donacion")
        opc = int(input("Seleccione una opcion: "))
        match opc:
            case 1:
                eliminar_retiro()
            case 2:
                eliminar_pago()
            case 3:
                eliminar_donacion()
            case 4:
                break
            case _:
                print("Seleccione una opcion valida")
                time.sleep(3)

def eliminar_retiro():
    while True:
        utils.borrarPantalla()
        print("\nEliminar Retiro por")
        print("1. ID")
        print("2. Parroquia")
        print("3. Regresar")
        opc = int(input("Seleccione una opcion: "))
        match opc:
            case 1:
                utils.borrarPantalla()
                lista_retiro_id()
                id = int(input("\nIngrese el id del retiro: "))
                condicion = f"id_retiro={id}"
                try:
                    bd_conections.eliminar_datos("retiro",condicion)
                    print("\nRetiro Eliminado")
                except Exception as e:
                    print(f"Error al eliminar retiro por ID: {e}")
                    
                time.sleep(3)
            case 2:
                utils.borrarPantalla()
                lista_retiro_id()
                parroquia = input("\nIngrese la parroquia del retiro: ")
                condicion = f"parroquia=\"{parroquia}\""
                try:
                    bd_conections.eliminar_datos("retiro",condicion)
                    print("\nRetiro Eliminado")
                except Exception as e:
                    print(f"Error al eliminar retiro por Parroquia: {e}")
                
                time.sleep(3)
            case 3:
                break
            case _:
                print("Seleccione una opcion valida")
                time.sleep(3)

def eliminar_pago():
    while True:
        utils.borrarPantalla()
        print("\nEliminar Pago por")
        print("1. ID")
        print("2. Regresar")
        opc = int(input("Seleccione una opcion: "))
        match opc:
            case 1:
                utils.borrarPantalla()
                lista_pago_id()
                id = int(input("\nIngrese el id del pago: "))
                condicion = f"id_pago={id}"
                try:
                    bd_conections.eliminar_datos("pago",condicion)
                    print("\nPago Eliminado")
                except Exception as e:
                    print(f"Error al eliminar pago por ID: {e}")
                    
                time.sleep(3)
            case 2:
                break
            case _:
                print("Seleccione una opcion valida")
                time.sleep(3)

def eliminar_donacion():
    while True:
        utils.borrarPantalla()
        print("\nEliminar Donación por")
        print("1. ID")
        print("2. Regresar")
        opc = int(input("Seleccione una opcion: "))
        match opc:
            case 1:
                utils.borrarPantalla()
                lista_donacion_id()
                id = int(input("\nIngrese el id de la donación: "))
                condicion = f"id_donacion={id}"
                try:
                    bd_conections.eliminar_datos("donacion",condicion)
                    print("\nDonación Eliminada")
                except Exception as e:
                    print(f"Error al eliminar donación por ID: {e}")
                    
                time.sleep(3)
            case 3:
                break
            case _:
                print("Seleccione una opcion valida")
                time.sleep(3)

def lista_retiro_id():
    tabla = "retiro"
    columnas = "id_retiro, parroquia"
    df = pd.DataFrame(bd_conections.visualizar_datos(tabla,columnas),columns=["ID", "Parroquia"])
    print("\n**Lista de Retiros**")
    print(df.to_string(index=False))
    print()

def lista_pago_id():
    tabla = "pago"
    columnas = "id_pago, valor"
    df = pd.DataFrame(bd_conections.visualizar_datos(tabla,columnas),columns=["ID", "Valor"])
    print("\n**Lista de Pagos**")
    print(df.to_string(index=False))
    print()

def lista_donacion_id():
    tabla = "donacion"
    columnas = "id_donacion, nombre"
    df = pd.DataFrame(bd_conections.visualizar_datos(tabla,columnas),columns=["ID", "Nombre"])
    print("\n**Lista de Donaciones**")
    print(df.to_string(index=False))
    print()