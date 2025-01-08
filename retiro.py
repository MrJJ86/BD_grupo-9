import utils
import bd_conections
import pandas as pd
from datetime import date
import time
import participante as part
import servidor as serv

def retiro():
    es_volver = False
    while not es_volver:
        utils.borrarPantalla()
        print("\nMenu Retiros")
        print("1. Registrar Retiro")
        print("2. Actualizar Retiro")
        print("3. Eliminar Registro")
        print("4. Listas de Registros")
        print("5. Ingresar Donaciones")
        print("6. Ingresar Pagos")
        print("7. Regresar")
        opcion = int(input("Seleccione una opcion: "))
        match opcion:
            case 1:
                ingresar_retiro()
            case 2:
                actualizar_retiro()
            case 3:
                eliminar_registro()
            case 4:
                lista_registro()
            case 5:
                ingresar_donaciones()
            case 6:
                ingresar_pagos()
            case 7:
                es_volver =  True
            case _:
                print("\nIngrese una opcion valida")
                time.sleep(2)


def ingresar_retiro():
    utils.borrarPantalla()
    print("\nIngresar Retiro")
    parroquia= input("\nIngrese la parroquia donde se realizara el retiro: ")
    tipo= input("Indica para que personas es el retiro (Hombres/Mujeres/Jovenes mujeres/Jovenes Hombres): ")
    fecha= input("Ingrese fecha del retiro (yyyy-mm-dd): ")
    
    utils.borrarPantalla()
    time.sleep(2)
    print("\nRegistrando Retiro...\n")
    utils.borrarPantalla()
    time.sleep(2)

    #Seccion de SQL
    try:
        cond_retiro = f"parroquia='{parroquia}' AND tipo='{tipo}' AND fecha='{fecha}'"
        retiro_existente = bd_conections.visualizar_datos("retiro","id_retiro",cond_retiro)
        
        if len(retiro_existente) == 0:
            campos_retiro = ["parroquia","tipo","fecha"]
            valores_retiro = {
                "parroquia": parroquia,
                "tipo": tipo,
                "fecha": fecha}
            
            bd_conections.insertar_datos("retiro",campos_retiro,valores_retiro)
            
            id_retiro = bd_conections.visualizar_datos("retiro","id_retiro",cond_retiro).pop()
            print(f"Retiro registrado exitosamente.")
        else:
            print("Este retiro ya está registrado en la base de datos.")
    except Exception as e:
        print(f"Ocurrió un error al registrar el retiro: {e}")
    time.sleep(2)


def actualizar_retiro():
    utils.borrarPantalla()
    print("\nActualizar Retiro")

    # Valida que el ID sea un número válido
    try:
        lista_retiro_id()
        id_retiro = int(input("Ingrese el ID del retiro que desea actualizar: "))
    except ValueError:
        print("El ID debe ser un número entero.")
        time.sleep(2)
        return  

    # Verifica si el retiro existe
    try:
        cond_retiro = f"id_retiro={id_retiro}"
        retiro_existente = bd_conections.visualizar_datos("retiro", "*", cond_retiro)

        if len(retiro_existente) == 0:
            print("No se encontró un retiro con ese ID.")
            time.sleep(2)
            return

        _, parroquia_actual, tipo_actual, fecha_actual = retiro_existente[0]
        print(f"\nDatos actuales del retiro con ID {id_retiro}:")
        print(f"Parroquia: {parroquia_actual}")
        print(f"Tipo: {tipo_actual}")
        print(f"Fecha: {fecha_actual}")

       # Solicita al usuario los nuevos datos
        nueva_parroquia = input(f"Nuevo valor para la parroquia (actual: {parroquia_actual}): ").strip() or parroquia_actual
        nuevo_tipo = input(f"Nuevo valor para el tipo (actual: {tipo_actual}): ").strip() or tipo_actual
        nueva_fecha= input(f"Nueva fecha (actual {fecha_actual}): ").strip() or fecha_actual

        # Se actualiza los datos en la database
        valores_actualizados = {
            "parroquia": nueva_parroquia,
            "tipo": nuevo_tipo,
            "fecha":nueva_fecha
        }
        bd_conections.actualizar_datos("retiro", valores_actualizados, f"id_retiro={id_retiro}")

        print(f"\nRetiro con ID {id_retiro} actualizado exitosamente.")
        time.sleep(2)

    except Exception as e:
        print(f"Ocurrió un error al actualizar el retiro: {e}")
        time.sleep(2)


