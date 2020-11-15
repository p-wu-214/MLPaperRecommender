import torch.nn as nn


class DNNRecommender(nn.Module):
    def __init__(self, input_dim, output_dim):
        super(DNNRecommender, self).__init__()
        self.linear1 = nn.Linear(input_dim, input_dim)
        self.linear2 = nn.Linear(input_dim, input_dim)
        self.linear3 = nn.Linear(input_dim, output_dim)

    def forward(self, x):
        x = self.linear1(x)
        x = self.linear2(x)
        y = self.linear3(x)

        return y
