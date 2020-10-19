import json

links_file = open('links.txt', 'r', encoding="utf8")
links_list = []

while(1):
    line = links_file.readline()
    if not line:
        print("Koniec suboru, ziadne duplicity")
        break
    line = line.strip()
    line = line.strip(",")
    link_object = json.loads(line)
    for i in links_list:
        if i == link_object.get('l'):
            print("DUPLICITA PRI: " + link_object.get('l'))
    links_list.append(link_object.get('l'))
