# Comprobar si está instalado pip

import subprocess

import os


def check_and_install_pip():
    try:
        # Verificar si pip3 está instalado
        subprocess.check_output(["pip3", "--version"])
        print("pip3 ya está instalado en el sistema.")
    except Exception:
        # Si pip3 no está instalado, actualizar y luego instalarlo
        print("pip3 no está instalado en el sistema. Se procederá a instalarlo.")
        try:
            subprocess.check_call(["sudo", "apt", "update"])
            subprocess.check_call(["sudo", "apt", "install", "python3-pip", "-y"])
            print("pip3 se ha instalado correctamente.")
        except Exception as e:
            print("Hubo un error al intentar instalar pip3:", e)


if __name__ == "__main__":
    # Comprobar e instalar pip3

    check_and_install_pip()

    # Descargar el repositorio de Git
    subprocess.check_call(
        [
            "git",
            "clone",
            "https://github.com/CDPS-ETSIT/practica_creativa2.git",
        ]
    )

    # Obtén el path absoluto del archivo en ejecución
    directorio_actual = os.path.dirname(os.path.abspath(__file__))
    # Concatena las partes para obtener la ubicación completa del archivo
    ruta_del_archivo = os.path.join(
        directorio_actual,
        "practica_creativa2",
        "bookinfo",
        "src",
        "productpage",
        "requirements.txt",
    )

    # Instalar las dependencias desde el archivo requirements.txt
    print(
        "####################### Ejecutando:",
        "pip3",
        "install",
        "-r",
        "requirements.txt",
        "#######################",
    )
    subprocess.check_call(["sudo", "pip3", "install", "-r", ruta_del_archivo])

    # Actualizar la biblioteca requests
    print(
        "####################### Ejecutando:",
        "pip3",
        "install",
        "--upgrade",
        "requests",
        "#######################",
    )
    subprocess.check_call(["sudo", "pip3", "install", "--upgrade", "requests"])

    # Instalar la biblioteca testresources
    print(
        "####################### Ejecutando:",
        "pip3",
        "install",
        "testresources",
        "#######################",
    )
    subprocess.check_call(["sudo", "pip3", "install", "testresources"])

    # Actualizar la biblioteca json2html
    print(
        "####################### Ejecutando:",
        "pip3",
        "install",
        "--upgrade",
        "json2html",
        "#######################",
    )
    subprocess.check_call(["sudo", "pip3", "install", "--upgrade", "json2html"])

    # Concatena las partes para obtener la ubicación completa del archivo
    ruta_del_archivo = os.path.join(
        directorio_actual,
        "practica_creativa2",
        "bookinfo",
        "src",
        "productpage",
        "productpage_monolith.py",
    )

    # Ejecutar el script productpage_monolith.py en el puerto 80
    subprocess.check_call(["sudo", "python3", ruta_del_archivo, "9080"])
