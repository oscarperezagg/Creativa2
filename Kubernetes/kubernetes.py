import subprocess
import os


import subprocess


def run_command(command):
    """Ejecuta un comando en la terminal y devuelve su salida y un booleano indicando el éxito."""
    try:
        result = subprocess.run(
            command, shell=True, check=True, text=True, capture_output=True
        )
        return result.stdout, None, True
    except subprocess.CalledProcessError as e:
        return None, e.stderr, False


################ CHECKS ################


def is_docker_installed():
    """Verifica si Docker está instalado."""
    _, success = run_command("docker --version")
    return success


def is_kubernetes_installed():
    """Verifica si Kubernetes está instalado."""
    _, success = run_command("kubectl version --client")
    return success


################ SETUP ################


def setup_docker():
    """Configura Docker en un sistema basado en Debian."""
    print("\nAñadiendo la clave GPG oficial de Docker...")
    run_command(
        "curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg"
    )

    print("\nAñadiendo el repositorio de Docker...")
    run_command(
        "echo 'deb [arch=amd64 signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(. /etc/os-release && echo \"$VERSION_CODENAME\") stable' | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null"
    )

    print("\nActualizando paquetes...")
    run_command("sudo apt update")

    print("\nInstalando Docker...")
    run_command(
        "sudo apt install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin -y"
    )

    print("\nVerificando la versión de Docker...")
    version, _ = run_command("docker --version")
    print(version)


def setup_kubernetes():
    """Configura Kubernetes en un sistema basado en Debian."""
    print("\nActualizando paquetes...")
    run_command("sudo apt update")

    print("\nAñadiendo la clave GPG de Kubernetes...")
    run_command(
        "curl -fsSL https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo gpg --dearmor -o /etc/apt/keyrings/kubernetes.gpg"
    )

    print("\nAñadiendo el repositorio de Kubernetes...")
    run_command(
        "echo 'deb [arch=amd64 signed-by=/etc/apt/keyrings/kubernetes.gpg] http://apt.kubernetes.io/ kubernetes-xenial main' | sudo tee -a /etc/apt/sources.list"
    )

    print("\nActualizando paquetes después de añadir el repositorio de Kubernetes...")
    run_command("sudo apt update")

    print("\nInstalando kubeadm, kubelet y kubectl...")
    run_command("sudo apt install kubeadm kubelet kubectl -y")

    print("\nMarcando paquetes para que no se actualicen automáticamente...")
    run_command("sudo apt-mark hold kubeadm kubelet kubectl")

    print("\nVerificando la versión de kubeadm...")
    version, _ = run_command("kubeadm version")
    print(version)


def setup_images():
    """Configura y construye imágenes Docker para el proyecto."""

    # Guardar el directorio actual
    original_directory = os.getcwd()

    # Clonar el repositorio de GitHub
    print("\nClonando el repositorio de GitHub...")
    output, error, success = run_command(
        "git clone https://github.com/CDPS-ETSIT/practica_creativa2.git"
    )
    if not success:
        print("\n -> Algo fue mal! Error: \n" + (error or "Desconocido"))
        return

    # Cambiar al directorio específico
    try:
        print("\nCambiando al directorio del proyecto...")
        os.chdir("practica_creativa2/bookinfo/src/reviews")
    except Exception as e:
        print(f"Error al cambiar de directorio: {e}")
        return

    # Construir el proyecto con Docker y Gradle
    print("\nConstruyendo el proyecto con Docker y Gradle...")
    output, error, success = run_command(
        'docker run --rm -u root -v "$(pwd)":/home/gradle/project -w /home/gradle/project gradle:4.8.1 gradle clean build'
    )
    if not success:
        print("\n -> Algo fue mal! Error: \n" + (error or "Desconocido"))
        return

    # Volver al directorio original
    os.chdir(original_directory)

    # Comandos para construir imágenes Docker
    docker_build_commands = [
        "sudo docker build -t g39/productpage -f dockerfiles/productpage .",
        "sudo docker build -t g39/details -f dockerfiles/details .",
        "sudo docker build -t g39/ratings -f dockerfiles/ratings .",
        "sudo docker build -t g39/reviews -f practica_creativa2/bookinfo/src/reviews/Dockerfile .",
    ]

    for command in docker_build_commands:
        print(f"\nConstruyendo imagen Docker con el comando: {command}")
        output, error, success = run_command(command)
        if not success:
            print("\n -> Algo fue mal! Error: \n" + (error or "Desconocido"))
            return


################ PROGRAM ################

if not is_docker_installed():
    print("\nDocker no está instalado. Ejecutando el proceso de configuración...")
    setup_docker()
else:
    print("\nDocker ya está instalado.")

if not is_kubernetes_installed():
    print("\nKubernetes no está instalado. Ejecutando el proceso de configuración...")
    setup_kubernetes()
else:
    print("\nKubernetes ya está instalado. No es necesario volver a configurarlo.")


setup_images()
