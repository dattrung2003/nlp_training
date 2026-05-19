import re

class SentenceOneHotEncoder:
    def __init__(self, max_seq_len=None, padding='post', truncation='post'):
        """
        Args:
            max_seq_len (int): Maximum length of the sequence.
            padding (str): 'pre' or 'post' padding with zero vectors.
            truncation (str): 'pre' or 'post' truncation if length exceeds max_seq_len.
        """
        self.max_seq_len = max_seq_len
        self.padding = padding
        self.truncation = truncation
        self.vocab = []
        self.word_to_idx = {}
        
    def _tokenize(self, text):
        return re.findall(r'\b\w+\b', text.lower())

    def fit(self, corpus):
        unique_words = set()
        for sentence in corpus:
            unique_words.update(self._tokenize(sentence))
        
        # Sort vocabulary for consistent index positioning
        self.vocab = sorted(list(unique_words))
        self.word_to_idx = {word: idx for idx, word in enumerate(self.vocab)}
        return self

    def transform(self, sentence):
        tokens = self._tokenize(sentence)
        vocab_size = len(self.vocab)
        
        if vocab_size == 0:
            raise ValueError("Vocabulary is empty. Please run .fit() first.")

        # 1. Map tokens to their respective one-hot vectors
        one_hot_sequence = []
        for token in tokens:
            if token in self.word_to_idx:
                # Create a blank zero vector matching vocabulary dimensions
                vector = [0] * vocab_size
                vector[self.word_to_idx[token]] = 1
                one_hot_sequence.append(vector)
            else:
                # Out-Of-Vocabulary (OOV) tokens get a clean zero vector
                one_hot_sequence.append([0] * vocab_size)

        # 2. Handle Truncation if sequence is too long
        if self.max_seq_len and len(one_hot_sequence) > self.max_seq_len:
            if self.truncation == 'post':
                one_hot_sequence = one_hot_sequence[:self.max_seq_len]
            elif self.truncation == 'pre':
                one_hot_sequence = one_hot_sequence[-self.max_seq_len:]

        # 3. Handle Padding if sequence is too short
        if self.max_seq_len and len(one_hot_sequence) < self.max_seq_len:
            pad_count = self.max_seq_len - len(one_hot_sequence)
            zero_vector = [0] * vocab_size
            pad_vectors = [zero_vector for _ in range(pad_count)]
            
            if self.padding == 'post':
                one_hot_sequence.extend(pad_vectors)
            elif self.padding == 'pre':
                one_hot_sequence = pad_vectors + one_hot_sequence

        return one_hot_sequence