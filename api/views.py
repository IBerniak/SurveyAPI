from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import generics, mixins
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework import status
from django.utils import timezone
from surveys.models import Survey, Question, Answer
from .serializers import *


class SurveyView(generics.ListCreateAPIView):

    queryset = Survey.objects.all()
    serializer_class = SurveySerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def list(self, request):
        '''
        Returns a list of surveys. For authenticated request all surveys,
        for unauthenticated relevant to current date surveys.
        Method GET.
        '''
        if request.auth:
            queryset = self.get_queryset().order_by('-start_date')
        else:
            queryset = self.get_queryset().filter(
                start_date__lte=timezone.now()
                ).filter(
                    finish_date__gt=timezone.now()
                    ).order_by('-start_date')

        serializer = SurveySerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        '''
        Creates a new survey. Token is necessary.
        Method POST.
        '''
        serializer = SurveySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SurveyDetailView(mixins.UpdateModelMixin,
                       mixins.DestroyModelMixin,
                       generics.GenericAPIView):
    queryset = Survey.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get(self, request, pk):
        '''
        Returns a detail view of a survey. Method GET.
        '''
        survey = get_object_or_404(self.get_queryset(), pk=pk)
        questions_queryset = Question.objects.filter(survey=survey)
        serializer = SurveyDetailSerializer(survey,
                                            context={'questions': questions_queryset})
        return Response(serializer.data)

    def put(self, request, pk):
        '''
        Edits the current survey. Method PUT. Token.
        '''
        return self.update(request, pk)

    def delete(self, request, pk):
        '''
        Deletes the current survey. Method DELETE. Token.
        '''
        return self.destroy(request, pk)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return SurveyDetailSerializer
        else:
            return SurveySerializer


class QuestionsView(generics.ListCreateAPIView):

    queryset = Question.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def list(self, request, pk):
        '''
        Returns a list of questions belonged to the survey (pk). Method GET.
        '''
        survey = get_object_or_404(Survey.objects.all(), pk=pk)
        queryset = self.get_queryset().filter(survey=survey)

        serializer = QuestionSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, pk):
        '''
        Creates a new question belonged to the survey. Metod POST. Token.
        '''
        serializer = QuestionNewSerializer(data=request.data, context={'pk': pk})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return QuestionSerializer
        else:
            return QuestionNewSerializer


class QuestionDetailView(mixins.UpdateModelMixin,
                         mixins.DestroyModelMixin,
                         generics.GenericAPIView):

    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)


    def get(self, request, s_pk, pk):
        '''
        Returns a detail view of a question. Method GET.
        '''
        question = get_object_or_404(self.queryset, pk=pk)
        serializer = QuestionNestedSerializer(question, context={'question': question})
        return Response(serializer.data)

    def put(self, request, s_pk, pk):
        '''
        Edits the current question. Method PUT. Token.
        '''
        return self.update(request, s_pk, pk)

    def delete(self, request, s_pk, pk):
        '''
        Deletes the current question. Method DELETE. Token.
        '''
        return self.destroy(request, s_pk, pk)


class AnswersView(generics.ListCreateAPIView):

    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def list(self, request, s_pk, pk):
        '''
        Returns a list of answers belonged to the question (pk). Method GET.
        '''
        question = get_object_or_404(Question.objects.all(), pk=pk)
        queryset = self.get_queryset().filter(question=question)

        serializer = AnswerSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, s_pk,  pk):
        '''
        Creates a new answer belonged to the question. Metod POST. Token.
        '''
        serializer = AnswerNewSerializer(data=request.data, context={'pk': pk})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AnswerDetailView(mixins.RetrieveModelMixin,
                       mixins.UpdateModelMixin,
                       mixins.DestroyModelMixin,
                       generics.GenericAPIView):

    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)


    def get(self, request, s_pk, q_pk, pk):
        '''
        Returns a detail view of an answer. Method GET.
        '''
        return self.retrieve(request, s_pk, q_pk, pk)

    def put(self, request, s_pk, q_pk, pk):
        '''
        Edits the current answer. Method PUT. Token.
        '''
        return self.update(request, s_pk, q_pk, pk)

    def delete(self, request, s_pk, q_pk, pk):
        '''
        Deletes the current answer. Method DELETE. Token.
        '''
        return self.destroy(request, s_pk, q_pk, pk)


class CustomerView(generics.ListCreateAPIView):

    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = (IsAuthenticated,)

    def list(self, request):
        '''
        Returns a list of customers. Method GET. Token.
        '''
        queryset = self.get_queryset()
        serializer = CustomerSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        '''
        Creates a new customer. Metod POST. Token.
        '''
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomerDetailView(mixins.RetrieveModelMixin,
                         mixins.UpdateModelMixin,
                         mixins.DestroyModelMixin,
                         generics.GenericAPIView):

    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get(self, request, pk):
        '''
        Returns a detail view for a customer. Method GET.
        '''
        return self.retrieve(request, pk)

    def put(self, request, pk):
        '''
        Edits the customer. Method PUT. Token.
        '''
        return self.update(request, pk)

    def delete(self, request, pk):
        '''
        Deletes the customer. Method DELETE. Token.
        '''
        return self.destroy(request, pk)


class CustomersComplSurveyView(generics.GenericAPIView):
    queryset = CompletedSurvey.objects.all()

    def get(self, request, pk):
        '''
        Returns a list of customer's completed surveys. Method GET.
        '''
        customer = get_object_or_404(Customer.objects.all(), pk=pk)
        queryset = self.get_queryset().filter(customer=customer)
        serializer = CompletedSurveySerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, pk):
        '''
        Commits a completed survey, creates an instance of a completed surveys
        and instances of all given answers. Method POST.
        '''
        serializer = SurveyCommitSerializer(data=request.data)
        if serializer.is_valid():
            commited_survey = serializer.save()
            serializer = SurveyCommitSerializer(commited_survey)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return CompletedSurveySerializer
        else:
            return SurveyCommitSerializer


class CustComplSurvDetailView(generics.GenericAPIView):
    queryset = CompletedSurvey.objects.all()
    serializer_class = ComplSurvDetailSerializer

    def get(self, request, c_pk, pk):
        '''
        Returns a detail view for a completed survey with a list of given answers
        belonged to that survey. Method GET.
        '''
        completed_survey = get_object_or_404(self.get_queryset(), pk=pk)
        answers_queryset = GivenAnswer.objects.filter(completed_survey=completed_survey)
        serializer = ComplSurvDetailSerializer(completed_survey,
                                               context={'answers': answers_queryset})
        return Response(serializer.data)
