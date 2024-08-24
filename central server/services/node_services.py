import os
import json
from models.node_model import Node

import torch
from collections import OrderedDict



nodes_registry = {}

def register_node(node_data):
    node = Node(
        node_id=node_data.get('nodeID'),
        cpu=node_data.get('CPU'),
        ram=node_data.get('RAM'),
        status="Active"
    )

    nodes_registry[node.node_id] = node

  
    if not os.path.exists('nodes'):
        os.makedirs('nodes')

 
    with open(f'nodes/{node.node_id}.json', 'w') as f:
        json.dump(node.to_dict(), f)

    return {"message": "Node registered successfully", "node": node.to_dict()}

def assign_tasks_to_nodes(dataset):
    tasks_assigned = {}
    
    dataset_size = len(dataset['data'])
    
   
    total_cpu = sum(node.cpu for node in nodes_registry.values())
    total_ram = sum(node.ram for node in nodes_registry.values())
    

    total_capability = total_cpu + total_ram  
   
    assigned_data_size = 0
    for i, node_id in enumerate(nodes_registry):
        node = nodes_registry[node_id]
        
        
        node_capability = node.cpu + node.ram
        node_weight = node_capability / total_capability
        
       
        node_shard_size = int(node_weight * dataset_size)
        
  
        if i == len(nodes_registry) - 1:
            node_shard_size = dataset_size - assigned_data_size
        

        start_index = assigned_data_size
        end_index = assigned_data_size + node_shard_size
        assigned_data_size += node_shard_size
        

        tasks_assigned[node_id] = {
            "shard": dataset['data'][start_index:end_index],
            "CPU": node.cpu,
            "RAM": node.ram
        }

    return {"message": "Tasks assigned to nodes", "tasks": tasks_assigned}



received_models = []

# Function to receive trained models from nodes
def receive_model(model_data):
    global received_models
    
    print("Received trained model from node.")
    

    received_models.append(model_data['state_dict'])
    
    
    if len(received_models) >= 2: 
        print("Aggregating models from nodes.")
        aggregated_model = aggregate_models(received_models)
        print("Model aggregation complete.")

        torch.save(aggregated_model, 'aggregated_model.pth')
    
    return {"message": "Model received and aggregation in progress."}


def aggregate_models(models, data_points_per_node):
    total_data_points = sum(data_points_per_node)
    avg_model = OrderedDict()
    

    for key in models[0]:
        avg_model[key] = torch.zeros_like(torch.tensor(models[0][key]))
    

    for i, model in enumerate(models):
        weight = data_points_per_node[i] / total_data_points
        for key in model:
            avg_model[key] += torch.tensor(model[key]) * weight
    
    return avg_model
