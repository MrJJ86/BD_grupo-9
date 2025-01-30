import utils
import bd_conections
import pandas as pd
from datetime import datetime
import time
import participante as part
import servidor as serv

def retiro():
    es_volver = False
    while not es_volver:
        utils.borrarPantalla()
        print("\nMenu Retiros")
        print("1. Ingresar Registros")
        print("2. Actualizar Registros")
        print("3. Eliminar Registros")
        print("4. Listas de Registros")
        print("5. Regresar")
        opcion = int(input("Seleccione una opcion: "))
        match opcion:
            case 1:
                ingresar_registros()
            case 2:
                actualizar_registros()
            case 3:
                eliminar_registros()
            case 4:
                listas_registros()
            case 5:
                es_volver =  True
            case _:
                print("\nIngrese una opcion valida")
                time.sleep(2)


def ingresar_registros():
    while True:
        utils.borrarPantalla()
        print("\nIngresar Registros")
        print("1. Retiro")
        print("2. Donación")
        print("3. Pago")
        print("4. Regresar")
        opcion = int(input("Seleccione una opcion: "))
        match opcion:
            case 1:
                ingresar_retiro()
            case 2:
                ingresar_donaciones()
            case 3:
                ingresar_pago()
            case 4:
                break
            case _:
                print("\nIngrese una opcion válida")
                time.sleep(2)  

def ingresar_retiro():
    utils.borrarPantalla()
    print("\nIngresar Retiro")
    parroquia= input("\nIngrese la parroquia donde se realizara el retiro: ")
    tipo= input("Indica para que personas es el retiro (Hombres/Mujeres/Jovenes mujeres/Jovenes Hombres): ")
    fecha= obtener_fecha()
    
    utils.borrarPantalla()
    time.sleep(2)
    print("\nRegistrando Retiro...\n")
    utils.borrarPantalla()
    time.sleep(2)

    #Seccion de SQL
    try:
        # Verificar si el retiro ya existe  
        cond_retiro = f"parroquia='{parroquia}' AND tipo='{tipo}' AND fecha='{fecha}'"
        retiro_existente = bd_conections.visualizar_datos("retiro","id_retiro",cond_retiro)
        
        if len(retiro_existente) > 0:
            print("Este retiro ya está registrado en la base de datos.")
            time.sleep(2)
            return None
        
        # Registrar el retiro
        datos_retiro = (parroquia, tipo, fecha)
        resultado_retiro = bd_conections.llamar_procedimiento("InsertarRetiro", datos_retiro)
        if resultado_retiro == "Proceso Exitoso":
            print("\nRetiro registrado exitosamente.")
        else:
            print(f"\n{resultado_retiro}")
            time.sleep(5)
            return None
             
    except Exception as e:
        print(f"Ocurrió un error al registrar el retiro: {e}")
    time.sleep(2)

def ingresar_donaciones():
    while True:
        utils.borrarPantalla()
        print("\nIngreso de Donación")
        
        lista_retiro_id()
        # Se ingresa el ID del retiro donde se quiere hacer la donacion
        try:
            id_ingresado = int(input("\nIngrese el ID del retiro al cual se asociará la donación: "))
        except ValueError:
            print("Debe ingresar un número válido para el ID del retiro.")
            time.sleep(2)
            continue

        # Verifica si el retiro existe
        id_retiro = bd_conections.verificar_id("RetiroPorId", id=id_ingresado)
        if isinstance(id_retiro, str):
            print(f"\n{id_retiro}")
            time.sleep(5)
            return
        
        if(id_retiro != None):
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
            cond_donacion = f"nombre='{nombre}' AND detalle='{detalle}' AND valor='{valor}' AND id_retiro='{id_retiro}'"
            donacion_existente = bd_conections.visualizar_datos("donacion", "id_donacion", cond_donacion)
                
            if len(donacion_existente)==0:
                # Si la donación no existe, se inserta en la base de datos.
                try:
                    resultado = bd_conections.llamar_procedimiento("InsertarDonacion", (nombre, detalle, valor, id_retiro))
                    
                    if resultado == "Proceso Exitoso":
                        print("\nDonación registrada correctamente.")
                    else:
                        print(f"Error al registrar la donación: {resultado}")
                except Exception as e:
                    print(f"Error al registrar la donación: {e}")
            else:
                print("Esta donacion ya está registrado en la base de datos.")
            time.sleep(2)

        else:
            print(f"El retiro con el id {id_ingresado} no existe")
        time.sleep(2)

