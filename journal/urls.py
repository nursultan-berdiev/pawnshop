from django.urls import path
from .views import excel_report
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', login_required(views.index), name='index'),
    path('products/', login_required(views.product_list), name='product_list'),
    path('create/', login_required(views.product_create), name='product_create'),
    path('products/<int:pk>/update', login_required(views.ProductUpdateView.as_view()), name='product_update'),
    path('products/<int:pk>/delete', login_required(views.ProductDeleteView.as_view()), name='product_delete'),
    path('client/<int:pk>/excel-report', login_required(excel_report), name='excel-report'),
    path('products/<int:pk>/', login_required(views.ProductDetailView.as_view()), name='product_detail'),
    path('products/<int:pk>/early_payment', login_required(views.early_repayment), name='early_repayment'),
    path('new_day/', login_required(views.new_day), name='new_day'),
    path('products/<int:pk>/prolongation', login_required(views.prolongation), name='prolongation'),
]
