from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from ..models.Slider import Slider
from ..models.Collection import Collection
from ..models.Product import Product
from ..models.Page import Page
from ..models.Category import Category


def index(request):
    sliders = Slider.objects.all()
    collections = Collection.objects.all()

    best_seller = Product.objects.filter(is_best_seller=True)
    new_arrival = Product.objects.filter(is_new_arrival=True)
    featured = Product.objects.filter(is_featured=True)
    special_offer = Product.objects.filter(is_special_offer=True)
    available = Product.objects.filter(is_available=True)

    
    return render(request, 'shop/index.html', {
        'sliders': sliders, 
        'collections': collections,
        'best_seller': best_seller,
        'new_arrival': new_arrival,
        'featured': featured,
        'special_offer': special_offer,
        'available': available,
        })


def display_page(request, slug):
    page = get_object_or_404(Page, slug=slug)

    return render(request, 'shop/page.html', {
        'page': page,
        })


def display_product(request, slug):
    product = get_object_or_404(Product, slug=slug)

    return render(request, 'shop/single_product.html', {
        'product': product,
        })


def shop(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    
    sort_by_price = request.session.get('sort-price', 'asc')
    
    showing = request.session.get('showing', 6)
    
    # category_id = request.GET.get('category_id', 'all')

    # if category_id and category_id  != 'all':
    #     category = get_object_or_404(Category, id=category_id)
    #     products = category.product_set.all()
    # else:
    #     products = Product.objects.all()

        
    if 'showing' in request.GET and request.GET['showing'] != "":
        showing = int(request.GET['showing'])
        request.session['showing'] = showing

    
    if 'category_id' in request.GET and request.GET['category_id'] != "":
        category_id = int(request.GET['category_id'])
    
    if 'sort-price' in request.GET and request.GET['sort-price'] != "":
        sort_by_price = request.GET['sort-price']
        request.session['sort-price'] = sort_by_price
    
    # display = request.GET.get('display', 'grid')
    display = request.session.get('display', 'grid')

    if 'display' in request.GET: 
        display = request.GET['display']
        request.session['display'] = display
        
    if sort_by_price == 'asc': 
        products = products.order_by('solde_price')
    elif sort_by_price == 'desc':
        products = products.order_by('-solde_price')    

    page = request.GET.get('page', 1)    
    paginator = Paginator(products, showing)
 
    try:
        product_pages = paginator.page(page)
    except PageNotAnInteger:
        product_pages = paginator.page(1)
    except EmptyPage:
        product_pages = paginator.page(paginator.num_pages)
    except:
        product_pages = paginator.page(1)
        
        

    return render(request, 'shop/shop_list.html', {
        'products': product_pages,
        'categories': categories,
        'display': display,
        # 'showing': showing,
        'sort_by_price': sort_by_price,
        })
    