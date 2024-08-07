from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import BadHeaderError, HttpResponse
from django.shortcuts import render, redirect
from .forms import RegisterForm
from .models import Product, Category


def home(request):
	categories = Category.objects.all()
	half = len(categories) // 2
	categories1 = categories[:half]
	categories2 = categories[half:]
	return render(request, 'home.html', {'categories1': categories1, 'categories2': categories2})

def about(request):
	return render(request, 'about.html', {})

def contact(request):
	return render(request, 'contact.html', {})

def detail(request):
	return render(request, 'detail.html', {})
	
def blog(request):
	return render(request, 'blog.html', {})

def blog_detail(request):
	return render(request, 'blog_detail.html', {})

def login_user(request):
	if request.method == "POST":
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)

			# # Do some shopping cart stuff
			# current_user = Profile.objects.get(user__id=request.user.id)
			# # Get their saved cart from database
			# saved_cart = current_user.old_cart
			# # Convert database string to python dictionary
			# if saved_cart:
			# 	# Convert to dictionary using JSON
			# 	converted_cart = json.loads(saved_cart)
			# 	# Add the loaded cart dictionary to our session
			# 	# Get the cart
			# 	cart = Cart(request)
			# 	# Loop thru the cart and add the items from the database
			# 	for key,value in converted_cart.items():
			# 		cart.db_add(product=key, quantity=value)

			messages.success(request, ("You Have Been Logged In!"))
			return redirect('home')
		else:
			messages.success(request, ("There was an error, please try again..."))
			return redirect('login')

	else:
		return render(request, 'login.html', {})

def logout_user(request):
	logout(request)
	messages.success(request, ("You have been logged out."))
	return redirect('home')


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, "Account created successfully!")
            return redirect('home')  # redirect to login or home page
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

def product(request):
	products = Product.objects.all()
	return render(request, 'product.html', {'products': products})

def detail(request, pk):
	product = Product.objects.get(id=pk)
	return render(request, 'detail.html', {'product': product})