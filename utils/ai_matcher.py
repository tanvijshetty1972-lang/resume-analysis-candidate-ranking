from sentence_transformers import SentenceTransformer, util

# Load once
model = SentenceTransformer('all-MiniLM-L6-v2')

def semantic_similarity(text1, text2):
    embeddings1 = model.encode(text1, convert_to_tensor=True)
    embeddings2 = model.encode(text2, convert_to_tensor=True)
    cosine_score = util.cos_sim(embeddings1, embeddings2).item()
    return round(cosine_score * 100, 2)
