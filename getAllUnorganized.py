import os
from sys import exit
from shutil import copyfile

data_path = 'data'
new_dir = 'unorganized_data'

if os.path.exists(new_dir):
    print new_dir + ' already exists'
    exit(1)

os.mkdir(new_dir)

for topic in os.listdir(data_path):
    if topic == 'parsed':
        continue

    for category in os.listdir(os.path.join(data_path, topic)):
        try:
            x = category.split('-')[1]
            if x == 'NOT CATEGORIZED':
                continue
        except:
            pass

        for f in os.listdir(os.path.join(data_path, topic, category)):
            if not f.endswith('.json'):
                continue

            copyfile(os.path.join(data_path, topic, category, f),
                    os.path.join(new_dir, f))
