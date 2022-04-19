from itertools import product
import json
from unicodedata import category
from django.shortcuts import get_object_or_404, redirect, render
from web.models import Blog, Category, Discount, Office, Order, OrderTypes, Product, Slider, SubCategory
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

# Discounts

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
def control_discounts_all(request):
    discounts = Discount.objects.all()
    context = {
        "base": base_context(request=request),
        "discounts":discounts
    }
    return render(request, "control/discounts/all.html", context)


def control_discount_add(request):
    context = {
        "base": base_context(request=request)
    }
    return render(request, "control/discounts/add.html", context)


def control_discount_create(request):    
    if request.method == "POST": 
        title, unit = request.POST["title"], request.POST["unit"]
        if title.lower().strip() in list(map(lambda discount: discount.title.lower().strip(), Discount.objects.all())):
            return redirect(SECURE_PATH_ADMIN+"subcategory/add/?error")
        else:
            Discount.objects.create(title=title, unit=unit)
            return redirect(SECURE_PATH_ADMIN+"discounts/?created")

    else: 
        answer = {
            "code": 404,
            "error": "Page Not Found"
        }
        return JsonResponse(answer, safe=False)


def control_discount_detail(request, id):
    discount = get_object_or_404(Discount, id=id)
    context = {
        "base": base_context(request=request),
        "discount": discount
    }
    return render(request, "control/discounts/detail.html", context)


def control_discount_edit(request):
    if request.method == "POST":
        discount = get_object_or_404(Discount, id=request.POST["discount_id"])
        title, unit = request.POST["title"], request.POST["unit"]
        discount.unit = unit

        if title.lower().strip() == discount.title.lower().strip():
            discount.save()
            return redirect(SECURE_PATH_ADMIN + f"discount/{discount.id}/?edited")
        elif title.lower().strip() in list(map(lambda discount: discount.title.lower().strip(),Discount.objects.all())):
            discount.save()
            return redirect(SECURE_PATH_ADMIN + f"discount/{discount.id}/?error")
        else:
            discount.title = title
            discount.save()
            return redirect(SECURE_PATH_ADMIN + f"discount/{discount.id}/?edited")
        
    else: 
        answer = {
            "code": 404,
            "error": "Page Not Found"
        }
        return JsonResponse(answer, safe=False)



def control_discount_delete(request):
    if request.method == "POST": 
        discount = get_object_or_404(Discount, id=request.POST["discount_id"])
        discount.delete()
        return redirect(SECURE_PATH_ADMIN + "discounts/?deleted")
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


