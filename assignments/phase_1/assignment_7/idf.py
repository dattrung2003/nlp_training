import math
from collections import defaultdict


def tokenize(text: str) -> set[str]:
    return set(text.lower().split())


def document_frequency(documents: list[str]) -> dict[str, int]:
    df = defaultdict(int)
    for doc in documents:
        for term in tokenize(doc): 
            df[term] += 1
    return dict(df)


def compute_idf(
    documents: list[str],
    smooth: bool = False,
) -> dict[str, float]:
    N  = len(documents)
    df = document_frequency(documents)

    idf = {}
    for term, freq in df.items():
        if smooth:
            idf[term] = math.log((N + 1) / (freq + 1)) + 1
        else:
            idf[term] = math.log(N / freq)

    return dict(sorted(idf.items(), key=lambda x: x[1], reverse=True))


def print_df_table(df: dict[str, int], N: int) -> None:
    col = 10
    div = "  " + "─" * 40

    print(div)
    print(f"  {'Term':<{col}} {'df(t)':>{col}} {'df/N (%)':>{col}}")
    print(div)
    for term, freq in sorted(df.items(), key=lambda x: -x[1]):
        pct = (freq / N) * 100
        bar = "█" * freq
        print(f"  {term:<{col}} {freq:>{col}}   {pct:>{8}.1f}%   {bar}")
    print(div + "\n")


def print_idf_table(idf: dict[str, float], df: dict[str, int], N: int) -> None:
    col = 10
    div = "  " + "─" * 52

    print(div)
    print(f"  {'Term':<{col}} {'df(t)':>{col}} {'N/df(t)':>{col}} {'IDF':>{col}}")
    print(div)
    for term, score in idf.items():
        freq  = df[term]
        ratio = N / freq
        tag   = ""
        if score == 0.0:
            tag = "  ← log(1) = 0  [in every doc]"
        elif score == max(idf.values()):
            tag = "  ← highest IDF [rare]"
        print(f"  {term:<{col}} {freq:>{col}} {ratio:>{col}.1f} {score:>{col}.4f}{tag}")
    print(div + "\n")


def print_intuition(N: int) -> None:
    print("  Why common words score LOW and rare words score HIGH:\n")
    print(f"  IDF(t) = log( N / df(t) )   [N = {N} here]\n")

    cases = [
        ("in every doc",  N,     "df = N   → N/df = 1   → log(1) = 0.000"),
        ("very common",   N - 1, f"df = {N-1}   → N/df ≈ 1.x → small log"),
        ("half the docs", N // 2,f"df = {N//2}   → N/df = 2   → log(2) ≈ 0.693"),
        ("rare",          2,     "df = 2   → N/df = large → bigger log"),
        ("unique",        1,     "df = 1   → N/df = N   → log(N) = max"),
    ]

    col = 16
    div = "  " + "─" * 62
    print(div)
    print(f"  {'Scenario':<{col}} {'df':>6} {'N/df':>8} {'IDF':>8}   Formula hint")
    print(div)
    for label, df_val, hint in cases:
        ratio = N / df_val
        score = math.log(ratio)
        print(f"  {label:<{col}} {df_val:>6} {ratio:>8.2f} {score:>8.4f}   {hint}")
    print(div)



# Main 

if __name__ == "__main__":
    documents = [
        "NLP is fun",
        "I love NLP",
        "NLP NLP NLP",
        "deep learning is powerful",
        "I love deep learning",
    ]

    N  = len(documents)
    df = document_frequency(documents)
    idf = compute_idf(documents)

    print(f"\n📄 Corpus ({N} documents):")
    for i, doc in enumerate(documents):
        print(f"  D{i+1}: \"{doc}\"")

    print(f"\n📊 Document Frequency — df(t):")
    print_df_table(df, N)

    print("📐 IDF Scores — IDF(t) = log( N / df(t) ):")
    print_idf_table(idf, df, N)

    print("💡 Bonus — Intuition:")
    print_intuition(N)

    idf_smooth = compute_idf(documents, smooth=True)
    print("🔧 Smoothed IDF (avoids zero for universal terms):\n")
    col = 10
    div = "  " + "─" * 38
    print(div)
    print(f"  {'Term':<{col}} {'Raw IDF':>{col}} {'Smooth IDF':>{col}}")
    print(div)
    all_terms = sorted(idf.keys(), key=lambda t: -idf[t])
    for term in all_terms:
        print(f"  {term:<{col}} {idf[term]:>{col}.4f} {idf_smooth[term]:>{col}.4f}")
    print(div + "\n")