import torch
import json
#from codev2 import fitbitImport

'''
# fitbit data import
with open('heart.json') as heart, open('steps.json') as steps:
    heart_rate_data = json.load(heart)
    steps_data = json.load(steps)
    dataset = []
    for i in range(len(heart_rate_data['activities-heart-intraday']['dataset'])):
        one_minute = [float(heart_rate_data['activities-heart-intraday']['dataset'][i]['value']), float(steps_data['activities-steps-intraday']['dataset'][i]['value'])]
        dataset.append(one_minute)

random_data = torch.tensor(dataset)

print(random_data)'''

def fitbitImport(heart_rate_file, steps_file): # function for importing fitbit data
    with open(heart_rate_file) as heart, open(steps_file) as steps:
        heart_rate_data = json.load(heart)
        steps_data = json.load(steps)
        dataset = []
        for i in range(len(heart_rate_data['activities-heart-intraday']['dataset'])):
            one_minute = [heart_rate_data['activities-heart-intraday']['dataset'][i]['value']/100, steps_data['activities-steps-intraday']['dataset'][i]['value']/100]
            dataset.append(one_minute)

    return dataset


# makes a dataset with all training data combined
training_data1 = fitbitImport('heart_0407.json', 'steps_0407.json')
training_data2 = fitbitImport('heart_0507.json', 'steps_0507.json')
training_data3 = fitbitImport('heart_0607.json', 'steps_0607.json')
training_data1.extend(training_data2)
training_data1.extend(training_data3)
training_data = torch.tensor(training_data1)

print(training_data)