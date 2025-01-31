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
                ingresar_donacion()
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

def ingresar_donacion():
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

        # Determina si el pago pertenece a un participante o servidor
        while True:
            tipo_persona = input("¿El pago es realizado por un Participante (p) o un Servidor (s)? ").strip().lower()
            if tipo_persona in ('p', 's'):
                break
            print("Debe ingresar 'p' para Participante o 's' para Servidor.")

        lista_func = part.lista_participantes_id if tipo_persona == 'p' else serv.lista_servidor_id
        tabla_verificar = "ParticipantePorID" if tipo_persona == 'p' else "ServidorPorID"
        monto_maximo = 90 if tipo_persona == 'p' else 75
        id_persona = None

        # Se ingresa el id de la persona que va a realizar el pago
        while True:
            utils.borrarPantalla()
            lista_func()
            try:
                id_ingr = int(input("\nIngrese el ID de la persona que realizará el pago: "))
            except ValueError:
                print("Debe ingresar un número válido para el ID.")
                time.sleep(2)
                continue
            
            id_persona = bd_conections.verificar_id(tabla_verificar, id=id_ingr)
            if isinstance(id_persona, str):
                print(f"\n{id_persona}")
                time.sleep(5)
                continue
            
            if id_persona is not None:
                break
            print(f"El ID {id_ingr} no existe. Intente nuevamente.")
            time.sleep(2)

        # Se ingresa el id del retiro que se asocia al pago
        try:
            utils.borrarPantalla()
            lista_retiro_id()
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
        if id_retiro is None:
            print(f"El retiro con el ID {id_ingresado} no existe.")
            time.sleep(2)
            continue
        

        # Se ingresa el valor del pago
        while True:
            try:
                valor = float(input("Ingrese el valor del pago en $: "))
                if valor <= 0:
                    print("Error: El pago debe ser mayor a 0.")
                    time.sleep(2)
                    continue
                if valor > monto_maximo:
                    print(f"Error: El pago total no puede exceder ${monto_maximo}.")
                    time.sleep(2)
                    continue
                break
            except ValueError:
                print("Error: El monto debe ser un número.")
                time.sleep(2)
        
        pago_completado = (valor == monto_maximo)
        
        print("\nRegistrando pago...\n")
        time.sleep(2)
        utils.borrarPantalla()
        time.sleep(2)

        # Insertar pago en la base de datos
        bd_conections.llamar_procedimiento("InsertarPago", (valor, int(pago_completado), id_retiro, tipo_persona, id_persona))
        print("\nPago registrado correctamente.")
        time.sleep(2)
        return
     


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
            print("1. Actualizar Parroquia")
            print("2. Actualizar Tipo")
            print("3. Actualizar Fecha")
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

