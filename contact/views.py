from django.shortcuts import render, resolve_url as r
from django.http import HttpResponseRedirect, Http404
from contact.forms import ContactForm
from django.core import mail
from django.template.loader import render_to_string
from django.conf import settings
from contact.models import Contact

def contact(request):
    if request.method == 'POST':
        return create(request)
    else:
        return new(request)

def new(request):
    return render(request, 'contact/contact_form.html', {'form': ContactForm()})


def create(request):
    form = ContactForm(request.POST)

    if not form.is_valid():
        return render(request, 'contact/contact_form.html', {'form': form})

    _send_mail(
        'contact/contact_email.txt',
        form.cleaned_data,
        'Novo contato.',
        settings.DEFAULT_FROM_EMAIL,
        form.cleaned_data['email'])

    messages.success(request, 'Contato realizado com sucesso')
    return HttpResponseRedirect('/contact/')



def new(request):
    return render(request, 'contact/contact_form.html', {'form': ContactForm()})

def detail(request, pk):
    try:
        contact = Contact.objects.get(pk=pk)
    except Contact.DoesNotExist:
        raise Http404

    return render(request, 'contact/contact_detail.html', {'contact': contact})


def _send_mail(template_name, context, subject, from_, to):
    body = render_to_string(template_name, context)
    email = mail.send_mail(subject, body, from_, [from_, to])
