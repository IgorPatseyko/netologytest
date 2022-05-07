import pytest
from django.core import serializers
from django.urls import reverse
from model_bakery import baker

from rest_framework.test import APIClient

from students.models import Course, Student
from students.serializers import CourseSerializer


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def course_factory():
    def factory(*args, **kwargs):
        return baker.make(Course, *args, **kwargs)
    return factory


@pytest.fixture
def student_factory():
    def factory(*args, **kwargs):
        return baker.make(Student, *args, **kwargs)
    return factory


def test_example():
    assert True, "Just test example"


@pytest.mark.django_db
def test_retrieve_answer(client, course_factory):
    first_course = course_factory()
    response = client.get(path=reverse('courses-detail', args=[first_course.id]),)
    assert CourseSerializer(first_course).data == response.json()
    assert response.status_code == 200


@pytest.mark.django_db
def test_retrieve_list(client, course_factory):
    course_list = course_factory(_quantity=10)
    response = client.get(path=reverse('courses-list',))

    for i, obj in enumerate(response.json()):
        assert obj == CourseSerializer(course_list[i]).data
    assert response.status_code == 200


@pytest.mark.django_db
def test_filters(client, course_factory):
    course_list = course_factory(_quantity=10)

    for course in course_list:
        id = course.id
        name = course.name
        response = client.get(path=reverse('courses-list'), data={'id': id, 'name': name})
        assert len(response.json()) == 1
        # вдруг передасться 1 элемент правильный, а дальше еще что-то, возможно красивее еще один цикл добавить
        assert CourseSerializer(course).data == response.json()[0]
        assert response.status_code == 200


@pytest.mark.django_db
def test_create_course(client):
    count = Course.objects.count()

    response = client.post(reverse('courses-list'), data={'name': 'course name'})

    assert response.status_code == 201
    assert Course.objects.count() == count + 1


@pytest.mark.django_db
def test_update_course(client, course_factory):
    course = course_factory()
    data = {'name': 'course name'}

    response = client.patch(reverse('courses-detail', args=[course.id]), data=data)

    assert response.status_code == 200
    assert response.json()['name'] == data['name']


@pytest.mark.django_db
def test_delete_course(client, course_factory):
    course = course_factory()

    response = client.delete(reverse('courses-detail', args=[course.id]))

    assert response.status_code == 204
    assert Course.objects.count() == 0
