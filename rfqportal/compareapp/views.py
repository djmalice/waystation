from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views import View
from .models import Supplier, RFQ
from django.forms.models import model_to_dict
import json
from .services import get_quotes_for_rfq, send_quote_email, process_email_text
from .forms import RFQForm

class SupplierListView(View):
    def get(self, request):
        suppliers = Supplier.objects.all()
        return render(request, 'compareapp/supplier_list.html', {'suppliers': suppliers})

class SupplierDetailView(View):
    def get(self, request, pk):
        supplier = get_object_or_404(Supplier, pk=pk)
        return render(request, 'compareapp/supplier_detail.html', {'supplier': supplier})

    def post(self, request):
        data = json.loads(request.body)
        supplier = Supplier.objects.create(**data)
        return JsonResponse(model_to_dict(supplier), status=201)

    def put(self, request, pk):
        supplier = get_object_or_404(Supplier, pk=pk)
        data = json.loads(request.body)
        for field, value in data.items():
            setattr(supplier, field, value)
        supplier.save()
        return JsonResponse(model_to_dict(supplier))

    def delete(self, request, pk):
        supplier = get_object_or_404(Supplier, pk=pk)
        supplier.delete()
        return JsonResponse({"message": "Supplier deleted"}, status=204)

class RFQListView(View):
    def get(self, request):
        rfqs = RFQ.objects.all()
        return render(request, 'compareapp/rfq_list.html', {'rfqs': rfqs})

class RFQDetailView(View):
    def get(self, request, pk):
        rfq = get_object_or_404(RFQ, pk=pk)
        return render(request, 'compareapp/rfq_detail.html', {'rfq': rfq})

    def post(self, request):
        data = json.loads(request.body)
        rfq = RFQ.objects.create(**data)
        return JsonResponse(model_to_dict(rfq), status=201)

    def put(self, request, pk):
        rfq = get_object_or_404(RFQ, pk=pk)
        data = json.loads(request.body)
        for field, value in data.items():
            setattr(rfq, field, value)
        rfq.save()
        return JsonResponse(model_to_dict(rfq))

    def delete(self, request, pk):
        rfq = get_object_or_404(RFQ, pk=pk)
        rfq.delete()
        return JsonResponse({"message": "RFQ deleted"}, status=204)

class RFQQuotesView(View):
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

class SubmitQuoteEmailView(View):
    def get(self, request, pk):
        rfq = get_object_or_404(RFQ, pk=pk)
        return render(request, 'compareapp/submit_quote_email.html', {'rfq': rfq})

    def post(self, request, pk):
        email_content = request.POST.get('email_content')
        rfq = get_object_or_404(RFQ, pk=pk)
        # Assuming email_content contains the email text to be processed
        # Process the email content and extract data
        result = process_email_text(email_content,rfq)
        # Assuming process_email_text returns a dictionary with a status or similar
        if result.get('status') == 'success':
            return redirect('rfq-list')
        return render(request, 'compareapp/submit_quote_email.html', {'rfq': get_object_or_404(RFQ, pk=pk), 'error': 'Failed to process email content'})

class ProcessEmailView(View):
    def get(self, request):
        return render(request, 'compareapp/process_email.html')

    def post(self, request):
        email_text = request.POST.get('email_text')
        result = process_email_text(email_text)
        return JsonResponse(result)

class CreateRFQView(View):
    def get(self, request):
        form = RFQForm()
        return render(request, 'compareapp/create_rfq.html', {'form': form})

    def post(self, request):
        form = RFQForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('rfq-list')
        return render(request, 'compareapp/create_rfq.html', {'form': form, 'errors': form.errors})
