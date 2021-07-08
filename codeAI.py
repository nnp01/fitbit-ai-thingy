import torch
import json

model = []
model.append(torch.nn.Linear(3, 1))

plus_hr = 0 #variable for doctoring testing data

def fitbitImport(heart_rate_file, steps_file, calories_file): # function for importing fitbit data
    with open(heart_rate_file) as heartF, open(steps_file) as stepsF, open(calories_file) as caloriesF:
        heart_rate_data = json.load(heartF)
        steps_data = json.load(stepsF)
        calories_data = json.load(caloriesF)
        
        dataset = []
        for i in range(len(heart_rate_data['activities-heart-intraday']['dataset'])):
            heart_rate = heart_rate_data['activities-heart-intraday']['dataset'][i]['value']/100
            steps = steps_data['activities-steps-intraday']['dataset'][i]['value']/100
            calories = calories_data['activities-calories-intraday']['dataset'][i]['value']/100
            one_minute = [heart_rate, steps, calories]
            dataset.append(one_minute)
    return dataset

def fitbitImportDoctored(heart_rate_file, steps_file, calories_file): # function for importing fitbit data
    with open(heart_rate_file) as heartF, open(steps_file) as stepsF, open(calories_file) as caloriesF:
        heart_rate_data = json.load(heartF)
        steps_data = json.load(stepsF)
        calories_data = json.load(caloriesF)
        
        dataset = []
        for i in range(len(heart_rate_data['activities-heart-intraday']['dataset'])):
            heart_rate = (heart_rate_data['activities-heart-intraday']['dataset'][i]['value']+plus_hr)/100
            steps = steps_data['activities-steps-intraday']['dataset'][i]['value']/100
            calories = calories_data['activities-calories-intraday']['dataset'][i]['value']/100
            one_minute = [heart_rate, steps, calories]
            dataset.append(one_minute)
    return dataset

params_dict_list = []
for i in range(len(model)):
    params_dict = {}
    params_dict["params"] = model[i].parameters()
    params_dict_list.append(params_dict)

opt = torch.optim.SGD(params_dict_list, lr=1e-2, momentum=0.9)
loss_func = torch.nn.MSELoss()

# makes a dataset with all training data combined
training_data1 = fitbitImport('fitbit data/heart_0407.json', 'fitbit data/steps_0407.json', 'fitbit data/calories_0407.json')
training_data2 = fitbitImport('fitbit data/heart_0507.json', 'fitbit data/steps_0507.json', 'fitbit data/calories_0507.json')
training_data3 = fitbitImport('fitbit data/heart_0607.json', 'fitbit data/steps_0607.json', 'fitbit data/calories_0607.json')
training_data1.extend(training_data2)
training_data1.extend(training_data3)

training_data = torch.tensor(training_data1)
#training_data = torch.rand((100,10))

epoch = 10
for e in range(epoch):
    for d_i in training_data:
        d_o = d_i
        for i in range(len(model)):
            d_o = model[i](d_o.unsqueeze(0))
        
        loss = loss_func(d_i, d_o)

        last_loss = loss.item()
        #print(loss.item())
        opt.zero_grad()
        loss.backward()
        opt.step()

#inference
#anomaly_data_ = torch.tensor([[60/100, 0, 1.3]])
anomaly_data_ = torch.tensor(fitbitImportDoctored('fitbit data/heart_0707.json', 'fitbit data/steps_0707.json', 'fitbit data/calories_0707.json'))

anomaly_data = anomaly_data_
[elm.eval() for elm in model]
with torch.no_grad():
    for i in range(len(model)):
        anomaly_data_ = model[i](anomaly_data_)
    loss = loss_func(anomaly_data, anomaly_data_)
    inference = loss.item()

    #print("Last loss:       ", last_loss) # prints last loss
    #print("Inference Loss:  ", inference) # prints inference loss

    if (last_loss - 0.012)>inference: # tells the user if there could be a health issue
        print('<p><img style="width:160px" src="/checkmark.png"></p><b>Everything is alright!</b>')
    else:
        print('<p><img style="width:160px" src="/red_x.png"></p><b>There might be a problem!</b>')
    