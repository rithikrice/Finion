# Finion - AI-Powered Personal Finance Assistant

<div align="center">
  <img src="https://img.shields.io/badge/Flutter-02569B?style=for-the-badge&logo=flutter&logoColor=white" alt="Flutter" />
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/Go-00ADD8?style=for-the-badge&logo=go&logoColor=white" alt="Go" />
  <img src="https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi" alt="FastAPI" />
  <img src="https://img.shields.io/badge/Google%20Gemini-8E75B2?style=for-the-badge&logo=google&logoColor=white" alt="Gemini" />
  <img src="https://img.shields.io/badge/IBM%20Watson-BE95FF?style=for-the-badge&logo=ibm&logoColor=white" alt="Watson" />
</div>

## 📋 Overview

Finion is a comprehensive AI-powered personal finance management application that helps users track, analyze, and optimize their financial health. Built for a hackathon, it combines cutting-edge AI technology with real-time financial data to provide personalized insights and recommendations.

## ✨ Key Features

### 🤖 AI-Powered Intelligence
- **Natural Language Queries**: Ask questions about your finances in plain English
- **Google Gemini Integration**: Advanced AI responses using Gemini 1.5 Flash
- **IBM Watson Integration**: Enterprise-grade AI capabilities for enhanced analysis
- **Vertex AI Support**: Celebrity financial comparisons with robust fallback mechanisms

### 💼 Financial Management
- **Comprehensive Asset Tracking**: Monitor bank accounts, mutual funds, stocks (Indian & US), EPF, and more
- **Goal Management**: Create, track, and achieve financial goals with smart calculations
- **Credit Report Analysis**: Understand and improve your credit health
- **Net Worth Tracking**: Real-time calculation and visualization of total wealth

### 🎯 Personalized Features
- **Lifestyle Recommendations**: Get actionable suggestions to optimize spending
- **Celebrity Comparisons**: Compare your financial status with celebrities for motivation
- **Risk Analysis**: IBM Risk Guard for comprehensive portfolio risk assessment
- **Payment Scheduling**: Smart scheduling for bills and investments

### 📱 Modern User Experience
- **Flutter Mobile App**: Beautiful, responsive native mobile application
- **Real-time Streaming**: SSE support for live data updates
- **Voice Integration**: Voice-based financial queries and commands
- **Interactive Visualizations**: Charts and graphs for financial trends

## 🏗️ Architecture

[<img src="docs/architecture.png" alt="Finion Architecture" width="100%">](https://drive.google.com/file/d/1mZSSh-DG3EQbLjvidy1omMhwLHxM92oA/view)

## 🚀 Quick Start

### Prerequisites
- **Flutter** SDK (3.0+)
- **Python** 3.8+
- **Go** 1.23+
- **Google API Key** for Gemini
- **Google Cloud Project** (optional, for Vertex AI)
- **IBM Watson** credentials (optional)

### 1️⃣ Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export GOOGLE_API_KEY="your_gemini_api_key"
# Or create .env file

# Run the backend server
python main.py
```

Backend will be available at: http://localhost:8000

### 2️⃣ MCP Server Setup

```bash
# Navigate to MCP directory
cd fi-mcp-dev

# Install dependencies
go mod tidy

# Run the MCP server
FI_MCP_PORT=8080 go run .
```

MCP server will be available at: http://localhost:8080

### 3️⃣ Frontend Setup

```bash
# Navigate to frontend directory
cd frontEnd

# Install Flutter dependencies
flutter pub get

# Run the app
flutter run
# Or build for specific platform
flutter build apk  # Android
flutter build ios  # iOS
```

## 📊 Demo Mode

The application includes comprehensive demo data for testing:

1. **Backend Demo**: Use cookie `sessionid=demo_session_123`
2. **MCP Demo Users**: Multiple test phone numbers with different financial scenarios:
   - `1111111111`: New user with minimal assets
   - `2222222222`: Complete portfolio with all assets
   - `3333333333`: Moderate investor profile
   - See `fi-mcp-dev/README.md` for all 25+ demo scenarios

## 🔌 API Documentation

### Backend APIs (Port 8000)

| Category | Endpoints |
|----------|-----------|
| **AI Agent** | `POST /api/ask`, `POST /stream/ask` |
| **Financial Data** | `/api/net_worth`, `/api/credit_report`, `/api/epf_details` |
| **Transactions** | `/api/bank_transactions`, `/api/stock_transactions`, `/api/mf_transactions` |
| **Goals** | `GET/POST /api/goals`, `PUT/DELETE /api/goals/{id}` |
| **Lifestyle** | `GET /api/lifestyle-changes`, `POST /api/lifestyle-changes/apply` |
| **Celebrity** | `POST /api/celebrity-comparison` |

Full API documentation available at: http://localhost:8000/docs

### MCP Server APIs (Port 8080)

Stream endpoints for real-time financial data:
- `/stream/net_worth`
- `/stream/credit_report`
- `/stream/epf_details`
- `/stream/mf_transactions`
- `/stream/bank_transactions`

## 🧪 Testing

### Example API Calls

```bash
# Ask AI about finances
curl -X POST http://localhost:8000/api/ask \
  -H "Content-Type: application/json" \
  -H "Cookie: sessionid=demo_session_123" \
  -d '{"prompt": "What is my current net worth?"}'

# Create a financial goal
curl -X POST http://localhost:8000/api/goals \
  -H "Content-Type: application/json" \
  -H "Cookie: sessionid=demo_session_123" \
  -d '{
    "name": "Emergency Fund",
    "target_amount": 100000,
    "current_amount": 25000,
    "target_date": "2024-12-31T00:00:00",
    "category": "savings"
  }'

# Compare with celebrity
curl -X POST http://localhost:8000/api/celebrity-comparison \
  -H "Content-Type: application/json" \
  -H "Cookie: sessionid=demo_session_123" \
  -d '{
    "celebrity_name": "Elon Musk",
    "comparison_type": "all"
  }'
```

## 🛠️ Technology Stack

### Frontend
- **Flutter/Dart** - Cross-platform mobile framework
- **Provider** - State management
- **HTTP** - API communication
- **Charts** - Data visualization

### Backend
- **FastAPI** - High-performance Python web framework
- **SQLAlchemy** - ORM with in-memory SQLite
- **Google Generative AI** - Gemini 1.5 Flash integration
- **Vertex AI** - Enterprise AI capabilities
- **IBM Watson** - Advanced AI components
- **Pydantic** - Data validation
- **SSE** - Server-sent events for streaming

### MCP Server
- **Go** - High-performance server language
- **Gorilla Mux** - HTTP router
- **JSON** - Data serialization
- **Mock Authentication** - Simplified auth for demos

## 📦 IBM Watson Components

The backend includes advanced IBM Watson integrations:

1. **Financial Twin**: Creates a digital twin of user's financial profile
2. **Knowledge Augmented**: Enhances responses with external knowledge
3. **Payment Scheduler**: Intelligent payment and investment scheduling
4. **Risk Guard**: Comprehensive risk analysis and management

## 🔐 Security & Privacy

- Session-based authentication
- Secure API key management
- Environment variable configuration

## 🙏 Acknowledgments

- Google Gemini for AI capabilities
- IBM Watson for enterprise AI features
- Flutter team for the amazing framework
- FastAPI for the Python backend framework
- Go community for the robust MCP server implementation

---

<div align="center">
  <strong>Built with ❤️ for the IBM TechXchange 2025 Hackathon</strong>
  <br>
  <em>Empowering financial wellness through AI</em>
</div>