def ingresar_pago():
    while True:
        utils.borrarPantalla()
        print("\nIngreso de Pago")

        lista_retiro_id()
        try:
            id_ingresado = int(input("\nIngrese el ID del retiro al cual se asociará el pago: "))
        except ValueError:
            print("Debe ingresar un número válido para el ID del retiro.")
            time.sleep(2)
            continue
        
        # Verificar si el retiro existe
        id_retiro = bd_conections.verificar_id("RetiroPorId", id=id_ingresado)
        if isinstance(id_retiro, str):
            print(f"\n{id_retiro}")
            time.sleep(5)
            return
        
        if(id_retiro != None):
            # Determina si el pago pertenece a un participante o servidor
            while True:
                tipo_persona = input("¿El pago es realizado por un Participante (p) o un Servidor (s)? ").strip().lower()
                if tipo_persona in ('p', 's'):
                    break
                print("Debe ingresar 'p' para Participante o 's' para Servidor.")

            if tipo_persona == 'p':
                utils.borrarPantalla()
                # Obtener ID del participante
                while True:
                    try:
                        part.lista_participantes_id()
                        id_participante = int(input("\nIngrese el ID del participante que realizará el pago: "))
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
                utils.borrarPantalla()
                while True:
                    try:
                        serv.lista_servidor_id()
                        id_servidor = int(input("\nIngrese el ID del servidor que realizará el pago: "))
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

            # registrar el pago
            try:
                # Determinar la persona (participante o servidor)
                if tipo_persona == 'p':
                    id_persona = id_participante
                else:
                    id_persona = id_servidor

                # InsertarPago
                bd_conections.llamar_procedimiento(
                    "InsertarPago",
                    (valor, int(pago_completado), id_retiro, tipo_persona, id_persona)
                )

                print("\nPago registrado correctamente.")
                time.sleep(2)

            except Exception as e:
                print(f"Error al registrar el pago: {e}")
                time.sleep(2)
        else:
            print(f"El retiro con el id {id_ingresado} no existe")
        time.sleep(2)
        


def actualizar_registros():
    while True:
        utils.borrarPantalla()
        print("\nActualizar Registros")
        print("1. Actualizar Retiro")
        print("2. Actualizar Donación")
        print("3. Actualizar Pago")
        print("4. Regresar")
        opcion = int(input("Seleccione una opcion: "))
        match opcion:
            case 1:
                actualizar_retiro()
            case 2:
                actualizar_donacion()
            case 3:
                actualizar_pago()
            case 4:
                break
            case _:
                print("\nIngrese una opcion válida")
                time.sleep(2)

