from django.test import TestCase, Client
import datetime
from django.utils import timezone
from django.urls import reverse

from polls.models import Question

# Create your tests here.
class QuestionModelTests(TestCase):

    def test_was_published_recently_with_future_question(self):
        """
            was_published_recently returns False for questions whose
            pub_date is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date = time)
        self.assertEqual(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """
            was_published_recently returns False for questions whose
            pub_date is older than 1 day
        """
        time = timezone.now() - datetime.timedelta(days=10)
        old_question = Question(pub_date = time)
        self.assertEqual(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """
            was_published_recently returns True for questions whose
            pub_date is lesser than or equal 1 day
        """
        time = timezone.now() - datetime.timedelta(seconds=10000)
        recent_question = Question(pub_date = time)
        self.assertEqual(recent_question.was_published_recently(), True)


def create_question(question_text, days):
    """
        create a question with the given 'question_text' and published the given 
        number of 'days' offset to now (negative for questions published in the past, 
        positive for questions that have yet to be published).
    """
    time = timezone.now + datetime.timedelta(days = days)
    return Question(question_text = question_text, pub_date = time)

class QuestionIndexViewTests(TestCase):

    def test_no_questions(self):
        response = self.client.get(reverse('polls:index'))
        print(response.status_code)
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['latest_question_list'], [])
        self.assertContains(response.content, "No polls are available.")
