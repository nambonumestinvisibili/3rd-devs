import re
from typing import List, Dict, Any, Optional

# Placeholder for tokenizer import and initialization
# You should replace this with your actual tokenizer logic, e.g. tiktoken or transformers
class DummyTokenizer:
    def __init__(self, model_name: str, special_tokens: Dict[str, int]):
        self.model_name = model_name
        self.special_tokens = special_tokens

    def encode(self, text: str, special_tokens: List[str]) -> List[int]:
        # Dummy implementation: 1 token per 4 chars
        return [0] * max(1, len(text) // 4)

def create_by_model_name(model_name: str, special_tokens: Dict[str, int]):
    # Replace with actual tokenizer creation logic
    return DummyTokenizer(model_name, special_tokens)

class TextSplitter:
    def __init__(self, model_name: str = "gpt-4o"):
        self.MODEL_NAME = model_name
        self.SPECIAL_TOKENS = {
            "<|im_start|>": 100264,
            "<|im_end|>": 100265,
            "<|im_sep|>": 100266,
        }
        self.tokenizer: Optional[DummyTokenizer] = None

    def initialize_tokenizer(self):
        if not self.tokenizer:
            self.tokenizer = create_by_model_name(self.MODEL_NAME, self.SPECIAL_TOKENS)

    def format_for_tokenization(self, text: str) -> str:
        return f"<|im_start|>user\n{text}<|im_end|>\n<|im_start|>assistant<|im_end|>"

    def count_tokens(self, text: str) -> int:
        if not self.tokenizer:
            raise Exception("Tokenizer not initialized")
        formatted_content = self.format_for_tokenization(text)
        tokens = self.tokenizer.encode(formatted_content, list(self.SPECIAL_TOKENS.keys()))
        return len(tokens)

    def split(self, text: str, limit: int) -> List[Dict[str, Any]]:
        print(f"Starting split process with limit: {limit} tokens")
        self.initialize_tokenizer()
        chunks = []
        position = 0
        total_length = len(text)
        current_headers: Dict[str, List[str]] = {}

        while position < total_length:
            print(f"Processing chunk starting at position: {position}")
            chunk_text, chunk_end = self.get_chunk(text, position, limit)
            tokens = self.count_tokens(chunk_text)
            print(f"Chunk tokens: {tokens}")

            headers_in_chunk = self.extract_headers(chunk_text)
            self.update_current_headers(current_headers, headers_in_chunk)

            content, urls, images = self.extract_urls_and_images(chunk_text)

            chunks.append({
                "text": content,
                "metadata": {
                    "tokens": tokens,
                    "headers": dict(current_headers),
                    "urls": urls,
                    "images": images,
                }
            })

            print(f"Chunk processed. New position: {chunk_end}")
            position = chunk_end

        print(f"Split process completed. Total chunks: {len(chunks)}")
        return chunks

    def get_chunk(self, text: str, start: int, limit: int):
        print(f"Getting chunk starting at {start} with limit {limit}")
        overhead = self.count_tokens(self.format_for_tokenization("")) - self.count_tokens("")
        # Estimate initial end position
        end = min(start + max(1, (len(text) - start) * limit // max(1, self.count_tokens(text[start:]))), len(text))
        chunk_text = text[start:end]
        tokens = self.count_tokens(chunk_text)

        while tokens + overhead > limit and end > start:
            print(f"Chunk exceeds limit with {tokens + overhead} tokens. Adjusting end position...")
            end = self.find_new_chunk_end(text, start, end)
            chunk_text = text[start:end]
            tokens = self.count_tokens(chunk_text)

        end = self.adjust_chunk_end(text, start, end, tokens + overhead, limit)
        chunk_text = text[start:end]
        tokens = self.count_tokens(chunk_text)
        print(f"Final chunk end: {end}")
        return chunk_text, end

    def adjust_chunk_end(self, text: str, start: int, end: int, current_tokens: int, limit: int) -> int:
        min_chunk_tokens = int(limit * 0.8)
        next_newline = text.find('\n', end)
        prev_newline = text.rfind('\n', start, end)

        # Try extending to next newline
        if next_newline != -1 and next_newline < len(text):
            extended_end = next_newline + 1
            chunk_text = text[start:extended_end]
            tokens = self.count_tokens(chunk_text)
            if tokens <= limit and tokens >= min_chunk_tokens:
                print(f"Extending chunk to next newline at position {extended_end}")
                return extended_end

        # Try reducing to previous newline
        if prev_newline > start:
            reduced_end = prev_newline + 1
            chunk_text = text[start:reduced_end]
            tokens = self.count_tokens(chunk_text)
            if tokens <= limit and tokens >= min_chunk_tokens:
                print(f"Reducing chunk to previous newline at position {reduced_end}")
                return reduced_end

        return end

    def find_new_chunk_end(self, text: str, start: int, end: int) -> int:
        new_end = end - max(1, (end - start) // 10)
        if new_end <= start:
            new_end = start + 1
        return new_end

    def extract_headers(self, text: str) -> Dict[str, List[str]]:
        headers: Dict[str, List[str]] = {}
        header_regex = re.compile(r'(^|\n)(#{1,6})\s+(.*)')
        for match in header_regex.finditer(text):
            level = len(match.group(2))
            content = match.group(3).strip()
            key = f"h{level}"
            headers.setdefault(key, []).append(content)
        return headers

    def update_current_headers(self, current: Dict[str, List[str]], extracted: Dict[str, List[str]]):
        for level in range(1, 7):
            key = f"h{level}"
            if key in extracted:
                current[key] = extracted[key]
                self.clear_lower_headers(current, level)

    def clear_lower_headers(self, headers: Dict[str, List[str]], level: int):
        for l in range(level + 1, 7):
            headers.pop(f"h{l}", None)

    def extract_urls_and_images(self, text: str):
        urls = []
        images = []
        url_index = 0
        image_index = 0

        def image_repl(match):
            nonlocal image_index
            alt_text, url = match.group(1), match.group(2)
            images.append(url)
            result = f"![{alt_text}]({{${{img{image_index}}}}})"
            image_index += 1
            return result

        def url_repl(match):
            nonlocal url_index
            link_text, url = match.group(1), match.group(2)
            urls.append(url)
            result = f"[{link_text}]({{${{url{url_index}}}}})"
            url_index += 1
            return result

        content = re.sub(r'!\[([^\]]*)\]\(([^)]+)\)', image_repl, text)
        content = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', url_repl, content)
        return content, urls, images

# Example usage:
# splitter = TextSplitter()
# chunks = splitter.split("Your long text here...", 