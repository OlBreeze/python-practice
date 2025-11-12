from django.shortcuts import render
from datetime import datetime

def main_view(request):
    return render(request, 'home_main.html', {'some_date': datetime(2025, 11, 12, 10, 0)})
