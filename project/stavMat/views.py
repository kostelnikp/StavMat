from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.shortcuts import render, redirect

from .forms import ZakazniciRegisterForm, ZakazniciLoginForm, ZamestnanciLoginForm, ProjektForm, ZakaznikForm, \
    ZamestnanecForm, PracaForm, PouzityMaterialForm, MaterialForm, ZamestnanecCreateForm, FakturaForm
from .models import Zakaznici, Projekt, Zamestnanec, Praca, PouzityMaterial, Material, Faktura


# Create your views here.

def index(request):
    return render(request, 'stavMat/index.html')


def login_employee(request):
    login_form = ZamestnanciLoginForm()
    return render(request, 'stavMat/login_employee.html', {'login_form': login_form})


def logout_employee(request):
    logout(request)
    return redirect('login_employee')


def login_employee_form(request):
    if request.method == 'POST':
        login_form = ZamestnanciLoginForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data['prihlasovacie_meno']
            password = login_form.cleaned_data['prihlasovacie_heslo']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                allowed_groups = ['Zamestnanec', 'Vedúci podniku', 'Hlavný zamestnanec']
                if any(group.name in allowed_groups for group in user.groups.all()):
                    login(request, user)
                    return redirect('user_dashboard')
                else:
                    messages.error(request, 'Prístup povolený len pre zamestnancov.')
            else:
                messages.error(request, 'Nesprávne meno alebo heslo.')
    else:
        login_form = ZamestnanciLoginForm()
    return render(request, 'stavMat/login_employee.html', {'login_form': login_form})


def customer(request):
    return render(request, 'stavMat/customer.html')


def register_customer(request):
    register_form = ZakazniciRegisterForm()
    return render(request, 'stavMat/register_customer.html', {'register_form': register_form})


def register_customer_form(request):
    if request.method == 'POST':
        register_form = ZakazniciRegisterForm(request.POST)
        if register_form.is_valid():
            try:
                prihlasovacie_meno = register_form.cleaned_data.get('prihlasovacie_meno')
                prihlasovacie_heslo = register_form.cleaned_data.get('prihlasovacie_heslo')
                user = User.objects.create_user(username=prihlasovacie_meno, password=prihlasovacie_heslo)
                group = Group.objects.get(name='Zákazník')
                user.groups.add(group)
                user.save()
                register_form.save()
                messages.success(request, 'Registrácia úspešná.')
                return redirect('register_customer')
            except Exception as e:
                if 'username' in str(e):
                    messages.error(request, 'Toto prihlasovacie meno už existuje.')
                else:
                    messages.error(request, e)
        else:
            messages.error(request, 'Registrácia neúspešná.')
    else:
        register_form = ZakazniciRegisterForm()
    return render(request, 'stavMat/register_customer.html', {'register_form': register_form})


def login_customer(request):
    login_form = ZakazniciLoginForm()
    return render(request, 'stavMat/login_customer.html', {'login_form': login_form})


def logout_customer(request):
    logout(request)
    return redirect('login_customer')


def login_customer_form(request):
    if request.method == 'POST':
        login_form = ZakazniciLoginForm(request.POST)
        if login_form.is_valid():
            prihlasovacie_meno = login_form.cleaned_data['prihlasovacie_meno']
            prihlasovacie_heslo = login_form.cleaned_data['prihlasovacie_heslo']
            user = authenticate(request, username=prihlasovacie_meno, password=prihlasovacie_heslo)
            if user is not None:
                if Group.objects.filter(user=user, name='Zákazník').exists():
                    login(request, user)
                    return redirect('user_dashboard')
                else:
                    messages.error(request, 'Prístup povolený len pre zákazníkov.')
            else:
                messages.error(request, 'Nesprávne meno alebo heslo.')
    else:
        login_form = ZakazniciLoginForm()
    return render(request, 'stavMat/login_customer.html', {'login_form': login_form})


@login_required
def user_dashboard(request):
    user = request.user
    if user.groups.filter(name='Zákazník').exists():
        zakaznik = Zakaznici.objects.get(prihlasovacie_meno=user.username)
        return render(request, 'stavMat/login_customer_account.html', {'user': user, 'zakaznik': zakaznik})
    else:
        return render(request, 'stavMat/customer.html', {'user': user})


@login_required
def user_account(request):
    user = request.user
    zakaznik = Zakaznici.objects.get(prihlasovacie_meno=user.username)
    return render(request, 'stavMat/login_customer_account.html', {'user': user, 'zakaznik': zakaznik})


