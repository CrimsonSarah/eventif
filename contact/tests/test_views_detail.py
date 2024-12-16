from django.test import TestCase
from contact.models import Contact
from django.shortcuts import resolve_url as r

class ContactDetailGet(TestCase):
    def setUp(self):
        obj = Contact.objects.create(
            name='Cleber Fonseca',
            email='profcleberfonseca@gmail.com',
            phone='53-91234-5678',
            message='Olá, estou entrando em contato'
        )
        self.resp = self.client.get(r('contact:detail', obj.pk))

    def test_get(self):
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.resp,
                                'contact/contact_detail.html')

    def test_context(self):
        contact = self.resp.context['contact']
        self.assertIsInstance(contact, Contact)

    def test_html(self):
        contents = ('Cleber Fonseca',
                    'profcleberfonseca@gmail.com', '53-91234-5678', 'Olá, estou entrando em contato')
        with self.subTest():
            for expected in contents:
                self.assertContains(self.resp, expected)


class ContactDetailNotFound(TestCase):
    def test_not_found(self):
        resp = self.client.get(r('contact:detail', 0))
        self.assertEqual(resp.status_code, 404)