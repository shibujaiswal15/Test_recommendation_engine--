# 🔍 SHL Assessment Recommender

A smart web-based system that recommends SHL assessments based on natural language job descriptions using LLMs (Gemini API). It extracts constraints like required skills, duration, and job levels, then suggests the most relevant assessments.

> 🚀 Powered by **FastAPI**, **Next.js**, **Tailwind CSS**, and **Google Gemini API**

---

## 🌐 Live Links

- 💻 **Frontend App**: [https://shl-recommendation-system-4b7i71ru6-shibu-kumaris-projects.vercel.app/]
- 📱 **API Endpoint**: [https://shl-recommendation-engine-hnys.onrender.com/recommend](https://shl-recommendation-engine-hnys.onrender.com/recommend)

---

## 📦 Features

- 💬 Accepts natural language job prompts
- 🤖 Extracts constraints like skills, duration, and job level using Gemini
- ✅ Matches prompt with SHL assessment dataset
- 🔗 Provides links, duration, keys, and support flags (remote/adaptive)
- 🧾 Clean UI built using React + Tailwind
- 🧠 Scraped ~400+ assessments from SHL’s public catalog
- 🌍 Deployed using Render (API) and Vercel (frontend)

---

## 🧠 How It Works

1. User enters a prompt like:
   > “Looking for a mid-level data analyst with strong Excel and reasoning skills.”

2. Gemini API extracts:
   - Skills: Excel, Reasoning
   - Job level: Mid-level
   - Duration constraint: Optional

3. SHL assessments are filtered and scored based on match.

4. Final top-K assessments are returned to the user with useful metadata.

---

## ⚙️ Tech Stack

| Layer       | Stack                              |
|-------------|------------------------------------|
| Frontend    | Next.js, Tailwind CSS              |
| Backend     | FastAPI                            |
| AI/LLM      | Google Gemini API                  |
| Scraping    | Selenium, BeautifulSoup            |
| Deployment  | Render (API) + Vercel (Frontend)   |

---

## 🚀 Usage

### 1️⃣ Frontend (Web UI)

- Open the [frontend site](https://shl-recommendation-system-4b7i71ru6-shibu-kumaris-projects.vercel.app/)
- Enter a prompt
- Set how many assessments to recommend (1–20)
- Click "Recommend" and view clean results in a table
- frontend source code : https://github.com/shibujaiswal15/SHL-Recommendation-System

### 2️⃣ API Endpoint (POST)

- **URL**: `https://shl-recommendation-engine-hnys.onrender.com/recommend`
- **Method**: `POST`
- **Body**:

```
{
  "prompt": "We need an entry-level salesperson with communication skills.",
  "top_k": 5
}
```

- **Response**:

```
{
  "recommendations": [
    {
      "name": "MS Excel (New)",
      "link": "https://www.shl.com/...",
      "duration": 30,
      "skills": ["Knowledge & Skills"],
      "remote_support": "Yes",
      "adaptive_support": "No"
    }
  ]
}
```

---

## 🛠️ Development Setup

### 🧾 Backend (FastAPI)

```
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000
```

> Make sure you have `.env` with your Gemini key:

```
GEMINI_API_KEY=your_api_key_here
```

### 🧾 Frontend (Next.js)

```
cd frontend
npm install
npm run dev
```

---

## 📁 Project Structure

```
shl-assessment-recommender/
├── app/
│   ├── main.py                # FastAPI app
│   ├── utils/recommender.py  # Core recommendation logic
│   └── shl_tests.json         # Dataset
├── frontend/
│   └── src/app/page.tsx      # Next.js frontend
```

---

## 🩺 Health Check Endpoint

- **URL**: `/health`
- **Method**: `GET`
- **Response**:

```
{
  "status": "healthy"
}
```

---

## 📌 Future Improvements

- [ ] Add vector embeddings for better matching
- [ ] Add user login / history tracking
- [ ] Sort/filter table results by duration, adaptive, remote
- [ ] Support for multiple prompt types (e.g., CSV upload)

---

## 👤 Author

Made  by (https://github.com/shibujaiswal15)

---

## 📄 License

This project is licensed under the [MIT License](LICENSE)