@login_required
def user_project(request):
    user = request.user
    zakaznik = Zakaznici.objects.get(prihlasovacie_meno=user.username)
    projekty = Projekt.objects.filter(zakaznik=zakaznik)
    return render(request, 'stavMat/login_customer_project.html',
                  {'user': user, 'zakaznik': zakaznik, 'projekty': projekty})


@login_required
def create_project(request):
    user = request.user
    zakaznik = Zakaznici.objects.get(prihlasovacie_meno=user.username)
    if request.method == 'POST':
        projekt_form = ProjektForm(request.POST)
        if projekt_form.is_valid():
            projekt = projekt_form.save(commit=False)
            projekt.zakaznik = zakaznik
            projekt.save()
            messages.success(request, 'Projekt bol úspešne vytvorený.')
            return redirect('user_project')
        else:
            messages.error(request, 'Projekt nebol vytvorený.')
    else:
        projekt_form = ProjektForm()
    return render(request, 'stavMat/login_customer_project_create.html', {'projekt_form': projekt_form})


@login_required
def project_info(request, projekt_id):
    projekt = Projekt.objects.get(pk=projekt_id)
    user = request.user
    zakaznik = Zakaznici.objects.get(projekt=projekt)
    return render(request, 'stavMat/login_customer_project_info.html',
                  {'projekt': projekt, user: 'user', 'zakaznik': zakaznik})


@login_required
def project_edit(request, projekt_id):
    projekt = Projekt.objects.get(pk=projekt_id)
    if request.method == 'POST':
        projekt_form = ProjektForm(request.POST, instance=projekt)
        if projekt_form.is_valid():

            messages.success(request, 'Projekt bol úspešne upravený.')
            return redirect('user_project')
        else:
            messages.error(request, 'Projekt nebol upravený.')
    else:
        projekt_form = ProjektForm(instance=projekt)
    return render(request, 'stavMat/login_customer_project_info_change.html',
                  {'projekt': projekt, 'projekt_form': projekt_form})


@login_required
def edit_account(request):
    user = request.user
    zakaznik = Zakaznici.objects.get(prihlasovacie_meno=user.username)
    if request.method == 'POST':
        zakaznik_form = ZakaznikForm(request.POST, instance=zakaznik)
        if zakaznik_form.is_valid():
            zakaznik_form.save()
            messages.success(request, 'Údaje boli úspešne upravené.')
            return redirect('user_account')
        else:
            messages.error(request, 'Údaje neboli upravené.')
    else:
        zakaznik_form = ZakaznikForm(instance=zakaznik)
    return render(request, 'stavMat/login_customer_account_edit.html', {'zakaznik_form': zakaznik_form})


@login_required
def user_faktura(request):
    user = request.user
    zakaznik = Zakaznici.objects.get(prihlasovacie_meno=user.username)
    projekty = Projekt.objects.filter(zakaznik=zakaznik)
    faktury = Faktura.objects.filter(projekt__in=projekty)
    return render(request, 'stavMat/login_customer_faktura.html', {'faktury': faktury})

@login_required
def user_faktura_info(request, faktura_id):
    faktura = Faktura.objects.get(pk=faktura_id)
    return render(request, 'stavMat/login_customer_faktura_info.html', {'faktura': faktura})

@login_required
def employee_account(request):
    user = request.user
    zamestnanec = Zamestnanec.objects.get(prihlasovacie_meno=user.username)
    return render(request, 'stavMat/login_employee_account.html', {'zamestnanec': zamestnanec})


@login_required
def edit_employee_account(request):
    user = request.user
    zamestnanec = Zamestnanec.objects.get(prihlasovacie_meno=user.username)
    if request.method == 'POST':
        zamestnanec_form = ZamestnanecForm(request.POST, instance=zamestnanec)
        if zamestnanec_form.is_valid():
            zamestnanec_form.save()
            messages.success(request, 'Údaje boli úspešne upravené.')
            return redirect('employee_account')
        else:
            messages.error(request, 'Údaje neboli upravené.')
    else:
        zamestnanec_form = ZamestnanecForm(instance=zamestnanec)
    return render(request, 'stavMat/login_employee_account_edit.html', {'zamestnanec_form': zamestnanec_form})


@login_required
def employee_work(request):
    user = request.user
    zamestnanec = Zamestnanec.objects.get(prihlasovacie_meno=user.username)
    if user.groups.filter(name='Hlavný zamestnanec').exists() or user.groups.filter(name='Vedúci podniku').exists():
        prace = Praca.objects.all()
    else:
        prace = Praca.objects.filter(zamestnanec=zamestnanec)
    return render(request, 'stavMat/login_employee_praca.html', {'user': user, 'prace': prace})


