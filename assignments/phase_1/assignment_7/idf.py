import math
import re

def clean_and_tokenize(text):
    text = text.lower()
    return set(re.findall(r'\b\w+\b', text))

def compute_inverse_document_frequency(corpus):
    num_documents = len(corpus)
    
    tokenized_corpus = [clean_and_tokenize(doc) for doc in corpus]
    
    unique_words = set(word for doc in tokenized_corpus for word in doc)
    vocabulary = sorted(list(unique_words))
    
    document_frequencies = {word: 0 for word in vocabulary}
    for doc_words in tokenized_corpus:
        for word in doc_words:
            document_frequencies[word] += 1
            
    idf_weights = {}
    for word in vocabulary:
        df = document_frequencies[word]
        idf_value = math.log((1 + num_documents) / (1 + df)) + 1
        idf_weights[word] = round(idf_value, 4) 
        
    return idf_weights, vocabulary

# --- Test ---
corpus = [
    "The cat sat on the mat",
    "The dog chased the cat",
    "Deep learning is awesome"
]

idf_dictionary, vocabulary = compute_inverse_document_frequency(corpus)

print("Vocabulary & Their Computed IDF Weights:")
print("-" * 40)
for word, idf_val in idf_dictionary.items():
    print(f"{word:<12} -> IDF: {idf_val}")