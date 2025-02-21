import json

def read_file():
    with open('passwords.json', 'r') as file:
        # Let's see what's actually in the file
        data = json.load(file)
        print(data)

if __name__ == '__main__':
    read_file()