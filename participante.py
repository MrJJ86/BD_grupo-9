import utils
import bd_conections
import pandas as pd
from datetime import date
import time

estados_civil = {
    1:"Soltero/a",
    2:"Casado/a",
    3:"Divorciado/a",
    4:"Union Libre",
    5:"Viudo/a",
}

def participante():
    es_volver = False
    while not es_volver:
        utils.borrarPantalla()
        print("\nMenu Participantes")
        print("1. Registrar")
        print("2. Actualizar")
        print("3. Eliminar")
        print("4. Lista de Participantes")
        print("5. Regresar")
        opcion = int(input("Seleccione una opcion: "))
        match opcion:
            case 1:
                ingresar_participante()
            case 2:
                actualizar()
            case 3:
                eliminar()
            case 4:
                listas()
            case 5:
                es_volver =  True
            case _:
                print("\nIngrese una opcion valida")
                time.sleep(3)

def ingresar_participante():
    utils.borrarPantalla()
    print("\nIngresar Participante")
    nombres = input("\nNombres: ")
    apellidos = input("Apellidos: ")

    email = "null"
    if(input("Tiene email? (y/n): ") == "y"):
        email = input("Email: ")

    tel_casa = "null"
    if input("Tiene numero de telefono para la casa? (y/n): ") == "y":
        tel_casa = input("Telefono de la casa: ")
    celular = "null"
    if input("Tiene numero celular? (y/n): ") == "y":
        celular = input("Celular: ")
    
    print("Estado civil: ")
    for key,value in estados_civil.items():
        print(f"{key}. {value}")
    
    estado_civil = estados_civil.get(int(input("Seleccione una opcion: ")), "null")

    direccion = input("Direccion del Domicilio: ")
    fecha_nac = input("Fecha de Nacimiento (YYYY-MM-DD): ")
    edad = date.today().year - date.fromisoformat(fecha_nac).year
    talla = input("Talla de camisa (S/M/L/XL/...): ")
    fuma = 1 if (input("El participante fuma? (y/n): ") == "y") else 0
    ronca = 1 if (input("El participante Ronca? (y/n): ") == "y") else 0
    
    dieta = "null"
    if(input("Tiene dieta? (y/n): ") == "y"):
        dieta = input("Dieta: ")

    medicamento = "null"
    if(input("Tiene alguna medicacion? (y/n): ") == "y"):
        medicamento = input("Medicacion: ")

    limit_fisica = "null"
    if(input("Tiene limitaciones fisicas? (y/n): ") == "y"):
        limit_fisica = input("Limitiaciones fisicas: ")
    
    estudia = 1 if (input("El participante estudia? (y/n): ") == "y") else 0
    lugar_estudio = "null"
    if estudia == 1:
        lugar_estudio = input("Lugar de estudio: ")

    trabaja = 1 if (input("El participante trabaja? (y/n): ") == "y") else 0
    lugar_trabajo = "null"
    if(trabaja == 1):
        lugar_trabajo = input("Lugar de trabajo: ")
    
    bautismo = 1 if (input("Esta Bautizado? (y/n): ") == "y") else 0
    comunion = 1 if (input("Hizo la Primera Comunion? (y/n): ") == "y") else 0
    confirmacion = 1 if (input("Hizo la Confirmacion? (y/n): ") == "y") else 0
    
    matrimonio = 1 if (
        (estado_civil == estados_civil.get(2) or estado_civil == estados_civil.get(5))
        and input("Se caso por la iglesia? (y/n): ") == "y"
        ) else 0

    print("Familiar del Participante")
    fam_nombre = input("Nombre del Familiar: ")
    fam_apellido = input("Apellido del Familiar: ")
    parentesco = input("Parentesco con el Familiar: ")

    fam_email = "null"
    if( input("El Familiar tiene email? (y/n): ") == "y"):
        fam_email = input("Email del Familiar: ")

    fam_celular = input("Celular del Familiar: ")

    observaciones = "null"
    if(input("Tiene alguna observacion sobre el participante? (y/n): ") == "y"):
        observaciones = input("Observacion: ")
    
    utils.borrarPantalla()
    time.sleep(2)
    print("\nRegistrando Participante...\n")
    utils.borrarPantalla()
    time.sleep(2)

    #Seccion de SQL
    
    #TABLA FAMILIAR
    id_familiar = bd_conections.verificar_id("FamiliarPorNombreApellido",nombre=fam_nombre,apellido=fam_apellido)
    datos_familiar = (fam_nombre, fam_apellido, fam_email, fam_celular)
    
    # Por si falla la verificación del ID
    if(isinstance(id_familiar, str)):
        print(f"\n{id_familiar}")
        time.sleep(5)
        return None # Salir de la función por el error producido

    # Insertar Familiar
    if id_familiar == None:
        resultado_familiar = bd_conections.llamar_procedimiento("InsertarFamiliar", datos_familiar)
        if resultado_familiar == "Proceso Exitoso":
            print("\nFamiliar Registrado")
        else:
            print(f"\n{resultado_familiar}")
            time.sleep(5)
            return None # Salir de la función por el error producido
    
    id_familiar = bd_conections.verificar_id("FamiliarPorNombreApellido",nombre=fam_nombre,apellido=fam_apellido)

    #PARTICIPANTE
    datos_participante= (nombres,apellidos,email,tel_casa,celular,estado_civil,direccion,fecha_nac,edad,talla,id_familiar,parentesco)

    id_participante = bd_conections.verificar_id("ParticipantePorNombreApellido",nombre=nombres,apellido=apellidos)
    
    # Por si falla la verificación del ID
    if(isinstance(id_participante, str)):
        print(f"\n{id_participante}")
        time.sleep(5)
        return None # Salir de la función por el error producido

    if id_participante == None:
        #TABLA PARTICIPANTE
        resultado_participante = bd_conections.llamar_procedimiento("InsertarParticipante",datos_participante)
        if resultado_participante != "Proceso Exitoso":
            print(f"\n{resultado_participante}")
            time.sleep(5)
            return None # Salir de la función por el error producido
        
        id_participante = bd_conections.verificar_id("ParticipantePorNombreApellido",nombre=nombres,apellido=apellidos)

        #TABLA INFORMACION ADICIONAL
        datos_adicional= (id_participante,fuma,ronca,dieta,medicamento,limit_fisica,observaciones)
        resultado_info_adi = bd_conections.llamar_procedimiento("InsertarInformacionAdicional",datos_adicional)
        
        if resultado_info_adi != "Proceso Exitoso":
            print(f"\n{resultado_info_adi}")
        
        #TABLA ACTIVIDAD PARTICIPANTE
        
        datos_actividad= (id_participante,estudia,trabaja,lugar_estudio,lugar_trabajo)
        resultado_actividad = bd_conections.llamar_procedimiento("InsertarActividadParticipante",datos_actividad)
        
        if resultado_actividad != "Proceso Exitoso":
            print(f"\n{resultado_actividad}")
        
        #TABLA SACRAMENTOS
        datos_sacramentos= (id_participante,bautismo,comunion,confirmacion,matrimonio)
        resultado_sacramento = bd_conections.llamar_procedimiento("InsertarSacramentos",datos_sacramentos)

        if resultado_sacramento != "Proceso Exitoso":
            print(f"\n{resultado_sacramento}")
        
        print("\nParticipante Registrado")
        
    else:
        print("El participante ya esta registrado")
    
    time.sleep(3)

