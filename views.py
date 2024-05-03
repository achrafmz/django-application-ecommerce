from django.shortcuts import render, redirect, get_object_or_404
from .models import Product , Contact
from django.core.paginator import Paginator
from django.contrib import messages
from .forms import ProductForm,ContactForm
import google.generativeai as genai
from django.http import JsonResponse
import json
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm




def index(request):
    product_object = Product.objects.all()
    item_name = request.GET.get('search')
    if item_name != '' and item_name is not None:
        product_object = Product.objects.filter(title__icontains=item_name)
    return render(request, 'bi3smart/index.html', {'product_object': product_object})

def detail(request, myid):
    product_object = Product.objects.get(id=myid)
    return render(request, 'bi3smart/detail.html', {'product': product_object})


def shop(request):
    product_objects = Product.objects.all()
 

    # Obtenir le terme de recherche de l'URL
    item_name = request.GET.get('search')

    # Filtrer les produits en fonction du terme de recherche
    if item_name and item_name.strip():
        product_objects = product_objects.filter(title__icontains=item_name)
    paginator = Paginator(product_objects, 4)
    page_number = request.GET.get('page')
    product_object = paginator.get_page(page_number)

    return render(request, 'bi3smart/shop.html', {'product_object': product_object})

def product_list(request):
    product_object = Product.objects.all()
    item_name = request.GET.get('search')
    if item_name != '' and item_name is not None:
        product_object = Product.objects.filter(title__icontains=item_name)
    return render(request, 'bi3smart/product_list.html', {'product_object': product_object})

def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('product_list')  # Redirection vers la liste des produits après ajout
    else:
        form = ProductForm()
    return render(request, 'bi3smart/product_create.html', {'form': form})

def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('product_list')  # Rediriger vers la liste des produits après suppression
    return render(request, 'bi3smart/product_confirm_delete.html', {'product': product})

def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_list')  # Rediriger vers la liste des produits après modification
    else:
        form = ProductForm(instance=product)
    return render(request, 'bi3smart/product_form.html', {'form': form})




def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()  # Enregistrez les données du formulaire dans la base de données
            return redirect('success')  # Redirigez vers une page de confirmation ou une autre page
    else:
        form = ContactForm()
    return render(request, 'bi3smart/contact.html', {'form': form})

def contact_list(request):
    contact_object = Contact.objects.all()
    
    return render(request, 'bi3smart/contact_list.html', {'contact_object': contact_object})

GOOGLE_API_KEY = 'AIzaSyCRPt18x6p9hZZD7gTYWjUhlAAZnp6HUZE'
genai.configure(api_key=GOOGLE_API_KEY)

def chat_view(request):
    if request.method == 'POST':
        # Obtenez le message de l'utilisateur à partir du formulaire
        user_input = request.POST.get('user_input', '')

        # Utilisez le modèle de génération pour obtenir la réponse du chatbot
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(user_input)
        bot_response = ''.join([p.text for p in response.candidates[0].content.parts])

        # Renvoyez le message de l'utilisateur et la réponse du chatbot au template
        return render(request, 'bi3smart/chat.html', {'user_input': user_input, 'bot_response': bot_response})

    return render(request, 'bi3smart/chat.html')

def test(request):
    product_object = Product.objects.all()
    
    return render(request, 'bi3smart/test.html', {'product_object': product_object})



def get_products(request):
    products = Product.objects.all()
    data = [{'id': product.id, 'name': product.name, 'image': product.image.url, 'price': product.price} for product in products]
    return JsonResponse(data, safe=False)

def product_list(request):
    # Récupérer tous les produits depuis la base de données
    products = Product.objects.all()
    # Convertir les produits en format JSON
    products_json = json.dumps([{'id': product.id, 'name': product.name, 'image': product.image.url, 'price': product.price} for product in products])
    # Passer les données des produits au template
    return render(request, 'bi3smart/test.html', {'products_json': products_json})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Rediriger vers la page d'accueil après la connexion
    else:
        form = AuthenticationForm()
    return render(request, 'bi3smart/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('login')

def user_register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Rediriger vers la page de connexion après l'enregistrement
    else:
        form = UserCreationForm()
    return render(request, 'bi3smart/register.html', {'form': form})