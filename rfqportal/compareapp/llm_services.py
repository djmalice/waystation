import logging
from django.conf import settings
from openai import OpenAI
import json
from datetime import datetime

def extract_email_data(email_text: str, model: str = "gpt-4") -> dict:
    """
    Extracts structured data from a supplier email using GPT-4.

    Args:
        email_text (str): The raw email content.
        model (str): The OpenAI model to use (default is "gpt-4").

    Returns:
        dict: A dictionary with keys: supplier_company_name, main_contact_name, 
              main_contact_email, hq_address, payment_terms, date_submitted, 
              price_per_pound, country_of_origin, certifications, 
              minimum_order_quantity.
    """

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
        - price_per_pound: The quoted price per pound of the product, as a numeric value (e.g., 1.20).
        - country_of_origin: The country where the product originates.
        - certifications: A list of all certifications mentioned (as strings).
        - minimum_order_quantity: The minimum order quantity, as a numeric value (e.g., 10000).

        Return null for any field that cannot be confidently determined from the email content. Only extract and return the values mentioned in the email body.

        Here is the email:

        {email_text}
    """
    try:
        logging.info(f"Sending prompt to OpenAI:")
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
        )

        result = response.choices[0].message.content

         # Try parsing the response as JSON
        try:
                data = json.loads(result)
                if data.get("date_submitted") is None:
                    data["date_submitted"] = datetime.today().strftime('%Y-%m-%d')
                logging.info("Successfully extracted data.")
                return data
        except json.JSONDecodeError as json_err:
                logging.error(f"JSON decoding failed: {json_err}")
                logging.debug("Raw model output:\n" + result)
                return None

    except client.error.OpenAIError as api_err:
            logging.warning(f"API call failed: {api_err}")
            return None

    return data