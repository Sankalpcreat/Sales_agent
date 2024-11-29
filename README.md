# 🚀 AI Sales Assistant - Backend

<div align="center">

[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![OpenAI](https://img.shields.io/badge/OpenAI-412991?style=for-the-badge&logo=openai&logoColor=white)](https://openai.com/)

</div>

## 📋 Overview

This is the backend for the AI Sales Assistant, a powerful system designed to automate and enhance sales processes. The backend handles core business logic, API endpoints, and seamless integration with AI models and databases.

## 🏗️ Architecture

Here's a high-level architecture diagram of the backend system:

<div align="center">

![Backend Architecture](./assets/screen.png)

</div>

## ✨ Key Features

- 📊 **Lead Scoring**
  - Prioritize leads based on engagement metrics
  - Intelligent activity tracking
  - Real-time scoring updates

- 📬 **Automated Follow-Ups**
  - Smart reminder system
  - Personalized email sequences
  - Engagement tracking

- 📝 **AI-Powered Proposal Generation**
  - Customized proposal drafting
  - Dynamic template system
  - Brand consistency enforcement

- 📋 **Meeting Intelligence**
  - Automated meeting summarization
  - Action item extraction
  - Key points highlighting

- 🎯 **Smart Lead Suggestions**
  - FAISS-powered similarity search
  - Intelligent lead matching
  - Recommendation engine

## 🛠️ Tech Stack

- **Framework**: FastAPI
- **Database**: PostgreSQL
- **AI Models**: OpenAI GPT
- **Vector Search**: FAISS
- **Task Queue**: Celery
- **Cache**: Redis

## 🚀 Getting Started

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/sales-assistant-backend.git
cd sales-assistant-backend
```

2. **Set up environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. **Configure environment variables**
```bash
cp .env.example .env
# Edit .env with your configuration
```

4. **Run the server**
```bash
uvicorn app.main:app --reload
```

## 📚 API Documentation

Once the server is running, access the API documentation at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 🧪 Testing

Run the test suite:
```bash
pytest
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

<div align="center">
Made with ❤️ by the AI Sales Assistant Team
</div>
