import logging
from django.conf import settings
from openai import OpenAI
import json
from datetime import datetime
from pydantic import BaseModel

def extract_email_data(email_text: str, model: str = "o4-mini") -> dict:
    """
    Extracts structured data from a supplier email using GPT-4.

    Args:
        email_text (str): The raw email content.
        model (str): The OpenAI model to use (default is "o4-mini").

    Returns:
        dict: A dictionary with keys: supplier_company_name, main_contact_name, 
              main_contact_email, hq_address, payment_terms, date_submitted, 
              price_per, country_of_origin, certifications, 
              minimum_order_quantity.
    """
    class EmailData(BaseModel):
        supplier_company_name: str
        main_contact_name: str
        main_contact_email: str
        main_contact_phone: str
        hq_address: str
        payment_terms: str
        date_submitted: str
        price_per: float
        country_of_origin: str
        certifications: list[str]
        minimum_order_quantity: int


    # Set up OpenAI API key
    client = OpenAI(api_key = settings.OPENAI_API_KEY)
    system_prompt = "You are a helpful assistant that extracts structured data from emails."

    user_prompt = f"""
        Process the following email and extract a JSON object with the following fields:
        - supplier_company_name: The name of the supplier's company.
        - main_contact_name: The name of the main contact person at the supplier's company.
        - main_contact_email: The email address of the main contact person.
        - main_contact_phone: The phone number of the main contact person.
        - hq_address: The headquarters address of the supplier's company.
        - payment_terms: The payment terms mentioned in the email.
        - date_submitted: The date this email was submitted or sent (infer this from the current date if not mentioned).
        - price: The quoted price per pound or per gallon of the product, as a numeric value (e.g., 1.20).
        - country_of_origin: The country where the product originates.
        - certifications: A list of all certifications mentioned (as strings).
        - minimum_order_quantity: The minimum order quantity, as a numeric value (e.g., 10000).

        Return null for any field that cannot be confidently determined from the email content. Only extract and return the values mentioned in the email body.

        Here is the email:

        {email_text}
    """
    try:
        logging.info(f"Sending prompt to OpenAI:")
        response = client.responses.parse(
            model=model,
            input=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            text_format=EmailData
        )
        logging.info(f"Received response from OpenAI: {response}")

        # Check if the conversation was too long for the context window, resulting in incomplete JSON 
        if response.status == "incomplete" and response.incomplete_details.reason == "max_output_tokens":
            # your code should handle this error case
            pass

        # Check if the model's output included restricted content, so the generation of JSON was halted and may be partial
        if response.status == "incomplete" and response.incomplete_details.reason == "content_filter":
            # your code should handle this error case
            pass

        if response.status == "completed":         
            data = response.output_parsed
            if data.date_submitted is None:
                data.date_submitted = datetime.today().strftime('%Y-%m-%d')
            logging.info("Successfully extracted data.")
       
    except Exception as api_err:
            logging.warning(f"API call failed: {api_err}")
            return None

    return data