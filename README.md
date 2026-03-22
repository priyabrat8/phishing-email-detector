# Scanner HD — Phishing Detection System

![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)
![Django](https://img.shields.io/badge/Django-Backend-green)
![TailwindCSS](https://img.shields.io/badge/TailwindCSS-Frontend-38B2AC)
![Status](https://img.shields.io/badge/Status-Active-success)
![License](https://img.shields.io/badge/License-MIT-yellow)

> A powerful phishing detection system combining **Machine Learning (NLP)**, **URL threat analysis**, and **domain reputation analysis** to detect malicious emails and links.

---

## ✨ Features

- 🔍 NLP-based phishing detection (TF-IDF)
- 🔗 Advanced URL threat analysis
- 🛡️ Domain reputation and risk assessment
- ⚡ Real-time phishing risk scoring
- 🔒 Anti-abuse protection (CAPTCHA, rate limiting)
- 🎯 Clean UI with Tailwind CSS

---

## 🧠 System Architecture

```
Input (Email)
        │
        ▼
[ Content Analysis (TF-IDF) ]
        │
        ▼
[ URL Extraction Engine ]
        │
        ▼
[ Threat Analysis + Reputation Validation ]
        │
        ▼
[ Risk Scoring Engine ]
        │
        ▼
   Final Report (Score + Flags)
```

---

## 🔍 Content & NLP Analysis

- **TF-IDF Vectorization**
  - Detects phishing keywords and urgency patterns
- **Body Inspection**
  - Identifies social engineering tactics and impersonation

---

## 🔗 URL Heuristic Engine

- ✅ Structural validation (domain/IP check)
- ⚠️ Detects `@` obfuscation
- 🌐 Flags raw IP-based URLs
- 🧩 Deep subdomain detection
- 🧠 Long domain & hyphen phishing detection

---

## 🛡️ Reputation & Intelligence

- 📛 Blacklist checking
- ⏳ Domain age detection (WHOIS)
- 📧 Sender domain verification

---

## 🔒 Security & Anti-Abuse

- 🕳️ Honeypot fields
- 🚦 Rate limiting
- 🤖 Cloudflare Turnstile CAPTCHA

---

## 🛠️ Tech Stack

### Backend
- Python
- Django
- Scikit-learn

### Frontend
- HTML
- Tailwind CSS

### Databse
- PostgreSQL

### Deployment
- Render / Neno

---

## 🚀 Installation

### 1. Clone Repository

```bash
git clone https://github.com/priyabrat8/phishing-email-detector
cd phishing-email-detector
```

---

### 2. Setup Python Environment

```bash
pip install -r requirements.txt
```

---

## 🚀 Running the Project

### Start Tailwind

```bash
python manage.py tailwind start
```

### Start Django Server

```bash
python manage.py runserver
```

---

## 🏗️ Production Setup

```bash
chmod +x build.sh && ./build.sh
```

---

## 📝 Usage

1. Paste suspicious email or message
2. Complete CAPTCHA verification
3. View analysis report:
   - Phishing score
   - URL risk indicators
   - Domain intelligence
   - Sender credibility

---

## 📜 License

MIT License

---

## ⭐ Support

If you like this project:

- ⭐ Star the repo
- 🍴 Fork it
- 🚀 Share it