def eliminar_registro():
    while True:
        utils.borrarPantalla()
        print("\nEliminar Registro")
        print("1. Retiro")
        print("2. Pago")
        print("3. Donacion")
        print("4. Regresar")
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
                time.sleep(2)

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
            case 2:
                break
            case _:
                print("Seleccione una opcion valida")
                time.sleep(3)

def lista_retiro_id():
    tabla = "retiro"
    columnas = "id_retiro, parroquia, fecha"
    df = pd.DataFrame(bd_conections.visualizar_datos(tabla,columnas),columns=["ID",  "Parroquia" , "Fecha"])
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

def lista_registro():
    while True:
        utils.borrarPantalla()
        print("\nListas")
        print("1. Información de Retiros")
        print("2. Información de Pagos ")
        print("3. Información de Donaciones")
        print("4. Regresar")
        opc = int(input("Seleccione una opcion: "))
        match opc:
            case 1:
                utils.borrarPantalla()
                lista_info_retiros()
                input("Presione una Tecla para Regresar")
                time.sleep(2)
            case 2:
                utils.borrarPantalla()
                lista_info_pagos()
                input("Presione una Tecla para Regresar")
                time.sleep(2)
            case 3:
                utils.borrarPantalla()
                lista_info_donaciones()
                input("Presione una Tecla para Regresar")
                time.sleep(2)
            case 4:
                break
            case _:
                print("Seleccione una opcion valida")
                time.sleep(2)

def lista_info_retiros():
    tabla = "retiro"
    columnas_df = ["id_retiro","parroquia","tipo","fecha"]
    columnas_sql = ",".join(columnas_df)
    df = pd.DataFrame(bd_conections.visualizar_datos(tabla,columnas_sql), columns=columnas_df).to_string(index=False)
    print(df)

def lista_info_pagos():
    tabla = "pago"
    columnas_df = ["id_pago","valor","pago_completado"]
    columnas_sql = ",".join(columnas_df)
    df = pd.DataFrame(bd_conections.visualizar_datos(tabla,columnas_sql), columns=columnas_df).to_string(index=False)
    print(df)

def lista_info_donaciones():
    tabla = "donacion"
    columnas_df = ["id_donacion","nombre","detalle","valor"]
    columnas_sql = ",".join(columnas_df)
    df = pd.DataFrame(bd_conections.visualizar_datos(tabla,columnas_sql), columns=columnas_df).to_string(index=False)
    print(df)


def ingresar_donaciones():
    while True:
        utils.borrarPantalla()
        print("\nIngreso de Donación")
        
        lista_retiro_id()
        # Se ingresa el ID del retiro donde se quiere hacer la donacion
        try:
            id_retiro = int(input("\nIngrese el ID del retiro al cual se asociará la donación: "))
        except ValueError:
            print("Debe ingresar un número válido para el ID del retiro.")
            time.sleep(2)
            continue

        # Verifica si el retiro existe
        condicion = f"id_retiro={id_retiro}"
        retiro = bd_conections.visualizar_datos("retiro", "id_retiro", condicion)
        
        if not retiro:
            print("El ID de retiro no es válido. Intente nuevamente.")
            time.sleep(2)
            continue

        # El usuario ingresa los datos
        nombre = input("\nIngrese el nombre de la persona que realiza la donación: ").strip()
        detalle = input("Ingrese el detalle (motivo) de la donación: ").strip()
        
        while True:
            try:
                valor = float(input("Ingrese el valor de la donación: "))
                if valor <= 0:
                    print("El valor debe ser mayor que 0. Intente nuevamente.")
                    continue
                break
            except ValueError:
                print("Debe ingresar un número válido para el valor de la donación.")
     
        utils.borrarPantalla()
        time.sleep(2)
        print("\nRegistrando donacion...\n")
        utils.borrarPantalla()
        time.sleep(2)

        # Se ingresa los datos
        try:
            cond_donacion = f"nombre='{nombre}' AND detalle='{detalle}' AND valor='{valor}' AND id_retiro='{id_retiro}'"
            donacion_existente = bd_conections.visualizar_datos("donacion", "id_donacion", cond_donacion)
            
            if len(donacion_existente)==0:
                # Si la donación no existe, se inserta en la base de datos.
                columnas = ['nombre', 'detalle', 'valor', 'id_retiro']
                datos_donacion = {
                    'nombre': nombre,
                    'detalle': detalle,
                    'valor': valor,
                    'id_retiro': id_retiro}
                
                bd_conections.insertar_datos("donacion", columnas, datos_donacion)
                print("\nDonación registrada correctamente.")
            else:
                print("Esta donacion ya está registrado en la base de datos.")
        except Exception as e:
            print(f"Error al registrar la donación: {e}")
            time.sleep(2)


