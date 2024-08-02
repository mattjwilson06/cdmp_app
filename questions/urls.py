# questions/urls.py
from django.urls import path
from .views import QuestionPoolListView, QuestionPoolCreateView, QuestionCreateView, QuestionPoolDetailView

urlpatterns = [
    path('', QuestionPoolListView.as_view(), name='pool_list'),
    path('pools/create/', QuestionPoolCreateView.as_view(), name='pool_create'),
    path('pools/<int:pk>/', QuestionPoolDetailView.as_view(), name='pool_detail'),
    path('questions/create/', QuestionCreateView.as_view(), name='question_create'),
    path('questions/create/<int:pool_id>/', QuestionCreateView.as_view(), name='question_create_for_pool'),
]
