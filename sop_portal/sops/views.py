from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from django.conf import settings
from .models import SOP
from django.views.decorators.csrf import csrf_exempt
import json

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

# API endpoint to get all SOPs
@csrf_exempt
def api_sops(request):
    if request.method == 'GET':
        sops = SOP.objects.all().order_by('-uploaded_at')
        sop_list = []
        for sop in sops:
            sop_list.append({
                'id': sop.id,
                'title': sop.title,
                'team': sop.team,
                'sop_text': sop.sop_text,
                'uploaded_at': sop.uploaded_at.strftime('%Y-%m-%d %H:%M:%S')
            })
        return JsonResponse(sop_list, safe=False)
    
    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            title = data.get('title')
            team = data.get('team')
            sop_text = data.get('sop_text')
            
            if not title or not team or not sop_text:
                return JsonResponse({'error': 'Missing required fields'}, status=400)
            
            sop = SOP.objects.create(
                title=title,
                team=team,
                sop_text=sop_text
            )
            
            return JsonResponse({
                'id': sop.id,
                'title': sop.title,
                'team': sop.team,
                'sop_text': sop.sop_text,
                'uploaded_at': sop.uploaded_at.strftime('%Y-%m-%d %H:%M:%S')
            }, status=201)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

# API endpoint to handle individual SOP operations
@csrf_exempt
def api_sop_detail(request, sop_id):
    try:
        sop = get_object_or_404(SOP, id=sop_id)
    except:
        return JsonResponse({'error': 'SOP not found'}, status=404)
    
    if request.method == 'GET':
        return JsonResponse({
            'id': sop.id,
            'title': sop.title,
            'team': sop.team,
            'sop_text': sop.sop_text,
            'uploaded_at': sop.uploaded_at.strftime('%Y-%m-%d %H:%M:%S')
        })
    
    elif request.method == 'PATCH':
        try:
            data = json.loads(request.body)
            
            if 'title' in data:
                sop.title = data['title']
            if 'team' in data:
                sop.team = data['team']
            if 'sop_text' in data:
                sop.sop_text = data['sop_text']
                
            sop.save()
            
            return JsonResponse({
                'id': sop.id,
                'title': sop.title,
                'team': sop.team,
                'sop_text': sop.sop_text,
                'uploaded_at': sop.uploaded_at.strftime('%Y-%m-%d %H:%M:%S')
            })
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    elif request.method == 'DELETE':
        sop.delete()
        return JsonResponse({'success': 'SOP deleted successfully'})
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def delete_sop(request, sop_id):
    if not request.session.get("is_admin"):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({"error": "Unauthorized"}, status=401)
        else:
            return redirect("login")
    
    sop = get_object_or_404(SOP, id=sop_id)
    sop.delete()
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({"success": "SOP deleted"})
    else:
        messages.success(request, "SOP deleted successfully")
        return redirect("admin_page")

@csrf_exempt
def update_sop(request, sop_id):
    if not request.session.get("is_admin"):
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({"error": "Unauthorized"}, status=401)
        else:
            return redirect("login")
            
    sop = get_object_or_404(SOP, id=sop_id)
    
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            if 'sop_text' in data:
                sop.sop_text = data['sop_text']
                sop.save()
                return JsonResponse({"success": "SOP updated"})
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
    
    return JsonResponse({"error": "Invalid request"}, status=400)