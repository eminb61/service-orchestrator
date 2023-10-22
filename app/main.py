import docker
import requests
from fastapi import FastAPI

app = FastAPI()

VERTISIM_URL = "http://vertisim_service:5001"

@app.post("/reset_instance")
async def reset_instance():
    try:
        # Reset the Vertisim instance
        response_reset = requests.post(f'{VERTISIM_URL}/reset', timeout=10)
        
        if response_reset.status_code != 200:
            raise ConnectionError("Failed to reset Vertisim instance.")
        
        print("Successfully stopped the Vertisim instance.")
        
        # Initialize the new Vertisim instance and get initial state
        response_initialize = requests.get(f'{VERTISIM_URL}/get_initial_state', timeout=30)
        
        if response_initialize.status_code != 200:
            raise ConnectionError(f"Failed to get the initial states from new Vertisim instance. Status code: {response_initialize.status_code}, Response text: {response_initialize.text}")
        
        # Return the initial state to the caller
        return {"status": "Success", "initial_state": response_initialize.json()}
    
    except Exception as e:
        return {"status": "Error", "detail": str(e)}
    

# client = docker.from_env()

# @app.post("/reset_instance")
# async def reset_instance():
#     try:
#         # Terminate existing Vertisim instance if it exists
#         for container in client.containers.list(filters={"ancestor": "simulationandoptimization-vertisim_service"}):
#             container.stop()

#         # Create and start a new Vertisim instance
#         container = client.containers.run("simulationandoptimization-vertisim_service", detach=True, ports={'5000/tcp': None}, remove=True)
        
#         # Obtain the IP address/hostname and port to communicate with the new Vertisim instance
#         # Note: Adjust this section according to your Docker network settings
#         vertisim_host = container.name

#         # Fetch the initial state from the new Vertisim instance
#         response = requests.post(f'http://{vertisim_host}:5000/get_initial_state')
#         if response.status_code != 200:
#             raise ConnectionError("Failed to retrieve initial state from new Vertisim instance.")

#         # Return relevant details (e.g., dynamically assigned port, container ID, etc.) and initial state
#         return {"status": "Success", "detail": "Vertisim instance reset.", "id": container.id, "initial_state": response.json()}
#     except Exception as e:
#         return {"status": "Error", "detail": str(e)}    