def actualizar():
    while True:
        utils.borrarPantalla()
        print("\nActualizar Registro")
        print("1. Participante")
        print("2. Familiar")
        print("3. Regresar")
        opc = int(input("Seleccione una opcion: "))
        match opc:
            case 1:
                utils.borrarPantalla()
                lista_participantes_id()
                id_ingresado = int(input("\nIngrese el ID del participante a actualizar: "))

                id_participante = bd_conections.verificar_id("ParticipantePorID",id=id_ingresado)

                # Por si falla la verificación del ID
                if(isinstance(id_participante, str)):
                    print(f"\n{id_participante}")
                    time.sleep(5)
                    continue
                
                if(id_participante != None):
                    actualizar_participante(id_ingresado)
                else:
                    print(f"El participante con el id {id_ingresado} no existe")

                time.sleep(3)

            case 2:
                utils.borrarPantalla()
                lista_familiares_id()
                id_ingresado = int(input("\nIngrese el ID del familiar a actualizar: "))

                id_familiar = bd_conections.verificar_id("FamiliarPorID", id=id_ingresado)
                
                # Por si falla la verificación del ID
                if(isinstance(id_familiar, str)):
                    print(f"\n{id_familiar}")
                    time.sleep(5)
                    continue
                
                if(id_familiar != None):
                    actualizar_familiar(id_ingresado)
                else:
                    print(f"El familiar con el id {id_ingresado} no existe")

                time.sleep(3)

            case 3:
                break
            case _:
                print("Seleccione una opcion valida")
                time.sleep(3)