@login_required
def create_work(request):
    if request.method == 'POST':
        praca_form = PracaForm(request.POST)
        if praca_form.is_valid():
            praca = praca_form.save(commit=False)
            praca.save()
            messages.success(request, 'Práca bola úspešne vytvorená.')
            return redirect('employee_work')
        else:
            messages.error(request, 'Práca nebola vytvorená.')
    else:
        praca_form = PracaForm()
    return render(request, 'stavMat/login_employee_praca_create.html', {'praca_form': praca_form})


@login_required
def work_info(request, praca_id):
    user = request.user
    praca = Praca.objects.get(pk=praca_id)
    pouzity_material = PouzityMaterial.objects.filter(praca=praca)
    return render(request, 'stavMat/login_employee_praca_info.html',
                  {'praca': praca, 'user': user, 'pouzity_material': pouzity_material})


@login_required
def work_edit(request, praca_id):
    user = request.user
    praca = Praca.objects.get(pk=praca_id)
    pouzity_material = PouzityMaterial.objects.filter(praca=praca)
    if request.method == 'POST':
        praca_form = PracaForm(request.POST, instance=praca)
        if praca_form.is_valid():
            praca_form.save()
            messages.success(request, 'Práca bola úspešne upravená.')
            return redirect('employee_work')
        else:
            messages.error(request, 'Práca nebola upravená.')
    else:
        praca_form = PracaForm(instance=praca)
    return render(request, 'stavMat/login_employee_praca_info_change.html',
                  {'praca': praca, 'praca_form': praca_form, 'user': user, 'pouzity_material': pouzity_material})


@login_required
def work_edit_materials(request, praca_id):
    praca = Praca.objects.get(pk=praca_id)
    if request.method == 'POST':
        pouzity_material_form = PouzityMaterialForm(request.POST)
        if pouzity_material_form.is_valid():
            pouzity_material = pouzity_material_form.save(commit=False)
            pouzity_material.praca = praca
            pouzity_material.save()
            messages.success(request, 'Materiál bol úspešne pridaný ku práci.')
            return redirect('work_info', praca_id=praca_id)
        else:
            messages.error(request, 'Materiál nebol pridaný ku práci.')
    else:
        pouzity_material_form = PouzityMaterialForm()
    return render(request, 'stavMat/login_employee_praca_add_material.html',
                  {'pouzity_material_form': pouzity_material_form, 'praca': praca})


@login_required
def delete_material(request, praca_id, material_id):
    pouzity_material = PouzityMaterial.objects.get(pk=material_id)
    pouzity_material.delete()
    return redirect('work_info', praca_id=praca_id)


@login_required
def employee_details(request):
    zamestnanec = Zamestnanec.objects.all()
    user = request.user
    return render(request, 'stavMat/login_employee_details.html', {'zamestnanec': zamestnanec, 'user': user})


@login_required
def employee_info(request, zamestnanec_id):
    zamestnanec = Zamestnanec.objects.get(pk=zamestnanec_id)
    return render(request, 'stavMat/login_employee_details_info.html', {'zamestnanec': zamestnanec})


@login_required
def employee_edit(request, zamestnanec_id):
    zamestnanec = Zamestnanec.objects.get(pk=zamestnanec_id)
    if request.method == 'POST':
        zamestnanec_form = ZamestnanecForm(request.POST, instance=zamestnanec)
        if zamestnanec_form.is_valid():
            zamestnanec_form.save()
            messages.success(request, 'Zamestnanec bol úspešne upravený.')
            return redirect('employee_details')
        else:
            messages.error(request, 'Zamestnanec nebol upravený.')
    else:
        zamestnanec_form = ZamestnanecForm(instance=zamestnanec)
    return render(request, 'stavMat/login_employee_details_info_change.html',
                  {'zamestnanec': zamestnanec, 'zamestnanec_form': zamestnanec_form})


@login_required
def employee_materials(request):
    material = Material.objects.all()
    return render(request, 'stavMat/login_employee_materials.html', {'material': material})


@login_required
def create_material(request):
    if request.method == 'POST':
        material_form = MaterialForm(request.POST)
        if material_form.is_valid():
            material = material_form.save(commit=False)
            material.save()
            messages.success(request, 'Materiál bol úspešne vytvorený.')
            return redirect('employee_materials')
        else:
            messages.error(request, 'Materiál nebol vytvorený.')
    else:
        material_form = MaterialForm()
    return render(request, 'stavMat/login_employee_materials_create.html', {'material_form': material_form})


