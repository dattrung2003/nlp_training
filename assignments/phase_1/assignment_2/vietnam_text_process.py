import re
import html
from pathlib import Path

from underthesea import sent_tokenize
from underthesea import word_tokenize as underthesea_word_tokenize
from pyvi import ViTokenizer


_EMOJI_RE = re.compile(
    "["
    "\U0001F600-\U0001F64F"   # emoticons
    "\U0001F300-\U0001F5FF"   # symbols & pictographs
    "\U0001F680-\U0001F6FF"   # transport & map
    "\U0001F1E0-\U0001F1FF"   # flags
    "\U00002700-\U000027BF"   # dingbats
    "\U0001F900-\U0001F9FF"   # supplemental symbols
    "\U00002600-\U000026FF"   # misc symbols
    "\U00002B50-\U00002B55"
    "\U0001FA00-\U0001FA6F"
    "\U0001FA70-\U0001FAFF"
    "]+",
    flags=re.UNICODE,
)

_URL_RE  = re.compile(r"https?://\S+|www\.\S+", re.IGNORECASE)
_HTML_RE = re.compile(r"<[^>]+>")
_PUNCT_RE = re.compile(r"[^\w\s]", re.UNICODE)   # keeps letters, digits, _
_WS_RE   = re.compile(r"\s+")


class VietnameseTextProcessor:
    def __init__(
        self,
        stopwords_path: str | Path | None = None,
        use_pyvi: bool = False,
    ):
        self.use_pyvi = use_pyvi
        self.stopwords: set[str] = set()

        if stopwords_path is not None:
            self.load_stopwords(stopwords_path)


    def load_stopwords(self, path: str | Path) -> None:
        """Load stopwords from a .txt file (one word per line, # = comment)."""
        path = Path(path)
        if not path.exists():
            raise FileNotFoundError(f"Stopword file not found: {path}")

        with path.open(encoding="utf-8") as fh:
            words = {
                line.strip().lower()
                for line in fh
                if line.strip() and not line.startswith("#")
            }
        self.stopwords = words
        print(f"[INFO] Loaded {len(self.stopwords)} stopwords from '{path}'.")


    def remove_html(self, text: str) -> str:
        """
        Strip HTML/XML tags and decode HTML entities.
        """
        text = _HTML_RE.sub(" ", text)   # remove tags
        text = html.unescape(text)        # decode &amp; &lt; etc.
        return text

    def remove_urls(self, text: str) -> str:
        """
        Remove http/https URLs and bare www.* links.
        """
        return _URL_RE.sub(" ", text)

    def remove_emojis(self, text: str) -> str:
        """
        Remove Unicode emoji characters.
        """
        return _EMOJI_RE.sub(" ", text)

    def remove_punctuation(self, text: str) -> str:
        """
        Remove all punctuation (keeps letters, digits, whitespace, underscore).
        """
        return _PUNCT_RE.sub(" ", text)

    def lowercase(self, text: str) -> str:
        """Convert text to lowercase (works for both ASCII and Vietnamese)."""
        return text.lower()

    def normalize_whitespace(self, text: str) -> str:
        """Collapse multiple spaces / tabs / newlines into a single space."""
        return _WS_RE.sub(" ", text).strip()

    def sentence_tokenize(self, text: str) -> list[str]:
        """
        Split text into sentences using underthesea's Vietnamese sentence
        tokenizer.

        Returns a list of sentence strings.
        """
        return sent_tokenize(text)

    def word_tokenize(self, text: str) -> list[str]:
        """
        Tokenize text into words.

        """
        if self.use_pyvi:
            tokenized = ViTokenizer.tokenize(text)   # returns 'word_word' style
            return tokenized.split()

        tokens = underthesea_word_tokenize(text)
        return [t.replace(" ", "_") for t in tokens]


    def remove_stopwords(self, tokens: list[str]) -> list[str]:
        """
        Remove tokens that appear in the loaded stopword set.
        """
        if not self.stopwords:
            return tokens

        filtered = []
        for tok in tokens:
            normalised = tok.replace("_", " ").lower()
            if normalised not in self.stopwords and tok.lower() not in self.stopwords:
                filtered.append(tok)
        return filtered

    def preprocess(
        self,
        text: str,
        *,
        remove_stopwords: bool = True,
        return_sentences: bool = False,
    ) -> dict:
        """
        Run the complete preprocessing pipeline.

        Steps
        -----
        1.  Remove HTML tags & decode entities
        2.  Remove URLs
        3.  Sentence-tokenize  ← captured before further cleaning
        4.  Remove emojis
        5.  Lowercase
        6.  Remove punctuation
        7.  Normalize whitespace
        8.  Word-tokenize
        9.  Remove stopwords (optional)
        10. Rebuild final text string

        Parameters
        ----------
        text : str
            Raw input text.
        remove_stopwords : bool
            Whether to apply stopword filtering (default True).
        return_sentences : bool
            If True, include per-sentence token lists in the result.

        Returns
        -------
        dict with keys:
            sentences   – list of raw sentence strings
            tokens      – final token list (after all cleaning)
            final_text  – space-joined token string
            (sentences_tokens – optional, per-sentence token lists)
        """
        # ── 1. HTML ──────────────────────────────────────────────────────
        text = self.remove_html(text)

        # ── 2. URLs ──────────────────────────────────────────────────────
        clean_for_sent = self.normalize_whitespace(text)  # tidy before split
        url_removed    = self.remove_urls(text)

        # ── 3. Sentence tokenization (on HTML/URL-cleaned but otherwise raw) ──
        sentences = self.sentence_tokenize(clean_for_sent)

        # ── 4-7. Deep cleaning ────────────────────────────────────────────
        clean = self.remove_emojis(url_removed)
        clean = self.lowercase(clean)
        clean = self.remove_punctuation(clean)
        clean = self.normalize_whitespace(clean)

        # ── 8. Word tokenization ──────────────────────────────────────────
        tokens = self.word_tokenize(clean)

        # ── 9. Stopword removal ───────────────────────────────────────────
        if remove_stopwords:
            tokens = self.remove_stopwords(tokens)

        # ── 10. Rebuild text ──────────────────────────────────────────────
        final_text = " ".join(tokens)

        result = {
            "sentences":  sentences,
            "tokens":     tokens,
            "final_text": final_text,
        }

        if return_sentences:
            sentence_tokens = []
            for sent in sentences:
                s = self.remove_emojis(self.remove_urls(sent))
                s = self.lowercase(s)
                s = self.remove_punctuation(s)
                s = self.normalize_whitespace(s)
                toks = self.word_tokenize(s)
                if remove_stopwords:
                    toks = self.remove_stopwords(toks)
                sentence_tokens.append(toks)
            result["sentence_tokens"] = sentence_tokens

        return result




