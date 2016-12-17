import os
import sys
from shutil import copyfile

def main(argv):
    data_path = argv[0]
    if (not os.path.exists(data_path)):
        print data_path + ' does not exist!'
        sys.exit(1)

    new_dir = argv[1]
    if os.path.exists(new_dir):
        print new_dir + ' already exists'
        sys.exit(1)

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

if __name__ == "__main__":
    main(sys.argv[1:])
