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
from django.urls import path, re_path
from rest_framework.authtoken import views
from .views import *
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Survey API",
      default_version='v1',
      description='''API service for surveys, their creating, updating, deleteing,
      reading and commiting''',
      contact=openapi.Contact(email="iliia.berniak@gmail.com"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

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
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0),
            name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0),
            name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
