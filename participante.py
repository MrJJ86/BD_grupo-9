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
        print("3. eliminar")
        print("4. Lista de Participantes")
        print("5. Regresar")
        opcion = int(input("Seleccione una opcion:"))
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
    id_familiar = bd_conections.verificar_id("Familiar",fam_nombre,fam_celular)
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
    
    id_familiar = bd_conections.verificar_id("Familiar",fam_nombre,fam_celular)

    #PARTICIPANTE
    datos_participante= (nombres,apellidos,email,tel_casa,celular,estado_civil,direccion,fecha_nac,edad,talla,id_familiar,parentesco)

    id_participante = bd_conections.verificar_id("Participante",nombres,apellidos)
    
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
        
        id_participante = bd_conections.verificar_id("Participante",nombres,apellidos)

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
                id_participante = int(input("\nIngrese el ID del participante a actualizar: "))
                try:
                    resultado = bd_conections.visualizar_datos("participante","nombre",f"id_participante={id_participante}")
                    if(len(resultado) != 0):
                        actualizar_participante(id_participante)
                    else:
                        print(f"El participante con el id {id_participante} no existe")

                except Exception as e:
                    print(f"Error al comprobar si existe participante en actualizar datos: {e}")

                time.sleep(3)

            case 2:
                utils.borrarPantalla()
                lista_familiares_id()
                id_familiar = int(input("\nIngrese el ID del familiar a actualizar: "))
                try:
                    resultado = bd_conections.visualizar_datos("familiar","nombre",f"id_familiar={id_familiar}")
                    if(len(resultado) != 0):
                        actualizar_familiar(id_familiar)
                    else:
                        print(f"El familiar con el id {id_familiar} no existe")

                except Exception as e:
                    print(f"Error al comprobar si existe participante en actualizar datos: {e}")

                time.sleep(3)

            case 3:
                break
            case _:
                print("Seleccione una opcion valida")
                time.sleep(3)



def actualizar_participante(id_participante):
    tabla = "participante"
    condicion = f"id_participante={id_participante}"
    df_participante = pd.DataFrame(bd_conections.visualizar_datos(tabla,condicion=condicion)).to_string(index=False)
    df_adicional = pd.DataFrame(bd_conections.visualizar_datos("informacionadicional",condicion=condicion)).to_string(index=False)
    df_sacramentos = pd.DataFrame(bd_conections.visualizar_datos("sacramentos",condicion=condicion)).to_string(index=False)
    df_familiar = pd.DataFrame(bd_conections.visualizar_datos("participante join familiar using(id_familiar)","id_participante, participante.nombre, participante.apellido, familiar.nombre, familiar.apellido",condicion)).to_string(index=False)
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
                print(df_participante)
                nombre = input("Nombre: ")
                apellido = input("Apellido: ")
                try:
                    bd_conections.actualizar_datos(tabla,["nombre","apellido"],condicion,{"nombre":nombre,"apellido":apellido})
                except Exception as e:
                    print(f"Error al actualizar Participante: {e}")

                time.sleep(2)

            case 2:
                utils.borrarPantalla()
                print("\nActualizar Fecha de Nacimiento y edad del Participante")
                print(df_participante)
                fecha_nac = ""
                if(input("Cambiar fecha de nacimiento? (y/n): ")=="y"):
                    fecha_nac = input("Fecha de nacimiento (YYYY-MM-DD): ")

                edad = int(input("Edad: "))

                try:
                    if(fecha_nac == ""):
                        bd_conections.actualizar_datos(tabla,["edad"],condicion,(edad))
                    else:
                        bd_conections.actualizar_datos(tabla,["fecha_nacimiento","edad"],condicion,{"fecha_nacimiento":fecha_nac,"edad":edad})

                except Exception as e:
                    print(f"Error al actualizar Participante: {e}")

                time.sleep(2)

            case 3:
                utils.borrarPantalla()
                print("\nActualizar Email y Celular del Participante")
                print(df_participante)

                tel_casa = input("Telefono del domicilio: ")
                celular = input("Celular: ")
                email=input("Email: ")

                try:
                    bd_conections.actualizar_datos(tabla,["email","telefono_casa","celular"],condicion,{"email":email,"telefono_casa":tel_casa,"celular":celular})
                except Exception as e:
                    print(f"Error al actualizar Participante: {e}")

                time.sleep(2)
                
            case 4:
                utils.borrarPantalla()
                print("\nActualizar Direccion de Domicilio del Participante")
                print(df_participante)

                direccion = input("Direccion de domicilio: ")

                try:
                    bd_conections.actualizar_datos(tabla,["direccion"],condicion,{"direccion":direccion})
                except Exception as e:
                    print(f"Error al actualizar Participante: {e}")

                time.sleep(2)
                
            case 5:
                utils.borrarPantalla()
                print("\nActualizar Estado civil del Participante")
                print(df_participante)

                print("Estado civil: ")
                for key,value in estados_civil.items():
                    print(f"{key}. {value}")
                
                estado_civil = estados_civil.get(int(input("Seleccione una opcion: ")), "null")

                try:
                    bd_conections.actualizar_datos(tabla,["estado_civil"],condicion,{"estado_civil":estado_civil})
                except Exception as e:
                    print(f"Error al actualizar Participante: {e}")

                time.sleep(2)
                
            case 6:
                utils.borrarPantalla()
                print("\nActualizar Talla de Camisa del Participante")
                print(df_participante)

                talla = input("Talla (S/M/L/XL/...): ")
                

                try:
                    bd_conections.actualizar_datos(tabla,["talla"],condicion,{"talla":talla})
                except Exception as e:
                    print(f"Error al actualizar Participante: {e}")

                time.sleep(2)
                
            case 7:
                utils.borrarPantalla()
                print("\nActualizar Informacion adicional del participante del Participante")
                print(df_adicional)
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

                observaciones = "null"
                if(input("Tiene alguna observacion sobre el participante? (y/n): ") == "y"):
                    observaciones = input("Observacion: ")

                try:
                    bd_conections.actualizar_datos("informacionadicional",["fuma","ronca","dieta","medicamento","limitaciones_fisicas","observaciones"],condicion,{"fuma":fuma,"ronca":ronca,"dieta":dieta,"medicamento":medicamento,"limitaciones_fisicas":limit_fisica,"observaciones":observaciones})
                except Exception as e:
                    print(f"Error al actualizar Participante: {e}")

                time.sleep(2)
                
            case 8:
                utils.borrarPantalla()
                print("\nActualizar Sacramentos del Participante")
                print(df_sacramentos)

                bautismo = 1 if (input("Esta Bautizado? (y/n): ") == "y") else 0
                comunion = 1 if (input("Hizo la Primera Comunion? (y/n): ") == "y") else 0
                confirmacion = 1 if (input("Hizo la Confirmacion? (y/n): ") == "y") else 0
                matrimonio = 1 if (input("Se caso por la iglesia? (y/n): ") == "y") else 0

                try:
                    bd_conections.actualizar_datos("sacramentos",["hizoBautismo","hizoEucarestia","hizoConfirmacion","hizoMatrimonio"],condicion,{"hizoBautismo":bautismo,"hizoEucarestia":comunion,"hizoConfirmacion":confirmacion,"hizoMatrimonio":matrimonio})
                except Exception as e:
                    print(f"Error al actualizar Participante: {e}")
                time.sleep(2)
                
            case 9:
                utils.borrarPantalla()
                print("\nActualizar Familiar y Parentesco del Participante")
                print(df_familiar)

                id_familiar = -1
                if(input("Cambiar el familiar? (y/n): ")=="y"):
                    lista_familiares_id()
                    id_familiar = int(input("Seleccione el ID del nuevo familiar: "))
                    parentesco = input("Parentesco: ")
                
                parentesco = ""
                if(input("Cambiar parentesco del familiar? (y/n): ")=="y"):
                    parentesco = input("Parentesco: ")

                try:
                    if(id_familiar >= 0):
                        bd_conections.actualizar_datos(tabla,["id_familiar","parentesco"],condicion,(id_familiar,parentesco))
                    else:
                        if(parentesco != ""):
                            bd_conections.actualizar_datos(tabla,["parentesco"],condicion,(parentesco))
                except Exception as e:
                    print(f"Error al actualizar Participante: {e}")

                time.sleep(2)
                
            case 10:
                break
            case _:
                print("Seleccione una opcion valida")
                time.sleep(2)



