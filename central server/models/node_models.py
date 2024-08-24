class Node:
    def __init__(self, node_id, cpu, ram, status):
        self.node_id = node_id
        self.cpu = cpu
        self.ram = ram
        self.status = status

  
    def to_dict(self):
        return {
            "nodeID": self.node_id,
            "CPU": self.cpu,
            "RAM": self.ram,
            "Status": self.status
        }
