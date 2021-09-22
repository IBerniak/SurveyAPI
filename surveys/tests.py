'''
Providing simple tests for basic operations with surveys: creating and commiting.
'''
from .models import Survey, Question, CompletedSurvey, GivenAnswer, Customer
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


class SurveyTests(APITestCase):


    def setUp(self):
        self.user = User.objects.create_user(
            username='spam', email='user@foo.com', password='top_secret')
        self.client = APIClient()
        self.token = Token.objects.create(user=self.user)
        self.token.save()


    def test_create_survey(self):
        """
        Ensure an admin can create a new survey object.
        """
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        survey_url = '/api/surveys/'
        survey_data = {
                "title": "Test survey",
                "start_date": "2021-09-19T00:00:00",
                "finish_date": "2021-10-30T00:00:00",
                "description": "A survey for testing creating",
               }

        response = self.client.post(survey_url, survey_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Survey.objects.get().title, 'Test survey')


    def test_commit_survey(self):
        """
        Ensure a customer can commit his/her answers for the survey.
        """
        self.client.force_authenticate(user=None)
        # To ensure that an authentication is not necessary

        survey = Survey.objects.create(
                                       title="Test survey for commit",
                                       start_date="2021-09-19T00:00:00",
                                       finish_date="2021-10-30T00:00:00",
                                       description="A survey for testing creating",
                                       )
        question = Question.objects.create(
                                           text="Question",
                                           answer_type="ta",
                                           survey=survey
                                           )
        customer = Customer.objects.create()
        # To create a survey and customer to work with

        commit_url = f'/api/customers/{customer.pk}/surveys/'
        commit_data = {
                "customer": customer.pk,
                "survey": survey.pk,
                "given_answers": [{"question": question.pk, "answer": "Answer"}]
               }
        response = self.client.post(commit_url, commit_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CompletedSurvey.objects.get().customer.id, 1)
        self.assertEqual(GivenAnswer.objects.get().answer, "Answer")