def actualizar_donacion():
    utils.borrarPantalla()
    print("\nActualizar Donación")
    # Valida que el ID sea un número válido
    try:
        lista_donacion_id()
        id_ingresado = int(input("Ingrese el ID de la donación que desea actualizar: "))
    except ValueError:
        print("El ID debe ser un número entero.")
        time.sleep(2)
        return
    
    # Verifica si el retiro existe
    id_donacion = bd_conections.verificar_id("DonacionPorID", id=id_ingresado)
    if isinstance(id_donacion, str):
        print(f"\n{id_donacion}")
        time.sleep(5)
        return
    
    if(id_donacion != None):
        tabla = "donacion"
        condicion = f"id_retiro={id_donacion}"
        actualizar_datos = [id_donacion,None, None, None, None]

        while True:
            utils.borrarPantalla()
            print("\nActualizar Donación")
            print("1. Actualizar Nombre")
            print("2. Actualizar Detalle")
            print("3. Actualizar Valor")
            print("4. Regresar")
            opc = int(input("Seleccione una opcion: "))
            match opc:
                case 1:
                    utils.borrarPantalla()
                    print("\nActualizar Nombre de la donación")
                    df_nom_ape = pd.DataFrame(
                    bd_conections.visualizar_datos(tabla,"id_donacion, nombre",condicion=condicion),
                    columns=["ID","Nombre"]).to_string(index=False)
                    print(df_nom_ape)

                    nombre = input("\nNombre: ")
                    actualizar_datos[1] = nombre

                    resultado = bd_conections.llamar_procedimiento("ActualizarDonacion",tuple(actualizar_datos))
                    if(resultado != "Proceso Exitoso"):
                        print(f"\n{resultado}")
                        time.sleep(5)
                    else:
                        time.sleep(2)

                case 2:
                    utils.borrarPantalla()
                    print("\nActualizar Detalle de la donación")
                    df_nom_ape = pd.DataFrame(
                    bd_conections.visualizar_datos(tabla,"id_donacion, nombre, detalle",condicion=condicion),
                    columns=["ID","Nombre","Detalle"]).to_string(index=False)
                    print(df_nom_ape)

                    detalle = input("\nDetalle: ")
                    actualizar_datos[2] = detalle

                    resultado = bd_conections.llamar_procedimiento("ActualizarDonacion",tuple(actualizar_datos))
                    if(resultado != "Proceso Exitoso"):
                        print(f"\n{resultado}")
                        time.sleep(5)
                    else:
                        time.sleep(2)

                case 3:
                    utils.borrarPantalla()
                    print("\nActualizar Valor de la donación")
                    df_nom_ape = pd.DataFrame(
                        bd_conections.visualizar_datos(tabla, "id_donacion, nombre, valor", condicion=condicion),
                        columns=["ID", "Nombre", "Valor"]).to_string(index=False)
                    print(df_nom_ape)

                    while True:
                        try:
                            valor_adicional = float(input("\nIngrese el valor adicional a la donación: "))
                            if valor_adicional <= 0:
                                print("El valor debe ser mayor que 0. Intente nuevamente.")
                                continue
                            break
                        except ValueError:
                            print("Debe ingresar un número válido para el valor adicional.")

                    # Se actualiza el valor sumando el valor adicional
                    actualizar_datos[3] = valor_adicional

                    resultado = bd_conections.llamar_procedimiento("ActualizarDonacion", tuple(actualizar_datos))
                    if resultado != "Proceso Exitoso":
                        print(f"\n{resultado}")
                        time.sleep(5)
                    else:
                        print("\nValor de la donación actualizado correctamente.")
                        time.sleep(2)


                case 4:
                    break
                case _:
                    print("Seleccione una opcion valida")
                    time.sleep(2)                   

    else:
        print(f"La donacion con el id {id_ingresado} no existe")
    time.sleep(2)

