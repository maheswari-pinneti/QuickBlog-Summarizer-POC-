# 📝 Quick Blog Summarizer

**Quick Blog Summarizer** is a lightweight AI-powered web app that lets you input any blog URL and get a concise summary within seconds using state-of-the-art NLP models from Hugging Face 🤖✨

---

## 🚀 Features

- 🧠 Summarizes long blogs using pre-trained models like BART or T5.
- 🌐 Supports blogs from Medium, Dev.to, WordPress, and more.
- ⚡ Clean and responsive UI built with React.js.
- 🔎 Scrapes and sanitizes blog content automatically.
- 🛠️ Easy to deploy and extend.

---

## 🔧 Tech Stack

| Layer         | Technology                      |
|--------------|----------------------------------|
| Frontend      | React.js, Tailwind CSS, Axios    |
| Backend       | Flask, BeautifulSoup, Transformers |
| ML Model      | HuggingFace (BART or T5)         |
| Deployment    | Render / Heroku / Railway        |

---

## 🖼️ Demo Preview

> Coming soon...

---

## 📁 Folder Structure

```

quick-blog-summarizer/
│
├── client/                 # React frontend
│   ├── public/
│   └── src/
│       ├── components/
│       ├── App.jsx
│       └── index.js
│
├── server/                 # Flask backend
│   ├── app.py
│   ├── summarizer.py
│   └── requirements.txt
│
├── README.md
└── .gitignore

````

---

## ⚙️ Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/quick-blog-summarizer.git
cd quick-blog-summarizer
````

### 2. Setup Backend (Flask + Transformers)

```bash
cd server
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

`requirements.txt` sample:

```
Flask
transformers
torch
beautifulsoup4
newspaper3k
flask-cors
```

### 3. Setup Frontend (React)

```bash
cd client
npm install
npm run dev  # Vite or npm start if using CRA
```

---

## 🔥 API Overview

### `POST /summarize`

**Request Body:**

```json
{
  "url": "https://example.com/blog-post"
}
```

**Response:**

```json
{
  "summary": "This blog talks about..."
}
```

---

## 🧠 Model Choices

* `facebook/bart-large-cnn` (default)
* `sshleifer/distilbart-cnn-12-6`
* `t5-small` or `t5-base` (optional)

Changeable in `summarizer.py`.

---

## 📌 TODO

* [x] Basic summarization
* [ ] Loading spinner
* [ ] PDF download option
* [ ] Chrome Extension (future)
* [ ] Language switch (future)

---

## 🤝 Contributing

Pull requests are welcome. For major changes, please open an issue first.

---

## 📜 License

[MIT](LICENSE)

---

## 🙋‍♀️ Built by [Maheswari Pinneti](https://www.linkedin.com/in/maheswari-pinneti/)

````

---

## 🗂️ Sample File: `summarizer.py` (Backend)

```python
from transformers import pipeline
from newspaper import Article

summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def extract_and_summarize(url):
    article = Article(url)
    article.download()
    article.parse()
    text = article.text

    if len(text) < 50:
        return "Content is too short to summarize."

    summary = summarizer(text[:1024], max_length=120, min_length=30, do_sample=False)
    return summary[0]['summary_text']


---
