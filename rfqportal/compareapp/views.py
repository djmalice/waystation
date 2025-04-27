# Import necessary modules and classes
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views import View
from .models import Supplier, RFQ
from django.forms.models import model_to_dict
import json
from .services import get_quotes_for_rfq, send_quote_email, process_email_text, check_missing_fields_and_generate_email
from .forms import RFQForm

# Define views for handling supplier-related operations
class SupplierListView(View):
    """
    View to list all suppliers.
    """
    def get(self, request):
        suppliers = Supplier.objects.all()
        return render(request, 'compareapp/supplier_list.html', {'suppliers': suppliers})

class SupplierDetailView(View):
    """
    View to handle CRUD operations for a single supplier.
    """
    def get(self, request, pk):
        supplier = get_object_or_404(Supplier, pk=pk)
        return render(request, 'compareapp/supplier_detail.html', {'supplier': supplier})

    def post(self, request):
        # Create a new supplier
        data = json.loads(request.body)
        supplier = Supplier.objects.create(**data)
        return JsonResponse(model_to_dict(supplier), status=201)

    def put(self, request, pk):
        # Update an existing supplier
        supplier = get_object_or_404(Supplier, pk=pk)
        data = json.loads(request.body)
        for field, value in data.items():
            setattr(supplier, field, value)
        supplier.save()
        return JsonResponse(model_to_dict(supplier))

    def delete(self, request, pk):
        # Delete a supplier
        supplier = get_object_or_404(Supplier, pk=pk)
        supplier.delete()
        return JsonResponse({"message": "Supplier deleted"}, status=204)

# Define views for handling RFQ-related operations
class RFQListView(View):
    """
    View to list all RFQs.
    """
    def get(self, request):
        rfqs = RFQ.objects.all()
        return render(request, 'compareapp/rfq_list.html', {'rfqs': rfqs})

class RFQDetailView(View):
    """
    View to handle CRUD operations for a single RFQ.
    """
    def get(self, request, pk):
        rfq = get_object_or_404(RFQ, pk=pk)
        return render(request, 'compareapp/rfq_detail.html', {'rfq': rfq})

    def post(self, request):
        # Create a new RFQ
        data = json.loads(request.body)
        rfq = RFQ.objects.create(**data)
        return JsonResponse(model_to_dict(rfq), status=201)

    def put(self, request, pk):
        # Update an existing RFQ
        rfq = get_object_or_404(RFQ, pk=pk)
        data = json.loads(request.body)
        for field, value in data.items():
            setattr(rfq, field, value)
        rfq.save()
        return JsonResponse(model_to_dict(rfq))

    def delete(self, request, pk):
        # Delete an RFQ
        rfq = get_object_or_404(RFQ, pk=pk)
        rfq.delete()
        return JsonResponse({"message": "RFQ deleted"}, status=204)

# Define views for handling quotes related to an RFQ
class RFQQuotesView(View):
    """
    View to display quotes for a specific RFQ.
    """
    def get(self, request, pk):
        rfq = get_object_or_404(RFQ, pk=pk)
        quotes = get_quotes_for_rfq(pk)
        # Add supplier object to each quote if not already present
        for quote in quotes:
            if 'supplier' not in quote:
                supplier = Supplier.objects.get(pk=quote['supplier_id'])
                quote['supplier'] = {
                    'company_name': supplier.company_name,
                    'main_contact_name': supplier.main_contact_name,
                    'main_contact_email': supplier.main_contact_email,
                    'main_contact_phone': supplier.main_contact_phone,
                    'hq_address': supplier.hq_address,
                    'payment_terms': supplier.payment_terms
                }
        return render(request, 'compareapp/rfq_quotes.html', {'rfq': rfq, 'quotes': quotes})

# Define views for processing email submissions
class SubmitQuoteEmailView(View):
    """
    View to handle email submissions for a specific RFQ.
    """
    def get(self, request, pk):
        rfq = get_object_or_404(RFQ, pk=pk)
        return render(request, 'compareapp/submit_quote_email.html', {'rfq': rfq})

    def post(self, request, pk):
        # Process the submitted email content
        email_content = request.POST.get('email_content')
        rfq = get_object_or_404(RFQ, pk=pk)
        result = process_email_text(email_content, rfq)
        if result.get('status') == 'success':
            return redirect('rfq-list')
        return render(request, 'compareapp/submit_quote_email.html', {'rfq': rfq, 'error': 'Failed to process email content'})

class ProcessEmailView(View):
    """
    View to process email content and extract data.
    """
    def get(self, request):
        return render(request, 'compareapp/process_email.html')

    def post(self, request):
        email_text = request.POST.get('email_text')
        result = process_email_text(email_text)
        return JsonResponse(result)

# Define views for creating RFQs
class CreateRFQView(View):
    """
    View to create a new RFQ.
    """
    def get(self, request):
        form = RFQForm()
        return render(request, 'compareapp/create_rfq.html', {'form': form})

    def post(self, request):
        form = RFQForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('rfq-list')
        return render(request, 'compareapp/create_rfq.html', {'form': form, 'errors': form.errors})

# Define views for generating email drafts
class GenerateEmailView(View):
    """
    View to handle the generation of an email draft for missing fields in a quote.

    This view checks for missing fields in a quote and generates an email draft
    to request the missing information from the supplier.
    """
    def post(self, request, pk):
        """
        Handle POST requests to generate an email draft.

        Args:
            request (HttpRequest): The HTTP request object.
            pk (int): The primary key of the quote.

        Returns:
            JsonResponse: A JSON response containing the email draft or an error message.
        """
        result = check_missing_fields_and_generate_email(pk)
        return JsonResponse(result)
