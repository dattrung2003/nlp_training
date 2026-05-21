from collections import Counter


def build_vocabulary(documents: list[str]) -> list[str]:
    seen = {}
    for doc in documents:
        for token in tokenize(doc):
            if token not in seen:
                seen[token] = len(seen)          
    return sorted(seen, key=lambda t: seen[t])   


def tokenize(text: str) -> list[str]:
    return text.lower().split()



def word_frequency(document: str) -> Counter:
    return Counter(tokenize(document))


def bow_matrix(
    documents: list[str],
    mode: str = "count",          
) -> tuple[list[list[int]], list[str]]:
    """
    Build the document-term matrix.

    Returns
    -------
    matrix : list[list[int]]
        Rows = documents, columns = vocabulary terms.
    vocab  : list[str]
        Ordered vocabulary (column labels).
    """
    if mode not in ("count", "binary"):
        raise ValueError(f"mode must be 'count' or 'binary', got '{mode}'")

    vocab = build_vocabulary(documents)
    vocab_index = {term: i for i, term in enumerate(vocab)}

    matrix = []
    for doc in documents:
        freq = word_frequency(doc)
        row = [freq.get(term, 0) for term in vocab]

        if mode == "binary":
            row = [1 if v > 0 else 0 for v in row]

        matrix.append(row)

    return matrix, vocab


# Demo 

def pretty_print(matrix: list[list[int]], vocab: list[str], title: str) -> None:
    col_w = max(len(t) for t in vocab) + 2
    header = "".join(t.ljust(col_w) for t in vocab)
    print(f"\n{'─' * 40}")
    print(f"  {title}")
    print(f"{'─' * 40}")
    print(f"  {''.ljust(4)}{header}")
    for i, row in enumerate(matrix):
        cells = "".join(str(v).ljust(col_w) for v in row)
        print(f"  D{i+1}  {cells}")
    print(f"{'─' * 40}")
    print(f"  Matrix : {matrix}")
    print(f"  Vocab  : {vocab}\n")


if __name__ == "__main__":
    documents = [
        "NLP is fun",
        "I love NLP",
        "NLP NLP NLP",
    ]

    print("\n📄 Documents:")
    for i, doc in enumerate(documents):
        print(f"  D{i+1}: \"{doc}\"")

    vocab = build_vocabulary(documents)
    print(f"\n📚 Vocabulary ({len(vocab)} terms): {vocab}")

    print("\n📊 Word Frequencies:")
    for i, doc in enumerate(documents):
        print(f"  D{i+1}: {dict(word_frequency(doc))}")

    count_matrix, vocab = bow_matrix(documents, mode="count")
    pretty_print(count_matrix, vocab, "Count BoW")

    binary_matrix, _ = bow_matrix(documents, mode="binary")
    pretty_print(binary_matrix, vocab, "Binary BoW")