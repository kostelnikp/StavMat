from django.contrib.auth.hashers import make_password
from django.db import models


# Create your models here.

class Faktura(models.Model):
    datum_vystavenia = models.DateField(verbose_name='Dátum vystavenia', auto_now_add=True)
    datum_splatnosti = models.DateField('datum splatnosti')
    suma = models.DecimalField(max_digits=10, decimal_places=2)

    UHRADENÁ = 'U'
    NEUHRADENÁ = 'N'
    STAVY_PLATIEB = [
        (UHRADENÁ, 'Uhradená'),
        (NEUHRADENÁ, 'Neuhradená'),
    ]
    stav_platby = models.CharField(max_length=20, choices=STAVY_PLATIEB)
    projekt = models.ForeignKey('Projekt', null=True, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.id} - {self.projekt.nazov} - Stav: {self.stav_platby}'


class Projekt(models.Model):
    nazov = models.CharField(max_length=100, verbose_name='Názov')
    popis = models.TextField()
    adresa = models.CharField(max_length=30)
    psc = models.CharField(max_length=10, verbose_name='PSČ')
    mesto = models.CharField(max_length=20)
    stat = models.CharField(max_length=30, verbose_name='Štát')
    datum_zaciatku = models.DateField('Dátum začiatku')
    datum_ukoncenia = models.DateField(verbose_name='Dátum ukončenia', null=True, blank=True)

    UKONČENÝ = 'U'
    NEUKONČENÝ = 'N'
    STAVY_PROJEKTU = [
        (UKONČENÝ, 'Ukončený'),
        (NEUKONČENÝ, 'Neukončený'),
    ]
    stav = models.CharField(max_length=50, choices=STAVY_PROJEKTU)
    celkovy_rozpocet = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Celkový rozpočet')
    zakaznik = models.ForeignKey('Zakaznici', null=True, on_delete=models.CASCADE, verbose_name='Zákazník')

    def __str__(self):
        return f'{self.nazov}; Zakazník: {self.zakaznik.meno} {self.zakaznik.priezvisko}; Stav: {self.stav}'


class Zakaznici(models.Model):
    meno = models.CharField(max_length=50)
    priezvisko = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    telefon = models.CharField(max_length=20, verbose_name='Telefón')

    FYZICKA_OSOBA = 'F'
    PRAVNICKA_OSOBA = 'P'
    TYPY_OSOB = [
        (FYZICKA_OSOBA, 'Fyzická osoba'),
        (PRAVNICKA_OSOBA, 'Právnická osoba'),
    ]
    typ_osoby = models.CharField(max_length=1, choices=TYPY_OSOB)
    nazov_firmy = models.CharField(max_length=50, null=True, blank=True, verbose_name='Názov firmy', unique=True,
                                   error_messages={'unique': 'Tento názov firmy už existuje.'})
    ico = models.CharField(max_length=20, null=True, blank=True, verbose_name='IČO', unique=True,
                           error_messages={'unique': 'Toto IČO už existuje.'})
    dic = models.CharField(max_length=20, null=True, blank=True, verbose_name='DIČ', unique=True,
                           error_messages={'unique': 'Toto DIČ už existuje.'})

    prihlasovacie_meno = models.CharField(max_length=50)
    prihlasovacie_heslo = models.CharField(max_length=16)

    def __str__(self):
        return f'{self.meno} {self.priezvisko}, Typ osoby: {self.typ_osoby}'

    def save(self, *args, **kwargs):
        if not self.pk:
            self.prihlasovacie_heslo = make_password(self.prihlasovacie_heslo)
        return super().save(*args, **kwargs)


class Praca(models.Model):
    typ = models.CharField(max_length=50)
    datum_zaciatku = models.DateField(verbose_name='Dátum začiatku')
    datum_ukoncenia = models.DateField(null=True, blank=True, verbose_name='Dátum ukončenia')
    popis_prace = models.TextField(verbose_name='Popis práce')
    naklady = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Náklady')
    projekt = models.ForeignKey('Projekt', null=True, on_delete=models.CASCADE)
    zamestnanec = models.ForeignKey('Zamestnanec', null=True, on_delete=models.CASCADE)

    def __str__(self):
        return f'Projekt: {self.projekt.nazov}; Zamestnanec: {self.zamestnanec.meno} {self.zamestnanec.priezvisko}; Praca: {self.typ}'


class Zamestnanec(models.Model):
    meno = models.CharField(max_length=50)
    priezvisko = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    telefon = models.CharField(max_length=20, verbose_name='Telefón', unique=True, error_messages={'unique': 'Tento telefón už existuje.'})
    adresa_bydliska = models.CharField(max_length=30)
    psc = models.CharField(max_length=10, verbose_name='PSČ')
    mesto_bydliska = models.CharField(max_length=20)
    stat_bydliska = models.CharField(max_length=30, verbose_name='Štát bydliska')
    datum_nastupu = models.DateField(verbose_name='Dátum nástupu')
    kvalifikacie = models.TextField(null=True, blank=True, verbose_name='Kvalifikácie')
    VEDUCI = 'V'
    HLAVNY_ZAMESTNANEC = 'H'
    ZAMESTNANEC = 'Z'
    TYPY_OSOB = [
        (VEDUCI, 'Vedúci podniku'),
        (HLAVNY_ZAMESTNANEC, 'Hlavný zamestnanec'),
        (ZAMESTNANEC, 'Zamestnanec'),
    ]
    role = models.CharField(max_length=1, choices=TYPY_OSOB)
    prihlasovacie_meno = models.CharField(max_length=50)
    prihlasovacie_heslo = models.CharField(max_length=16)

    def __str__(self):
        return f'Rola: {self.role}; {self.meno} {self.priezvisko}'

    def save(self, *args, **kwargs):
        if not self.pk:
            self.prihlasovacie_heslo = make_password(self.prihlasovacie_heslo)
        return super().save(*args, **kwargs)


class PouzityMaterial(models.Model):
    mnozstvo = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Množstvo')
    jednotkova_cena = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Jednotková cena')
    praca = models.ForeignKey('Praca', null=True, on_delete=models.CASCADE, verbose_name='Práca')
    material = models.ForeignKey('Material', null=True, on_delete=models.CASCADE, verbose_name='Materiál')

    def __str__(self):
        return f'Praca: {self.praca.typ}; Material: {self.material.nazov}, Množstvo: {self.mnozstvo}'


class Material(models.Model):
    nazov = models.CharField(max_length=255, verbose_name='Názov')
    kod = models.CharField(max_length=50, verbose_name='Kód', unique=True, error_messages={'unique': 'Tento kód už existuje.'})

    def __str__(self):
        return f'{self.kod} - {self.nazov}'
