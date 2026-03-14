from django.db import models
from django.contrib.auth.models import User


class Country(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)

    class Meta:
        verbose_name = "Country"
        verbose_name_plural = "Countries"
        ordering = ["name"]
        db_table = "Country"

    def __str__(self):
        return self.name


class State(models.Model):
    country = models.ForeignKey(Country, on_delete=models.PROTECT, related_name="states")
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10)

    class Meta:
        verbose_name = "State"
        verbose_name_plural = "States"
        ordering = ["name"]
        unique_together = ("country", "code")
        db_table = "State"

    def __str__(self):
        return f"{self.name} - {self.country.code}"


class City(models.Model):
    state = models.ForeignKey(State, on_delete=models.PROTECT, related_name="cities")
    name = models.CharField(max_length=100)
    ibge_code = models.CharField(max_length=30, blank=True, null=True, db_column="codigo_ibge")

    class Meta:
        verbose_name = "City"
        verbose_name_plural = "Cities"
        ordering = ["name"]
        unique_together = ("state", "name")
        db_table = "City"

    def __str__(self):
        return f"{self.name} - {self.state.code}"


class Company(models.Model):
    legal_name = models.CharField(max_length=150, null=False, blank=False)
    trade_name = models.CharField(max_length=150, blank=True, null=True)
    cnpj = models.CharField(max_length=20, unique=True)
    city = models.ForeignKey(City, on_delete=models.PROTECT, related_name="companies")

    class Meta:
        verbose_name = "Company"
        verbose_name_plural = "Companies"
        ordering = ["legal_name"]
        db_table = "Company"

    def __str__(self):
        return self.legal_name


class Branch(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="branches")
    name = models.CharField(max_length=150)
    code = models.CharField(max_length=50)
    city = models.ForeignKey(City, on_delete=models.PROTECT, related_name="branches")

    class Meta:
        verbose_name = "Branch"
        verbose_name_plural = "Branches"
        ordering = ["name"]
        unique_together = ("company", "code")
        db_table = "Branch"

    def __str__(self):
        return f"{self.company.legal_name} - {self.name}"


class CostCenter(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name="cost_centers")
    code = models.CharField(max_length=20)
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Cost Center"
        verbose_name_plural = "Cost Centers"
        ordering = ["name"]
        unique_together = ("branch", "code")

    def __str__(self):
        return f"{self.code} - {self.name}"


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="employee")
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="employees")
    branch = models.ForeignKey(Branch, on_delete=models.PROTECT, related_name="employees")
    cost_center = models.ForeignKey(CostCenter, on_delete=models.PROTECT, related_name="employees")
    full_name = models.CharField(max_length=150)
    email = models.EmailField(blank=True, null=True)
    document = models.CharField(max_length=20, unique=True, help_text="CPF ou documento")
    hire_date = models.DateField(blank=True, null=True)
    active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Employee"
        verbose_name_plural = "Employees"
        ordering = ["full_name"]

    def __str__(self):
        return self.full_name