def actualizar_familiar(id_familiar):
    tabla = "familiar"
    condicion = f"id_familiar={id_familiar}"
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
                nombre = input("Nombre: ")
                apellido = input("Apellido: ")
                try:
                    bd_conections.actualizar_datos(tabla,["nombre","apellido"],condicion,(nombre,apellido))
                except Exception as e:
                    print(f"Error al actualizar familiar: {e}")

                time.sleep(2)

            case 2:
                utils.borrarPantalla()
                print("\nActualizar Nombres y Apellidos del Familiar")
                email = "null"
                if(input("El familiar tiene email? (y/n): ")=="y"):
                    email = input("Email: ")

                celular = input("Celular: ")
                try:
                    bd_conections.actualizar_datos(tabla,["email","celular"],condicion,(email,celular))
                except Exception as e:
                    print(f"Error al actualizar familiar: {e}")

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
                condicion = f"id_participante={id}"
                try:
                    bd_conections.eliminar_datos("participante",condicion)
                    print("\nParticipante Eliminado")
                except Exception as e:
                    print(f"Error al eliminar participante por ID: {e}")
                    
                time.sleep(3)
            case 2:
                utils.borrarPantalla()
                lista_participantes_id()
                nombre = input("\nIngrese el nombre del participante: ")
                apellido = input("Ingrese el apellido del participante: ")
                condicion = f"nombre=\"{nombre}\" and apellido=\"{apellido}\""
                try:
                    bd_conections.eliminar_datos("participante",condicion)
                    print("\nParticipante Eliminado")
                except Exception as e:
                    print(f"Error al eliminar participante por Nombre y Apellido: {e}")
                
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
                condicion = f"id_familiar={id}"
                try:
                    bd_conections.eliminar_datos("familiar",condicion)
                    print("\nFamiliar Eliminado")
                except Exception as e:
                    print(f"Error al eliminar familiar por ID: {e}")

                time.sleep(3)

            case 2:
                utils.borrarPantalla()
                lista_familiares_id()
                nombre = input("\nIngrese el nombre del familiar: ")
                apellido = input("Ingrese el apellido del familiar: ")
                condicion = f"nombre=\"{nombre}\" and apellido=\"{apellido}\""
                try:
                    bd_conections.eliminar_datos("familiar",condicion)
                    print("\nFamiliar Eliminado")
                except Exception as e:
                    print(f"Error al eliminar familiar por Nombre y Apellido: {e}")

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
        print("3. Familiares de cada Participante")
        print("4. Participantes por Retiro")
        print("5. Regresar")
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
                lista_familiares_por_participante()
                input("Presione una Tecla para Regresar")
                time.sleep(2)
            case 4:
                utils.borrarPantalla()
                lista_participantes_por_retiro()
                input("Presione una Tecla para Regresar")
                time.sleep(2)
            case 5:
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
