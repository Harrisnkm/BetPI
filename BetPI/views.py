from django.shortcuts import redirect

def redirect_to_dashboard(request):
    return redirect('dashboard/')