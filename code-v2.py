import torch
import json

model = []
model.append(torch.nn.Linear(2, 1))
model.append(torch.nn.Linear(1, 2))

params_dict_list = []
for i in range(len(model)):
    params_dict = {}
    params_dict["params"] = model[i].parameters()
    params_dict_list.append(params_dict)

opt = torch.optim.SGD(params_dict_list, lr=1e-2, momentum=0.9)
loss_func = torch.nn.MSELoss()

# fitbit data import
with open('heart.json') as heart, open('steps.json') as steps:
    heart_rate_data = json.load(heart)
    steps_data = json.load(steps)
    dataset = []
    for i in range(len(heart_rate_data['activities-heart-intraday']['dataset'])):
        one_minute = [heart_rate_data['activities-heart-intraday']['dataset'][i]['value']/100, steps_data['activities-steps-intraday']['dataset'][i]['value']/100]
        dataset.append(one_minute)

training_data = torch.tensor(dataset)

#training_data = torch.rand((100,10))

epoch = 10
for e in range(epoch):
    for d_i in training_data:
        d_o = d_i
        for i in range(len(model)):
            d_o = model[i](d_o.unsqueeze(0))
        
        loss = loss_func(d_i, d_o)

        myVariable = loss.item()
        #print(loss.item())
        opt.zero_grad()
        loss.backward()
        opt.step()
print(myVariable) # prints last loss

#inference
#anomaly_data_ = torch.rand((1,2))
anomaly_data_ = torch.tensor([[97/100, 102/100], [89/100, 99/100]])

anomaly_data = anomaly_data_
[elm.eval() for elm in model]
with torch.no_grad():
    for i in range(len(model)):
        anomaly_data_ = model[i](anomaly_data_)
    loss = loss_func(anomaly_data, anomaly_data_)
    print("Inference Loss:", loss.item())
    