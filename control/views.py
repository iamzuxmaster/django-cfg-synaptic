from django.shortcuts import get_object_or_404, redirect, render
from web.models import Category, Office, Product, Slider
from django.http import JsonResponse


SECURE_PATH_ADMIN = '/control/'

def base_context(request):
    try: 
        code = request.build_absolute_uri().split('?')[1]
    except: 
        code = None
    office = Office.objects.last()
    context = {
        "office": office,
        "code": code
    }
    return context

def control_index(request):
    categories = Category.objects.all()
    products = Product.objects.filter(drop=False)
    sliders = Slider.objects.all()
    context = {
        "base": base_context(request=request),
        "categories": categories, 
        "products": products,
        "sliders": sliders
    }
    return render(request, 'control/index.html', context)


def control_categories_all(request):
    categories = Category.objects.all()
    context = {
        "base": base_context(request=request),
        "categories":categories
    }
    return render(request, "control/categories/all.html", context)


def control_categories_add(request):
    context = {
        "base": base_context(request=request)
    }
    return render(request, "control/categories/add.html", context)


def control_categories_create(request):    
    if request.method == "POST": 
        title_ru = request.POST["title_ru"]
        title_uz = request.POST["title_uz"]
        priority = request.POST["priority"]
        if title_ru.lower().strip() in list(map(lambda category: category.title_ru.lower().strip(), Category.objects.all())):
            return redirect(SECURE_PATH_ADMIN+"category/add/?error")
        else:
            category = Category.objects.create(title_uz=title_uz, title_ru=title_ru, priority=priority)
            category.save()
            return redirect(SECURE_PATH_ADMIN+"categories/?created")
    else: 
        answer = {
            "code": 404,
            "error": "Page Not Found"
        }
        return JsonResponse(answer, safe=False)


def control_categories_detail(request, slug):
    category= get_object_or_404(Category, slug=slug)
    context = {
        "base": base_context(request=request),
        "category": category
    }
    return render(request, "control/categories/detail.html", context)


def control_categories_edit(request):
    if request.method == "POST":
        category = get_object_or_404(Category, slug=request.POST["category_slug"])
        category.priority = request.POST["priority"]
        title_ru = request.POST["title_ru"]
        category.title_uz = request.POST["title_uz"]
        if title_ru.lower() == category.title_ru.lower():
            category.save()
            return redirect(SECURE_PATH_ADMIN + f"category/{category.slug}/?edited")
        elif title_ru.lower().strip() in list(map(lambda category: category.title_ru.lower().strip(), Category.objects.all())):
            category.save()
            return redirect(SECURE_PATH_ADMIN + f"category/{category.slug}/?title_error")
        else:
            category.title_ru = title_ru
            category.save()
            return redirect(SECURE_PATH_ADMIN + f"category/{category.slug}/?edited")
        
    else: 
        answer = {
            "code": 404,
            "error": "Page Not Found"
        }
        return JsonResponse(answer, safe=False)


def control_categories_delete(request):
    if request.method == "POST": 
        category = get_object_or_404(Category, slug=request.POST["category_slug"])
        category.delete()
        return redirect(SECURE_PATH_ADMIN + "categories/?deleted")
    else: 
        answer = {
            "code": 404,
            "error": "Page Not Found"
        }
        return JsonResponse(answer, safe=False)
