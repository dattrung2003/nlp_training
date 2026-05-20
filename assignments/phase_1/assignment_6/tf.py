import re

def clean_and_tokenize(text):
    text = text.lower()
    return re.findall(r'\b\w+\b', text)

def compute_term_frequency(corpus):
    tokenized_corpus = [clean_and_tokenize(doc) for doc in corpus]
    
    unique_words = set(word for doc in tokenized_corpus for word in doc)
    vocabulary = sorted(list(unique_words))
    
    tf_matrix = []
    for doc in tokenized_corpus:
        total_words_in_doc = len(doc)
        
        if total_words_in_doc == 0:
            tf_matrix.append([0.0] * len(vocabulary))
            continue
            
        word_counts = {}
        for word in doc:
            word_counts[word] = word_counts.get(word, 0) + 1
            
        doc_tf_vector = []
        for word in vocabulary:
            count = word_counts.get(word, 0)
            tf_value = count / total_words_in_doc
            doc_tf_vector.append(round(tf_value, 4)) 
            
        tf_matrix.append(doc_tf_vector)
        
    return tf_matrix, vocabulary

# --- Test ---
corpus = [
    "The cat sat on the mat",
    "The dog chased the cat"
]

tf_matrix, vocabulary = compute_term_frequency(corpus)

print("Vocabulary:")
print(vocabulary)
print("\nTerm Frequency (TF) Matrix:")
for i, vector in enumerate(tf_matrix):
    print(f"Doc {i+1}: {vector}")