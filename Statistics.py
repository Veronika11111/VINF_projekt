import json


def parse_line(line):
    parsed_line = line.split(":")
    return parsed_line[0], float(parsed_line[1])


def find_name(link):
    names_file.seek(0)
    while 1:
        line = names_file.readline()
        if not line:
            break
        line = line.strip()
        line = line.strip(",")
        name_object = json.loads(line)
        if name_object.get("l") == link:
            return name_object.get("n")

    return None


file_suffix = "10_milionov_c"
results_file = open("results_file_" + file_suffix + ".txt", "r", encoding="utf8")
final_results_file = open("final_results_" + file_suffix + ".txt", "w", encoding="utf8")
names_file = open("names_10_milionov.txt", "r", encoding="utf8")

default_pr = 0.0001
counter = 0
links_with_default_pr = []

while counter < 20:
    line = results_file.readline()
    if not line:
        break

    link, page_rank = parse_line(line)
    name = find_name(link)

    if page_rank == default_pr:
        links_with_default_pr.append(name)
        continue

    counter = counter + 1
    final_results_file.write("----- " + str(counter) + ". -----\n")
    if name:
        final_results_file.write("Name: " + name + "\n")
    else:
        final_results_file.write("Name: not found" + "\n")
    final_results_file.write("Link: " + link + "\n")
    final_results_file.write("PageRank = " + "{:.10f}".format(page_rank) + "\n\n")

final_results_file.write("Links with default PR: \n" + '\n'.join([str(elem) for elem in links_with_default_pr]) + "\n")

results_file.close()
names_file.close()
final_results_file.close()
