import torch
import json

model = []
model.append(torch.nn.Linear(1, 1))
model.append(torch.nn.Linear(1, 1))

params_dict_list = []
for i in range(len(model)):
    params_dict = {}
    params_dict["params"] = model[i].parameters()
    params_dict_list.append(params_dict)

opt = torch.optim.SGD(params_dict_list, lr=1e-2, momentum=0.9)
loss_func = torch.nn.MSELoss()

# fitbit data import
with open('data.json') as data:
    input_data = json.load(data)
    heart_rates = []
    for i in range(len(input_data['activities-heart-intraday']['dataset'])):
        placeholder = [input_data['activities-heart-intraday']['dataset'][i]['value']]
        heart_rates.append(placeholder)

random_data = torch.tensor(heart_rates)
#random_data = torch.rand((100,10))

epoch = 10
for e in range(epoch):
    for d_i in random_data:
        d_o = d_i
        for i in range(len(model)):
            d_o = model[i](d_o.unsqueeze(0))
        
        loss = loss_func(d_i, d_o)
        print(loss.item())
        opt.zero_grad()
        loss.backward()
        opt.step()
    
#inference
anomaly_data_ = torch.rand((1,2))
anomaly_data = anomaly_data_
[elm.eval() for elm in model]
with torch.no_grad():
    for i in range(len(model)):
        anomaly_data_ = model[i](anomaly_data_)
    loss = loss_func(anomaly_data, anomaly_data_)
    print("Inference Loss:", loss.item())
    