def actualizar_participante(id_participante):
    tabla = "participante"
    condicion = f"id_participante={id_participante}"

    actualizar_datos = [id_participante,None, None, None, None, None, None, None, None, None, None, None, None, None, None]

    while True:
        utils.borrarPantalla()
        print("\nActualizar Participante")
        print("1. Nombres y Apellidos")
        print("2. Fecha de Nacimiento y edad")
        print("3. Email y Celular")
        print("4. Direccion Domicilio")
        print("5. Estado Civil")
        print("6. Talla de Camisa")
        print("7. Informacion Adicional")
        print("8. Sacramentos")
        print("9. Familiar y Parentesco")
        print("10. Regresar")
        opc = int(input("Seleccione una opcion: "))
        match opc:
            case 1:
                utils.borrarPantalla()
                print("\nActualizar Nombres y Apellidos del Participante")
                df_nom_ape = pd.DataFrame(
                    bd_conections.visualizar_datos(tabla,"id_participante, nombre, apellido",condicion=condicion),
                    columns=["ID","Nombre","Apellido"]).to_string(index=False)
                print(df_nom_ape)

                nombre = input("\nNombre: ")
                apellido = input("Apellido: ")

                actualizar_datos[1] = nombre
                actualizar_datos[2] = apellido
                resultado = bd_conections.llamar_procedimiento("ActualizarParticipante",tuple(actualizar_datos))

                if(resultado != "Proceso Exitoso"):
                    print(f"\n{resultado}")
                    time.sleep(5)
                else:
                    time.sleep(2)

            case 2:
                utils.borrarPantalla()
                print("\nActualizar Fecha de Nacimiento y edad del Participante")
                df_fecha_edad = pd.DataFrame(
                    bd_conections.visualizar_datos(tabla,"nombre, apellido, fecha_nacimiento, edad",condicion=condicion),
                    columns=["nombre","Apellido","fecha de nacimiento","edad"]).to_string(index=False)
                print(df_fecha_edad)

                fecha_nac = ""
                if(input("\nCambiar fecha de nacimiento? (y/n): ")=="y"):
                    fecha_nac = input("Fecha de nacimiento (YYYY-MM-DD): ")

                edad = int(input("Edad: "))

                resultado = ""
                if(fecha_nac == ""):
                    actualizar_datos[9] = edad
                    resultado = bd_conections.llamar_procedimiento("ActualizarParticipante",tuple(actualizar_datos))
                else:
                    actualizar_datos[8] = fecha_nac
                    actualizar_datos[9] = edad
                    resultado = bd_conections.llamar_procedimiento("ActualizarParticipante",tuple(actualizar_datos))

                if(resultado != "Proceso Exitoso"):
                    print(f"\n{resultado}")
                    time.sleep(5)
                else:
                    time.sleep(2)

            case 3:
                utils.borrarPantalla()
                print("\nActualizar Email y Celular del Participante")
                df_email_cel = pd.DataFrame(
                    bd_conections.visualizar_datos(tabla,"nombre, apellido, email, telefono_casa, celular",condicion=condicion),
                    columns=["nombre","Apellido","email","telefono domicilio","celular"]).to_string(index=False)
                print(df_email_cel)

                tel_casa = input("\nTelefono del domicilio: ")
                celular = input("Celular: ")
                email=input("Email: ")

                actualizar_datos[3] = email
                actualizar_datos[4] = tel_casa
                actualizar_datos[5] = celular

                resultado = bd_conections.llamar_procedimiento("ActualizarParticipante",tuple(actualizar_datos))

                if(resultado != "Proceso Exitoso"):
                    print(f"\n{resultado}")
                    time.sleep(5)
                else:
                    time.sleep(2)
                
            case 4:
                utils.borrarPantalla()
                print("\nActualizar Direccion de Domicilio del Participante")
                df_direccion = pd.DataFrame(
                    bd_conections.visualizar_datos(tabla,"nombre, apellido, direccion",condicion=condicion),
                    columns=["nombre","Apellido","direccion"]).to_string(index=False)
                print(df_direccion)

                direccion = input("\nDireccion de domicilio: ")

                actualizar_datos[7] = direccion
                
                resultado = bd_conections.llamar_procedimiento("ActualizarParticipante",tuple(actualizar_datos))

                if(resultado != "Proceso Exitoso"):
                    print(f"\n{resultado}")
                    time.sleep(5)
                else:
                    time.sleep(2)
                
            case 5:
                utils.borrarPantalla()
                print("\nActualizar Estado civil del Participante")
                df_civil = pd.DataFrame(
                    bd_conections.visualizar_datos(tabla,"nombre, apellido, estado_civil",condicion=condicion),
                    columns=["nombre","Apellido","estado civil"]).to_string(index=False)
                print(df_civil)

                print("\nEstado civil: ")
                for key,value in estados_civil.items():
                    print(f"{key}. {value}")
                
                estado_civil = estados_civil.get(int(input("Seleccione una opcion: ")), None)

                actualizar_datos[6] = estado_civil
                
                resultado = bd_conections.llamar_procedimiento("ActualizarParticipante",tuple(actualizar_datos))

                if(resultado != "Proceso Exitoso"):
                    print(f"\n{resultado}")
                    time.sleep(5)
                else:
                    time.sleep(2)
                
            case 6:
                utils.borrarPantalla()
                print("\nActualizar Talla de Camisa del Participante")
                df_talla = pd.DataFrame(
                    bd_conections.visualizar_datos(tabla,"nombre, apellido, talla",condicion=condicion),
                    columns=["nombre","Apellido","talla de camisa"]).to_string(index=False)
                print(df_talla)

                talla = input("\nTalla (S/M/L/XL/...): ")
                
                actualizar_datos[10] = talla
                
                resultado = bd_conections.llamar_procedimiento("ActualizarParticipante",tuple(actualizar_datos))

                if(resultado != "Proceso Exitoso"):
                    print(f"\n{resultado}")
                    time.sleep(5)
                else:
                    time.sleep(2)
                
            case 7:
                utils.borrarPantalla()
                print("\nActualizar Informacion adicional del participante del Participante")
                df_adicional = pd.DataFrame(
                    bd_conections.visualizar_datos("informacionadicional",condicion=condicion),
                    columns=["ID","fuma","ronca","dieta","medicacion","limitacion fisica","observaciones"])
                if(df_adicional.empty):
                    print("\nEl participante no tiene asociado ninguna informacion adicional")
                else:
                    print(df_adicional.to_string(index=False))

                if(df_adicional.empty):
                    print("\nAgregue la informacion adicional del participante: ")
                
                fuma = 1 if (input("\nEl participante fuma? (y/n): ") == "y") else 0
                ronca = 1 if (input("El participante Ronca? (y/n): ") == "y") else 0
                
                dieta = "null"
                if(input("Tiene dieta? (y/n): ") == "y"):
                    dieta = input("Dieta: ")

                medicamento = "null"
                if(input("Tiene alguna medicacion? (y/n): ") == "y"):
                    medicamento = input("Medicacion: ")

                limit_fisica = "null"
                if(input("Tiene limitaciones fisicas? (y/n): ") == "y"):
                    limit_fisica = input("Limitiaciones fisicas: ")

                observaciones = "null"
                if(input("Tiene alguna observacion sobre el participante? (y/n): ") == "y"):
                    observaciones = input("Observacion: ")

                datos_adicional = (id_participante, fuma, ronca, dieta, medicamento, limit_fisica, observaciones)
                resultado = ""
                if(df_adicional.empty):
                    resultado = bd_conections.llamar_procedimiento("InsertarInformacionAdicional", datos_adicional)
                else:
                    resultado = bd_conections.llamar_procedimiento("ActualizarInformacionAdicional", datos_adicional)

                if(resultado != "Proceso Exitoso"):
                    print(f"\n{resultado}")
                    time.sleep(5)
                else:
                    time.sleep(2)
                
            case 8:
                utils.borrarPantalla()
                print("\nActualizar Sacramentos del Participante")
                df_sacramentos = pd.DataFrame(
                    bd_conections.visualizar_datos("sacramentos",condicion=condicion),
                    columns=["ID","bautismo","eucaristia","confirmacion","matrimonio"])
                if(df_sacramentos.empty):
                    print("\nEl participante no tiene asociado ningun registro de sacramentos")
                else:
                    print(df_sacramentos.to_string(index=False))

                if(df_sacramentos.empty):
                    print("\nAgregue los sacramentos del participante: ")

                bautismo = 1 if (input("\nEsta Bautizado? (y/n): ") == "y") else 0
                comunion = 1 if (input("Hizo la Primera Comunion? (y/n): ") == "y") else 0
                confirmacion = 1 if (input("Hizo la Confirmacion? (y/n): ") == "y") else 0
                matrimonio = 1 if (input("Se caso por la iglesia? (y/n): ") == "y") else 0

                datos_sacramentos= (id_participante,bautismo,comunion,confirmacion,matrimonio)
                resultado = ""
                if(df_sacramentos.empty):
                    resultado = bd_conections.llamar_procedimiento("InsertarSacramentos",datos_sacramentos)
                else:
                    resultado = bd_conections.llamar_procedimiento("ActualizarSacramentos", datos_sacramentos)

                if(resultado != "Proceso Exitoso"):
                    print(f"\n{resultado}")
                    time.sleep(5)
                else:
                    time.sleep(2)
                
            case 9:
                utils.borrarPantalla()
                print("\nActualizar Familiar y Parentesco del Participante")
                df_familiar = pd.DataFrame(
                    bd_conections.visualizar_datos(
                    "participante join familiar using(id_familiar)",
                    "id_participante, participante.nombre, participante.apellido, familiar.nombre, familiar.apellido",
                    condicion),
                    columns=["ID","nombre Participante","apellido participante","nombre familiar","apellido familiar"])
                if(df_familiar.empty):
                    print("\nEl participante no tiene ningun familiar asignado")
                else:
                    print(df_familiar.to_string(index=False))

                id_familiar = -1
                parentesco = ""
                if(input("Cambiar el familiar? (y/n): ")=="y"):
                    lista_familiares_id()
                    id_familiar = int(input("Seleccione el ID del nuevo familiar: "))
                    parentesco = input("Parentesco: ")
                
                if(id_familiar < 0 and input("Cambiar parentesco del familiar? (y/n): ")=="y"):
                    parentesco = input("Parentesco: ")

                if(id_familiar > 0):
                    actualizar_datos[11] = id_familiar
                    actualizar_datos[12] = parentesco
                else:
                    if(parentesco != ""):
                        actualizar_datos[12] = parentesco
                
                if(id_familiar >= 0 or parentesco != ""):
                    resultado = bd_conections.llamar_procedimiento("ActualizarParticipante",tuple(actualizar_datos))

                    if(resultado != "Proceso Exitoso"):
                        print(f"\n{resultado}")
                        time.sleep(5)
                    else:
                        time.sleep(2)
                
            case 10:
                break
            case _:
                print("Seleccione una opcion valida")
                time.sleep(2)



