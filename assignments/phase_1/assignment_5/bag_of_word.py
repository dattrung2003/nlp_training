import re

def clean_and_tokenize(text):
    """Lowers the text and splits it into words, removing punctuation."""
    text = text.lower()
    words = re.findall(r'\b\w+\b', text)
    return words

def build_bow(corpus):
    tokenized_corpus = [clean_and_tokenize(doc) for doc in corpus]
    
    unique_words = set()
    for doc in tokenized_corpus:
        unique_words.update(doc)
    
    vocabulary = sorted(list(unique_words))
    
    word_to_index = {word: idx for idx, word in enumerate(vocabulary)}
    
    bow_matrix = []
    for doc in tokenized_corpus:
        doc_vector = [0] * len(vocabulary)
        
        for word in doc:
            if word in word_to_index:
                idx = word_to_index[word]
                doc_vector[idx] += 1
                
        bow_matrix.append(doc_vector)
        
    return bow_matrix, vocabulary

# --- Test ---
corpus = [
    "The cat sat on the mat.",
    "The dog chased the cat!",
    "Mad cats and mad dogs."
]

bow_matrix, vocabulary = build_bow(corpus)

print("Vocabulary (Features):")
print(vocabulary)
print("\nBag-of-Words Vectors:")
for i, vector in enumerate(bow_matrix):
    print(f"Doc {i+1}: {vector}")