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
    try:
        cond_fam = f"nombre=\"{fam_nombre}\"" + " and " + f"apellido=\"{fam_apellido}\""
        familiarBD = bd_conections.visualizar_datos("familiar","id_familiar", cond_fam)
    except Exception as e:
        print(f"Error al visualizar datos del familiar: {e}")

    datos_familiar= {'nombre': fam_nombre, 'apellido': fam_apellido, 'email': fam_email, 'celular': fam_celular}

    id_familiar = 0
    if len(familiarBD) == 0:
        try:
            campos_familiar = ["nombre","apellido","email","celular"]
            bd_conections.insertar_datos("familiar",campos_familiar,datos_familiar)
            id_familiar = bd_conections.visualizar_datos("familiar","id_familiar", cond_fam).pop()
            print("\nFamiliar Registrado")
        except Exception as e:
            print(f"Error al insertar datos de familiar: {e}")
        
    else:
        id_familiar = familiarBD.pop()

    datos_participante= {'nombre': nombres, 'apellido': apellidos, 'email': email, 'telefono_casa': tel_casa, 'celular': celular, 'estado_civil': estado_civil, 'direccion': direccion, 'fecha_nacimiento': fecha_nac, 'edad': edad, 'talla': talla, 'id_familiar': id_familiar, "parentesco": parentesco}

    campos_participante = ["nombre","apellido","email","telefono_casa","celular","estado_civil","direccion","fecha_nacimiento","edad","talla","id_familiar","parentesco"]
    try:
        cond_part = f"nombre=\"{nombres}\"" + " and " + f"apellido=\"{apellidos}\""
        participanteDB = bd_conections.visualizar_datos("participante","id_participante",cond_part)
        if(len(participanteDB) == 0):

            try:
                bd_conections.insertar_datos("participante",campos_participante,datos_participante)
                id_participante = bd_conections.visualizar_datos("participante","id_participante",cond_part).pop()
            except Exception as e:
                print(f"Error al insertar el participante: {e}")

            try:
                datos_adicional= {'id_participante': id_participante, 'fuma': fuma, 'ronca': ronca, 'dieta': dieta, 'medicamento': medicamento, 'limitaciones_fisicas': limit_fisica, 'observaciones': observaciones}
                campos_adicional = ["id_participante","fuma","ronca","dieta","medicamento","limitaciones_fisicas","observaciones"]
                bd_conections.insertar_datos("informacionadicional",campos_adicional,datos_adicional)
            except Exception as e:
                print(f"Error al insertar informacion adicional: {e}")
            
            try:
                datos_actividad= {'id_participante': id_participante, 'estudia': estudia, 'trabaja': trabaja, 'lugar_estudio': lugar_estudio, 'lugar_trabajo': lugar_trabajo}
                campos_actividad = ["id_participante","estudia","trabaja","lugar_estudio","lugar_trabajo"]
                bd_conections.insertar_datos("actividadparticipante", campos_actividad, datos_actividad)
            except Exception as e:
                print(f"Error al insertar la actividad del participante: {e}")
            
            try:
                datos_sacramentos= {'id_participante': id_participante, 'hizoBautismo': bautismo, 'hizoEucarestia': comunion, 'hizoConfirmacion': confirmacion, 'hizoMatrimonio': matrimonio}
                campos_sacramentos = ["id_participante","hizoBautismo","hizoEucarestia","hizoConfirmacion","hizoMatrimonio"]
                bd_conections.insertar_datos("sacramentos",campos_sacramentos,datos_sacramentos)
            except Exception as e:
                print(f"Error al insertar los sacramentos del participante: {e}")
            

            print("\nParticipante Registrado")
        else:
            print("El participante ya esta registrado")
    except Exception as e:
        print(f"Error al comprobar si participante existe: {e}")
    
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
    tabla = "participante"
    columnas = "id_participante, nombre, apellido"
    df = pd.DataFrame(bd_conections.visualizar_datos(tabla,columnas),columns=["ID", "nombre", "apellido"])
    print("\n**Lista de Participante**")
    print(df.to_string(index=False))
    print()

def lista_familiares_id():
    tabla = "familiar"
    columnas = "id_familiar, nombre, apellido"
    df = pd.DataFrame(bd_conections.visualizar_datos(tabla,columnas),columns=["ID", "nombre", "apellido"])
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
                lista_familiares_por_participante()
                input("Presione una Tecla para Regresar")
                time.sleep(2)
            case 5:
                break
            case _:
                print("Seleccione una opcion valida")
                time.sleep(2)

def lista_info_principal_participante():
    tabla = "participante"
    columnas_df = ["id_participante","nombre","apellido","email","telefono_casa","celular","estado_civil","direccion","fecha_nacimiento","edad","talla"]
    columnas_sql = ",".join(columnas_df)
    df = pd.DataFrame(bd_conections.visualizar_datos(tabla,columnas_sql), columns=columnas_df).to_string(index=False)
    print(df)


def lista_info_adicional_participante():
    tabla = "participante join informacionadicional using(id_participante) join actividadparticipante using(id_participante) join sacramentos using(id_participante)"
    columnas_df = ["id_participante","nombre","apellido","fuma","ronca","dieta","medicamento","limitaciones_fisicas","observaciones","hizoBautismo","hizoEucarestia","hizoConfirmacion","hizoMatrimonio","estudia","trabaja","lugar_estudio","lugar_trabajo"]
    columnas_sql = ",".join(columnas_df)
    df = pd.DataFrame(bd_conections.visualizar_datos(tabla,columnas_sql), columns=columnas_df).to_string(index=False)
    print(df)


def lista_familiares_por_participante():
    tabla = "participante join familiar using(id_familiar)"
    columnas_df = ["id_participante","participante.nombre","participante.apellido","parentesco","familiar.nombre","familiar.apellido","familiar.email","familiar.celular"]
    columnas_sql = ",".join(columnas_df)
    df = pd.DataFrame(bd_conections.visualizar_datos(tabla,columnas_sql), columns=columnas_df).to_string(index=False)
    print(df)


def lista_participantes_por_retiro():
    pass

def lista_participante():
    tabla = "participante join informacionadicional using(id_participante) join actividadparticipante using(id_participante) join familiar using(id_familiar)"
    columnas = "id_participante,participante.nombre,participante.apellido,participante.email,telefono_casa,participante.celular,estado_civil,direccion,fecha_nacimiento,edad,talla,estudia,lugar_estudio,trabaja,lugar_trabajo,fuma,ronca,dieta,medicamento,limitaciones_fisicas,observaciones,parentesco,familiar.nombre,familiar.apellido,familiar.celular"
    df = pd.DataFrame(bd_conections.visualizar_datos(tabla,columnas), columns=columnas.split(","))
    print()
    print(df)
    input("Presione una Tecla para Regresar")
