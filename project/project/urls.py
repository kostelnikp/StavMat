"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from stavMat import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),

    # Employee
    path('login/', views.login_employee, name='login_employee'),
    path('login/loginEmployee', views.login_employee_form, name='login_employee_form'),
    path('employee/logout/', views.logout_employee, name='logout_employee'),

    # Customer
    path('customer/', views.customer, name='customer'),
    path('customer/register/', views.register_customer, name='register_customer'),
    path('customer/registerCustomer/', views.register_customer_form, name='register_customer_form'),
    path('customer/login/', views.login_customer, name='login_customer'),
    path('customer/logout/', views.logout_customer, name='logout_customer'),
    path('customer/loginCustomer/', views.login_customer_form, name='login_customer_form'),

    # Logged customer
    path('customer/account', views.user_dashboard, name='user_dashboard'),
    path('customer/account/', views.user_account, name='user_account'),
    path('customer/project/', views.user_project, name='user_project'),
    path('customer/project/create/', views.create_project, name='create_project'),
    path('customer/project/info/<int:projekt_id>/', views.project_info, name='project_info'),
    path('customer/project/info/edit/<int:projekt_id>/', views.project_edit, name='project_edit'),
    path('customer/account/edit/', views.edit_account, name='edit_account'),
    path('customer/faktura/', views.user_faktura, name='user_faktura'),
    path('customer/faktura/info/<int:faktura_id>/', views.user_faktura_info, name='user_faktura_info'),

    # Logged employee
    path('employee/account/', views.employee_account, name='employee_account'),
    path('employee/account/edit/', views.edit_employee_account, name='edit_employee_account'),
    path('employee/work/', views.employee_work, name='employee_work'),
    path('employee/work/create/', views.create_work, name='create_work'),
    path('employee/work/info/<int:praca_id>/', views.work_info, name='work_info'),
    path('employee/work/info/edit/<int:praca_id>/', views.work_edit, name='work_edit'),
    path('employee/work/info/edit/<int:praca_id>/materials', views.work_edit_materials, name='work_edit_materials'),
    path('employee/work/info/edit/<int:praca_id>/materials/<int:material_id>/', views.delete_material,
         name='delete_material'),
    path('employee/details/', views.employee_details, name='employee_details'),
    path('employee/details/info/<int:zamestnanec_id>/', views.employee_info, name='employee_info'),
    path('employee/details/info/edit/<int:zamestnanec_id>/', views.employee_edit, name='employee_edit'),
    path('employee/details/create/', views.create_employee, name='create_employee'),
    path('employee/details/delete/<int:zamestnanec_id>/', views.delete_employee, name='delete_employee'),
    path('employee/materials/', views.employee_materials, name='employee_materials'),
    path('employee/materials/create/', views.create_material, name='create_material'),
    path('employee/materials/delete/<int:material_id>/', views.delete_material_spec, name='delete_material_spec'),
    path('employee/customer/', views.employee_customer, name='employee_customer'),
    path('employee/customer/info/<int:zakaznik_id>/', views.customer_info, name='customer_info'),
    path('employee/faktura/', views.employee_faktura, name='employee_faktura'),
    path('employee/faktura/create/', views.create_faktura, name='create_faktura'),
    path('employee/faktura/info/<int:faktura_id>/', views.faktura_info, name='faktura_info'),
    path('employee/faktura/info/edit/<int:faktura_id>/', views.faktura_edit, name='faktura_edit'),


]
