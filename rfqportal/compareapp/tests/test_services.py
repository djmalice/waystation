from unittest.mock import patch
from django.test import TestCase
from ..services import create_supplier, update_supplier, delete_supplier, create_rfq, update_rfq, delete_rfq, get_quotes_for_rfq, process_email_text
from ..models import Supplier, RFQ, Quote, Email

class ServicesTestCase(TestCase):

    def setUp(self):
        # Set up initial data for testing
        self.supplier_data = {
            "company_name": "Test Supplier",
            "main_contact_name": "John Doe",
            "main_contact_email": "john@example.com",
            "main_contact_phone": "1234567890",
            "hq_address": "123 Test St",
            "payment_terms": "Net 30"
        }
        self.rfq_data = {
            "amount_required_lbs": 100.5,
            "item": "Test Item",
            "ship_to_location": "456 Test Ave",
            "required_certifications": "ISO 9001",
            "due_date": "2023-12-31"
        }

    def test_create_supplier(self):
        supplier = create_supplier(self.supplier_data)
        self.assertEqual(supplier.company_name, self.supplier_data["company_name"])

    def test_update_supplier(self):
        supplier = create_supplier(self.supplier_data)
        updated_data = {"main_contact_name": "Jane Doe"}
        updated_supplier = update_supplier(supplier.pk, updated_data)
        self.assertEqual(updated_supplier.main_contact_name, "Jane Doe")

    def test_delete_supplier(self):
        supplier = create_supplier(self.supplier_data)
        delete_supplier(supplier.pk)
        self.assertFalse(Supplier.objects.filter(pk=supplier.pk).exists())

    def test_create_rfq(self):
        rfq = create_rfq(self.rfq_data)
        self.assertEqual(rfq.item, self.rfq_data["item"])

    def test_update_rfq(self):
        rfq = create_rfq(self.rfq_data)
        updated_data = {"description": "Updated Description"}
        updated_rfq = update_rfq(rfq.pk, updated_data)
        self.assertEqual(updated_rfq.description, "Updated Description")

    def test_delete_rfq(self):
        rfq = create_rfq(self.rfq_data)
        delete_rfq(rfq.pk)
        self.assertFalse(RFQ.objects.filter(pk=rfq.pk).exists())

    def test_get_quotes_for_rfq(self):
        rfq = create_rfq(self.rfq_data)
        quotes = get_quotes_for_rfq(rfq.id)
        self.assertEqual(quotes, [])