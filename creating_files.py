import re
import json
import time
import gzip


def line_regex_name(line, current_link_info):  # if line contains name of link, save it to object LinkInfo
    match = re.search(".+<http://rdf\\.freebase\\.com/ns/type\\.object\\.name>.+", line)
    if match:
        founded_name = re.search('\\".+\\"', line)
        if not current_link_info.name:
            founded_name_string = founded_name.group()
            founded_name_string = founded_name_string.strip("\"")
            current_link_info.name = founded_name_string


def line_regex_link(line, current_link_info):
    if line.find("<http://rdf.freebase.com/ns/type>") == -1 and line.find("www.w3.org") == -1 and line.find("common.") == -1 and line.find("base.type_ontology.") == -1 and line.find("measurement_unit.") == -1:
        match = re.search("<http://rdf\\.freebase\\.com/ns.{28,}<http://rdf.freebase.com/ns/.+", line)
        if match:
            start_position_link2 = line.rfind("<http://rdf.freebase.com/ns/") + 28
            end_of_link_position = line.rfind(">")
            link2 = line[start_position_link2:end_of_link_position]
            current_link_info.neighbours.add(link2)


def write_LinkInfo_to_files(current_link_info):
    if current_link_info.name:
        json_name = json.dumps({"l":current_link_info.link, "n":current_link_info.name})
        names_file.write(json_name + ",\n")
    if current_link_info.neighbours:
        neighbours_list = list(current_link_info.neighbours)
        json_neighbours = json.dumps({"l":current_link_info.link, "n":neighbours_list})
        links_file.write(json_neighbours + ",\n")


class LinkInfo:
    link = None
    name = None
    neighbours = set()

    def __init__(self, link):
        self.link = link
        self.neighbours = set()
        self.name = None

# START OF PROGRAM


number_of_lines_to_read = int(input("Please enter number of lines to read:"))
print(number_of_lines_to_read)

start_time = time.time()

names_file = open('names_'+str(number_of_lines_to_read)+'.txt', 'w', encoding="utf8")
links_file = open('links_'+str(number_of_lines_to_read)+'.txt', 'w', encoding="utf8")

freebase_dump_file = gzip.open("C:\\Users\\Veronika\\Documents\\ING\\VINF\\freebase\\freebase-rdf-latest.gz", "rt", encoding="utf8")

current_link = None
last_link = None

number_of_read_lines = 0

while number_of_read_lines < number_of_lines_to_read:
    dump_line = freebase_dump_file.readline()
    number_of_read_lines = number_of_read_lines + 1
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



freebase_dump_file.close()
names_file.close()
links_file.close()

print("subory su vytvorene")
print("--- %s seconds ---" % (time.time() - start_time))
# the files links.txt and names.txt are created


