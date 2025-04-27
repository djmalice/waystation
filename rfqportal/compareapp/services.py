from .models import Supplier, RFQ, Quote, Email
from .llm_services import extract_email_data
import json

def create_supplier(data):
    return Supplier.objects.create(**data)

def update_supplier(pk, data):
    supplier = Supplier.objects.get(pk=pk)
    for field, value in data.items():
        setattr(supplier, field, value)
    supplier.save()
    return supplier

def delete_supplier(pk):
    supplier = Supplier.objects.get(pk=pk)
    supplier.delete()

def create_rfq(data):
    return RFQ.objects.create(**data)

def update_rfq(pk, data):
    rfq = RFQ.objects.get(pk=pk)
    for field, value in data.items():
        setattr(rfq, field, value)
    rfq.save()
    return rfq

def delete_rfq(pk):
    rfq = RFQ.objects.get(pk=pk)
    rfq.delete()

def get_quotes_for_rfq(rfq_id):
    quotes = Quote.objects.filter(rfq_id=rfq_id).values()
    return list(quotes)

def send_quote_email(rfq_id, email):
    # Logic to send email (e.g., using Django's EmailMessage)
    # For now, return a placeholder status
    return "Email sent successfully"

def process_email_text(email_text, rfq):
    # Simulate LLM processing (replace with actual LLM API call)
    extracted_data = extract_email_data(email_text)

    if extracted_data is None:
        return {"status": "fail", "message": "Failed to extract data from email."}

    # Convert Pydantic model to dictionary
    extracted_data_dict = extracted_data.dict()

    # Parse extracted data and create or retrieve related objects
    supplier, _ = Supplier.objects.get_or_create(
        company_name=extracted_data_dict["supplier_company_name"],
        defaults={
            "main_contact_name": extracted_data_dict["main_contact_name"],
            "main_contact_email": extracted_data_dict["main_contact_email"],
            "main_contact_phone": extracted_data_dict["main_contact_phone"],
            "hq_address": extracted_data_dict["hq_address"],
            "payment_terms": extracted_data_dict["payment_terms"]
        }
    )

    quote = Quote.objects.create(
        rfq=rfq,
        supplier=supplier,
        date_submitted=extracted_data_dict["date_submitted"],
        price_per=extracted_data_dict["price_per"],
        country_of_origin=extracted_data_dict["country_of_origin"],
        certifications=",".join(extracted_data_dict["certifications"]),
        minimum_order_quantity=extracted_data_dict["minimum_order_quantity"]
    )

    email = Email.objects.create(
        related_quote=quote,
        extracted_data=json.dumps(extracted_data_dict),  # Store as JSON string
        content=email_text
    )

    return {"status": "success", "message": "Quote, Supplier, RFQ, and Email created successfully", "quote_id": quote.id}
