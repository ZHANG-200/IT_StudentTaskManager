from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from rango.models import Student, Course, Assignment

class RangoModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='teststudent', password='password123', email='test@example.com')
        self.student = Student.objects.create(user=self.user, phone_number='07123456789')

    def test_student_model_creation(self):
        self.assertEqual(self.student.user.username, 'teststudent')
        self.assertEqual(self.student.phone_number, '07123456789')
        self.assertEqual(str(self.student), 'teststudent')

    def test_course_model_creation(self):
        course = Course.objects.create(name='Computing 101', student=self.student)
        self.assertEqual(course.name, 'Computing 101')
        self.assertEqual(course.student, self.student)

    def test_assignment_model_creation(self):
        course = Course.objects.create(name='Maths', student=self.student)
        assignment = Assignment.objects.create(
            student=self.student,
            course=course,
            name='Algebra Quiz',
            state=False,
            deadline='2024-05-20'
        )
        self.assertEqual(assignment.name, 'Algebra Quiz')
        self.assertFalse(assignment.state)
        self.assertEqual(assignment.deadline, '2024-05-20')

class RangoViewAndAuthTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.register_url = reverse('rango:register')
        self.login_url = reverse('rango:login')
        self.dashboard_url = reverse('rango:view_courses')

        self.user = User.objects.create_user(username='existinguser', password='safe_password')
        self.student = Student.objects.create(user=self.user, phone_number='111222333')

        self.course = Course.objects.create(name='History', student=self.student)
        self.assignment1 = Assignment.objects.create(student=self.student, course=self.course, name='A1', deadline='2024-12-01')
        self.assignment2 = Assignment.objects.create(student=self.student, course=self.course, name='A2', deadline='2024-01-01')

    def test_registration_process(self):
        post_data = {
            'username': 'newuser',
            'password': 'newpassword123',
            'email': 'new@test.com',
            'phone': '099887766'
        }
        self.client.post(self.register_url, post_data)
        self.assertTrue(User.objects.filter(username='newuser').exists())
        self.assertTrue(Student.objects.filter(phone_number='099887766').exists())

    def test_user_login_success(self):
        post_data = {'username': 'existinguser', 'password': 'safe_password'}
        response = self.client.post(self.login_url, post_data)
        self.assertRedirects(response, self.dashboard_url)

    def test_view_courses_sorting(self):
        sorted_assignments = Assignment.objects.filter(
            student=self.student
        ).order_by('deadline')

        self.assertEqual(list(sorted_assignments), [self.assignment2, self.assignment1])

class RangoURLReverseTests(TestCase):

    def test_reverse_urls(self):
        self.assertEqual(reverse('rango:add_course'), '/rango/course/add/')
        self.assertEqual(reverse('rango:view_courses'), '/rango/dashboard/')
        self.assertEqual(reverse('rango:register'), '/rango/register/')
        self.assertEqual(reverse('rango:login'), '/rango/login/')
        self.assertEqual(reverse('rango:add_assignment'), '/rango/assignment/add/')
        self.assertEqual(reverse('rango:view_courses_page'), '/rango/courses/')

    def test_reverse_with_args(self):
        self.assertEqual(reverse('rango:delete_assignment', kwargs={'assignment_id': 5}), '/rango/assignment/delete/5/')
        self.assertEqual(reverse('rango:delete_course', kwargs={'course_id': 3}), '/rango/course/delete/3/')
        self.assertEqual(reverse('rango:edit_assignment', kwargs={'assignment_id': 10}), '/rango/assignment/edit/10/')
        self.assertEqual(reverse('rango:mark_assignment_done', kwargs={'assignment_id': 7}), '/rango/assignment/7/done/')
        self.assertEqual(reverse('rango:assignment_detail', kwargs={'assignment_id': 2}), '/rango/assignment/2/')