def actualizar_familiar(id_familiar):
    tabla = "familiar"
    condicion = f"id_familiar={id_familiar}"
    actualizar_datos = [id_familiar, None, None, None, None]
    while True:
        utils.borrarPantalla()
        print("\nActualizar Familiares")
        print("1. Nombres y Apellidos")
        print("2. Email y Celular")
        print("3. Regresar")
        opc = int(input("Seleccione una opcion: "))
        match opc:
            case 1:
                utils.borrarPantalla()
                print("\nActualizar Nombres y Apellidos del Familiar")
                df_nom_ape = pd.DataFrame(
                    bd_conections.visualizar_datos(tabla,"id_familiar, nombre, apellido",condicion=condicion),
                    columns=["ID","nombre","apellido"]).to_string(index=False)
                print(df_nom_ape)

                nombre = input("\nNombre: ")
                apellido = input("Apellido: ")

                actualizar_datos[1] = nombre
                actualizar_datos[2] = apellido
                
                resultado = bd_conections.llamar_procedimiento("ActualizarFamiliar",tuple(actualizar_datos))

                if(resultado != "Proceso Exitoso"):
                    print(f"\n{resultado}")
                    time.sleep(5)
                else:
                    time.sleep(2)

            case 2:
                utils.borrarPantalla()
                print("\nActualizar Email y Celular del Familiar")
                df_email_cel = pd.DataFrame(
                    bd_conections.visualizar_datos(tabla,"nombre, apellido, email, celular",condicion=condicion),
                    columns=["nombre","apellido","email","celular"]).to_string(index=False)
                print(df_email_cel)

                email = None
                if(input("El familiar tiene email? (y/n): ")=="y"):
                    email = input("Email: ")

                celular = input("Celular: ")

                actualizar_datos[3] = email
                actualizar_datos[4] = celular
                
                resultado = bd_conections.llamar_procedimiento("ActualizarFamiliar",tuple(actualizar_datos))

                if(resultado != "Proceso Exitoso"):
                    print(f"\n{resultado}")
                    time.sleep(5)
                else:
                    time.sleep(2)

            case 3:
                break
            case _:
                print("Seleccione una opcion valida")
                time.sleep(2)


