from django.urls import path
from .views import  \
    ActiveListView, LoanDetailView, \
    createLoanView, update_loan, \
    LoanDeleteView, my_view, excel_report, dashboard, loan_create, loan_list
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', login_required(ActiveListView.as_view()), name='journal-home'),
    path('client/<int:pk>/', login_required(LoanDetailView.as_view()), name='client-detail'),
    path('journal/', login_required(loan_list), name='journal'),
    path('journal/client/new/', login_required(createLoanView), name='client-create'),
    path('client/<int:pk>/update', login_required(update_loan), name='client-update'),
    path('client/<int:pk>/delete', login_required(LoanDeleteView.as_view()), name='client-delete'),
    path('client/<int:pk>/excel-report', login_required(excel_report), name='excel-report'),
    path('dashboard/', login_required(dashboard), name='dashboard'),
    path('journal/loan/new/', login_required(loan_create), name='loan_create'),
]
