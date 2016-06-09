import json

import os

if __name__ == '__main__':

    print os.path.dirname(__file__)
    with open('items.json') as data_file:
        data = json.load(data_file)

    print data
