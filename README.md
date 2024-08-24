# GNN-Backend


## **Overview**

**This module doesn't include SMPC.**


This module is designed to handle distributed **Graph Neural Network (GNN)** training across multiple nodes in a decentralized environment. The central server coordinates the task distribution and collects trained models from the nodes for aggregation. Each node performs GNN training on a shard of the dataset that has been assigned to it.

This module is part of a larger project(**PPFGNN/PETGNN**) and focuses specifically on the **GNN** training tasks, allowing for **smart distribution of tasks based on hardware capabilities** and **weighted model aggregation**. Although the project is functional in terms of core logic, it remains incomplete and is designed as a **separate module** to handle GNN-specific functionality in the broader system.

## **Key Features**

### **1. Smart Distribution of Tasks Based on Hardware**

One of the critical features of this system is the **smart task distribution** that assigns tasks to nodes based on their hardware capabilities, such as **CPU cores** and **RAM**. Nodes with higher processing power and memory are assigned larger chunks of the dataset to balance the workload effectively across the distributed system.

This ensures that:
- Nodes with better hardware resources are utilized more effectively by being assigned a proportionally larger dataset.
- The distribution is optimized to prevent nodes from being overwhelmed or underutilized.

#### **How it Works**:
- The central server keeps track of the **CPU cores** and **RAM** of each node as part of the node registration process.
- During dataset upload, the server calculates the total available hardware resources and assigns tasks based on the **weighted hardware capability** of each node.
- Nodes with higher computational power receive larger dataset shards to ensure efficient utilization of resources.

### **2. Model Averaging (Federated Learning)**

Once the nodes complete their training on their respective dataset shards, they send the trained models (in the form of **PyTorch `state_dict`**) back to the central server. The server then performs **model aggregation** using a weighted averaging approach, where the models are averaged based on the amount of data processed by each node.

#### **How it Works**:
- Each node sends its trained model along with the number of data points (samples) it trained on.
- The central server aggregates the models using **weighted averaging**, giving higher weight to models trained on larger datasets.
- The final aggregated model is stored on the server for further use or evaluation.

### **3. Incomplete Module (Work in Progress)**

This module is currently **incomplete** and functions as a separate component from the main project. It focuses on:
- **Task assignment** for GNN training based on hardware.
- **Model training** and **aggregation** for GNNs.
  
It is designed to handle **GNN-specific** functionality, making it easier to extend the larger system by integrating this module in the future.

---

