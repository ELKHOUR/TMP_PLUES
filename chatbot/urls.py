from django.urls import path
from . import views

app_name = "chatbot"

urlpatterns = [
    path("product/", views.chatbot_product, name="chatbot_product"),
    path("company/", views.chatbot_company, name="chatbot_company"),
    path("services/", views.chatbot_services, name="chatbot_services"),
    path("general/", views.chatbot_general, name="chatbot_general"),
    path("search_CommonQuestions/", views.search_CommonQuestions, name="search_CommonQuestions"),
    path('saveUpdateOne/', views.save_or_update_question_fuzzy, name="save_update"),
]
