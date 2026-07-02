from rest_framework.routers import DefaultRouter
from .views import CourseViewSet, StudentViewSet, EnrollmentViewSet, DepartmentViewSet
router = DefaultRouter()
router.register('departments', DepartmentViewSet)
router.register('courses', CourseViewSet)
router.register('students', StudentViewSet)
router.register('enrollments', EnrollmentViewSet)

urlpatterns = router.urls