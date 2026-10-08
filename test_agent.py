import unittest
from agent import PayPalAIAgent

class TestPayPalAIAgent(unittest.TestCase):
    def setUp(self):
        self.agent = PayPalAIAgent()

    def test_catalog_retrieval(self):
        cat = self.agent.get_catalog()
        self.assertIn("pos_pyme", cat)
        self.assertIn("web_scraper", cat)
        self.assertIn("landing_page", cat)
        self.assertEqual(cat["pos_pyme"]["price"], 5.00)

    def test_checkout_url_generation(self):
        checkout = self.agent.generate_paypal_checkout_url("pos_pyme", 2)
        self.assertEqual(checkout["quantity"], 2)
        self.assertEqual(checkout["total_amount"], 10.00)
        self.assertIn("paypal.me/maxter19/10USD", checkout["paypal_me_url"])
        self.assertIn("paypal.com/cgi-bin/webscr", checkout["paypal_checkout_url"])

    def test_natural_language_intent_matching(self):
        # Catalog intent
        res = self.agent.process_message("¿Me muestras tu catálogo de productos?")
        self.assertEqual(res["intent"], "view_catalog")

        # Purchase intent
        res = self.agent.process_message("Quiero comprar la caja pos para mi negocio")
        self.assertEqual(res["intent"], "order_pos")
        self.assertIsNotNone(res["action_data"])
        self.assertEqual(res["action_data"]["total_amount"], 5.00)

        # Scraper intent
        res = self.agent.process_message("Necesito extraer datos con un scraper")
        self.assertEqual(res["intent"], "order_scraper")
        self.assertEqual(res["action_data"]["total_amount"], 45.00)

if __name__ == "__main__":
    unittest.main()