def eliminar():
    while True:
        utils.borrarPantalla()
        print("\nEliminar Registro")
        print("1. Participante")
        print("2. Familiar")
        print("3. Regresar")
        opc = int(input("Seleccione una opcion: "))
        match opc:
            case 1:
                eliminar_participante()
            case 2:
                eliminar_familiar()
            case 3:
                break
            case _:
                print("Seleccione una opcion valida")
                time.sleep(3)


def eliminar_participante():
    while True:
        utils.borrarPantalla()
        print("\nEliminar Participante por")
        print("1. ID")
        print("2. Nombre y Apellido")
        print("3. Regresar")
        opc = int(input("Seleccione una opcion: "))
        match opc:
            case 1:
                utils.borrarPantalla()
                lista_participantes_id()
                id = int(input("\nIngrese el id del participante: "))

                resultado = bd_conections.llamar_procedimiento("EliminarParticipantePorID",tuple([id]))

                if(resultado != "Proceso Exitoso"):
                    print(f"\n{resultado}")
                    time.sleep(5)
                else:
                    print("Participante Eliminado")
                    time.sleep(3)
                
            case 2:
                utils.borrarPantalla()
                lista_participantes_id()
                nombre = input("\nIngrese el nombre del participante: ")
                apellido = input("Ingrese el apellido del participante: ")
                
                resultado = bd_conections.llamar_procedimiento("EliminarParticipantePorNombreApellido",(nombre, apellido))

                if(resultado != "Proceso Exitoso"):
                    print(f"\n{resultado}")
                    time.sleep(5)
                else:
                    print("Participante Eliminado")
                    time.sleep(3)
                
            case 3:
                break
            case _:
                print("Seleccione una opcion valida")
                time.sleep(3)


