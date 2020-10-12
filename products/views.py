from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .models import Products

# Create your views here.
def home(request):
    products = Products.objects
    return render(request, 'products/home.html', {'products': products})

# create product form
@login_required(login_url='signup')
def create(request):
    if request.method == 'POST':
        if request.POST['title'] and request.POST['url'] and request.POST['body'] and 'icon' in request.FILES and 'image' in request.FILES:
            
            product = Products()

            product.title = request.POST['title']
            product.url = request.POST['url']
            if not product.url.startswith('http://') or product.url.startswith('http://'):
                product.url = 'http://'+product.url
            product.body = request.POST['body']
        
            product.icon = request.FILES['icon']
            product.image = request.FILES['image']
            product.pub_date = timezone.now()
            product.hunter = request.user

            product.save()

            return redirect('home')

        else:
            return render(request, 'products/create.html', {'error': 'All fields  are required.'})
    return render(request, 'products/create.html')

def detail(request, product_id):
    product = get_object_or_404(Products, pk=product_id)
    return render(request, 'products/detail.html', {'product': product})

@login_required(login_url='signup')
def upvote(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Products, pk=product_id)
        product.votes_total += 1
        product.save()
        return redirect('detail', product_id)

    return redirect('detail', product_id)
