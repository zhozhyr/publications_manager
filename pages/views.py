from django.shortcuts import render


def about(request):
    return render(request, 'pages/about.html')


def contacts(request):
    return render(request, 'pages/contacts.html')
