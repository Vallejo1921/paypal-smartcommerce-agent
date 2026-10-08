#!/usr/bin/env python3
"""
HTTP Server and Interactive Web Interface for PayPal SmartCommerce AI Agent
"""

import http.server
import socketserver
import json
import urllib.parse
from agent import PayPalAIAgent

PORT = 8089
agent = PayPalAIAgent()

HTML_PAGE = """<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>PayPal SmartCommerce AI Agent</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <style>
    body { font-family: 'Plus Jakarta Sans', sans-serif; }
    .chat-bubble { max-width: 80%; }
  </style>
</head>
<body class="bg-slate-950 text-slate-100 flex flex-col h-screen">

  <!-- Header -->
  <header class="border-b border-slate-800 bg-slate-900/60 backdrop-blur px-6 py-4 flex items-center justify-between">
    <div class="flex items-center gap-3">
      <div class="w-10 h-10 rounded-xl bg-blue-600 flex items-center justify-center font-black text-xl text-white shadow-lg shadow-blue-500/20">
        P
      </div>
      <div>
        <h1 class="font-bold text-lg leading-tight flex items-center gap-2">
          PayPal SmartCommerce AI <span class="text-xs bg-emerald-500/20 text-emerald-400 px-2 py-0.5 rounded-full border border-emerald-500/30">Online</span>
        </h1>
        <p class="text-xs text-slate-400">Asistente Autónomo de Ventas y Pagos en Vivo</p>
      </div>
    </div>
    <div class="flex items-center gap-3">
      <a href="https://paypal.me/maxter19" target="_blank" class="text-xs font-semibold bg-slate-800 hover:bg-slate-700 px-3 py-2 rounded-lg border border-slate-700 transition">
        Merchant: Maxer Digital
      </a>
    </div>
  </header>

  <!-- Chat container -->
  <main class="flex-1 overflow-y-auto p-4 sm:p-6 space-y-4 max-w-4xl mx-auto w-full" id="chatContainer">
    <!-- Welcome message -->
    <div class="flex items-start gap-3">
      <div class="w-8 h-8 rounded-lg bg-blue-600 flex items-center justify-center text-sm font-bold flex-shrink-0">IA</div>
      <div class="bg-slate-900 border border-slate-800 rounded-2xl rounded-tl-sm p-4 chat-bubble shadow-xl">
        <p class="text-sm text-slate-200">
          👋 ¡Hola! Soy tu <strong>Agente de Comercio Inteligente con PayPal</strong>. Puedo ayudarte a consultar productos, cotizar servicios técnicos o generar enlaces de pago instantáneos.
        </p>
        <div class="mt-3 flex flex-wrap gap-2">
          <button onclick="sendQuickMessage('Ver catálogo')" class="text-xs bg-slate-800 hover:bg-slate-700 border border-slate-700 px-3 py-1.5 rounded-lg text-blue-400 font-medium transition">
            📋 Ver Catálogo
          </button>
          <button onclick="sendQuickMessage('Quiero la Caja POS PyME')" class="text-xs bg-slate-800 hover:bg-slate-700 border border-slate-700 px-3 py-1.5 rounded-lg text-emerald-400 font-medium transition">
            💳 Comprar Caja POS ($5 USD)
          </button>
          <button onclick="sendQuickMessage('Necesito un Web Scraper')" class="text-xs bg-slate-800 hover:bg-slate-700 border border-slate-700 px-3 py-1.5 rounded-lg text-indigo-400 font-medium transition">
            📊 Cotizar Web Scraper ($45 USD)
          </button>
        </div>
      </div>
    </div>
  </main>

  <!-- Input form -->
  <footer class="border-t border-slate-800 bg-slate-900/60 p-4">
    <div class="max-w-4xl mx-auto flex gap-2">
      <input type="text" id="userInput" placeholder="Escribe tu consulta (ej. 'Quiero comprar la Caja POS' o 'Dame el catálogo')..." class="flex-1 bg-slate-950 border border-slate-800 focus:border-blue-500 rounded-xl px-4 py-3 text-sm text-slate-100 placeholder-slate-500 focus:outline-none transition">
      <button onclick="sendMessage()" class="bg-blue-600 hover:bg-blue-500 text-white font-semibold px-6 py-3 rounded-xl text-sm transition flex items-center gap-2 shadow-lg shadow-blue-500/20">
        Enviar
      </button>
    </div>
  </footer>

  <script>
    const chatContainer = document.getElementById('chatContainer');
    const userInput = document.getElementById('userInput');

    userInput.addEventListener('keypress', (e) => {
      if (e.key === 'Enter') sendMessage();
    });

    function appendUserMessage(text) {
      const msg = document.createElement('div');
      msg.className = 'flex items-start justify-end gap-3';
      msg.innerHTML = `
        <div class="bg-blue-600 rounded-2xl rounded-tr-sm p-4 chat-bubble shadow-xl text-sm text-white font-medium">
          ${text}
        </div>
      `;
      chatContainer.appendChild(msg);
      chatContainer.scrollTop = chatContainer.scrollHeight;
    }

    function appendAgentMessage(data) {
      const msg = document.createElement('div');
      msg.className = 'flex items-start gap-3';
      
      let actionHtml = '';
      if (data.action_data && data.action_data.paypal_me_url) {
        actionHtml = `
          <div class="mt-4 p-4 rounded-xl bg-slate-950/80 border border-emerald-500/30 flex flex-col sm:flex-row items-center justify-between gap-3">
            <div>
              <div class="text-xs text-slate-400">Total a Pagar</div>
              <div class="text-lg font-bold text-emerald-400">$${data.action_data.total_amount} ${data.action_data.currency}</div>
              <div class="text-[11px] text-slate-500">Ref: ${data.action_data.invoice_id}</div>
            </div>
            <a href="${data.action_data.paypal_me_url}" target="_blank" class="w-full sm:w-auto bg-emerald-600 hover:bg-emerald-500 text-white font-bold px-5 py-2.5 rounded-lg text-xs shadow-lg shadow-emerald-600/20 transition flex items-center justify-center gap-2">
              Pagar con PayPal Instantáneo
            </a>
          </div>
        `;
      } else if (data.intent === 'view_catalog' && data.action_data) {
        let itemsHtml = Object.values(data.action_data).map(item => `
          <div class="p-3 rounded-xl bg-slate-950 border border-slate-800 flex justify-between items-center">
            <div>
              <div class="font-bold text-xs text-slate-200">${item.name}</div>
              <div class="text-[11px] text-slate-400">${item.description}</div>
            </div>
            <div class="text-right">
              <div class="font-bold text-emerald-400 text-xs">$${item.price} ${item.currency}</div>
            </div>
          </div>
        `).join('');
        actionHtml = `<div class="mt-3 space-y-2">${itemsHtml}</div>`;
      }

      msg.innerHTML = `
        <div class="w-8 h-8 rounded-lg bg-blue-600 flex items-center justify-center text-sm font-bold flex-shrink-0">IA</div>
        <div class="bg-slate-900 border border-slate-800 rounded-2xl rounded-tl-sm p-4 chat-bubble shadow-xl">
          <p class="text-sm text-slate-200">${data.message}</p>
          ${actionHtml}
        </div>
      `;
      chatContainer.appendChild(msg);
      chatContainer.scrollTop = chatContainer.scrollHeight;
    }

    async function sendQuickMessage(text) {
      userInput.value = text;
      sendMessage();
    }

    async function sendMessage() {
      const text = userInput.value.trim();
      if (!text) return;
      userInput.value = '';
      appendUserMessage(text);

      try {
        const resp = await fetch('/api/chat', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ message: text })
        });
        const data = await resp.json();
        appendAgentMessage(data);
      } catch (err) {
        console.error(err);
      }
    }
  </script>
</body>
</html>
"""

class RequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/" or self.path.startswith("/index"):
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(HTML_PAGE.encode("utf-8"))
        elif self.path == "/health":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "healthy", "service": "PayPal SmartCommerce AI"}).encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path == "/api/chat":
            content_length = int(self.headers.get("Content-Length", 0))
            post_data = self.rfile.read(content_length).decode("utf-8")
            try:
                body = json.loads(post_data)
                user_msg = body.get("message", "")
                result = agent.process_message(user_msg)
                
                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps(result, ensure_ascii=False).encode("utf-8"))
            except Exception as e:
                self.send_response(500)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

if __name__ == "__main__":
    server = socketserver.TCPServer(("", PORT), RequestHandler)
    print(f"[*] PayPal SmartCommerce AI Agent Server running at http://localhost:{PORT}")
    server.serve_forever()
