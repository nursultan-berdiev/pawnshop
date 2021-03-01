from django.urls import path
from .views import ClientListView, \
    ActiveListView, ClientDetailView, \
    ClientCreateView, ClientUpdateView, \
    ClientDeleteView, my_view, excel_report
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', login_required(ActiveListView.as_view()), name='journal-home'),
    path('client/<int:pk>/', login_required(ClientDetailView.as_view()), name='client-detail'),
    path('journal/', login_required(ClientListView.as_view()), name='journal'),
    path('client/new/', login_required(ClientCreateView.as_view()), name='client-create'),
    path('client/<int:pk>/update', login_required(ClientUpdateView.as_view()), name='client-update'),
    path('client/<int:pk>/delete', login_required(ClientDeleteView.as_view()), name='client-delete'),
    path('client/<int:pk>/excel-report', login_required(excel_report), name='excel-report'),
]
