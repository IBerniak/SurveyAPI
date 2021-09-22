from rest_framework import serializers
from surveys.models import *
from django.shortcuts import get_object_or_404


class SurveySerializer(serializers.ModelSerializer):
    '''
    Basic serializer for surveys.
    '''
    class Meta:
        model = Survey
        read_only_fields = ['id',]
        fields = ('id', 'title', 'start_date', 'finish_date', 'description')


class SurveyDetailSerializer(SurveySerializer):
    '''
    Serializer for survey's detail view, include nested field for questions and
    answers.
    '''
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        count = 1
        representation['questions'] = {}
        for question in self.context['questions']:
            question_serializer = QuestionNestedSerializer(question,
                                                           context={'question': question})
            representation['questions'][count] = question_serializer.data
            count +=1
        return representation


class SurveyTitleSerializer(serializers.ModelSerializer):
    '''
    Serializer for titles when used like nested.
    '''
    class Meta:
        model = Survey
        fields = ('id', 'title')


class QuestionSerializer(serializers.ModelSerializer):
    '''
    Basic question serializer.
    '''
    class Meta:
        model = Question
        read_only_fields = ['id', 'survey']
        fields = '__all__'


class QuestionNewSerializer(serializers.ModelSerializer):
    '''
    Question serializer for creating new one.
    '''
    class Meta:
        model = Question
        fields = '__all__'

    def validate(self, data):
        survey = get_object_or_404(Survey.objects.all(), pk=self.context['pk'])

        if data['survey'] != survey:
            pk = self.context['pk']
            raise serializers.ValidationError(
                              f'The question should belong to the {pk} survey')
        return data


class QuestionNestedSerializer(serializers.ModelSerializer):
    '''
    Question serializer which uses for nested serializing in detail survey
    serializer.
    '''
    class Meta:
        model = Question
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if self.context['question'].answer_type != 'ta':
            answers_queryset = Answer.objects.filter(question=self.context['question'])
            answers = AnswerSerializer(answers_queryset, many=True)
            representation['answers'] = answers.data
        return representation


class AnswerSerializer(serializers.ModelSerializer):
    '''
    Basic answer serializer.
    '''
    class Meta:
        model = Answer
        read_only_fields = ['id', 'question']
        fields = ('id', 'text', 'question')


class AnswerNewSerializer(serializers.ModelSerializer):
    '''
    Answer serializer for creating a new instance.
    '''
    class Meta:
        model = Answer
        fields = ('text', 'question')

    def validate(self, data):
        question = get_object_or_404(Question.objects.all(), pk=self.context['pk'])

        if data['question'] != question:
            pk = self.context['pk']
            raise serializers.ValidationError(
                              f'The answer should belong to the {pk} question')
        return data


class CustomerSerializer(serializers.ModelSerializer):
    '''
    Serializer to read and to write.
    '''
    class Meta:
        model = Customer
        read_only_fields = ['id',]
        fields = '__all__'


class CompletedSurveySerializer(serializers.ModelSerializer):
    '''
    Serializer to read for CompletedSurvey model.
    '''
    class Meta:
        model = CompletedSurvey
        fields = ['id', 'survey']
        depth = 1


class GivenAnswerSerializer(serializers.ModelSerializer):
    '''
    Serializer to read for GivenAnswer model.
    '''
    question = serializers.SlugRelatedField(read_only=True, slug_field='text')
    class Meta:
        model = GivenAnswer
        fields = ['question', 'answer']


class SurveyCommitSerializer(serializers.ModelSerializer):
    '''
    Serializer to create a new instance for CompletedSurvey model and new
    instances for GivenAnswer model in one action.
    '''
    given_answers = GivenAnswerSerializer(many=True, write_only=True)

    class Meta:
        model = CompletedSurvey
        fields = ['customer', 'survey', 'given_answers']

    def create(self, validated_data):

        answers_validated_data = validated_data.pop('given_answers')
        survey = validated_data['survey']
        completed_survey = CompletedSurvey.objects.create(**validated_data)

        given_answers_serializer = self.fields['given_answers']

        for each in answers_validated_data:
            each['completed_survey'] = completed_survey

        answers = given_answers_serializer.create(answers_validated_data)

        return completed_survey


class ComplSurvDetailSerializer(serializers.ModelSerializer):
    '''
    Detail serializer for a completed survey, including given answers belonged
    to that completed survey.
    '''
    survey = serializers.SlugRelatedField(read_only=True, slug_field='title')
    class Meta:
        model = CompletedSurvey
        fields = ['id', 'survey']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        count = 1
        representation['given_answers'] = {}
        for answer in self.context['answers']:
            given_answer_serializer = GivenAnswerSerializer(answer)
            representation['given_answers'][count] = given_answer_serializer.data
            count +=1
        return representation
