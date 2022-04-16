from django.shortcuts import render

# Create your views here.
def our_browser(request):
    return render(request, 'our_browser.html', {})