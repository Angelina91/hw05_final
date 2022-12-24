from http import HTTPStatus

from django.test import TestCase


class ViewTestClass(TestCase):
    def test_error_page_not_found_404(self):
        response = self.client.get("/nonexist-page/")
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertTemplateUsed(response, "core/404.html")

    # def test_error_csrf_failure_403(self):# хотела протестировать
    #                             и другие
    #                             страницы ошибок, но возникла с поиском адреса
    #     response = self.client.get('/permission_denied/')#не могу найти адрес
    #     self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
    #     self.assertTemplateUsed(response, 'core/403crf.html')
