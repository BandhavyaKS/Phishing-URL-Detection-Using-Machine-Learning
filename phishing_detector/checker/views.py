# checker/views.py
from django.shortcuts import render
from predictor import predict_url

from .models import URLCheck


def index(request):
    prediction = None
    if request.method == 'POST':
        url = request.POST.get('url', '').strip()
        if url:
            prediction = predict_url(url)
            URLCheck.objects.create(url=url, prediction=prediction)
    recent_checks = URLCheck.objects.all()[:10]
    return render(request, 'checker/index.html', {'prediction': prediction, 'recent_checks': recent_checks})


def dashboard(request):
    checks = URLCheck.objects.all()
    phishing_count = checks.filter(prediction='Phishing').count()
    legitimate_count = checks.filter(prediction='Legitimate').count()
    latest_checks = checks[:10]
    return render(request, 'checker/dashboard.html', {
        'checks': checks,
        'phishing_count': phishing_count,
        'legitimate_count': legitimate_count,
        'latest_checks': latest_checks,
    })