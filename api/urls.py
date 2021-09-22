'''
API designed with such architecture: url gives a noun as a resource ('plural/'
for collections and 'plural/id' for one instance), http-method gives a verb
matched to an action on that resource. Nested resources belongs to their 'parent'
resources.
Some methods on several endpoints requires authentication by a token which can be
recieved from 'authentication/' url with username and password.
On collections' endpoints GET for list and POST for creating are provided.
On concrete instance endpoints GET for detail PUT for editing and DELETE for deleting.
'''
from django.urls import path
from rest_framework.authtoken import views
from .views import *


urlpatterns = [
    path('authentication/', views.ObtainAuthToken.as_view()),
    path('surveys/', SurveyView.as_view()),
    path('surveys/<int:pk>/', SurveyDetailView.as_view()),
    path('surveys/<int:pk>/questions/', QuestionsView.as_view()),
    path('surveys/<int:s_pk>/questions/<int:pk>/', QuestionDetailView.as_view()),
    path('surveys/<int:s_pk>/questions/<int:pk>/answers/', AnswersView.as_view()),
    path('surveys/<int:s_pk>/questions/<int:q_pk>/answers/<int:pk>/',
         AnswerDetailView.as_view()),
    path('customers/', CustomerView.as_view()),
    path('customers/<int:pk>/', CustomerDetailView.as_view()),
    path('customers/<int:pk>/surveys/', CustomersComplSurveyView.as_view()),
    path('customers/<int:c_pk>/surveys/<int:pk>/', CustComplSurvDetailView.as_view()),
]
