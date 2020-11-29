import re
import gzip
from whoosh.index import create_in
from whoosh.fields import *
from whoosh.qparser import QueryParser
import os.path

freebase_dump_file = gzip.open("C:\\Users\\Veronika\\Documents\\ING\\VINF\\freebase\\freebase-rdf-latest.gz", "rt", encoding="utf8", errors='replace')

schema = Schema(link=ID(stored=False, unique=True), name=TEXT(stored=True))
if not os.path.exists("names"):
    os.mkdir("names")
ix = create_in("names", schema)
writer = ix.writer()

counter = 0
for dump_line in freebase_dump_file:
    end_of_link_position = dump_line.find(">")
    founded_link = dump_line[28:end_of_link_position]
    match = re.search(".+<http://rdf\\.freebase\\.com/ns/type\\.object\\.name>.+", dump_line)
    if match:
        founded_name = re.search('\\".+\\"', dump_line)
        founded_name_string = founded_name.group()
        founded_name_string = founded_name_string.strip("\"")
        # names_file.write(founded_link + ":" + founded_name_string + "\n")
        writer.add_document(link=founded_link, name=founded_name_string)
        counter = counter + 1
    if counter == 1000000:
        writer.commit()
        print("milion zapisanych")
        counter = 0
writer.commit()


print("index vytvoreny")

# with ix.searcher() as searcher:
#     query = QueryParser("link", ix.schema).parse(u"award.award_winner")
#     results = searcher.search(query)
#     for result in results:
#         print(result.fields())

