from django.urls import path
from .views import (
    NewStoryForm
    )

urlpatterns = [
    path('new/', NewStoryForm.as_view(), name='new'),
]
