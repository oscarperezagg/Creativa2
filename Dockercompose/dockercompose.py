import subprocess
import os


def prune_docker():
    try:
        # Eliminar todos los contenedores detenidos
        subprocess.run("docker container prune -f", shell=True, check=True)

        # Eliminar todas las imágenes no utilizadas
        subprocess.run("docker image prune -a -f", shell=True, check=True)

        print("La limpieza de Docker se completó correctamente.")

    except subprocess.CalledProcessError as e:
        print(f"Ocurrió un error: {e}")


def run_commands():
    try:
        # Guardar el directorio actual
        original_directory = os.getcwd()

        try:
            # Clonar el repositorio de GitHub
            git_clone_command = (
                "git clone https://github.com/CDPS-ETSIT/practica_creativa2.git"
            )
            subprocess.run(git_clone_command, shell=True, check=True)
        except Exception:
            pass
        # Cambiar al directorio específico
        os.chdir("practica_creativa2/bookinfo/src/reviews")

        # Ejecutar Docker con Gradle para construir el proyecto
        docker_gradle_command = 'docker run --rm -u root -v "$(pwd)":/home/gradle/project -w /home/gradle/project gradle:4.8.1 gradle clean build'
        subprocess.run(docker_gradle_command, shell=True, check=True)

        # Cambiar al directorio raíz del proyecto
        os.chdir(original_directory)

        # Construir imágenes con Docker Compose
        docker_compose_build_command = "docker-compose build"
        subprocess.run(docker_compose_build_command, shell=True, check=True)

        # Levantar los contenedores con Docker Compose
        docker_compose_up_command = "docker-compose up"
        subprocess.run(docker_compose_up_command, shell=True, check=True)

        print("Todos los comandos se ejecutaron correctamente.")

    except subprocess.CalledProcessError as e:
        print(f"Ocurrió un error al ejecutar los comandos: {e}")


if __name__ == "__main__":
    prune_docker()
    run_commands()
