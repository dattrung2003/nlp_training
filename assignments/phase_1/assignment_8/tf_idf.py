import math
from collections import Counter

def tokenize(text: str) -> list[str]:
    return text.lower().split()


def build_vocabulary(documents: list[str]) -> list[str]:
    seen: dict[str, int] = {}
    for doc in documents:
        for token in tokenize(doc):
            if token not in seen:
                seen[token] = len(seen)
    return sorted(seen, key=lambda t: seen[t])

def compute_tf(document: str) -> dict[str, float]:
    tokens = tokenize(document)
    total  = len(tokens)
    return {term: count / total for term, count in Counter(tokens).items()}

def compute_df(documents: list[str]) -> dict[str, int]:
    """df(t) = number of documents containing term t."""
    df: dict[str, int] = {}
    for doc in documents:
        for term in set(tokenize(doc)):   
            df[term] = df.get(term, 0) + 1
    return df


def compute_idf(
    documents: list[str],
    smooth: bool = False,
) -> dict[str, float]:
    N  = len(documents)
    df = compute_df(documents)
    if smooth:
        return {t: math.log((N + 1) / (f + 1)) + 1 for t, f in df.items()}
    return {t: math.log(N / f) for t, f in df.items()}

def l2_normalize(vector: list[float]) -> list[float]:
    """Scale vector to unit length: v / ||v||₂"""
    norm = math.sqrt(sum(v ** 2 for v in vector))
    return [v / norm for v in vector] if norm > 0 else vector


def tfidf_matrix(
    documents: list[str],
    smooth: bool    = False,
    normalize: bool = False,
) -> tuple[list[list[float]], list[str]]:
    vocab  = build_vocabulary(documents)
    idf    = compute_idf(documents, smooth=smooth)

    matrix = []
    for doc in documents:
        tf  = compute_tf(doc)
        row = [tf.get(term, 0.0) * idf.get(term, 0.0) for term in vocab]
        if normalize:
            row = l2_normalize(row)
        matrix.append(row)

    return matrix, vocab

def print_matrix(
    matrix: list[list[float]],
    vocab:  list[str],
    documents: list[str],
    title: str,
) -> None:
    col   = max(len(t) for t in vocab) + 2
    div   = "  " + "─" * (4 + col * len(vocab))

    print(f"\n{'─'*55}")
    print(f"  {title}")
    print(f"{'─'*55}")
    header = "".join(f"{t:^{col}}" for t in vocab)
    print(f"  {'':4}{header}")
    print(div)
    for i, (row, doc) in enumerate(zip(matrix, documents)):
        cells = "".join(f"{v:^{col}.4f}" for v in row)
        print(f"  D{i+1}  {cells}   \"{doc}\"")
    print(div)


def print_vocab(vocab: list[str]) -> None:
    print("\n📚 Vocabulary mapping:")
    div = "  " + "─" * 30
    print(div)
    print(f"  {'Index':>6}   {'Term'}")
    print(div)
    for i, term in enumerate(vocab):
        print(f"  {i:>6}   {term}")
    print(div)


def print_scores(
    matrix: list[list[float]],
    vocab:  list[str],
    documents: list[str],
    title: str = "Per-document TF-IDF breakdown",
) -> None:
    print(f"\n🔍 {title}:")
    for i, (row, doc) in enumerate(zip(matrix, documents)):
        print(f"\n  D{i+1}: \"{doc}\"")
        scores = sorted(
            ((vocab[j], row[j]) for j in range(len(vocab)) if row[j] > 0),
            key=lambda x: -x[1],
        )
        for term, score in scores:
            bar = "█" * int(score * 40)
            print(f"    {term:<14} {score:.4f}  {bar}")

# Main
if __name__ == "__main__":
    documents = [
        "I love NLP",
        "NLP is fun",
        "I love machine learning",
    ]

    print("\n📄 Corpus:")
    for i, doc in enumerate(documents):
        print(f"  D{i+1}: \"{doc}\"")

    vocab = build_vocabulary(documents)
    print_vocab(vocab)

    idf_raw    = compute_idf(documents, smooth=False)
    idf_smooth = compute_idf(documents, smooth=True)

    print("\n📐 IDF scores (raw vs smoothed):")
    div = "  " + "─" * 40
    print(div)
    print(f"  {'Term':<14} {'Raw IDF':>10} {'Smooth IDF':>12}")
    print(div)
    for term in vocab:
        print(
            f"  {term:<14}"
            f" {idf_raw.get(term, 0):>10.4f}"
            f" {idf_smooth.get(term, 0):>12.4f}"
        )
    print(div)

    raw_matrix, vocab = tfidf_matrix(documents, smooth=False, normalize=False)
    print_matrix(raw_matrix, vocab, documents, "TF-IDF Matrix (raw)")
    print_scores(raw_matrix, vocab, documents)

    smooth_matrix, _ = tfidf_matrix(documents, smooth=True, normalize=False)
    print_matrix(smooth_matrix, vocab, documents, "TF-IDF Matrix (smoothed IDF)")

    norm_matrix, _ = tfidf_matrix(documents, smooth=True, normalize=True)
    print_matrix(norm_matrix, vocab, documents, "TF-IDF Matrix (smoothed + L2 norm)")

    print("\n✅ L2-norm check — each row should equal 1.0:")
    for i, row in enumerate(norm_matrix):
        length = math.sqrt(sum(v ** 2 for v in row))
        print(f"  D{i+1}  ||v|| = {length:.6f}")

    print("\n📊 'nlp' score across all three modes:")
    idx = vocab.index("nlp")
    div = "  " + "─" * 48
    print(div)
    print(f"  {'Doc':<26} {'Raw':>8} {'Smooth':>8} {'Norm':>8}")
    print(div)
    for i, doc in enumerate(documents):
        print(
            f"  D{i+1}: {doc:<22}"
            f" {raw_matrix[i][idx]:>8.4f}"
            f" {smooth_matrix[i][idx]:>8.4f}"
            f" {norm_matrix[i][idx]:>8.4f}"
        )
    print(div + "\n")