from django.urls import path
from .import views
from .views import update_button_state_view,SSE

urlpatterns = [
    path("", views.home, name="home"),
    path("update_button_state/", update_button_state_view, name="update_button_state"),
    path('sse/', SSE.as_view(), name='sse'),  # SSE endpoint

]   
