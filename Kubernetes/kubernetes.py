import subprocess

def run_command(command):
    """ Ejecuta un comando en la terminal y devuelve su salida. """
    try:
        result = subprocess.run(command, shell=True, check=True, text=True, capture_output=True)
        return result.stdout, True
    except subprocess.CalledProcessError:
        return None, False


def is_docker_installed():
    """ Verifica si Docker está instalado. """
    _, success = run_command("docker --version")
    return success

def is_kubernetes_installed():
    """ Verifica si Kubernetes está instalado. """
    _, success = run_command("kubectl version --client")
    return success


def setup_docker():
    """ Configura Docker en un sistema basado en Debian. """
    print("\nAñadiendo la clave GPG oficial de Docker...\n")
    run_command("curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg")

    print("\nAñadiendo el repositorio de Docker...\n")
    run_command("echo 'deb [arch=amd64 signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(. /etc/os-release && echo \"$VERSION_CODENAME\") stable' | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null")

    print("\nActualizando paquetes...\n")
    run_command("sudo apt update")

    print("\nInstalando Docker...\n")
    run_command("sudo apt install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin -y")

    print("\nVerificando la versión de Docker...\n")
    version, _ = run_command("docker --version")
    print(version)

def setup_kubernetes():
    """ Configura Kubernetes en un sistema basado en Debian. """
    print("\nActualizando paquetes...\n")
    run_command("sudo apt update")

    print("\nAñadiendo la clave GPG de Kubernetes...\n")
    run_command("curl -fsSL https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo gpg --dearmor -o /etc/apt/keyrings/kubernetes.gpg")

    print("\nAñadiendo el repositorio de Kubernetes...\n")
    run_command("echo 'deb [arch=amd64 signed-by=/etc/apt/keyrings/kubernetes.gpg] http://apt.kubernetes.io/ kubernetes-xenial main' | sudo tee -a /etc/apt/sources.list")

    print("\nActualizando paquetes después de añadir el repositorio de Kubernetes...\n")
    run_command("sudo apt update")

    print("\nInstalando kubeadm, kubelet y kubectl...\n")
    run_command("sudo apt install kubeadm kubelet kubectl -y")

    print("\nMarcando paquetes para que no se actualicen automáticamente...\n")
    run_command("sudo apt-mark hold kubeadm kubelet kubectl")

    print("\nVerificando la versión de kubeadm...\n")
    version, _ = run_command("kubeadm version")
    print(version)
    
    
if not is_docker_installed():
    print("\nDocker no está instalado. Ejecutando el proceso de configuración...")
    setup_docker()
else:
    print("\nDocker ya está instalado.")

if not is_kubernetes_installed():
    print("\nKubernetes no está instalado. Ejecutando el proceso de configuración...\n")
    setup_kubernetes()
else:
    print("\nKubernetes ya está instalado. No es necesario volver a configurarlo.\n")


# git clone https://github.com/CDPS-ETSIT/practica_creativa2.git

#  sudo docker build -t g39/product-page .
