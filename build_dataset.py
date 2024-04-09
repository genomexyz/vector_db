import chromadb
import pandas as pd
#from sentence_transformers import SentenceTransformer
#embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
#
#class MyEmbeddingFunction(EmbeddingFunction):
#    def __call__(self, input: Documents) -> Embeddings:
#        batch_embeddings = embedding_model.encode(input)
#        return batch_embeddings.tolist()
#
#embed_fn = MyEmbeddingFunction()

dset_anime = pd.read_csv('dset/animes.csv')
print(dset_anime)
print(dset_anime.keys())

uid = list(dset_anime['uid'])
uid_str = [str(num) for num in uid]
title = list(dset_anime['title'])
metadata = dset_anime[['synopsis', 'genre', 'aired', 'episodes', 'members',
       'popularity', 'ranked', 'score', 'img_url', 'link']]
#print(metadata.loc[0])
#exit()
client = chromadb.PersistentClient(path="./anime_detail")

# create collection
collection = client.get_or_create_collection(
    name=f"anime_title"
)

#collection.add(
#    documents=title,
#    metadatas=metadata,
#    ids=uid_str
#)


for i in range(len(uid_str)):
    print('cek progress %s/%s'%(i+1, len(uid_str)))
    single_uid = uid_str[i]
    single_title = title[i]
    single_metadata = {}
    single_metadata['synopsis'] = metadata['synopsis'].loc[i]
    single_metadata['genre'] = metadata['genre'].loc[i]
    single_metadata['aired'] = metadata['aired'].loc[i]
    single_metadata['episodes'] = float(metadata['episodes'].loc[i])
    single_metadata['members'] = float(metadata['members'].loc[i])
    single_metadata['popularity'] = float(metadata['popularity'].loc[i])
    single_metadata['ranked'] = float(metadata['ranked'].loc[i])
    single_metadata['score'] = float(metadata['score'].loc[i])
    single_metadata['img_url'] = metadata['img_url'].loc[i]
    single_metadata['link'] = metadata['link'].loc[i]
    try:
        collection.add(
            documents=single_title,
            metadatas=single_metadata,
            ids=single_uid
        )
    except chromadb.errors.DuplicateIDError:
        print('already add')
        continue