@login_required
def delete_material_spec(request, material_id):
    material = Material.objects.get(pk=material_id)
    material.delete()
    messages.success(request, 'Materiál bol úspešne vymazaný.')
    return redirect('employee_materials')

@login_required
def create_employee(request):
    if request.method == 'POST':
        zamestnanec_form = ZamestnanecCreateForm(request.POST)
        if zamestnanec_form.is_valid():
            try:
                prihlasovacie_meno = zamestnanec_form.cleaned_data.get('prihlasovacie_meno')
                prihlasovacie_heslo = zamestnanec_form.cleaned_data.get('prihlasovacie_heslo')
                user = User.objects.create_user(username=prihlasovacie_meno, password=prihlasovacie_heslo)
                zamestnanec_group = zamestnanec_form.cleaned_data.get('role')
                group = None
                if zamestnanec_group == 'Z':
                    group = Group.objects.get(name='Zamestnanec')
                elif zamestnanec_group == 'V':
                    group = Group.objects.get(name='Vedúci podniku')
                elif zamestnanec_group == 'H':
                    group = Group.objects.get(name='Hlavný zamestnanec')

                user.groups.add(group)
                user.save()
                zamestnanec_form.save()
                messages.success(request, 'Zamestnanec bol úspešne vytvorený.')
                return redirect('employee_details')
            except Exception as e:
                if 'username' in str(e):
                    messages.error(request, 'Toto prihlasovacie meno už existuje.')
                else:
                    messages.error(request, e)
        else:
            messages.error(request, 'Zamestnanec nebol vytvorený.')
    else:
        zamestnanec_form = ZamestnanecCreateForm()
    return render(request, 'stavMat/login_employee_details_create.html', {'zamestnanec_form': zamestnanec_form})


@login_required
def delete_employee(request, zamestnanec_id):
    zamestnanec = Zamestnanec.objects.get(pk=zamestnanec_id)
    zamestnanec.delete()
    user = User.objects.get(username=zamestnanec.prihlasovacie_meno)
    user.delete()
    messages.success(request, 'Zamestnanec bol úspešne vymazaný.')
    return redirect('employee_details')


@login_required
def employee_customer(request):
    zakaznik = Zakaznici.objects.all()
    return render(request, 'stavMat/login_employee_customer.html', {'zakaznik': zakaznik})


@login_required
def customer_info(request, zakaznik_id):
    zakaznik = Zakaznici.objects.get(pk=zakaznik_id)
    projekt = Projekt.objects.filter(zakaznik=zakaznik)
    return render(request, 'stavMat/login_employee_customer_info.html', {'zakaznik': zakaznik, 'projekt': projekt})


@login_required
def employee_faktura(request):
    faktura = Faktura.objects.all()
    return render(request, 'stavMat/login_employee_faktura.html', {'faktura': faktura})


@login_required
def create_faktura(request):
    if request.method == 'POST':
        faktura_form = FakturaForm(request.POST)
        if faktura_form.is_valid():
            faktura = faktura_form.save(commit=False)
            faktura.save()
            messages.success(request, 'Faktúra bola úspešne vytvorená.')
            return redirect('employee_faktura')
        else:
            messages.error(request, 'Faktúra nebola vytvorená.')
    else:
        faktura_form = FakturaForm()
    return render(request, 'stavMat/login_employee_faktura_create.html', {'faktura_form': faktura_form})


@login_required
def faktura_info(request, faktura_id):
    faktura = Faktura.objects.get(pk=faktura_id)
    return render(request, 'stavMat/login_employee_faktura_info.html', {'faktura': faktura})


@login_required
def faktura_edit(request, faktura_id):
    faktura = Faktura.objects.get(pk=faktura_id)
    if request.method == 'POST':
        faktura_form = FakturaForm(request.POST, instance=faktura)
        if faktura_form.is_valid():
            faktura_form.save()
            messages.success(request, 'Faktúra bola úspešne upravená.')
            return redirect('employee_faktura')
        else:
            messages.error(request, 'Faktúra nebola upravená.')
    else:
        faktura_form = FakturaForm(instance=faktura)
    return render(request, 'stavMat/login_employee_faktura_info_change.html',
                  {'faktura': faktura, 'faktura_form': faktura_form})
