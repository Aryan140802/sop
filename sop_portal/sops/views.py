from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from django.conf import settings
from .models import SOP
from django.views.decorators.csrf import csrf_exempt

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        if username == settings.ADMIN_USERNAME and password == settings.ADMIN_PASSWORD:
            request.session["is_admin"] = True
            return redirect("admin_page")
        else:
            messages.error(request, "Invalid credentials")
    return render(request, "login.html")

def logout_view(request):
    request.session.flush()
    return redirect("login")

def admin_page(request):
    if not request.session.get("is_admin"):
        return redirect("login")
    sops = SOP.objects.all().order_by('-uploaded_at')
    return render(request, "admin.html", {"sops": sops})





@csrf_exempt
def delete_sop(request, sop_id):
    if not request.session.get("is_admin"):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({"error": "Unauthorized"}, status=401)
        else:
            return redirect("login")
    

@csrf_exempt
def update_sop(request, sop_id):
    if not request.session.get("is_admin"):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({"error": "Unauthorized"}, status=401)
        else:
            return redirect("login")
