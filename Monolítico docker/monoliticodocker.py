import subprocess

def run_docker_commands():
    try:
        # Construir la imagen Docker
        build_command = "sudo docker build -t g39/product-page ."
        subprocess.run(build_command, shell=True, check=True)

        # Ejecutar el contenedor Docker
        run_command = "sudo docker run --name g39-product-page -p 9080:9080 -e GROUPO_NUMERO=g39 -d g39/product-page"
        subprocess.run(run_command, shell=True, check=True)

        print("Comandos Docker ejecutados correctamente.")
    except subprocess.CalledProcessError as e:
        print(f"Ocurrió un error al ejecutar los comandos: {e}")

if __name__ == "__main__":
    run_docker_commands()
