import re
from collections import Counter


class WhitespaceTokenizer:

    def lowercase(self, text: str) -> str:
        return text.lower()

    def normalize_whitespace(self, text: str) -> str:
        return re.sub(r'\s+', ' ', text).strip()

    def tokenize(self, text: str) -> list[str]:
        text = self.lowercase(text)
        text = self.normalize_whitespace(text)
        return text.split()


    def remove_punctuation(self, text: str) -> str:
        return re.sub(r'[^\w\s]', '', text)

    def tokenize_clean(self, text: str) -> list[str]:
        text = self.lowercase(text)
        text = self.remove_punctuation(text)
        text = self.normalize_whitespace(text)
        return text.split()

    def token_frequency(self, tokens: list[str]) -> dict[str, int]:
        return dict(Counter(tokens))

    def batch_tokenize(self, texts: list[str], clean: bool = False) -> list[list[str]]:
        """
        Tokenize a list of strings.

        Args:
            texts: List of raw input strings.
            clean: If True, also removes punctuation before splitting.

        Returns:
            A list of token lists, one per input string.
        """
        fn = self.tokenize_clean if clean else self.tokenize
        return [fn(text) for text in texts]



# if __name__ == "__main__":
#     tokenizer = WhitespaceTokenizer()

#     sample = "Hello world!   \nNLP is fun.\n"
#     print("INPUT :", repr(sample))

#     step1 = tokenizer.lowercase(sample)
#     print("\nStep 1 – lowercase         :", repr(step1))

#     step2 = tokenizer.normalize_whitespace(step1)
#     print("Step 2 – normalize spaces  :", repr(step2))

#     tokens = tokenizer.tokenize(sample)
#     print("Step 3 – split             :", tokens)

#     print("Tokenize_clean (punctuation removed):")
#     print(tokenizer.tokenize_clean(sample))

#     freq_text = "the cat sat on the mat the cat"
#     freq_tokens = tokenizer.tokenize(freq_text)
#     print("Token_frequency:")
#     print("Tokens :", freq_tokens)
#     print("Freq   :", tokenizer.token_frequency(freq_tokens))

#     batch = [
#         "I love NLP",
#         "Tokenization is easy",
#     ]
#     print("Batch_tokenize:")
#     for raw, toks in zip(batch, tokenizer.batch_tokenize(batch)):
#         print(f"  {repr(raw):30s} → {toks}")

#     print("\n Batch_tokenize (clean=True, punctuation removed):")
#     messy_batch = ["Hello, World!", "NLP is fun -- really fun."]
#     for raw, toks in zip(messy_batch, tokenizer.batch_tokenize(messy_batch, clean=True)):
#         print(f"  {repr(raw):35s} → {toks}")