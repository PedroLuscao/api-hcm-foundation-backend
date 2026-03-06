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


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('id')
    serializer_class = UserSerializer


class CountryViewSet(viewsets.ModelViewSet):
    queryset = Country.objects.all().order_by('id')
    serializer_class = CountrySerializer


class StateViewSet(viewsets.ModelViewSet):
    queryset = State.objects.all().order_by('id')
    serializer_class = StateSerializer


class CityViewSet(viewsets.ModelViewSet):
    queryset = City.objects.all().order_by('id')
    serializer_class = CitySerializer


class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all().order_by('id')
    serializer_class = CompanySerializer


class BranchViewSet(viewsets.ModelViewSet):
    queryset = Branch.objects.all().order_by('id')
    serializer_class = BranchSerializer


class CostCenterViewSet(viewsets.ModelViewSet):
    queryset = CostCenter.objects.all().order_by('id')
    serializer_class = CostCenterSerializer


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all().order_by('id')
    serializer_class = EmployeeSerializer