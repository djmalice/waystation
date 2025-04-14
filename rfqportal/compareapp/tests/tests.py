from django.test import TestCase
from ..models import Supplier, RFQ, Quote, Email

class SupplierModelTest(TestCase):
    def setUp(self):
        self.supplier = Supplier.objects.create(
            company_name="Test Supplier",
            main_contact_name="John Doe",
            main_contact_email="john.doe@example.com",
            main_contact_phone="1234567890",
            hq_address="123 Test Street",
            payment_terms="Net 30"
        )

    def test_supplier_creation(self):
        self.assertEqual(self.supplier.company_name, "Test Supplier")
        self.assertEqual(self.supplier.main_contact_name, "John Doe")
        self.assertEqual(self.supplier.main_contact_email, "john.doe@example.com")
        self.assertEqual(self.supplier.main_contact_phone, "1234567890")
        self.assertEqual(self.supplier.hq_address, "123 Test Street")
        self.assertEqual(self.supplier.payment_terms, "Net 30")

class RFQModelTest(TestCase):
    def setUp(self):
        self.rfq = RFQ.objects.create(
            item="Test Item",
            due_date="2023-12-31",
            amount_required_lbs=100.5,
            ship_to_location="456 Test Avenue",
            required_certifications="ISO 9001"
        )

    def test_rfq_creation(self):
        self.assertEqual(self.rfq.item, "Test Item")
        self.assertEqual(self.rfq.due_date, "2023-12-31")
        self.assertEqual(self.rfq.amount_required_lbs, 100.5)
        self.assertEqual(self.rfq.ship_to_location, "456 Test Avenue")
        self.assertEqual(self.rfq.required_certifications, "ISO 9001")

class QuoteModelTest(TestCase):
    def setUp(self):
        self.supplier = Supplier.objects.create(company_name="Test Supplier")
        self.rfq = RFQ.objects.create(item="Test Item")
        self.quote = Quote.objects.create(
            rfq=self.rfq,
            supplier=self.supplier,
            date_submitted="2023-12-01",
            price_per_pound=10.5,
            country_of_origin="USA",
            certifications="ISO 9001",
            minimum_order_quantity=100
        )

    def test_quote_creation(self):
        self.assertEqual(self.quote.rfq, self.rfq)
        self.assertEqual(self.quote.supplier, self.supplier)
        self.assertEqual(self.quote.date_submitted, "2023-12-01")
        self.assertEqual(self.quote.price_per_pound, 10.5)
        self.assertEqual(self.quote.country_of_origin, "USA")
        self.assertEqual(self.quote.certifications, "ISO 9001")
        self.assertEqual(self.quote.minimum_order_quantity, 100)

class EmailModelTest(TestCase):
    def setUp(self):
        self.supplier = Supplier.objects.create(company_name="Test Supplier")
        self.rfq = RFQ.objects.create(item="Test Item")
        self.quote = Quote.objects.create(rfq=self.rfq, supplier=self.supplier)
        self.email = Email.objects.create(
            related_quote=self.quote,
            extracted_data={"key": "value"},
            content="Test email content"
        )

    def test_email_creation(self):
        self.assertEqual(self.email.related_quote, self.quote)
        self.assertEqual(self.email.extracted_data, {"key": "value"})
        self.assertEqual(self.email.content, "Test email content")
