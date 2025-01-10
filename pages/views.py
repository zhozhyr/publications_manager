from django.shortcuts import render
from django.views.generic import TemplateView


class About(TemplateView):
    template_name = 'pages/about.html'


class Contacts(TemplateView):
    template_name = 'pages/contacts.html'


def page_not_found(request, exception):
    return render(request, 'pages/404.html', status=404)


def page_internal_server_error(request):
    return render(request, 'pages/500.html', status=500)


def page_csrf_forbidden(request, reason=''):
    return render(request, 'pages/403csrf.html', status=403)
