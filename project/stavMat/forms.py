from django import forms

from .models import Zakaznici, Zamestnanec, Projekt, Praca, PouzityMaterial, Material, Faktura


class ZakazniciRegisterForm(forms.ModelForm):
    class Meta:
        model = Zakaznici
        fields = ['meno', 'priezvisko', 'email', 'telefon', 'typ_osoby', 'nazov_firmy', 'ico', 'dic',
                  'prihlasovacie_meno', 'prihlasovacie_heslo']

    def clean(self):
        cleaned_data = super().clean()
        typ_osoby = cleaned_data.get('typ_osoby')
        nazov_firmy = cleaned_data.get('nazov_firmy')
        ico = cleaned_data.get('ico')
        dic = cleaned_data.get('dic')

        if typ_osoby == Zakaznici.PRAVNICKA_OSOBA:
            if not nazov_firmy:
                raise forms.ValidationError("Prosím vyplňte názov firmy.")
            if not ico:
                raise forms.ValidationError("Prosím vyplňte IČO.")
            if not dic:
                raise forms.ValidationError("Prosím vyplňte DIČ.")

        return cleaned_data


class ZakazniciLoginForm(forms.ModelForm):
    prihlasovacie_heslo = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Zakaznici
        fields = ['prihlasovacie_meno', 'prihlasovacie_heslo']


class ZamestnanciLoginForm(forms.ModelForm):
    prihlasovacie_heslo = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Zamestnanec
        fields = ['prihlasovacie_meno', 'prihlasovacie_heslo']


class ProjektForm(forms.ModelForm):
    class Meta:
        model = Projekt
        fields = '__all__'
        exclude = ['zakaznik']


class ZakaznikForm(forms.ModelForm):
    class Meta:
        model = Zakaznici
        fields = '__all__'
        exclude = ['prihlasovacie_meno', 'prihlasovacie_heslo']


class ZamestnanecForm(forms.ModelForm):
    class Meta:
        model = Zamestnanec
        fields = '__all__'
        exclude = ['prihlasovacie_meno', 'prihlasovacie_heslo', 'role', 'datum_nastupu']


class ZamestnanecCreateForm(forms.ModelForm):
    prihlasovacie_heslo = forms.CharField(widget=forms.PasswordInput)
    datum_nastupu = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Zamestnanec
        fields = '__all__'


class PracaForm(forms.ModelForm):
    datum_zaciatku = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    datum_ukoncenia = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False)

    class Meta:
        model = Praca
        fields = '__all__'


class PouzityMaterialForm(forms.ModelForm):
    class Meta:
        model = PouzityMaterial
        fields = '__all__'
        exclude = ['praca']


class MaterialForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = '__all__'

class FakturaForm(forms.ModelForm):
    datum_splatnosti = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Faktura
        fields = '__all__'
