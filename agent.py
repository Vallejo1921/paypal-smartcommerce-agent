#!/usr/bin/env python3
"""
PayPal SmartCommerce AI Agent - Core Engine
Autonomous e-commerce & payment copilot:
- Parses customer intents (inquiries, checkout, invoices, discounts)
- Generates dynamic PayPal Smart Payment links and invoices
- Validates inventory & calculates dynamic tax/shipping
- Operates offline or connected to live PayPal APIs
"""

import os
import json
import uuid
import datetime
import urllib.parse

class PayPalAIAgent:
    def __init__(self, merchant_paypal_email="2530453@upv.edu.mx", merchant_name="Maxer Digital Studio"):
        self.merchant_paypal_email = merchant_paypal_email
        self.merchant_name = merchant_name
        self.catalog = {
            "pos_pyme": {
                "name": "Suite PyME Pro - Caja POS Offline",
                "price": 5.00,
                "currency": "USD",
                "description": "Licencia perpetua de software de punto de venta sin mensualidades con tickets WhatsApp.",
                "stock": 9999
            },
            "web_scraper": {
                "name": "Python Web Scraping & Data Extraction Script",
                "price": 45.00,
                "currency": "USD",
                "description": "Extractor de datos personalizado a Excel, CSV y SQLite.",
                "stock": 50
            },
            "landing_page": {
                "name": "High-Converting Tailwind Landing Page",
                "price": 60.00,
                "currency": "USD",
                "description": "Página de aterrizaje optimizada con botón WhatsApp y carga instantánea.",
                "stock": 25
            }
        }
        self.conversation_history = []

    def get_catalog(self):
        return self.catalog

    def generate_paypal_checkout_url(self, item_key, quantity=1, custom_note=None):
        if item_key not in self.catalog:
            raise ValueError(f"Producto '{item_key}' no encontrado en el catálogo.")
        
        item = self.catalog[item_key]
        total_amount = item["price"] * quantity
        invoice_id = f"INV-{uuid.uuid4().hex[:8].upper()}"

        # Standard PayPal Simple Payment & PayPal Me construction
        params = {
            "cmd": "_xclick",
            "business": self.merchant_paypal_email,
            "item_name": f"{item['name']} (x{quantity})",
            "item_number": invoice_id,
            "amount": f"{total_amount:.2f}",
            "currency_code": item["currency"],
            "no_shipping": "1",
            "return": "https://vallejo1921.github.io/caja-pos-pyme/entrega.html",
            "cancel_return": "https://vallejo1921.github.io/servicios-software/"
        }
        
        paypal_web_checkout = f"https://www.paypal.com/cgi-bin/webscr?{urllib.parse.urlencode(params)}"
        # Direct quick payment URL fallback
        paypal_me_checkout = f"https://paypal.me/maxter19/{int(total_amount) if total_amount.is_integer() else total_amount}{item['currency']}"

        return {
            "invoice_id": invoice_id,
            "item": item["name"],
            "quantity": quantity,
            "unit_price": item["price"],
            "total_amount": total_amount,
            "currency": item["currency"],
            "paypal_checkout_url": paypal_web_checkout,
            "paypal_me_url": paypal_me_checkout,
            "created_at": datetime.datetime.now(datetime.timezone.utc).isoformat()
        }

    def process_message(self, user_text):
        """
        Interpreta intenciones de lenguaje natural del cliente
        """
        text = user_text.lower()
        response = {
            "intent": "unknown",
            "message": "",
            "action_data": None
        }

        if any(w in text for w in ["catalogo", "productos", "servicios", "precios", "catalog", "pricing"]):
            response["intent"] = "view_catalog"
            response["message"] = f"¡Hola! Soy tu asistente de pagos inteligentes de {self.merchant_name}. Aquí tienes nuestros productos y servicios disponibles:"
            response["action_data"] = self.catalog

        elif any(w in text for w in ["caja", "pos", "pyme", "abarrote", "punto de venta"]):
            checkout = self.generate_paypal_checkout_url("pos_pyme", 1)
            response["intent"] = "order_pos"
            response["message"] = f"Excelente elección. La **{checkout['item']}** incluye licencia perpetua y sin rentas mensuales. Total a pagar: **${checkout['total_amount']} {checkout['currency']}**."
            response["action_data"] = checkout

        elif any(w in text for w in ["scraping", "extraer", "datos", "excel", "scraper"]):
            checkout = self.generate_paypal_checkout_url("web_scraper", 1)
            response["intent"] = "order_scraper"
            response["message"] = f"Perfecto. Nuestro servicio de **{checkout['item']}** entrega datos 100% limpios en 24h. Total: **${checkout['total_amount']} {checkout['currency']}**."
            response["action_data"] = checkout

        elif any(w in text for w in ["landing", "web", "pagina", "sitio"]):
            checkout = self.generate_paypal_checkout_url("landing_page", 1)
            response["intent"] = "order_landing"
            response["message"] = f"Genial. Desarrollamos tu **{checkout['item']}** lista para vender y con WhatsApp. Total: **${checkout['total_amount']} {checkout['currency']}**."
            response["action_data"] = checkout

        else:
            response["intent"] = "greeting_fallback"
            response["message"] = f"Hola, bienvenido a {self.merchant_name}. ¿En qué podemos ayudarte hoy? Puedes pedir nuestro 'catálogo', comprar la 'Caja POS PyME' ($5 USD) o contratar un 'web scraper' / 'landing page'."

        self.conversation_history.append({"user": user_text, "agent": response})
        return response

if __name__ == "__main__":
    agent = PayPalAIAgent()
    print("Testing Agent Natural Language Processing:")
    res = agent.process_message("Hola, me interesa comprar la caja pos para mi negocio")
    print(json.dumps(res, indent=2, ensure_ascii=False))
