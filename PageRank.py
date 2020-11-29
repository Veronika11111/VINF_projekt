import json
import time

start_time = time.time()
files_suffix = "50000000"
links_file = open("links_" + files_suffix + ".txt", "r", encoding="utf8")
iterations_file = open("iterations_" + files_suffix + "_d.txt", "w", encoding="utf8")

page_ranks = dict()
default_page_rank = 1000
threshold_value = 0.001

# initialization of page_ranks dict
for line in links_file:
    line = line.strip(",\n")
    link_object = json.loads(line)
    page_ranks[link_object.get('l')] = list([default_page_rank, 0, link_object.get('n')])
    for neighbour in link_object.get('n'):
        if neighbour not in page_ranks:
            page_ranks[neighbour] = list([default_page_rank, 0, []])

# now, the dict is initialized to default pageranks for all pages, which were in file links
print("dictionary inicializovaná")


biggest_change = 100        # only for beginning

# PageRank algo starts
no_iterations = 0

while biggest_change > threshold_value:

    biggest_change = 0
    no_iterations = no_iterations+1
    if no_iterations > 50:
        print("koniec, lebo preslo 50 iteracii")
        break

    for link, pr_values in page_ranks.items():
        number_of_neighbours = len(pr_values[2]) or 1
        donated_PR = pr_values[0]/number_of_neighbours
        for neighbour in pr_values[2]:
            page_ranks[neighbour][1] = page_ranks[neighbour][1] + donated_PR

    # for line in links_file:
    #     line = line.strip(",\n")
    #     link_object = json.loads(line)
    #     number_of_neighbours = len(link_object.get('n'))
    #     donated_PR = page_ranks[link_object.get('l')][0]/number_of_neighbours
    #     for neighbour in link_object.get('n'):
    #        page_ranks[neighbour][1] = page_ranks[neighbour][1] + donated_PR

    for link in page_ranks:
        change = abs(page_ranks[link][0] - page_ranks[link][1])
        if change > biggest_change:
            biggest_change = change
        page_ranks[link][0] = page_ranks[link][1]   # this iteration value to old iteration value
        page_ranks[link][1] = 0.0    # new iteration value will be 0

    iterations_file.write(str(no_iterations) + " -> " + "{:.10f}".format(biggest_change) + "\n")
    print(str(no_iterations) + " -> " + "{:.10f}".format(biggest_change) + "\n")

iterations_file.write("default page rank= " + "{:.5f}".format(default_page_rank) + "\n")
iterations_file.write("threshold= " + "{:.5f}".format(threshold_value) + "\n")
iterations_file.write("--- %s seconds ---" % (time.time() - start_time))

# writing results to results_file
results_file = open('results_file_' + files_suffix + '_d.txt', 'w', encoding="utf8")

for link, pr_values in sorted(page_ranks.items(), key=lambda item: item[1][0], reverse=True):
    results_file.write(link + ":" + "{:.20}".format(pr_values[0]) + "\n")
    # if pr_values[0] < 0.000000000001:
    #     break

results_file.close()