def ingresar_pagos():
    while True:
        utils.borrarPantalla()
        print("\nIngreso de Pago")

        lista_retiro_id()
        try:
            id_retiro = int(input("\nIngrese el ID del retiro al cual se asociará el pago: "))
        except ValueError:
            print("Debe ingresar un número válido para el ID del retiro.")
            time.sleep(2)
            continue
        
        # Verificar si el retiro existe
        condicion = f"id_retiro={id_retiro}"
        retiro = bd_conections.visualizar_datos("retiro", "id_retiro", condicion)
        
        if not retiro:
            print("El ID de retiro no es válido. Intente nuevamente.")
            time.sleep(2)
            continue
        
        # Determina si el pago pertenece a un participante o servidor
        while True:
            tipo_persona = input("¿El pago es realizado por un Participante (p) o un Servidor (s)? ").strip().lower()
            if tipo_persona in ('p', 's'):
                break
            print("Debe ingresar 'p' para Participante o 's' para Servidor.")

        if tipo_persona == 'p':
            # Obtener ID del participante
            while True:
                try:
                    part.lista_participantes_id()
                    id_participante = int(input("\nIngrese el ID del participante: "))
                    condicion_part = f"id_participante={id_participante}"
                    participante = bd_conections.visualizar_datos("participante", "id_participante", condicion_part)
                    if not participante:
                        print("El ID del participante no es válido. Intente nuevamente.")
                        continue
                    break
                except ValueError:
                    print("Debe ingresar un número válido para el ID del participante.")
        else:
            # Obtener ID del servidor
            while True:
                try:
                    serv.lista_servidor_id()
                    id_servidor = int(input("\nIngrese el ID del servidor: "))
                    condicion_serv = f"id_servidor={id_servidor}"
                    servidor = bd_conections.visualizar_datos("servidor", "id_servidor", condicion_serv)
                    if not servidor:
                        print("El ID del servidor no es válido. Intente nuevamente.")
                        continue
                    break
                except ValueError:
                    print("Debe ingresar un número válido para el ID del servidor.")

        # Se ingresa los detalles del pago
        while True:
            try:
                valor = float(input("\nIngrese el valor del pago: "))
                if valor <= 0:
                    print("El valor debe ser mayor que 0. Intente nuevamente.")
                    continue
                break
            except ValueError:
                print("Debe ingresar un número válido para el valor del pago.")
        
        while True:
            pago_completado = input("¿El pago está completado? (s/n): ").strip().lower()
            if pago_completado == 's':
                pago_completado = True
                break
            elif pago_completado == 'n':
                pago_completado = False
                break
            else:
                print("Debe ingresar 's' para sí o 'n' para no.")
                utils.borrarPantalla()

        time.sleep(2)
        print("\nRegistrando pago...\n")
        utils.borrarPantalla()
        time.sleep(2)

        # Se ingresa los datos
        try:
            columnas = ['valor', 'pago_completado', 'id_retiro']
            datos_pago = {
                'valor': valor,
                'pago_completado': pago_completado,
                'id_retiro': id_retiro
            }
            bd_conections.insertar_datos("pago", columnas, datos_pago)

            # Obtener el ID del pago recién registrado
            cond_pago = f"valor='{valor}' AND pago_completado={int(pago_completado)} AND id_retiro={id_retiro}"
            nuevo_pago = bd_conections.visualizar_datos("pago", "id_pago", cond_pago)
            id_pago = nuevo_pago[0][0]

            # Registrar en participante_pago o servidor_pago según el caso
            if tipo_persona == 'p':
                columnas_rel = ['id_pago', 'id_participante']
                datos_rel = {'id_pago': id_pago, 'id_participante': id_participante}
                bd_conections.insertar_datos("participante_pago", columnas_rel, datos_rel)
            else:
                columnas_rel = ['id_pago', 'id_servidor']
                datos_rel = {'id_pago': id_pago, 'id_servidor': id_servidor}
                bd_conections.insertar_datos("servidor_pago", columnas_rel, datos_rel)

            print("\nPago registrado correctamente.")
            time.sleep(2)

        except Exception as e:
            print(f"Error al registrar el pago: {e}")
            time.sleep(2)