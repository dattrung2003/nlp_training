import math
import re

def clean_and_tokenize(text, return_set=False):
    words = re.findall(r'\b\w+\b', text.lower())
    return set(words) if return_set else words

def compute_tfidf(corpus):
    num_documents = len(corpus)
    
    tokenized_corpus_tf = [clean_and_tokenize(doc, return_set=False) for doc in corpus]
    tokenized_corpus_idf = [clean_and_tokenize(doc, return_set=True) for doc in corpus]
    
    unique_words = set(word for doc in tokenized_corpus_tf for word in doc)
    vocabulary = sorted(list(unique_words))
    
    document_frequencies = {word: 0 for word in vocabulary}
    for doc_words in tokenized_corpus_idf:
        for word in doc_words:
            document_frequencies[word] += 1
            
    idf_weights = {}
    for word in vocabulary:
        df = document_frequencies[word]
        idf_value = math.log((1 + num_documents) / (1 + df)) + 1
        idf_weights[word] = idf_value

    tfidf_matrix = []
    
    for doc in tokenized_corpus_tf:
        total_words_in_doc = len(doc)
        
        doc_tfidf_vector = []
        
        if total_words_in_doc == 0:
            tfidf_matrix.append([0.0] * len(vocabulary))
            continue
            
        word_counts = {}
        for word in doc:
            word_counts[word] = word_counts.get(word, 0) + 1
            
        for word in vocabulary:
            count = word_counts.get(word, 0)
            tf_value = count / total_words_in_doc
            
            idf_value = idf_weights[word]
            
            tfidf_value = tf_value * idf_value
            doc_tfidf_vector.append(round(tfidf_value, 4)) 
            
        tfidf_matrix.append(doc_tfidf_vector)
        
    return tfidf_matrix, vocabulary

# --- Test ---
corpus_test = [
    "The cat sat on the mat",
    "The dog chased the cat",
    "Deep learning is awesome"
]

tfidf_matrix, vocab = compute_tfidf(corpus_test)

print("Vocabulary chung:")
print(vocab)
print("\nMa trận TF-IDF kết quả:")
for i, vector in enumerate(tfidf_matrix):
    print(f"Doc {i+1}: {vector}")