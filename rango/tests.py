from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from rango.models import Student, Course, Assignment

class RangoModelTests(TestCase):
    """
    Tests for database models based on the ER diagram and table specifications.
    """
    def setUp(self):
        # Create a base user and student profile for testing
        self.user = User.objects.create_user(username='teststudent', password='password123', email='test@example.com')
        self.student = Student.objects.create(user=self.user, phone_number='07123456789')

    def test_student_model_creation(self):
        """Tests if the Student profile correctly links to the User model."""
        self.assertEqual(self.student.user.username, 'teststudent')
        self.assertEqual(self.student.phone_number, '07123456789')
        self.assertEqual(str(self.student), 'teststudent')

    def test_course_model_creation(self):
        """Tests Course creation linked to a Student."""
        course = Course.objects.create(name='Computing 101', student=self.student)
        self.assertEqual(course.name, 'Computing 101')
        self.assertEqual(course.student, self.student)

    def test_assignment_model_creation(self):
        """Tests Assignment fields including the state and deadline (Char15)[cite: 69]."""
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
    """
    Tests for authentication (M1) and business logic views.
    """
    def setUp(self):
        self.client = Client()
        self.register_url = reverse('rango:register')
        self.login_url = reverse('rango:login')
        self.dashboard_url = reverse('rango:view_courses')
        
        # Pre-create a user for login testing
        self.user = User.objects.create_user(username='existinguser', password='safe_password')
        self.student = Student.objects.create(user=self.user, phone_number='111222333')

    def test_registration_process(self):
        """Tests M1: Student registration saves info to database."""
        post_data = {
            'username': 'newuser',
            'password': 'newpassword123',
            'email': 'new@test.com',
            'phone': '099887766'
        }
        response = self.client.post(self.register_url, post_data)
        
        # Verify user and student creation
        self.assertTrue(User.objects.filter(username='newuser').exists())
        self.assertTrue(Student.objects.filter(phone_number='099887766').exists())
        # Check redirect to dashboard
        self.assertRedirects(response, self.dashboard_url)

    def test_user_login_success(self):
        """Tests M1: Successful login with valid credentials[cite: 17]."""
        post_data = {'username': 'existinguser', 'password': 'safe_password'}
        response = self.client.post(self.login_url, post_data)
        self.assertRedirects(response, self.dashboard_url)

    def test_view_courses_sorting(self):
        """Tests M4: Assignments are ordered by due date[cite: 19]."""
        course = Course.objects.create(name='History', student=self.student)
        # Create assignments with different deadlines
        Assignment.objects.create(student=self.student, course=course, name='A1', deadline='2024-12-01')
        Assignment.objects.create(student=self.student, course=course, name='A2', deadline='2024-01-01')
        
        response = self.client.get(self.dashboard_url)
        # Verify the assignment list in context is sorted by deadline
        assignments = response.context['assignments']
        self.assertEqual(assignments[0].name, 'A2') # Earlier date first

class RangoURLReverseTests(TestCase):
    """
    Tests to ensure named URLs and reverse resolution are configured correctly .
    """
    def test_reverse_urls(self):
        self.assertEqual(reverse('rango:add_course'), '/rango/course/add/')
        self.assertEqual(reverse('rango:view_courses'), '/rango/dashboard/')
        self.assertEqual(reverse('rango:register'), '/rango/register/')

    def test_reverse_with_args(self):
        """Tests dynamic URLs for edit/delete functions[cite: 22]."""
        url = reverse('rango:delete_assignment', kwargs={'assignment_id': 5})
        self.assertEqual(url, '/rango/assignment/delete/5/')