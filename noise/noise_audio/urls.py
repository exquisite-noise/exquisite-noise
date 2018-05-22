from django.urls import path
from .views import (
    NewStoryForm,
    ContinueStoryForm
    )

urlpatterns = [
    path('new/', NewStoryForm.as_view(), name='new'),
    path('add/<int:clip_id>/', ContinueStoryForm.as_view(), name='add'),
]
