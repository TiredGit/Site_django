from django.test import TestCase
from site_app import factories, models
from django.urls import reverse

class TestSite(TestCase):
    def setUp(self):
        self.service1 = factories.ServiceFactory()
        self.service2 = factories.ServiceFactory()
        self.user1 = factories.MyUserFactory()
        self.user2 = factories.MyUserFactory()
        self.category1 = factories.CategoryFactory()
        self.category2 = factories.CategoryFactory()
        self.review1 = factories.ReviewFactory()

    def test_get_category_list(self):
        print()
        url = reverse('main')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        print('main:', 'success')
        self.assertEqual(response.context['categories'].count(), models.Category.objects.count())
        print('main categories:', response.context['categories'].count(), models.Category.objects.count())


    def test_get_review_list(self):
        print()
        url = reverse('main')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        print('main:', 'success')
        self.assertEqual(response.context['reviews'].count(), models.Review.objects.count())
        print('main reviews:', response.context['reviews'].count(), models.Review.objects.count())

    def test_users_count(self):
        print()
        self.assertEqual(models.MyUser.objects.count(), 3)
        print('users:', models.MyUser.objects.count())

    def test_get_category_detail(self):
        print()
        url = reverse('category_detail', kwargs={'pk': self.category1.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        print('detail:', 'success')