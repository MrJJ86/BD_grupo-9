import sys
import participante as prt
import servidor as ser
import utils
import time

def main():
    es_salida = False
    while not es_salida:
        utils.borrarPantalla()
        print("******BASE DE DATOS******")
        print("***MINISTERIO DE EMAUS***")
        print("\nMenu Principal")
        print("1. Participantes")
        print("2. Servidores")
        print("3. Retiro")
        print("4. Salir")
        opc = int(input("Seleccione una opcion: "))
        match opc:
            case 1:
                prt.participante()
            case 2:
                ser.servidor()
            case 3:
                break
            case 4:
                es_salida = True
            case _:
                print("\nIngrese una opcion valida")
                time.sleep(3)
        
    salir()


def salir():
    print("Gracias por usar nuestro sistema")
    sys.exit()


if __name__ == "__main__":
    main()