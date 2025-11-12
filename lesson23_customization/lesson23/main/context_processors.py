def site_info_main(request):
    """Добавляет информацию о сайте в каждый шаблон"""
    return {
        'site_name': 'My Awesome Django Site',
        'author': 'Olga Golovash',
    }