def eliminar_familiar():
    while True:
        utils.borrarPantalla()
        print("\nEliminar Familiar por")
        print("1. ID")
        print("2. Nombre y Apellido")
        print("3. Regresar")
        opc = int(input("Seleccione una opcion: "))
        match opc:
            case 1:
                utils.borrarPantalla()
                lista_familiares_id()
                id = int(input("\nIngrese el id del familiar: "))
                
                resultado = bd_conections.llamar_procedimiento("EliminarFamiliarPorID",tuple([id]))

                if(resultado != "Proceso Exitoso"):
                    print(f"\n{resultado}")
                    time.sleep(5)
                else:
                    print("Familiar Eliminado")
                    time.sleep(3)

            case 2:
                utils.borrarPantalla()
                lista_familiares_id()
                nombre = input("\nIngrese el nombre del familiar: ")
                apellido = input("Ingrese el apellido del familiar: ")
                
                resultado = bd_conections.llamar_procedimiento("EliminarFamiliarPorNombreApellido",(nombre, apellido))

                if(resultado != "Proceso Exitoso"):
                    print(f"\n{resultado}")
                    time.sleep(5)
                else:
                    print("Familiar Eliminado")
                    time.sleep(3)

            case 3:
                break
            case _:
                print("Seleccione una opcion valida")
                time.sleep(3)