def control_products_discount_add(request):
    data = json.loads(request.body)
    title = data["title"]
    unit = data["unit"]
    if title.lower().strip() in list(map(lambda discount: discount.title.lower().strip(), Discount.objects.all())):
        answer ={
            "code": 403,
            "error": "Есть категория с таким названием.!"
        }
        return JsonResponse(answer, safe=False)
    else:
        discount = Discount.objects.create(title=title, unit=unit)


    answer ={
        "code": 200,
        "discount": {"id": discount.id, "title": discount.title}
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
            if request.POST["discount_id"] != '0':
                discount = get_object_or_404(Discount, id=request.POST["discount_id"])
            else:
                discount = None

            Product.objects.create(category=category, subcategory=subcategory, title_ru=title_ru, title_uz=title_uz, priority=priority, price=price, description_ru=description_ru, description_uz=description_uz, img_min=img_min, img_full=img_full, discount=discount)
            return redirect(SECURE_PATH_ADMIN + 'products/?created')
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
        if request.POST["discount_id"] != '0':
            product.discount = get_object_or_404(Discount, id=request.POST["discount_id"])
        else:
            product.discount = None
        try: 
            product.img_full = request.FILES["file"]
            product.img_min  = request.FILES["file"]
        except:
            pass

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
        
def control_product_delete(request):
    if request.method == "POST":
        product = get_object_or_404(Product, slug=request.POST["product_slug"])
        product.delete()
        return redirect(SECURE_PATH_ADMIN + "products/?deleted")



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


# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

# Blog

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

def control_sliders_delete(request):
    if request.method == "POST":
        slug = request.POST["slider_slug"]
        slider = get_object_or_404(Slider, slug=slug)
        slider.delete()
    return redirect(SECURE_PATH_ADMIN+"sliders/?deleted")


def control_blogs_all(request):
    blogs= Blog.objects.all()
    context = {
        "base": base_context(request=request),
        "blogs":blogs
    }
    return render(request, "control/blogs/all.html", context)


def control_blog_add(request):
    context = {
        "base": base_context(request=request)
    }
    return render(request, "control/blogs/add.html", context)


def control_blog_create(request):    
    if request.method == "POST" and request.FILES["file"]:  
        title_ru = request.POST["title_ru"]
        title_uz = request.POST["title_uz"]
        description_uz = request.POST["description_uz"]
        description_ru = request.POST["description_ru"]

        if title_ru.lower().strip() in list(map(lambda category: category.title_ru.lower().strip(), Blog.objects.all())):
            return redirect(SECURE_PATH_ADMIN+"blog/add/?error")
        else:
            Blog.objects.create(
                title_uz=title_uz, title_ru=title_ru, description_ru=description_ru, description_uz=description_uz,
                img_full=request.FILES["file"])
            return redirect(SECURE_PATH_ADMIN+"blogs/?created")
    else: 
        answer = {
            "code": 404,
            "error": "Page Not Found"
        }
        return JsonResponse(answer, safe=False)


def control_blog_detail(request, id):
    blog= get_object_or_404(Blog, id=id)
    context = {
        "base": base_context(request=request),
        "blog": blog
    }
    return render(request, "control/blogs/detail.html", context)


def control_blog_edit(request):    
    if request.method == "POST" or request.FILES["file"]:  
        blog = get_object_or_404(Blog, id=request.POST["blog_id"])
        blog.title_uz = request.POST["title_uz"]
        blog.description_uz = request.POST["description_uz"]
        blog.description_ru = request.POST["description_ru"]
        try: 
            blog.img_full = request.FILES["file"]
        except:
            pass

        if request.POST["title_ru"].lower().strip() == blog.title_ru.lower().strip():
            blog.save()
            return redirect(SECURE_PATH_ADMIN+f"blog/{blog.id}/?edited")
        if request.POST["title_ru"].lower().strip() in list(map(lambda blog: blog.title_ru.lower().strip(), Blog.objects.all())):
            blog.save()
            return redirect(SECURE_PATH_ADMIN+"blog/add/?error")
        else:
            blog.title_ru = request.POST["title_ru"]
            blog.save()
            return redirect(SECURE_PATH_ADMIN+f"blog/{blog.id}/?edited")


def control_blog_delete(request):
    if request.method == "POST":
        blog = get_object_or_404(Blog, id=request.POST["blog_id"])
        blog.delete()
        return redirect(SECURE_PATH_ADMIN + "blogs/?deleted")

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

# Orders

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
def control_orders_all(request): 
    ordertypes = OrderTypes.objects.all()
    context = {
        "base": base_context(request=request),
        "ordertypes": ordertypes
    }
    return render(request, "control/orders/all.html", context)

def control_order_edit(request): 
    data = json.loads(request.body)
    order = Order.objects.get(id=data["order_id"])
    ordertype = OrderTypes.objects.get(id=data["ordertype_id"])
    order.ordertypes = ordertype
    order.save()
    answer = {
        "code": 200
    }
    return JsonResponse(answer, safe=False)

def control_ordertype_edit(request):
    data = json.loads(request.body)
    ordertype = OrderTypes.objects.get(id=data["ordertype_id"])
    ordertype.title_ru = data["title_ru"]
    ordertype.save()
    answer = {
        "code": 200, 
        "ordertype": {"id": ordertype.id, "title_ru": ordertype.title_ru}
    }
    return JsonResponse(answer, safe=False)

def control_ordertype_create(request):
    data = json.loads(request.body)
    ordertype = OrderTypes.objects.create(title_ru=data["title_ru"])
    ordertype.save()
    answer = {
        "code": 200, 
        "ordertype": {"id": ordertype.id, "title_ru": ordertype.title_ru}
    }
    return JsonResponse(answer, safe=False)

def control_ordertype_delete(request):
    data = json.loads(request.body)
    ordertype = OrderTypes.objects.get(id=data["ordertype_id"])
    ordertype.delete()
    answer = {
        "code": 200
    }
    return JsonResponse(answer, safe=False)