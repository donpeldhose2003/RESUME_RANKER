from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def rank_resumes(jd_text, resume_tuples):
    filenames = [fname for fname, _ in resume_tuples]
    docs = [text for _, text in resume_tuples]
    all_texts = [jd_text] + docs

    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform(all_texts)
    similarity_scores = cosine_similarity(vectors[0:1], vectors[1:]).flatten()

    ranked = sorted(zip(filenames, similarity_scores), key=lambda x: x[1], reverse=True)
    return ranked
