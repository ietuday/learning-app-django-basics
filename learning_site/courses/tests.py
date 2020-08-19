from django.core.urlresolvers import reverse
from django.test import TestCase
from django.utils import timezone
from .models import Course, Step

# Create your tests here.
class CourseModelTest(TestCase):
	def test_course_creation(self):
		course = Course.objects.create(
			title="Testing Python Code",
			description = "A description for Testing Python Code"
		)
		now = timezone.now();
		self.assertLess(course.created_at, now)


class StepModelTest(TestCase):
	def test_step_fulltitle(self):
		step = Step.objects.create(
			title="Test model",
			description="How to create a working test model",
			course_id = 3,
			order = 5
		)

		self.assertIn('#5', step.fulltitle())



class CourseViewsTests(TestCase):
	def setUp(self):
		self.course = Course.objects.create(
			title = "Course #1",
			description = "Description of the course #1"
		)

		self.course2 = Course.objects.create(
			title = "Course #2",
			description = "Description of the course #2"
		)

		self.step = Step.objects.create(
			title = "Introduction to view test",
			description = "How to create a view test",
			course = self.course
		)

	def test_course_list_view(self):
		resp = self.client.get(reverse('courses:list'))
		self.assertEqual(resp.status_code, 200)
		self.assertIn(self.course, resp.context['courses'])
		self.assertIn(self.course2, resp.context['courses'])
		self.assertTemplateUsed(resp, 'courses/course_list.html')
		self.assertContains(resp, self.course.title);


	def test_course_detail_view(self):
		resp = self.client.get(reverse('courses:detail', kwargs={'pk': self.course.pk}))
		self.assertEqual(resp.status_code, 200)
		self.assertEqual(self.course, resp.context['course'])
		self.assertNotEqual(self.course2, resp.context['course'])
		self.assertTemplateUsed(resp, 'courses/course_detail.html')
		self.assertContains(resp, self.course.title)

	def test_step_detail_view(self):
		resp = self.client.get(reverse('courses:step', kwargs={'step_pk': self.step.pk, 'course_pk': self.step.course_id}))
		self.assertEqual(resp.status_code, 200)
		self.assertEqual(self.step, resp.context['step'])
		self.assertTemplateUsed(resp, 'courses/step_detail.html')
		self.assertContains(resp, self.step.title)