def lista_participantes_id():
    vista = "view_participanteID"
    df = pd.DataFrame(bd_conections.visualizar_datos(vista),columns=["ID", "nombre", "apellido"])
    print("\n**Lista de Participante**")
    print(df.to_string(index=False))
    print()

def lista_familiares_id():
    vista = "view_familiarID"
    df = pd.DataFrame(bd_conections.visualizar_datos(vista),columns=["ID", "nombre", "apellido"])
    print("\n**Lista de Familiares**")
    print(df.to_string(index=False))
    print()

def listas():
    while True:
        utils.borrarPantalla()
        print("\nListas")
        print("1. Info Principal del Participante")
        print("2. Info Adicional del participante")
        print("3. Info de los Familiares")
        print("4. Familiares de cada Participante")
        print("5. Participantes por Retiro")
        print("6. Regresar")
        opc = int(input("Seleccione una opcion: "))
        match opc:
            case 1:
                utils.borrarPantalla()
                lista_info_principal_participante()
                input("Presione una Tecla para Regresar")
                time.sleep(2)
            case 2:
                utils.borrarPantalla()
                lista_info_adicional_participante()
                input("Presione una Tecla para Regresar")
                time.sleep(2)
            case 3:
                utils.borrarPantalla()
                lista_info_familiares()
                input("Presione una Tecla para Regresar")
                time.sleep(2)
            case 4:
                utils.borrarPantalla()
                lista_familiares_por_participante()
                input("Presione una Tecla para Regresar")
                time.sleep(2)
            case 5:
                utils.borrarPantalla()
                lista_participantes_por_retiro()
                input("Presione una Tecla para Regresar")
                time.sleep(2)
            case 6:
                break
            case _:
                print("Seleccione una opcion valida")
                time.sleep(2)

def lista_info_principal_participante():
    vista = "view_infoPrincipalParticipante"
    columnas_df = ["ID_Participante","nombre","apellido","email","telefono_casa","celular","estado_civil","direccion","fecha_nacimiento","edad","talla"]
    df = pd.DataFrame(bd_conections.visualizar_datos(vista), columns=columnas_df).to_string(index=False)
    print(df)


def lista_info_adicional_participante():
    vista = "view_infoAdicionalParticipante"
    columnas_df = ["ID_Participante","nombre","apellido","fuma","ronca","dieta","medicamento","limitaciones_fisicas","observaciones","estudia","trabaja","lugar_estudio","lugar_trabajo","hizoBautismo","hizoEucarestia","hizoConfirmacion","hizoMatrimonio"]
    df = pd.DataFrame(bd_conections.visualizar_datos(vista), columns=columnas_df).to_string(index=False)
    print(df)

def lista_info_familiares():
    tabla = "familiar"
    columnas_df = ["ID_Familiar","nombre","apellido","email","celular"]
    df = pd.DataFrame(bd_conections.visualizar_datos(tabla), columns=columnas_df).to_string(index=False)
    print(df)

def lista_familiares_por_participante():
    vista = "view_participantesFamiliares"
    columnas_df = ["ID_Participante","nombre","apellido","parentesco","nombre familiar","apellido familiar","email familiar","celular familiar"]
    df = pd.DataFrame(bd_conections.visualizar_datos(vista), columns=columnas_df).to_string(index=False)
    print(df)


def lista_participantes_por_retiro():
    vista = "view_participanteRetiro"
    columnas_df = ["ID_Retiro","parroquia","tipo","fecha","nombre participante","apellido participante"]
    df = pd.DataFrame(bd_conections.visualizar_datos(vista), columns=columnas_df).to_string(index=False)
    print(df)
