# 🧠 QuickBlog Summarizer POC

> An AI-powered web application that scrapes and summarizes blog content using Hugging Face Transformers. Built with React, Flask, and BeautifulSoup.

---

## 📌 Overview

**QuickBlog Summarizer** is a Proof-of-Concept (PoC) project that allows users to input any blog URL, extract the content, and receive an AI-generated summary. It combines web scraping techniques with state-of-the-art NLP models (like **DistilBART** or **T5**) from Hugging Face to deliver concise blog summaries in real-time.

---

## 🚀 Features

- 🔗 Input any blog URL
- 🔍 Scrape blog content using `BeautifulSoup`
- 🤖 Summarize using Hugging Face Transformers API
- 🌐 React frontend with clean UI
- 🐍 Flask backend with API routing
- 📦 Easy to set up and run locally

---

## 🛠️ Tech Stack

| Frontend | Backend | AI/ML | Web Scraping | Others |
|----------|---------|-------|--------------|--------|
| React.js | Flask   | Hugging Face Transformers (T5 / DistilBART) | BeautifulSoup, Requests | HTML, CSS, JavaScript, Python |

---

## 📸 UI Preview

> *(Add screenshots or demo video here if available)*  
> ![QuickBlog Summarizer UI](assets/demo.png)

---

## 📂 Project Structure

```

QuickBlog-Summarizer-POC/
├── client/                # React frontend
├── server/                # Flask backend
│   ├── app.py             # Flask app logic
│   └── summarize.py       # Web scraping and Hugging Face summarization
├── README.md
└── requirements.txt       # Python dependencies

````

---

## ⚙️ Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/maheswari-pinneti/QuickBlog-Summarizer-POC-.git
cd QuickBlog-Summarizer-POC-
````

### 2. Backend Setup (Flask)

```bash
cd server
pip install -r requirements.txt
python app.py
```

This starts your Flask server at `http://localhost:5000`.

### 3. Frontend Setup (React)

```bash
cd ../client
npm install
npm start
```

This starts your React app at `http://localhost:3000`.

---

## 🔗 API Usage (Backend Endpoint)

```http
POST /summarize
Content-Type: application/json

{
  "url": "https://example.com/blog-post"
}
```

Returns a summarized blog paragraph from the content extracted.

---

## ✅ Example Use Case

> Enter the URL of a long technical blog article
> → Backend scrapes the text
> → Hugging Face summarizes it
> → You get a quick version of the article in seconds!

---

## 🤝 Contributions

This is a solo project built by [Maheswari Pinneti](https://www.linkedin.com/in/maheswari-pinneti/).
Feel free to fork, improve, or collaborate.

---

## 📅 Timeline

* **Start Date**: July 2025
* **Status**: 🚧 In Progress

---

## 📄 License

This project is for educational and demonstration purposes.

---

## ⭐ Star This Repo

If you found this project helpful, please give it a ⭐ to support!



---

🤝 Contributors
Maheswari Pinneti

Made with ❤️ by Maheswari Pinneti



