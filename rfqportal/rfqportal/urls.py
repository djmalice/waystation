from django.urls import path
from compareapp.views import SupplierListView, SupplierDetailView, RFQListView, RFQDetailView, RFQQuotesView, SubmitQuoteEmailView, ProcessEmailView, CreateRFQView

urlpatterns = [
    path('suppliers/', SupplierListView.as_view(), name='supplier-list'),
    path('suppliers/<int:pk>/', SupplierDetailView.as_view(), name='supplier-detail'),
    path('rfqs/', RFQListView.as_view(), name='rfq-list'),
    path('rfqs/<int:pk>/', RFQDetailView.as_view(), name='rfq-detail'),
    path('rfqs/<int:pk>/quotes/', RFQQuotesView.as_view(), name='rfq-quotes'),
    path('rfqs/<int:pk>/submit-quote-email/', SubmitQuoteEmailView.as_view(), name='submit-quote-email'),
    path('process-email/', ProcessEmailView.as_view(), name='process-email'),
    path('rfqs/create/', CreateRFQView.as_view(), name='create-rfq'),
]