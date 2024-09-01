from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import BadHeaderError, HttpResponse
from django.shortcuts import render, redirect
from .forms import RegisterForm, ContactForm, SubscriberForm
from .models import Product, Category, MainCategory, UserProfile
from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404
from .models import Product, Review
from django.core.mail import send_mail
from django.conf import settings
from .forms import UserProfileForm, ProductForm, ProfileImageForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

def home(request):
	categories = Category.objects.all()
	half = len(categories) // 2
	categories1 = categories[:half]
	categories2 = categories[half:]
	return render(request, 'home.html', {'categories1': categories1, 'categories2': categories2})

def about(request):
	return render(request, 'about.html', {})

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact_message = form.save()
            
            # Sending the email
            send_mail(
                subject=contact_message.subject,
                message=f"Message from {contact_message.name} <{contact_message.email}>:\n\n{contact_message.message}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.ADMIN_EMAIL],
                fail_silently=False,
            )
            messages.success(request, ("We've received your message. Thanks for contacting!"))
            return redirect('home')
    else:
        form = ContactForm()
    
    return render(request, 'contact.html', {'form': form})


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
    reviews = product.reviews.all()
    if request.method == 'POST':
            rating = request.POST.get('rating')
            comment = request.POST.get('comment')
            if rating:
                Review.objects.create(
                    product=product,
                    user=request.user,
                    rating=rating,
                    comment=comment
                )
    return render(request, 'detail.html', {'product': product, 'reviews': reviews,})


def download_image(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    image_path = product.image.path 
    
    try:
        response = FileResponse(open(image_path, 'rb'), as_attachment=True, filename=product.image.name)
        return response
    except FileNotFoundError:
        raise Http404("Image not found")
	

def subscribe(request):
    if request.method == 'POST':
        form = SubscriberForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thank you for subscribing!')
            return redirect('home')  # Redirect to a success page or the same page
        else:
            messages.error(request, 'This email is already subscribed.')
            return redirect('home')
    else:
        form = SubscriberForm()
    return render(request, 'home.html', {'form': form})



from django.shortcuts import get_object_or_404

@login_required
def profile(request, username=None, user_id=None):
    if username:
        user = get_object_or_404(User, username=username)
    else:
        user = request.user

    try:
        user_profile = user.userprofile
    except UserProfile.DoesNotExist:
        user_profile = UserProfile.objects.create(user=user)
        
    if request.method == 'POST':
        form = ProfileImageForm(request.POST or None, request.FILES or None, instance=user_profile, user=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile image updated successfully!")
            return redirect('profile', username=user.username)  # Redirect to the profile page with the username
    else:
        form = ProfileImageForm(instance=user_profile)

    full_name = f"{user.first_name} {user.last_name}".strip()
    is_editing = request.GET.get('edit', False)
    show_following = request.GET.get('show') == 'following'
    if not user_profile.profile_image:
        user_profile.profile_image = 'uploads/profile_pics/default.png'
    maincategories = MainCategory.objects.all()
    user_products = Product.objects.filter(user=user)
    following_list = user_profile.following.all() if show_following else []
    context = {
        'user_profile': user_profile, 
        'maincategories': maincategories, 
        'form': form, 
        'user_products': user_products, 
        'full_name': full_name, 
        'is_editing': is_editing,
        'following_list': following_list,
        'show_following': show_following,
    }
    return render(request, 'profile.html', context)


@login_required
def category(request, maincategory_id):
    maincategory = MainCategory.objects.get(id=maincategory_id)
    categories = Category.objects.filter(maincategory=maincategory)
    return render(request, 'category.html', {'categories': categories, 'maincategory': maincategory})

@login_required
def add_product(request, category_id):
    category = Category.objects.get(id=category_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.category = category
            product.user = request.user
            product.save()
            messages.success(request, 'Product added successfully!')
            return redirect('profile')  # Redirect to profile or wherever you want
    else:
        form = ProductForm()
    return render(request, 'add_product.html', {'form': form, 'category': category})

def edit_profile(request):
	return render(request, 'edit_profile.html', {})


@login_required
def userprofile(request, user_id):
    
    user = get_object_or_404(User, id=user_id)
    user_profile = get_object_or_404(UserProfile, user=user)
    form = ProfileImageForm(instance=user_profile)

    # Remaining logic for handling profile display, form submissions, etc.
    full_name = f"{user_profile.user.first_name} {user_profile.user.last_name}".strip()
    show_following = request.GET.get('show') == 'following'
    if not user_profile.profile_image:
        user_profile.profile_image = 'uploads/profile_pics/default.png'
    maincategories = MainCategory.objects.all()
    user_products = Product.objects.filter(user=user_profile.user)
    following_list = user_profile.following.all() if show_following else []
    context = {
        'user_profile': user_profile,
        'maincategories': maincategories,
        'form': form,
        'user_products': user_products,
        'full_name': full_name,
        'user': user, 
        'following_list': following_list,
        'show_following': show_following,
    }
    return render(request, 'userprofile.html', context)



@login_required
def follow_user(request, user_id):
    """Allow a user to follow another user."""
    user_to_follow = get_object_or_404(UserProfile, user__id=user_id)
    user_profile = request.user.userprofile

    if user_to_follow != user_profile:
        user_profile.follow(user_to_follow)
        messages.success(request, f"You are now following {user_to_follow.user.username}.")
    else:
        messages.error(request, "You cannot follow yourself.")

    return redirect('profile', user_id=user_to_follow.user.id)

@login_required
def unfollow_user(request, user_id):
    """Allow a user to unfollow another user."""
    user_to_unfollow = get_object_or_404(UserProfile, user__id=user_id)
    user_profile = request.user.userprofile

    if user_to_unfollow != user_profile:
        user_profile.unfollow(user_to_unfollow)
        messages.success(request, f"You have unfollowed {user_to_unfollow.user.username}.")
    else:
        messages.error(request, "You cannot unfollow yourself.")

    return redirect('profile', user_id=user_to_unfollow.user.id)
