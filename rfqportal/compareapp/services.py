# Import necessary modules and models
from .models import Supplier, RFQ, Quote, Email
from .llm_services import extract_email_data
from celery import shared_task
import json

# Define service functions for supplier operations
def create_supplier(data):
    """
    Create a new supplier.

    Args:
        data (dict): Data for creating the supplier.

    Returns:
        Supplier: The created supplier object.
    """
    return Supplier.objects.create(**data)

def update_supplier(pk, data):
    """
    Update an existing supplier.

    Args:
        pk (int): Primary key of the supplier to update.
        data (dict): Data for updating the supplier.

    Returns:
        Supplier: The updated supplier object.
    """
    supplier = Supplier.objects.get(pk=pk)
    for field, value in data.items():
        setattr(supplier, field, value)
    supplier.save()
    return supplier

def delete_supplier(pk):
    """
    Delete a supplier.

    Args:
        pk (int): Primary key of the supplier to delete.
    """
    supplier = Supplier.objects.get(pk=pk)
    supplier.delete()

# Define service functions for RFQ operations
def create_rfq(data):
    """
    Create a new RFQ.

    Args:
        data (dict): Data for creating the RFQ.

    Returns:
        RFQ: The created RFQ object.
    """
    return RFQ.objects.create(**data)

def update_rfq(pk, data):
    """
    Update an existing RFQ.

    Args:
        pk (int): Primary key of the RFQ to update.
        data (dict): Data for updating the RFQ.

    Returns:
        RFQ: The updated RFQ object.
    """
    rfq = RFQ.objects.get(pk=pk)
    for field, value in data.items():
        setattr(rfq, field, value)
    rfq.save()
    return rfq

def delete_rfq(pk):
    """
    Delete an RFQ.

    Args:
        pk (int): Primary key of the RFQ to delete.
    """
    rfq = RFQ.objects.get(pk=pk)
    rfq.delete()

# Define service functions for quote operations
def get_quotes_for_rfq(rfq_id):
    """
    Retrieve all quotes for a specific RFQ.

    Args:
        rfq_id (int): ID of the RFQ.

    Returns:
        list: List of quotes for the RFQ.
    """
    quotes = Quote.objects.filter(rfq_id=rfq_id).values()
    return list(quotes)

@shared_task(bind=True)
def process_email_text(self, email_text, rfq_id):
    """
    Process email text and extract data.

    Args:
        email_text (str): The email content.
        rfq (RFQ): The RFQ object related to the email.

    Returns:
        dict: Status and message of the processing result.
    """
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

    rfq = RFQ.objects.get(pk=rfq_id)
    quote = Quote.objects.create(
        rfq=rfq,
        supplier=supplier,
        date_submitted=extracted_data_dict["date_submitted"],
        price_per=extracted_data_dict["price_per"],
        country_of_origin=extracted_data_dict["country_of_origin"],
        certifications=",".join(extracted_data_dict["certifications"]),
        minimum_order_quantity=extracted_data_dict["minimum_order_quantity"]
    )

    Email.objects.create(
        related_quote=quote,
        extracted_data=json.dumps(extracted_data_dict),  # Store as JSON string
        content=email_text
    )

def check_missing_fields_and_generate_email(quote_id):
    """
    Check for missing fields in a quote and generate an email draft.

    Args:
        quote_id (int): ID of the quote to check.

    Returns:
        dict: Status and email draft or error message.
    """
    # Get the quote and related supplier
    try:
        quote = Quote.objects.get(id=quote_id)
        supplier = quote.supplier
    except Quote.DoesNotExist:
        return {"status": "fail", "message": "Quote not found."}

    # Define required fields and check for missing values
    required_fields = {
        "main_contact_name": supplier.main_contact_name,
        "main_contact_email": supplier.main_contact_email,
        "main_contact_phone": supplier.main_contact_phone,
        "hq_address": supplier.hq_address,
        "payment_terms": supplier.payment_terms,
        "date_submitted": quote.date_submitted,
        "price_per": quote.price_per,
        "country_of_origin": quote.country_of_origin,
        "certifications": quote.certifications,
        "minimum_order_quantity": quote.minimum_order_quantity,
    }

    missing_fields = {field: value for field, value in required_fields.items() if not value}

    if not missing_fields:
        return {"status": "success", "message": "No missing fields."}

    # Generate email draft
    email_body = f"Dear {supplier.company_name},\n\n"
    email_body += "We noticed that some information is missing from your quote. Could you please provide the following details?\n\n"
    for field in missing_fields:
        email_body += f"- {field.replace('_', ' ').capitalize()}\n"
    email_body += "\nThank you for your prompt attention to this matter.\n\nBest regards,\n[Your Company Name]"

    return {"status": "missing", "email_body": email_body}
