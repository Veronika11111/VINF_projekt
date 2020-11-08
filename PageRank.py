import json
import time

start_time = time.time()
links_file = open("links_10_milionov.txt", "r", encoding="utf8")

page_ranks = dict()
default_page_rank = 0.000001

# initialization of page_ranks dict
while(1):
    line = links_file.readline()
    if not line:
        break
    line = line.strip()
    line = line.strip(",")
    link_object = json.loads(line)
    page_ranks[link_object.get('l')] = list([default_page_rank, 0])
    for neighbour in link_object.get('n'):
        page_ranks[neighbour] = list([default_page_rank, 0])

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

min_PR_value = 1
min_PR_link = None
for link in page_ranks:
    if (not page_ranks[link][0] == default_page_rank) and page_ranks[link][0] > max_PR_value:
        max_PR_link = link
        max_PR_value = page_ranks[link][0]
    # if page_ranks[link][0] < min_PR_value:
    #     min_PR_value = page_ranks[link][0]
    #     min_PR_link = link

print("link s max PR: " + max_PR_link)
print("hodnota PR: " + "{:.100f}".format(max_PR_value))
# print("link s min PR: " + min_PR_link)
# print("hodnota PR: " + "{:.100f}".format(min_PR_value))
print("--- %s seconds ---" % (time.time() - start_time))

sorted_PR = {k: v for k, v in sorted(page_ranks.items(), key=lambda item: item[1])}


results_file = open('results_file.txt', 'w', encoding="utf8")
results_file.write(json.dumps(sorted_PR, indent=4))
results_file.close()
