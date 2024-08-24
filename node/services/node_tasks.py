import torch
import torch.nn.functional as F
from torch_geometric.nn import GCNConv
from torch_geometric.data import Data


class GCN(torch.nn.Module):
    def __init__(self, num_node_features, hidden_channels, num_classes):
        super(GCN, self).__init__()
        self.conv1 = GCNConv(num_node_features, hidden_channels)
        self.conv2 = GCNConv(hidden_channels, num_classes)

    def forward(self, x, edge_index):
   
        x = self.conv1(x, edge_index)
        x = F.relu(x)
        
      
        x = self.conv2(x, edge_index)
        return F.log_softmax(x, dim=1)


def execute_task(task):
    shard = task.get("shard")
    print(f"Executing task with dataset shard: {shard}")

 
    node_features = torch.tensor(shard, dtype=torch.float32)
    edge_index = torch.tensor([[0, 1], [1, 0]], dtype=torch.long)  


    model = GCN(num_node_features=node_features.size(1), hidden_channels=16, num_classes=2)
    

    optimizer = torch.optim.Adam(model.parameters(), lr=0.01)
    criterion = torch.nn.CrossEntropyLoss()


    target = torch.tensor([0, 1], dtype=torch.long)


    model.train()
    for epoch in range(10):
        optimizer.zero_grad() 

       
        out = model(node_features, edge_index)

     
        loss = criterion(out, target)
        
  
        loss.backward()
        optimizer.step()

        print(f"Epoch {epoch+1}: Loss = {loss.item()}")

    print("Task execution (training) completed.")
    return model  
