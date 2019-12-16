import json

def get_list():
    try:
        with open('db.json') as file:
            data = json.load(file)
        return data
    except:
        return []
    

def write_one(ieo):
    ieos = get_list()
    ieos.insert(0, ieo)

    with open('db.json', 'w') as file:
        json.dump(ieos, file, indent=2)
        name = ieo['name']
        print(f'Добавил в db - {name} \n')
