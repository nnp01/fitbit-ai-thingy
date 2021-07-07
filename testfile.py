import torch
import json

# fitbit data import
with open('heart.json') as heart, open('steps.json') as steps:
    heart_rate_data = json.load(heart)
    steps_data = json.load(steps)
    dataset = []
    for i in range(len(heart_rate_data['activities-heart-intraday']['dataset'])):
        one_minute = [float(heart_rate_data['activities-heart-intraday']['dataset'][i]['value']), float(steps_data['activities-steps-intraday']['dataset'][i]['value'])]
        dataset.append(one_minute)

random_data = torch.tensor(dataset)

print(random_data)