from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    # return HttpResponse("<html><body>Hello HOME</body></html>")
    return render(request, 'home/home.html')

def home_page(request):
    return render(request, 'home/home.html')

def about_page(request):
    # return HttpResponse("Сторінка про нас")
    return render(request, 'home/about.html')

def contact_page(request):
    # return HttpResponse("Зв'яжіться з нами")
    return render(request, 'home/contact.html')

def post_view(request, id):
    context = {'post_id': id}
    return render(request, 'home/post.html', context)

def profile_view(request, username):
    context = {'username': username}
    return render(request, 'home/profile.html', context)

def event_view(request, year, month, day):
    context = {
        'year': year,
        'month': month,
        'day': day,
        'full_date': f"{year}-{month}-{day}"
    }
    return render(request, 'home/event.html', context)