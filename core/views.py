from django.shortcuts import render

# Create your views here.
# Viwe for index page
def index(request):
    return render(request, "core/index.html")

# View for dashboard page
def dashboard(request):
    return render(request, "core/dashboard.html")

# View for demo landing page
def demo_loading(request):
    return render(request, "core/demo_loading.html")