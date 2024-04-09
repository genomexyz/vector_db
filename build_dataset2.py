import chromadb
import pandas as pd
import hashlib
#from sentence_transformers import SentenceTransformer
#embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
#
#class MyEmbeddingFunction(EmbeddingFunction):
#    def __call__(self, input: Documents) -> Embeddings:
#        batch_embeddings = embedding_model.encode(input)
#        return batch_embeddings.tolist()
#
#embed_fn = MyEmbeddingFunction()

def generate_uid(input_string):
    # Create a SHA-256 hash object
    hash_object = hashlib.sha256()
    
    # Update the hash object with the input string
    hash_object.update(input_string.encode())
    
    # Generate the hexadecimal representation of the hash
    uid = hash_object.hexdigest()
    
    return uid

dset_anime = pd.read_csv('dset/animes.csv')
print(dset_anime)
print(dset_anime.keys())

dset_review = pd.read_csv('dset/reviews.csv')
print(dset_review)
print(dset_review.keys())

client = chromadb.PersistentClient(path="./animedb")

# create collection
collection = client.get_or_create_collection(
    name=f"animereview"
)


limit_review = 20
history_anime = {}
for i in range(len(dset_review)):
    print('cek progress %s/%s'%(i+1, len(dset_review)))
    single_review = dset_review['text'].loc[i]
    single_review_uid = generate_uid(single_review)
    filtered_anime = dset_anime[dset_anime['uid'] == dset_review['anime_uid'].loc[i]]
    if len(filtered_anime) == 0:
        continue
    single_anime = list(filtered_anime['title'])[0]
    single_anime_synopsis = list(filtered_anime['synopsis'])[0]
    anime_detail = '''
title:%s
synopsis: %s
'''%(single_anime, single_anime_synopsis)
    single_review += '\n' + anime_detail

    single_metadata = {'title': single_anime}

    try:
        history_anime[single_anime] += 1
        if history_anime[single_anime] > limit_review:
            print('too much review for %s, skipped'%(single_anime))
            continue
    except KeyError:
        history_anime[single_anime] = 1

    try:
        collection.add(
            documents=single_review,
            metadatas=single_metadata,
            ids=single_review_uid
        )
    except chromadb.errors.DuplicateIDError:
        print('already add')
        continue
    except chromadb.errors.IDAlreadyExistsError as id_error:
        print(f"already add => {id_error}")
        continue
    #print(filtered_anime, len(filtered_anime))