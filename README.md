# 🤖 PayPal SmartCommerce AI Agent

> **Autonomous Conversational E-Commerce & Instant Payment Settlement Agent**  
> Developed for the **PayPal AI Global Hackathon 2026** / Independent Open-Source Commerce.

---

## 🌟 Overview
**PayPal SmartCommerce AI Agent** is a full-stack conversational commerce solution that bridges natural language processing and the PayPal Payment ecosystem. It enables small businesses, freelancers, and e-commerce stores to deploy an AI agent that:
1. **Understands Natural Language Customer Purchase Intents** (inquiries, catalog browsing, customized requests).
2. **Generates Real-Time, Dynamic PayPal Smart Checkout & PayPal.me Links** with unique invoice references.
3. **Eliminates Shopping Cart Abandonment** with an instant, zero-friction conversational checkout flow.
4. **Supports Micro-Merchants & SMBs** with zero monthly maintenance costs.

---

## 🚀 Key Features
- **Conversational Checkout**: Customers chat naturally ("I want to buy the PyME POS box" or "Quote a web scraping script") and receive an instant payment quote.
- **Dynamic Invoicing**: Generates secure references and dynamic PayPal URLs on-the-fly (`paypal.com/cgi-bin/webscr` and `paypal.me`).
- **Zero-Dependency Lightweight Core**: Python stdlib + pure Tailwind CSS UI for ultra-low latency (< 50ms response time).
- **100% Tested**: Integrated test suite covering intent parsing, invoice math, and payment routing.

---

## 🛠️ Architecture & Tech Stack
- **Engine**: Python 3 (Object-Oriented Agentic Architecture in `agent.py`).
- **Server**: Standalone asynchronous HTTP server in `server.py` (Port 8089).
- **Frontend**: Responsive Tailwind CSS chat application with real-time intent rendering.
- **Verification**: Hermetic unit test suite (`test_agent.py`).

---

## 📦 How to Run Locally

```bash
# 1. Run unit tests
python3 test_agent.py -v

# 2. Launch the AI agent server
python3 server.py
```
Open [http://localhost:8089](http://localhost:8089) in your browser to interact with the agent.

---

## 🏆 Hackathon Submission Metadata
- **Track**: AI Agents & Conversational Commerce
- **Target Platform**: PayPal Smart Payment Buttons & PayPal.me Instant Rails
- **Lead Developer**: @Vallejo1921 (Maxer Digital Studio)
- **Official Contact**: 2530453@upv.edu.mx
