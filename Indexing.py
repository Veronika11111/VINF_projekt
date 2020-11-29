import json
from whoosh.index import create_in
from whoosh.fields import *
from whoosh.qparser import QueryParser
import os.path

def parse_line(line):
    parsed_line = line.split(":")
    try:
        float_number = float(parsed_line[1])
    except ValueError:
        float_number = 0.0

    return parsed_line[0], float_number

file_suffix = "50000000_a"
results_file = open("results_file_" + file_suffix + ".txt", "r", encoding="utf8")

schema = Schema(link=ID(stored=False), page_rank=NUMERIC(stored=True, sortable=True))
if not os.path.exists("index_a"):
    os.mkdir("index_a")
ix = create_in("index_a", schema)
writer = ix.writer()

for line in results_file:
    link, page_rank = parse_line(line)
    writer.add_document(link=link, page_rank=page_rank)

writer.commit()

with ix.searcher() as searcher:
    query = QueryParser("link", ix.schema).parse(u"education.education")
    results = searcher.search(query)
    print(results)

results_file.close()

