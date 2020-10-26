import json
import time

start_time = time.time()
links_file = open("links_1000000.txt", "r", encoding="utf8")

page_ranks = {'key': list([0.25, 0])}

# initialization of page_ranks dict
while(1):
    line = links_file.readline()
    if not line:
        break
    line = line.strip()
    line = line.strip(",")
    link_object = json.loads(line)
    page_ranks[link_object.get('l')] = list([0.25, 0])
    for neighbour in link_object.get('n'):
        page_ranks[neighbour] = list([0.25, 0])

# now, the dict is initialized to default pageranks for all pages, which were in file links
print("pocet zaznamov v dictionary")
print(len(page_ranks.keys()))

# PageRank algo starts

for iteration in range(80):
    links_file.seek(0)

    while(1):
        line = links_file.readline()
        if not line:
            break
        line = line.strip()
        line = line.strip(",")
        link_object = json.loads(line)
        number_of_neighbours = len(link_object.get('n'))
        donated_PR = page_ranks[link_object.get('l')][0]/number_of_neighbours
        for neighbour in link_object.get('n'):
           page_ranks[neighbour][1] = page_ranks[neighbour][1] + donated_PR

    for link in page_ranks:
        page_ranks[link][0] = page_ranks[link][1]   # this iteration value to old iteration value
        page_ranks[link][1] = 0     # new iteration value will be 0

max_PR_value = 0
max_PR_link = None
for link in page_ranks:
    if page_ranks[link][0] > max_PR_value:
        max_PR_link = link
        max_PR_value = page_ranks[link][0]

print("link s max PR: " + max_PR_link)
print("hodnota PR: " + "{:.100f}".format(max_PR_value))
print("--- %s seconds ---" % (time.time() - start_time))
