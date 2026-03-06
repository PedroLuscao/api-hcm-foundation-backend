from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet,
    CompanyViewSet,
    BranchViewSet,
    CountryViewSet,
    StateViewSet,
    CityViewSet,
    EmployeeViewSet,
    CostCenterViewSet
)

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'companies', CompanyViewSet, basename='company')
router.register(r'branches', BranchViewSet, basename='branch')
router.register(r'countries', CountryViewSet, basename='country')
router.register(r'states', StateViewSet, basename='state')
router.register(r'cities', CityViewSet, basename='city')
router.register(r'employees', EmployeeViewSet, basename='employee')
router.register(r'cost-centers', CostCenterViewSet, basename='costcenter')

urlpatterns = router.urls