def actualizar_retiro():
    utils.borrarPantalla()
    print("\nActualizar Retiro")

    # Valida que el ID sea un número válido
    try:
        lista_retiro_id()
        id_ingresado = int(input("Ingrese el ID del retiro que desea actualizar: "))
    except ValueError:
        print("El ID debe ser un número entero.")
        time.sleep(2)
        return  
    
    # Verifica si el retiro existe
    id_retiro = bd_conections.verificar_id("RetiroPorID", id=id_ingresado)

    # Por si falla la verificación del ID
    if isinstance(id_retiro, str):
        print(f"\n{id_retiro}")
        time.sleep(5)
        return
    
    if(id_retiro != None):
        tabla = "retiro"
        condicion = f"id_retiro={id_retiro}"
        actualizar_datos = [id_retiro,None, None, None]

        while True:
            utils.borrarPantalla()
            print("\nActualizar Retiro")
            print("1. Actualizar Parroquia del Retiro")
            print("2. Actualizar Tipo del Retiro")
            print("3. Actualizar Fecha del Retiro")
            print("4. Regresar")
            opc = int(input("Seleccione una opcion: "))
            match opc:
                case 1:
                    utils.borrarPantalla()
                    print("\nActualizar Parroquia del Retiro")
                    df_nom_ape = pd.DataFrame(
                    bd_conections.visualizar_datos(tabla,"id_retiro, parroquia",condicion=condicion),
                    columns=["ID","Parroquia"]).to_string(index=False)
                    print(df_nom_ape)

                    parroquia = input("\nParroquia: ")
                    actualizar_datos[1] = parroquia

                    resultado = bd_conections.llamar_procedimiento("ActualizarRetiro",tuple(actualizar_datos))
                    if(resultado != "Proceso Exitoso"):
                        print(f"\n{resultado}")
                        time.sleep(5)
                    else:
                        time.sleep(2)
                
                case 2:
                    utils.borrarPantalla()
                    print("\nActualizar Tipo del Retiro")
                    df_nom_ape = pd.DataFrame(
                    bd_conections.visualizar_datos(tabla,"id_retiro, parroquia, tipo",condicion=condicion),
                    columns=["ID","Parroquia","Tipo"]).to_string(index=False)
                    print(df_nom_ape)

                    tipo = input("\nTipo(Hombres/Mujeres/Jovenes mujeres/Jovenes Hombres): ")
                    actualizar_datos[2] = tipo

                    resultado = bd_conections.llamar_procedimiento("ActualizarRetiro",tuple(actualizar_datos))
                    if(resultado != "Proceso Exitoso"):
                        print(f"\n{resultado}")
                        time.sleep(5)
                    else:
                        time.sleep(2)

                case 3:
                    utils.borrarPantalla()
                    print("\nActualizar Fecha del Retiro")
                    df_nom_ape = pd.DataFrame(
                    bd_conections.visualizar_datos(tabla,"id_retiro, parroquia, fecha",condicion=condicion),
                    columns=["ID","Parroquia","Fecha"]).to_string(index=False)
                    print(df_nom_ape)

                    fecha= obtener_fecha()
                    actualizar_datos[3] = fecha

                    resultado = bd_conections.llamar_procedimiento("ActualizarRetiro",tuple(actualizar_datos))
                    if(resultado != "Proceso Exitoso"):
                        print(f"\n{resultado}")
                        time.sleep(5)
                    else:
                        time.sleep(2)

                case 4:
                    break
                case _:
                    print("Seleccione una opcion valida")
                    time.sleep(2)
                
    else:
        print(f"El retiro con el id {id_ingresado} no existe")
    time.sleep(2)



