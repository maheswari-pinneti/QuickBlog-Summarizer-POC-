### ✅ QuickBlog Summarizer – Issue Tracker & Fix Checklist

#### 🧠 Functionality Issues

* [ ] Support for dynamic websites (JavaScript-rendered content like Medium)
* [ ] Fallback mechanism if blog content extraction fails
* [ ] Multilingual blog support for non-English content
* [ ] Add option to customize summary length (Short / Medium / Detailed)
* [ ] Allow model selection (T5, BART, custom models)

---

#### 💻 Frontend (React) Issues

* [ ] Add loading spinner or progress indicator while summarizing
* [ ] Show toast/error message when blog fetch or summary fails
* [ ] Validate input field for empty or invalid blog URLs
* [ ] Sanitize and clean user input before sending to backend
* [ ] Display clear UX messages for timeout or broken blogs

---

#### 🛠️ Backend (Flask) Issues

* [ ] Handle HTTP errors during blog scraping (`404`, `403`, etc.)
* [ ] Use `.env` file for Hugging Face API key instead of hardcoding
* [ ] Restructure project into `/client` (React) and `/server` (Flask)
* [ ] Improve content parsing using `newspaper3k` or `trafilatura`
* [ ] Add logging for API responses, request status, and error debugging

---

#### 📦 Project & Deployment Issues

* [ ] Add step-by-step local setup instructions to `README.md`
* [ ] Add deployment guide for Vercel (React) and Render (Flask)
* [ ] Include screenshots or screen recording of demo in README
* [ ] Create live demo link for public use
* [ ] Add badges (build passing, license, tech stack) to README

---

#### 🔐 Optional Security/Performance

* [ ] Rate-limit API requests to prevent abuse
* [ ] Content moderation to avoid summarizing inappropriate blogs
* [ ] Cache frequent blog requests using local storage or Redis (optional)

---
