from django.urls import path
from compareapp.views import SupplierListView, SupplierDetailView, RFQListView, RFQDetailView, RFQQuotesView, SubmitQuoteEmailView, CreateRFQView, GenerateEmailView

urlpatterns = [
    path('',RFQListView.as_view(), name='home'),
    path('suppliers/', SupplierListView.as_view(), name='supplier-list'),
    path('suppliers/<str:pk>/', SupplierDetailView.as_view(), name='supplier-detail'),
    path('rfqs/', RFQListView.as_view(), name='rfq-list'),
    path('rfqs/<int:pk>/', RFQDetailView.as_view(), name='rfq-detail'),
    path('rfqs/<int:pk>/quotes/', RFQQuotesView.as_view(), name='rfq-quotes'),
    path('rfqs/<int:pk>/submit-quote-email/', SubmitQuoteEmailView.as_view(), name='submit-quote-email'),
    path('rfqs/create/', CreateRFQView.as_view(), name='create-rfq'),
    path('generate-email/<int:pk>/', GenerateEmailView.as_view(), name='generate-email'),
]