# def _banner(title: str) -> None:
#     print(f"\n{'─' * 52}")
#     print(f"  {title}")
#     print(f"{'─' * 52}")


# if __name__ == "__main__":

#     sample_en = """\
# <p>Hello!!!</p>
# I am learning NLP 😄
# Visit https://abc.com now!!!
# """

#     sample_vi = """\
# <b>Chào mừng</b> bạn đến với khóa học NLP! 🎉
# Hãy truy cập https://example.com để xem thêm.
# Xử lý ngôn ngữ tự nhiên rất thú vị và hữu ích.
# """

#     STOPWORDS = Path("vietnamese_stopwords.txt")

#     _banner("English sample — no stopwords")
#     proc = VietnameseTextProcessor()
#     result = proc.preprocess(sample_en, remove_stopwords=False)

#     print("Sentences:")
#     for s in result["sentences"]:
#         print(f"  {repr(s)}")
#     print("\nTokens:")
#     print(" ", result["tokens"])
#     print("\nFinal text:")
#     print(" ", result["final_text"])

#     _banner("Vietnamese sample — with stopword removal")
#     proc_vi = VietnameseTextProcessor(stopwords_path=STOPWORDS)
#     result_vi = proc_vi.preprocess(sample_vi, remove_stopwords=True,
#                                    return_sentences=True)

#     print("Sentences:")
#     for s in result_vi["sentences"]:
#         print(f"  {repr(s)}")

#     print("\nPer-sentence tokens:")
#     for i, toks in enumerate(result_vi["sentence_tokens"], 1):
#         print(f"  [{i}] {toks}")

#     print("\nAll tokens (stopwords removed):")
#     print(" ", result_vi["tokens"])

#     print("\nFinal text:")
#     print(" ", result_vi["final_text"])

#     _banner("Step-by-step walkthrough")
#     p = VietnameseTextProcessor()
#     raw = '<p>Hello!!!</p>\nI am learning NLP 😄\nVisit https://abc.com now!!!'
#     print(f"0. Raw       : {repr(raw)}")
#     s = p.remove_html(raw);         print(f"1. HTML      : {repr(s)}")
#     s = p.remove_urls(s);           print(f"2. URLs      : {repr(s)}")
#     s = p.remove_emojis(s);         print(f"3. Emojis    : {repr(s)}")
#     s = p.lowercase(s);             print(f"4. Lowercase : {repr(s)}")
#     s = p.remove_punctuation(s);    print(f"5. Punct     : {repr(s)}")
#     s = p.normalize_whitespace(s);  print(f"6. Spaces    : {repr(s)}")
#     t = p.word_tokenize(s);         print(f"7. Tokens    : {t}")