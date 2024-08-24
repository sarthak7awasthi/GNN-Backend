import os
import requests
from flask import Flask, request, jsonify
from utils.hardware import get_hardware_info
from services.node_tasks import execute_task

server_url = os.getenv("CENTRAL_SERVER_URL", "http://localhost:5000")



@app.route('/api/receive_task', methods=['POST'])
def receive_task():
    task = request.json
    print(f"Received task: {task}")
    execute_assigned_task(task)
    return jsonify({"message": "Task received and executed."})



# Function to register the node with the central server
def register_node():
    node_info = get_hardware_info()  
    response = requests.post(f"{server_url}/api/register_node", json=node_info) 
    
    if response.status_code == 200:
        print("Node registered successfully:", response.json())
        return node_info["nodeID"]  
    else:
        print("Failed to register node:", response.status_code)
        return None

def execute_assigned_task(task):
  
    model = execute_task(task)
    
    send_model_to_server(model)


def send_model_to_server(model):
    print("Sending trained model back to the server...")

    model_data = {"state_dict": model.state_dict()}
    

    response = requests.post(f"{server_url}/api/send_model", json=model_data)
    
    if response.status_code == 200:
        print("Model sent successfully:", response.json())
    else:
        print("Failed to send model:", response.status_code)


def run_node():

    node_id = register_node()
    
    if node_id:
        
        response = requests.post(f"{server_url}/api/upload_dataset", json=dataset)

			
        
        if response.status_code == 200:
            tasks = response.json()["tasks"]
            if node_id in tasks:
                print(f"Task assigned to node {node_id}: {tasks[node_id]}")
                execute_assigned_task(tasks[node_id])
            else:
                print(f"No task assigned to node {node_id}.")
        else:
            print("Failed to upload dataset or assign tasks:", response.status_code)

if __name__ == "__main__":

    app.run(host="0.0.0.0", port=5000) 