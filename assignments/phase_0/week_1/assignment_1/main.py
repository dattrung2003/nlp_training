from collections import Counter

def word_frequency(documents):
    """
    documents: list[str]
    return: dict chứa tần suất xuất hiện của các từ
    """
    freq = Counter()

    for doc in documents:
        words = doc.lower().split()
        freq.update(words)

    return dict(freq)


documents = [
    "the quick brown fox",
    "the lazy dog sleeps",
    "the fox jumps over the dog"
]

result = word_frequency(documents)

for word, count in result.items():
    print(f"{word}: {count}")