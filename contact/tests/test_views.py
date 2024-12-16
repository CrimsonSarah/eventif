from django.test import TestCase
from django.core import mail
from contact.forms import ContactForm


class ContactGet(TestCase):
    def setUp(self):
        self.response = self.client.get('/contact/')

    def teste_get(self):
        self.assertEqual(200, self.response.status_code)

    def teste_template(self):
        self.assertTemplateUsed(
            self.response, 'contact/contact_form.html')

    def teste_html(self):
        tags = (
            ('<form', 1),
            ('<input', 5),
            ('type="text"', 2),
            ('type="email"', 1),
            ('<textarea', 1),
            ('type="submit"', 1)
        )
        for text, count in tags:
            with self.subTest():
                self.assertContains(self.response, text, count)

    def teste_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')


class ContactPostValid(TestCase):
    def setUp(self):
        data = dict(name="Sarah Donato",
                    email='alternativegen@gmail.com.com', phone='53-12345-6789', message="teste")
        self.resp = self.client.post('/contact/', data)

    def teste_post(self):
        self.assertRedirects(self.resp, '/contact/1')

    def teste_email(self):
        self.assertEqual(1, len(mail.outbox))


class ContactPostInvalid(TestCase):
    def setUp(self):
        self.resp = self.client.post('/contact/', {})

    def teste_post(self):
        self.assertEqual(200, self.resp.status_code)

    def teste_template(self):
        self.assertTemplateUsed(
            self.resp, 'contact/contact_form.html')

    def teste_tem_form(self):
        form = self.resp.context['form']
        self.assertIsInstance(form, ContactForm)

    def teste_form_error(self):
        form = self.resp.context['form']
        self.assertTrue(form.errors)
