from django.urls import path, include
from users.views import TestLoginView, ActivateUser

urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('activate/<str:uid>/<str:token>/', ActivateUser.as_view({'get': 'activation'}), name='activate'),
    path('test-login/', TestLoginView.as_view(), name='test-login')
]
