from itertools import product
import json
from unicodedata import category
from django.shortcuts import get_object_or_404, redirect, render
from web.models import Category, Discount, Office, Product, Slider, SubCategory
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


# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

# Categories

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

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



# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

# Subcategory

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
def control_subcategories_all(request):
    subcategories = SubCategory.objects.all()
    context = {
        "base": base_context(request=request),
        "subcategories":subcategories
    }
    return render(request, "control/subcategories/all.html", context)


def control_subcategories_add(request):
    categories = Category.objects.all()
    context = {
        "base": base_context(request=request),
        "categories":categories
    }
    return render(request, "control/subcategories/add.html", context)


def control_subcategories_category_add(request):
    data = json.loads(request.body)
    title_ru,  title_uz , priority = data["title_ru"],  data["title_uz"], data["priority"]

    if title_ru.lower().strip() in list(map(lambda category: category.title_ru.lower().strip(), Category.objects.all())):
        answer ={
            "code": 403,
            "error": "Есть категория с таким названием.!"
        }
        return JsonResponse(answer, safe=False)
    else:
        category = Category.objects.create(title_ru=title_ru, title_uz=title_uz, priority=priority)
        category.save()

    answer ={
        "code": 200,
        "category": {"id": category.id, "title_ru": category.title_ru}
    }


    return JsonResponse(answer, safe=False)


def control_subcategories_create(request):    
    if request.method == "POST": 
        title_ru, title_uz, priority = request.POST["title_ru"], request.POST["title_uz"], request.POST["priority"]
        category = get_object_or_404(Category, id=request.POST["category_id"])

        if title_ru.lower().strip() in list(map(lambda subcategory: subcategory.title_ru.lower().strip(), SubCategory.objects.all())):
            return redirect(SECURE_PATH_ADMIN+"subcategory/add/?error")
        else:
            subcategory = SubCategory.objects.create(category=category,title_uz=title_uz, title_ru=title_ru, priority=priority)
            subcategory.save()
            return redirect(SECURE_PATH_ADMIN+"subcategories/?created")

    else: 
        answer = {
            "code": 404,
            "error": "Page Not Found"
        }
        return JsonResponse(answer, safe=False)


def control_subcategories_detail(request, slug):
    categories = Category.objects.all()
    subcategory = get_object_or_404(SubCategory, slug=slug)
    context = {
        "base": base_context(request=request),
        "categories": categories, 
        "subcategory": subcategory
    }
    return render(request, "control/subcategories/detail.html", context)


def control_subcategories_edit(request):
    if request.method == "POST":
        category = get_object_or_404(Category, id=request.POST["category_id"])
        subcategory = get_object_or_404(SubCategory, slug=request.POST["subcategory_slug"])
        title_ru, title_uz, priority = request.POST["title_ru"], request.POST["title_uz"], request.POST["priority"]
        subcategory.title_uz = title_uz
        subcategory.priority = priority
        subcategory.category = category

        if title_ru.lower().strip() == subcategory.title_ru.lower().strip():
            subcategory.save()
            return redirect(SECURE_PATH_ADMIN + f"subcategory/{subcategory.slug}/?edited")
        elif title_ru.lower().strip() in list(map(lambda subcategory: subcategory.title_ru.lower().strip(), SubCategory.objects.all())):
            subcategory.save()
            return redirect(SECURE_PATH_ADMIN + f"subcategory/{subcategory.slug}/?title_error")
        else:
            subcategory.title_ru = title_ru
            subcategory.save()
            return redirect(SECURE_PATH_ADMIN + f"subcategory/{subcategory.slug}/?edited")
        
    else: 
        answer = {
            "code": 404,
            "error": "Page Not Found"
        }
        return JsonResponse(answer, safe=False)


def control_subcategories_delete(request):
    if request.method == "POST": 
        category = get_object_or_404(SubCategory, slug=request.POST["subcategory_slug"])
        category.delete()
        return redirect(SECURE_PATH_ADMIN + "subcategories/?deleted")
    else: 
        answer = {
            "code": 404,
            "error": "Page Not Found"
        }
        return JsonResponse(answer, safe=False)




# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

# Products

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

def control_products_all(request):
    products = Product.objects.filter(drop=False)
    context = {
        "base": base_context(request=request),
        "products": products
    }
    return render(request, "control/products/all.html", context)


def control_product_add(request):
    categories = Category.objects.all()
    subcategories = SubCategory.objects.all()
    context = {
        "base": base_context(request=request),
        "categories": categories,
        "subcategories": subcategories,
        
    }
    return render(request, "control/products/add.html", context)


def control_products_subcategory_add(request):
    data = json.loads(request.body)
    category  = get_object_or_404(Category, id=data["category_id"])
    title_ru,  title_uz , priority = data["title_ru"],  data["title_uz"], data["priority"]

    if title_ru.lower().strip() in list(map(lambda subcategory: subcategory.title_ru.lower().strip(), SubCategory.objects.all())):
        answer ={
            "code": 403,
            "error": "Есть категория с таким названием.!"
        }
        return JsonResponse(answer, safe=False)
    else:
        subcategory = SubCategory.objects.create(category=category, title_ru=title_ru, title_uz=title_uz, priority=priority)
        subcategory.save()

    answer ={
        "code": 200,
        "subcategory": {"id": subcategory.id, "title_ru": subcategory.title_ru}
    }


    return JsonResponse(answer, safe=False)


def control_product_create(request):
    if request.method == "POST" and request.FILES["file"]:
        if request.POST["title_ru"].lower().strip() not in list(map(lambda product: product.title_ru.lower().strip(), Product.objects.all())):
            category = get_object_or_404(Category, id=request.POST["category_id"])
            subcategory = get_object_or_404(SubCategory, id=request.POST["subcategory_id"])
            title_ru = request.POST["title_ru"]
            title_uz = request.POST["title_uz"]
            description_ru = request.POST["description_ru"]
            description_uz = request.POST["description_uz"]
            priority = request.POST["priority"]
            price = request.POST["price"]
            img_min = request.FILES["file"]
            img_full = request.FILES["file"]
            Product.objects.create(category=category, subcategory=subcategory, title_ru=title_ru, title_uz=title_uz, priority=priority, price=price, description_ru=description_ru, description_uz=description_uz, img_min=img_min, img_full=img_full)
            return redirect(SECURE_PATH_ADMIN + 'products/?success')
        else: 
            return redirect(SECURE_PATH_ADMIN + 'product/add/?error')

    else: 
        answer = {
            "code": 404,
            "error": "Page Not Found"
        }
        return JsonResponse(answer, safe=False)

def control_product_detail(request, slug):
    categories = Category.objects.all()
    subcategories = SubCategory.objects.all()
    discounts = Discount.objects.all()
    product =  get_object_or_404(Product, slug=slug)
    context = {
        "base": base_context(request=request),
        "categories": categories,
        "subcategories": subcategories,
        "discounts": discounts,
        "product": product
    }
    return render(request, 'control/products/detail.html', context)


def control_product_edit(request):
    if request.method == 'POST' or request.FILES["file"]:
        product = get_object_or_404(Product, slug=request.POST["product_slug"])
        product.category = get_object_or_404(Category, id=request.POST["category_id"])
        product.subcategory = get_object_or_404(SubCategory, id=request.POST["subcategory_id"])
        product.title_uz = request.POST["title_uz"]
        product.description_ru = request.POST["description_ru"]
        product.description_uz = request.POST["description_uz"]
        product.priority = request.POST["priority"]
        product.price = request.POST["price"]

        if request.POST["title_ru"].lower().strip() == product.title_ru.lower().strip():
            product.save()
            return redirect(SECURE_PATH_ADMIN + f"product/{product.slug}/?edited")

        elif request.POST["title_ru"].lower().strip() not in list(map(lambda product: product.title_ru, Product.objects.filter(drop=False))):
            product.title_ru = request.POST["title_ru"]
            product.save()
            return redirect(SECURE_PATH_ADMIN + f"product/{product.slug}/?edited")
            
        else: 
            product.save()
            return redirect(SECURE_PATH_ADMIN + f"product/{product.slug}/?error")
        




# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

# Sliders

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$



def control_sliders_all(request):
    sliders = Slider.objects.all()
    context = {
        "base": base_context(request=request),
        "sliders": sliders
    }
    return render(request, "control/sliders/all.html", context)


def control_sliders_add(request):
    context = {
        "base": base_context(request=request)
    }
    return render(request, "control/sliders/add.html", context)


def control_sliders_create(request):
    if request.method == "POST" and request.FILES["file"]: 
        title_ru = request.POST["title_ru"]
        title_uz = request.POST["title_uz"]
        content_uz = request.POST["content_uz"]
        content_ru = request.POST["content_ru"]
        description_ru = request.POST["description_ru"]
        desctiption_uz = request.POST["description_uz"]
        priority = request.POST["priority"]
        if title_ru.lower().strip() in list(map(lambda slider: slider.title_ru.lower().strip(), Slider.objects.all())):
            return redirect(SECURE_PATH_ADMIN+"category/add/?error")
        else:
            slider = Slider.objects.create(
                title_uz=title_uz,
                title_ru=title_ru,
                priority=priority,
                img_min = request.FILES["file"],
                img_full = request.FILES["file"],
                description_ru = description_ru,
                description_uz = desctiption_uz
                )
            
            slider.content_ru=content_ru
            slider.content_uz=content_uz
            slider.save()
            return redirect(SECURE_PATH_ADMIN+"sliders/?created")
    else: 
        answer = {
            "code": 404,
            "error": "Page Not Found"
        }
        return JsonResponse(answer, safe=False)


def control_sliders_detail(request, slug):
    slider = get_object_or_404(Slider, slug=slug)
    context = {
        "base": base_context(request=request),
        "slider":slider
    }
    return render(request, "control/sliders/detail.html", context)



def control_sliders_edit(request):
    if request.method == "POST" or request.FILES["file"]:
        content_uz = request.POST["content_uz"]
        content_ru = request.POST["content_ru"]
        description_ru = request.POST["description_ru"]
        description_uz = request.POST["description_uz"]
        slider = get_object_or_404(Slider, slug=request.POST["slider_slug"])
        title_ru, title_uz, priority = request.POST["title_ru"], request.POST["title_uz"], request.POST["priority"]
        slider.title_uz = title_uz
        slider.content_ru = content_ru
        slider.content_uz = content_uz
        slider.description_ru = description_ru
        slider.description_uz = description_uz
        slider.priority = priority
        try: 
            slider.img_full = request.FILES["file"]
            slider.img_min = request.FILES["file"]
        except:
            pass

        
        if title_ru.lower().strip() == slider.title_ru.lower().strip():
            slider.save()
            return redirect(SECURE_PATH_ADMIN + f"slider/{slider.slug}/?edited")
        elif title_ru.lower().strip() in list(map(lambda slider: slider.title_ru.lower().strip(), Slider.objects.all())):
            slider.save()
            return redirect(SECURE_PATH_ADMIN + f"slider/{slider.slug}/?title_error")
        else:
            slider.title_ru = title_ru
            slider.save()
            return redirect(SECURE_PATH_ADMIN + f"slider/{slider.slug}/?edited")
        
    else: 
        answer = {
            "code": 404,
            "error": "Page Not Found"
        }
        return JsonResponse(answer, safe=False)



def control_sliders_delete(request):
    if request.method == "POST":
        slug = request.POST["slider_slug"]
        slider = get_object_or_404(Slider, slug=slug)
        slider.delete()
    return redirect(SECURE_PATH_ADMIN+"sliders/?deleted")