def actualizar_pago():
    while True:
        utils.borrarPantalla()
        print("\nActualizar Pago")

        # Determina si el pago a actualizar pertenece a un participante o servidor
        while True:
            tipo_persona = input("¿El pago es realizado por un Participante (p) o un Servidor (s)? ").strip().lower()
            if tipo_persona in ('p', 's'):
                break
            print("Debe ingresar 'p' para Participante o 's' para Servidor.")

        lista_func = part.lista_participantes_id if tipo_persona == 'p' else serv.lista_servidor_id
        tabla_verificar = "ParticipantePorID" if tipo_persona == 'p' else "ServidorPorID"
        monto_maximo = 90 if tipo_persona == 'p' else 75
        id_persona = None

        # Se ingresa el id de la persona que va a realizar el pago
        while True:
            utils.borrarPantalla()
            lista_func()
            try:
                id_ingr = int(input("\nIngrese el ID de la persona cuyo pago se va a actualizar: "))
            except ValueError:
                print("Debe ingresar un número válido para el ID.")
                time.sleep(2)
                continue
            
            id_persona = bd_conections.verificar_id(tabla_verificar, id=id_ingr)
            if isinstance(id_persona, str):
                print(f"\n{id_persona}")
                time.sleep(5)
                continue
            
            if id_persona is not None:
                break
            print(f"El ID {id_ingr} no existe. Intente nuevamente.")
            time.sleep(2)


        # Se ingresa el id del retiro que se asocia al pago
        while True:
            try:
                utils.borrarPantalla()
                lista_participanteXretiros(id_persona)
                id_ingresado = int(input("Ingrese el ID del retiro asociado al pago que se desea actualizar: "))
            except ValueError:
                print("Debe ingresar un número válido para el ID del retiro.")
                time.sleep(2)
                continue
            
            id_retiro = bd_conections.verificar_id("RetiroPorId", id=id_ingresado)
            if isinstance(id_retiro, str):
                print(f"\n{id_retiro}")
                time.sleep(5)
                continue
            
            if id_retiro is not None:
                break

            print(f"El retiro con el ID {id_ingresado} no existe. Intente nuevamente.")
            time.sleep(2)

        
        # Obtener el ID del pago
        while True:
            utils.borrarPantalla()
            lista_pagoXretiroXparticipante(id_persona, id_retiro)
            try:
                id_in = int(input("\nIngrese el ID del pago: "))
            except ValueError:
                print("Debe ingresar un número válido para el ID.")
                time.sleep(2)
                continue

            id_pago = bd_conections.verificar_id("PagoPorID", id=id_in)
            if isinstance(id_pago, str):
                print(f"\n{id_pago}")
                time.sleep(5)
                continue
            
            if id_pago is not None:
                break

            print(f"El ID {id_in} no existe. Intente nuevamente.")
            time.sleep(2)
        
        if id_pago is None:
            print("Error: No se pudo verificar el ID del pago. Intente de nuevo.")
            time.sleep(2)
            return
        
        # Obtener el valor actual del pago
        resultado = bd_conections.visualizar_datos(
            tabla="pago",
            columnas="valor",
            condicion=f"id_pago = {id_pago}"
        )
        if resultado and len(resultado) > 0:
            valor_actual = resultado[0][0]
        else:
            print("Error: No se pudo obtener el valor actual del pago.")
            time.sleep(2)
            return
        print(f"Valor actual del pago: ${valor_actual}")
    
        # Se ingresa los datos nuevos
        while True:
            try:
                nuevo_valor = float(input(f"Ingrese el nuevo valor del pago (máximo ${monto_maximo}): "))
                if nuevo_valor <= 0:
                    print("Error: El pago debe ser mayor a 0.")
                    time.sleep(2)
                    continue
                if (nuevo_valor + valor_actual) > monto_maximo:
                    print(f"Error: El pago total no puede exceder ${monto_maximo}.")
                    time.sleep(2)
                    continue
                
                valor_actual += nuevo_valor
                break

            except ValueError:
                print("Error: El monto debe ser un número.")
                time.sleep(2)
            
        pago_completado = (valor_actual == monto_maximo)

        print("\nActualizando pago...\n")
        time.sleep(2)
        utils.borrarPantalla()
        time.sleep(2)

        # Se actualiza el valor del pago
        bd_conections.llamar_procedimiento("ActualizarPago",  (valor_actual, int(pago_completado), id_retiro, tipo_persona, id_persona))
        print("\nPago actualizado correctamente.")
        time.sleep(2)
        return


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
    columnas = "id_pago, valor, pago_completado"
    df = pd.DataFrame(bd_conections.visualizar_datos(tabla,columnas),columns=["ID", "Valor", "Pago_Completado"])
    print("\n**Lista de Pagos**")
    print(df.to_string(index=False))
    print()

def lista_donacion_id():
    tabla = "donacion"
    columnas = "id_donacion, nombre, valor"
    df = pd.DataFrame(bd_conections.visualizar_datos(tabla,columnas),columns=["ID", "Nombre", "Valor"])
    print("\n**Lista de Donaciones**")
    print(df.to_string(index=False))

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


def lista_participanteXretiros(id_participante):
    vista = "view_participanteXretiros"
    columns_df= ["id_retiro", "parroquia", "tipo", "fecha"]
    columnas_str = ", ".join(columns_df)
    cond_df=  f"Id_Participante = {id_participante}"
    df = pd.DataFrame(bd_conections.visualizar_datos(tabla=vista, columnas=columnas_str, condicion=cond_df), columns=columns_df)
    print("\n**Lista de Retiros asociados al Participante ingresado**")
    print(df.to_string(index=False))
    print()

def lista_pagoXretiroXparticipante(id_participante, id_retiro):
    vista = "view_pagoXretiroXparticipante"
    columns_df = ["id_pago" ,"parroquia", "tipo", "fecha", "nombre", "apellido", "valor", "pago_completado"]
    columnas_str = ", ".join(columns_df)
    cond_df = f"Id_Retiro = {id_retiro} AND Id_Participante = {id_participante}"
    
    result = bd_conections.visualizar_datos(tabla=vista, columnas=columnas_str, condicion=cond_df)
    
    if result is None or len(result) == 0:
        print("\n**No se encontraron registros para el pago asociado al participante y el retiro.**")
        return

    df = pd.DataFrame(result, columns=columns_df)
    print("\n**Info del Pago asociado al participante y el retiro ingresado**")
    print(df.to_string(index=False))
    print()



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