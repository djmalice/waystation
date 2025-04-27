from datetime import date
from django.test import TestCase, Client
from django.urls import reverse
from ..models import Supplier, RFQ, Quote
import json
from ..forms import RFQForm

class SupplierDetailViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.supplier = Supplier.objects.create(company_name="Supplier-A")

    def test_get_supplier(self):
        response = self.client.get(reverse('supplier-detail', args=[self.supplier.pk]))
        self.assertEqual(response.status_code, 200)

    def test_put_supplier(self):
        data = {"company_name": "Updated-Supplier"}
        response = self.client.put(reverse('supplier-detail', args=[self.supplier.pk]), data=json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["company_name"], "Updated-Supplier")

    def test_delete_supplier(self):
        response = self.client.delete(reverse('supplier-detail', args=[self.supplier.pk]))
        self.assertEqual(response.status_code, 204)

class RFQDetailViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.rfq = RFQ.objects.create(item="Item A")

    def test_get_rfq(self):
        response = self.client.get(reverse('rfq-detail', args=[self.rfq.id]))
        self.assertEqual(response.status_code, 200)

    def test_put_rfq(self):
        data = {"item": "Updated Item"}
        response = self.client.put(reverse('rfq-detail', args=[self.rfq.id]), data=json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["item"], "Updated Item")

    def test_delete_rfq(self):
        response = self.client.delete(reverse('rfq-detail', args=[self.rfq.id]))
        self.assertEqual(response.status_code, 204)

class SubmitQuoteEmailViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.rfq = RFQ.objects.create(item="Item A")

    def test_post_submit_quote_email(self):
        data = {"email_content": "Sample email content"}
        response = self.client.post(reverse('submit-quote-email', args=[self.rfq.id]), data=data)
        self.assertEqual(response.status_code, 302)  # Redirects to RFQ list

class CreateRFQViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_get_create_rfq_page(self):
        response = self.client.get(reverse('create-rfq'))
        self.assertEqual(response.status_code, 200)

    def test_post_create_rfq_valid(self):
        # Valid data for RFQ creation
        data = {
            "item": "Item B",
            "due_date": "2025-05-01",
            "amount_required_lbs": 100.5,
            "ship_to_location": "123 Test Street",
            "required_certifications": "ISO 9001, ISO 14001"
        }
        form = RFQForm(data=data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['item'], "Item B")
        self.assertEqual(form.cleaned_data['due_date'], date(2025, 5, 1))
        self.assertEqual(form.cleaned_data['amount_required_lbs'], 100.5)
        self.assertEqual(form.cleaned_data['ship_to_location'], "123 Test Street")
        self.assertEqual(form.cleaned_data['required_certifications'], "ISO 9001, ISO 14001")

        response = self.client.post(reverse('create-rfq'), data=data)
        self.assertEqual(response.status_code, 302)  # Redirect to RFQ list
        self.assertTrue(RFQ.objects.filter(item="Item B").exists())

    def test_post_create_rfq_invalid(self):
        # Invalid data for RFQ creation (missing required fields)
        data = {
            "item": "",
            "due_date": "",
            "amount_required_lbs": "",
            "ship_to_location": "",
            "required_certifications": ""
        }
        form = RFQForm(data=data)
        self.assertFalse(form.is_valid())
        response = self.client.post(reverse('create-rfq'), data=data)
        self.assertEqual(response.status_code, 200)  # Re-renders the form with errors
        self.assertContains(response, "This field is required.")  # Check for error message
        self.assertFalse(RFQ.objects.filter(item="").exists())

class GenerateEmailViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.rfq = RFQ.objects.create(item="Item A")
        self.supplier = Supplier.objects.create(company_name="Supplier A")
        self.quote = Quote.objects.create(rfq=self.rfq, supplier=self.supplier, price_per=10.5)

    def test_post_generate_email(self):
        response = self.client.post(reverse('generate-email', args=[self.quote.id]))
        self.assertEqual(response.status_code, 200)
        self.assertIn("email_body", response.json())
        self.assertIn("missing", response.json()["status"])

    # Test with no missing fields
    def test_post_generate_email_no_missing_fields(self):
        response = self.client.post(reverse('generate-email', args=[self.quote.id]), data={"missing": False})
        self.assertEqual(response.status_code, 200)
        self.assertIn("email_body", response.json())
        self.assertNotIn("missing", response.json())

