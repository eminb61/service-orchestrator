import docker
import requests
from fastapi import FastAPI

app = FastAPI()
client = docker.from_env()


@app.post("/reset_instance")
async def reset_instance():
    try:
        # Terminate existing Vertisim instance if it exists
        for container in client.containers.list(filters={"ancestor": "vertisim_image"}):
            container.stop()

        # Create and start a new Vertisim instance
        container = client.containers.run("vertisim_image", detach=True, ports={'5000/tcp': None})
        
        # Obtain the IP address/hostname and port to communicate with the new Vertisim instance
        # Note: Adjust this section according to your Docker network settings
        vertisim_host = container.attrs['NetworkSettings']['IPAddress']

        # Fetch the initial state from the new Vertisim instance
        response = requests.post(f'http://{vertisim_host}:5000/get_initial_state')
        if response.status_code != 200:
            raise ConnectionError("Failed to retrieve initial state from new Vertisim instance.")

        # Return relevant details (e.g., dynamically assigned port, container ID, etc.) and initial state
        return {"status": "Success", "detail": "Vertisim instance reset.", "id": container.id, "initial_state": response.json()}
    except Exception as e:
        return {"status": "Error", "detail": str(e)}
