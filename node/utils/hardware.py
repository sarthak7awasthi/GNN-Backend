import psutil
import uuid


def get_hardware_info():
    cpu_cores = psutil.cpu_count(logical=True)
    total_ram = psutil.virtual_memory().total // (1024 ** 3)  
    node_id = str(uuid.uuid4())  
    
    return {
        "nodeID": node_id,  
        "CPU": f"{cpu_cores} cores",
        "RAM": f"{total_ram} GB"
    }

