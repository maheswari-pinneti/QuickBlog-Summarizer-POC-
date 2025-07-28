import requests
from bs4 import BeautifulSoup
from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM
import torch


class BlogSummarizer:
    def __init__(self, model_name='facebook/bart-large-cnn'):
        self.model_name = model_name
        self.device = 0 if torch.cuda.is_available() else -1  # Ensure CPU fallback
        print(f"Device set to {'cuda' if self.device == 0 else 'cpu'}")
        self.summarizer = pipeline('summarization', model=model_name, device=self.device)

    def extract_text(self, url):
        try:
            headers = {'User-Agent': 'Mozilla/5.0'}
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')

            article = soup.find('article')
            if article:
                text = article.get_text(separator=' ', strip=True)
            else:
                divs = soup.find_all('div')
                text_candidates = [
                    div.get_text(separator=' ', strip=True)
                    for div in divs if len(div.get_text(strip=True).split()) > 100
                ]
                text = max(text_candidates, key=len) if text_candidates else ""

            return ' '.join(text.split())

        except Exception as e:
            print(f"[Error] Failed to extract text: {e}")
            raise ValueError("Could not extract article content.")

    def auto_length(self, word_count):
        if word_count < 100:
            return (40, 15)
        elif word_count < 300:
            return (80, 30)
        elif word_count < 800:
            return (150, 60)
        elif word_count < 1500:
            return (250, 100)
        elif word_count < 3000:
            return (350, 150)
        else:
            return (450, 200)

    def summarize(self, text, max_length=None, min_length=None):
        max_input_words = 450
        words = text.split()
        word_count = len(words)

        summaries = []
        for i in range(0, word_count, max_input_words):
            chunk = " ".join(words[i:i + max_input_words])
            if not chunk.strip():
                continue

            chunk_len = len(chunk.split())
            auto_max, auto_min = self.auto_length(chunk_len)

            max_len = max_length if max_length else auto_max
            min_len = min_length if min_length else auto_min

            try:
                result = self.summarizer(chunk, max_length=max_len, min_length=min_len, do_sample=False)
                summaries.append(result[0]['summary_text'])
            except Exception as e:
                print(f"[Chunk Error] at chunk {i // max_input_words}: {e}")
                continue

        if not summaries:
            raise ValueError("Failed to generate summaries from chunks.")

        combined = " ".join(summaries)
        final_len = len(combined.split())

        if final_len > max_input_words:
            auto_max, auto_min = self.auto_length(final_len)
            max_len = max_length if max_length else auto_max
            min_len = min_length if min_length else auto_min
            try:
                final_summary = self.summarizer(combined, max_length=max_len, min_length=min_len, do_sample=False)
                return final_summary[0]['summary_text']
            except Exception as e:
                print("[Final Summary Error]:", e)
                return combined
        else:
            return combined

    def summarize_url(self, url, max_length=None, min_length=None):
        text = self.extract_text(url)
        print(f"Extracted word count: {len(text.split())}")
        if not text or len(text.split()) < 20:
            raise ValueError("Extracted content too short to summarize.")
        return self.summarize(text, max_length=max_length, min_length=min_length)
