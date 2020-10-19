import re
import json


def line_regex_name(line, current_link_info):  # if line contains name of link, save it to file names.json
    match = re.search(".+<http://rdf\\.freebase\\.com/ns/type\\.object\\.name>.+", line)
    if match:
        founded_name = re.search('\\".+\\"', line)
        if not current_link_info.name:
            founded_name_string = founded_name.group()
            founded_name_string = founded_name_string.strip("\"")
            current_link_info.name = founded_name_string


def line_regex_link(line, current_link_info):
    if line.find("<http://rdf.freebase.com/ns/type.object.type>") == -1 and line.find("www.w3.org") == -1:
        match = re.search("<http://rdf\\.freebase\\.com/ns.{28,}<http://rdf.freebase.com/ns/.+", line)
        if match:
            start_position_link2 = line.rfind("<http://rdf.freebase.com/ns/") + 28
            end_of_link_position = line.rfind(">")
            link2 = line[start_position_link2:end_of_link_position]
            current_link_info.neighbours.append(link2)


def write_LinkInfo_to_files(current_link_info):
    if current_link_info.name:
        json_name = json.dumps({current_link_info.link: current_link_info.name})
        names_file.write(json_name + ",\n")
    if current_link_info.neighbours:
        json_neighbours = json.dumps({current_link_info.link: current_link_info.neighbours})
        links_file.write(json_neighbours + ",\n")


class LinkInfo:
    link = None
    name = None
    neighbours = list()

    def __init__(self, link):
        self.link = link
        self.neighbours = []
        self.name = None

# START OF PROGRAM

# TODO pri otvoreni suboru pridat na zaciatok {
names_file = open('names.txt', 'a', encoding="utf8")
links_file = open('links.txt', 'a', encoding="utf8")

freebase_dump_file = open("C:\\Users\\Veronika\\Documents\\ING\\VINF\\freebase-head-1000000", "r", encoding="utf8")

current_link = None
last_link = None

while 1:
    dump_line = freebase_dump_file.readline()
    # if it is EOF
    if not dump_line:
        write_LinkInfo_to_files(current_link)
        break

    # extracting link from line
    end_of_link_position = dump_line.find(">")
    founded_link = dump_line[28:end_of_link_position]

    if not current_link:
        current_link = LinkInfo(founded_link)

    elif not founded_link == current_link.link:
        write_LinkInfo_to_files(current_link)
        last_link = current_link  # deep copy, shalow copy
        current_link = LinkInfo(founded_link)

    line_regex_name(dump_line, current_link)
    line_regex_link(dump_line, current_link)

# TODO pri zatvarani suboru pridat na koniec } POZOR bude tam posledna ciarka, ktoru asi treba vymazat

freebase_dump_file.close()

