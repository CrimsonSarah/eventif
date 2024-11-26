from django.test import TestCase
from django.core import mail

class ContactPostValid(TestCase):
    def setUp(self):
        data = dict(name="Sarah Donato",
                    email='alternativegen@gmail.com', phone='53-12345-6789', message="Teste")
        self.client.post('/contact/', data)
        self.email = mail.outbox[0]

    def teste_assunto(self):
        expect = 'Novo contato.'
        self.assertEqual(expect, self.email.subject)

    def teste_remetente(self):
        expect = 'contato@eventif.com.br'
        self.assertEqual(expect, self.email.from_email)

    def teste_destinatario(self):
        expect = ['contato@eventif.com.br', 'alternativegen@gmail.com']
        self.assertEqual(expect, self.email.to)

    def teste_corpo(self):
        contents = (
            'Sarah Donato', 'alternativegen@gmail.com', '53-12345-6789', 'Teste'
        )
        for content in contents:
            with self.subTest():
                self.assertIn(content, self.email.body)