from django.contrib.auth.models import User
from rest_framework import viewsets
from .models import Company, Branch, Country, State, City, Employee, CostCenter
from .serializers import (
    UserSerializer,
    CompanySerializer,
    BranchSerializer,
    CountrySerializer,
    StateSerializer,
    CitySerializer,
    EmployeeSerializer,
    CostCenterSerializer
)
from .webhooks import WebhookMixin


class UserViewSet(WebhookMixin, viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('id')
    serializer_class = UserSerializer


class CountryViewSet(WebhookMixin, viewsets.ModelViewSet):
    queryset = Country.objects.all().order_by('id')
    serializer_class = CountrySerializer


class StateViewSet(WebhookMixin, viewsets.ModelViewSet):
    queryset = State.objects.all().order_by('id')
    serializer_class = StateSerializer


class CityViewSet(WebhookMixin, viewsets.ModelViewSet):
    queryset = City.objects.all().order_by('id')
    serializer_class = CitySerializer


class CompanyViewSet(WebhookMixin, viewsets.ModelViewSet):
    queryset = Company.objects.all().order_by('id')
    serializer_class = CompanySerializer


class BranchViewSet(WebhookMixin, viewsets.ModelViewSet):
    queryset = Branch.objects.all().order_by('id')
    serializer_class = BranchSerializer


class CostCenterViewSet(WebhookMixin, viewsets.ModelViewSet):
    queryset = CostCenter.objects.all().order_by('id')
    serializer_class = CostCenterSerializer


class EmployeeViewSet(WebhookMixin, viewsets.ModelViewSet):
    queryset = Employee.objects.all().order_by('id')
    serializer_class = EmployeeSerializer