from django.db import models

class Supplier(models.Model):
    company_name = models.CharField(max_length=255, primary_key=True)
    main_contact_name = models.CharField(max_length=255, null=True, blank=True)
    main_contact_email = models.EmailField(null=True, blank=True)
    main_contact_phone = models.CharField(max_length=20, null=True, blank=True)
    hq_address = models.TextField(null=True, blank=True)
    payment_terms = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.company_name

class RFQ(models.Model):
    item = models.CharField(max_length=255)
    due_date = models.DateField(null=True, blank=True)
    amount_required_lbs = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    ship_to_location = models.TextField(null=True, blank=True)
    required_certifications = models.TextField(null=True, blank=True)  # List of certifications

    def __str__(self):
        return f"RFQ for {self.item} (Due: {self.due_date})"

class Quote(models.Model):
    rfq = models.ForeignKey(RFQ, on_delete=models.CASCADE, related_name="rfqs")
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name="suppliers")
    date_submitted = models.DateField(null=True, blank=True)
    price_per_pound = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    country_of_origin = models.CharField(max_length=255, null=True, blank=True)
    certifications = models.TextField(null=True, blank=True)  # List of certifications
    minimum_order_quantity = models.BigIntegerField(null=True, blank=True)

    def __str__(self):
        return f"Quote by {self.supplier.company_name} for {self.rfq.item}"

class Email(models.Model):
    related_quote = models.ForeignKey(Quote, on_delete=models.CASCADE, related_name="emails", null=True, blank=True)
    extracted_data = models.JSONField(null=True, blank=True)  # JSON field to store extracted quote or supplier data
    content = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Email related to Quote ID {self.related_quote.id if self.related_quote else 'N/A'}"
