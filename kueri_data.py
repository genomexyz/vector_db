import chromadb
import pandas as pd

client = chromadb.PersistentClient(path="./animedb")

# create collection
collection = client.get_or_create_collection(
    name=f"animereview"
)

#client = chromadb.PersistentClient(path="./anime_detail")
#
## create collection
#collection = client.get_or_create_collection(
#    name=f"anime_title"
#)

results = collection.query(
    #query_texts=["sports anime where they use tits and ass for competition"],
    #query_texts=["5 magical girl story but with mindblowing plot twist"],
    #query_texts=["anime with big controversy (dad marry his daughter)"],
    #query_texts=["anime where AI control all life aspects"],
    query_texts=["a popular vn adaptation about 7 mage fight for holy grail"],
    n_results=5
)

#print(results)
#print(results.keys())
#print()
for i in range(len(results['documents'][0])):
    #print(results['documents'][0][i])
    print(results['metadatas'][0][i])
    print('==============================================')