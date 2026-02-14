import json

if __name__ == '__main__':
    with open("./templates/dependant.json") as f:
        print(json.dumps(json.load(f)))
