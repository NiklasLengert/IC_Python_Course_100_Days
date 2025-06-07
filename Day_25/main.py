
import os
# import csv
import pandas as pd
basic_path = os.path.dirname(__file__)

# with open(os.path.join(os.path.dirname(__file__), 'weather_data.csv')) as file:
#     data = file.readlines()
#     print(data)

# with open(os.path.join(os.path.dirname(__file__), 'weather_data.csv')) as file:
#     data = csv.reader(file)
#     temperatures = []
#     for row in data:
#         if row[1] != 'temp':
#             temperatures.append(int(row[1]))
#     print(temperatures)
 
# data = pd.read_csv(os.path.join(basic_path, 'weather_data.csv'))
# print(data)
# print(data['temp'])

# data_dict = data.to_dict()
# print(data_dict)

# temp_list = data['temp'].to_list()
# temp_sum = sum(temp_list)
# avg_temp = round(temp_sum / len(temp_list), 2)
# print(f"Average temperature: {avg_temp}")
# avg_temp = data['temp'].mean()
# print(f"Average temperature: {avg_temp}")

# max_temp = data['temp'].max()
# print(f"Maximum temperature: {max_temp}")

# Get data in columns
# print(data['condition'])
# print(data.condition)

# Get data in rows
# print(data[data.day == 'Monday'])
# print(data[data.temp == max_temp])

# monday = data[data.day == 'Monday']
# print(monday.condition)
# print(monday.temp * 9/5 + 32)  # Convert Celsius to Fahrenheit

# data_dict = {
#     "students": ["Angela", "James", "Lily"],
#     "scores": [56, 76, 98]
# }

# data = pd.DataFrame(data_dict)
# data.to_csv(os.path.join(basic_path, 'new_data.csv'), index=False)
# print(data)
    
# data = pd.read_csv(os.path.join(basic_path, 'squirrel_data.csv'))

# gray_squirrels_data = data[data['Primary Fur Color'] == 'Gray']
# red_squirrels_data = data[data['Primary Fur Color'] == 'Cinnamon']
# black_squirrels_data = data[data['Primary Fur Color'] == 'Black']

# gray_squirrels_count = len(gray_squirrels_data)
# red_squirrels_count = len(red_squirrels_data)
# black_squirrels_count = len(black_squirrels_data)

# print(f"Gray Squirrels: {gray_squirrels_count}")
# print(f"Red Squirrels: {red_squirrels_count}")
# print(f"Black Squirrels: {black_squirrels_count}")

# data_dict = {
#     "Fur Color": ["Gray", "Cinnamon", "Black"],
#     "Count": [gray_squirrels_count, red_squirrels_count, black_squirrels_count]
# }

# pandas_data = pd.DataFrame(data_dict)
# pandas_data.to_csv(os.path.join(basic_path, 'squirrel_count.csv'), index=False)