def eliminar_registros():
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
        try:
            opc = int(input("Seleccione una opción: "))
        except ValueError:
            print("La opción debe ser un número entero.")
            time.sleep(2)
            continue
        
        match opc:
            case 1:
                utils.borrarPantalla()
                lista_retiro_id()
                try:
                    id_ingresado = int(input("\nIngrese el ID del retiro: "))
                except ValueError:
                    print("El ID debe ser un número entero.")
                    time.sleep(2)
                    continue

                # Verifica si el retiro existe
                id_retiro = bd_conections.verificar_id("RetiroPorId",id=id_ingresado)
                if(isinstance(id_retiro, str)):
                    print(f"\n{id_retiro}")
                    time.sleep(5)
                    continue
                
                if(id_retiro != None):
                    # Elimina el retiro por ID
                    resultado = bd_conections.llamar_procedimiento("EliminarRetiroPorID", tuple([id_retiro]))

                    if(resultado != "Proceso Exitoso"):
                        print(f"\n{resultado}")
                        time.sleep(5)
                    else:
                        print("Retiro Eliminado")
                        time.sleep(2)
                    
                else:
                    print(f"El retiro con el id {id_ingresado} no existe")
                time.sleep(2)

            case 2:
                utils.borrarPantalla()
                lista_retiro_id()
                parroquia = input("\nIngrese la parroquia del retiro (Se eliminarán todos los retiros con el nombre de esa parroquia): ").strip()
                if not parroquia:
                    print("La parroquia no puede estar vacía.")
                    time.sleep(2)
                    continue
                
                # Verifica si hay retiros asociados a la parroquia
                retiros_existen = bd_conections.verificar_id("Retiro", nombre=parroquia)
                if retiros_existen == 0:
                    print(f"No se encontraron retiros para la parroquia {parroquia}.")
                    time.sleep(2)
                    continue

                # Elimina el retiro por parroquia
                try:
                    resultado = bd_conections.llamar_procedimiento("EliminarRetiroPorParroquia", (parroquia,))
                    if resultado == "Proceso Exitoso":
                        print("\nRetiros eliminados exitosamente.")
                    else:
                        print(f"\nError: {resultado}")
                except Exception as e:
                    print(f"Error al eliminar retiros por parroquia: {e}")
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
        print("2. Nombre")
        print("3. Regresar")
        opc = int(input("Seleccione una opcion: "))
        
        match opc:
            case 1:
                utils.borrarPantalla()
                lista_donacion_id()
                try:
                    id = int(input("\nIngrese el ID de la donación: "))
                    # Verifica si la donación existe
                    donacion = bd_conections.visualizar_datos("donacion", "id_donacion", f"id_donacion={id}")
                    if not donacion:
                        print("No se encontró una donación con ese ID.")
                        time.sleep(2)
                        continue
                    
                    # eliminar por ID
                    bd_conections.llamar_procedimiento("EliminarDonacionPorID", (id,))
                    print("\nDonación eliminada correctamente.")
                except Exception as e:
                    print(f"Error al eliminar donación por ID: {e}")
                
                time.sleep(3)

            case 2:
                utils.borrarPantalla()
                lista_donacion_id()
                nombre = input("\nIngrese el nombre de la donación: ").strip()
                if not nombre:
                    print("El nombre no puede estar vacío.")
                    time.sleep(2)
                    continue

                # Verifica si la donación existe
                donacion = bd_conections.visualizar_datos("donacion", "id_donacion", f"nombre='{nombre}'")
                if not donacion:
                    print("No se encontró una donación con ese nombre.")
                    time.sleep(2)
                    continue

                # eliminar por nombre
                try:
                    bd_conections.llamar_procedimiento("EliminarDonacionPorNombre", (nombre,))
                    print("\nDonación eliminada correctamente.")
                except Exception as e:
                    print(f"Error al eliminar donación por nombre: {e}")
                
                time.sleep(3)

            case 3:
                break

            case _:
                print("Seleccione una opción válida.")
                time.sleep(3)



def listas_registros():
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

def lista_info_retiros():
    tabla = "retiro"
    columnas_df = ["id_retiro","Parroquia","Tipo","Fecha"]
    df = pd.DataFrame(bd_conections.visualizar_datos(tabla), columns=columnas_df).to_string(index=False)
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



def obtener_fecha():
    #Solicita al usuario una fecha en formato 'YYYY-MM-DD' y la valida.
    while True:
        fecha = input("Ingrese la fecha (YYYY-MM-DD): ").strip()

        if not fecha:
            print("Error: No ingresaste nada. Inténtalo de nuevo.")
            continue

        try:
            fecha_valida = datetime.strptime(fecha, "%Y-%m-%d").date()
            return fecha_valida
        except ValueError:
            print("Error: Formato incorrecto o fecha inválida. Inténtalo nuevamente.")