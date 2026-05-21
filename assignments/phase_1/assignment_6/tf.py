from collections import Counter

def tokenize(text: str) -> list[str]:
    return text.lower().split()


def raw_count(document: str) -> dict[str, int]:
    return dict(Counter(tokenize(document)))


def term_frequency(document: str) -> dict[str, float]:
    tokens = tokenize(document)
    total  = len(tokens)

    if total == 0:
        return {}

    counts = Counter(tokens)
    return {term: count / total for term, count in counts.items()}


def compare(document: str) -> None:
    tokens  = tokenize(document)
    total   = len(tokens)
    counts  = raw_count(document)
    tf      = term_frequency(document)

    col = 10   

    print(f"\n  Document : \"{document}\"")
    print(f"  Tokens   : {tokens}")
    print(f"  Total    : {total}\n")

    header = f"  {'Term':<{col}} {'Raw Count':>{col}} {'TF (norm)':>{col}}"
    div    = "  " + "─" * (len(header) - 2)

    print(div)
    print(f"  {'Term':<{col}} {'Raw Count':>{col}} {'Normalized TF':>{col}}")
    print(div)

    for term in counts:                     
        raw = counts[term]
        tf_val = tf[term]
        bar = "█" * raw                       
        print(f"  {term:<{col}} {raw:>{col}}     {tf_val:>{col}.4f}   {bar}")

    print(div)
    total_tf = sum(tf.values())
    print(f"  {'TOTAL':<{col}} {total:>{col}}     {total_tf:>{col}.4f}   ← always sums to 1.0\n")


# Main

if __name__ == "__main__":
    document = "NLP NLP is fun"

    tf = term_frequency(document)
    print("\n📐 TF Result:")
    print(f"  {tf}")

    print("\n📊 Raw Count vs Normalized TF:")
    compare(document)

    print("─" * 55)
    print("  Effect of document length on raw count vs TF\n")
    print("  Same topic, different lengths — TF stays stable:\n")

    docs = {
        "short"  : "NLP is fun",
        "medium" : "NLP NLP is fun",
        "long"   : "NLP NLP NLP NLP is fun fun fun fun fun",
    }

    col = 8
    print(f"  {'Doc':<8} {'nlp raw':>{col}} {'nlp TF':>{col}}   {'fun raw':>{col}} {'fun TF':>{col}}")
    print("  " + "─" * 48)
    for label, doc in docs.items():
        rc = raw_count(doc)
        tf = term_frequency(doc)
        print(
            f"  {label:<8}"
            f" {rc.get('nlp', 0):>{col}}"
            f" {tf.get('nlp', 0.0):>{col}.4f}"
            f"   {rc.get('fun', 0):>{col}}"
            f" {tf.get('fun', 0.0):>{col}.4f}"
        )
    print()
    print("  ↑ Raw count grows with length; TF reflects true proportion.\n")