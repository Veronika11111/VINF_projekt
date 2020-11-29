import whoosh.index as index
from whoosh.qparser import QueryParser
from whoosh.query import NumericRange

def parse_line(line):
    parsed_line = line.split(":")
    try:
        float_number = float(parsed_line[1])
    except ValueError:
        float_number = 0.0

    return parsed_line[0], float_number

while True:
    print("------------------------------")
    print("What you want to do?")
    print("A - find name based on link identifier (only for first milion of names)")
    print("B - find PageRank based on link identifier (for parameters a)")
    print("C - number of link with PageRank 0.0")
    print("D - find links with PageRanks in range")
    print("E - to cancel program")

    user_input = input()

    if user_input == 'E':
        break

    if user_input == 'A':
        ix = index.open_dir("names")
        if not ix:
            print("Missing index directory")
            continue
        print("link identifier: ")
        searched_link = input()
        with ix.searcher() as searcher:
            query = QueryParser("link", ix.schema).parse(searched_link)
            results = searcher.search(query)
            if (len(results) == 0):
                print("this link doesn`t exist in index")
            else:
                for result in results:
                    print(result.fields())

    elif user_input == 'B':
        ix = index.open_dir("index_a")
        if not ix:
            print("Missing index directory")
            continue
        print("link identifier: ")
        searched_link = input()
        with ix.searcher() as searcher:
            query = QueryParser("link", ix.schema).parse(searched_link)
            results = searcher.search(query)
            if (len(results) == 0):
                print("this link doesn`t exist in index")
            else:
                for result in results:
                    print(result.fields())

    elif user_input == 'C':
        print("results_file name:")
        results_file_name = input()
        results_file = open(results_file_name, "r", encoding="utf8")
        if not results_file:
            print("no such file")
            continue
        number_of_lines_with_zero_PR = 0
        for line in results_file:
            link, page_rank = parse_line(line)
            if (page_rank == 0.0):
                number_of_lines_with_zero_PR = number_of_lines_with_zero_PR + 1
        print("number of links with zero PageRank: ")
        print(number_of_lines_with_zero_PR)

    elif user_input == 'D':
        print("results_file name:")
        results_file_name = input()
        results_file = open(results_file_name, "r", encoding="utf8")
        if not results_file:
            print("no such file")
            continue
        print("set range in format number1-number2")
        numbers = input()
        parsed_line = numbers.split("-")
        try:
            smaller_num = float(parsed_line[0])
            bigger_num = float(parsed_line[1])
        except ValueError:
            print("wrong number format")
            continue

        list_of_links = list()
        for line in results_file:
            link, page_rank = parse_line(line)
            if (page_rank > smaller_num and page_rank< bigger_num):
                list_of_links.append(link)

        print("number of link with PageRank from range")
        print(len(list_of_links))
        print("how many of them do you want to print?")
        number_of_printed_links = int(input())
        for i in range(number_of_printed_links):
            print(list_of_links[i])

    else:
        print("wrong input")
