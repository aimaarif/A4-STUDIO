from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import BadHeaderError, HttpResponse
from django.shortcuts import render, redirect
from .forms import RegisterForm, ContactForm, SubscriberForm
from .models import Product, Category, MainCategory, UserProfile
from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404
from .models import Product, ProductReview, Wishlist
from .forms import ProductReviewForm
from django.core.mail import send_mail
from django.conf import settings
from .forms import UserProfileForm, ProductForm, ProfileImageForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import models, IntegrityError
from django.db.models import Avg
from django.core.paginator import Paginator

def home(request):
    categories = Category.objects.all()
    half = len(categories) // 2
    categories1 = categories[:half]
    categories2 = categories[half:]

    return render(request, 'home.html', {'categories1': categories1, 'categories2': categories2,})

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

	

def login_user(request):
	if request.method == "POST":
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
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
    sort_option = request.GET.get('sort', '')

    if sort_option == 'rating_asc':
        products = Product.objects.annotate(avg_rating=Avg('reviews__rating')).order_by('avg_rating')
    elif sort_option == 'rating_desc':
        products = Product.objects.annotate(avg_rating=Avg('reviews__rating')).order_by('-avg_rating')
    elif sort_option == 'name_asc':
        products = Product.objects.all().order_by('name')
    elif sort_option == 'name_desc':
        products = Product.objects.all().order_by('-name')
    elif sort_option == 'date_desc':
        products = Product.objects.all().order_by('-created_at')
    elif sort_option == 'date_asc':
        products = Product.objects.all().order_by('created_at')
    else:
        products = Product.objects.all()

    paginator = Paginator(products, 12)  # Show 12 products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    total_products = products.count()
    maincategories = MainCategory.objects.all()

    context = {
        'maincategories': maincategories,
        'products': page_obj,  # Pass the paginated products
        'page_obj': page_obj,  # Pass the page object for pagination controls
        'total_products':total_products,
    }

    return render(request, 'product.html', context)


@login_required
def detail(request, pk):
    maincategories = MainCategory.objects.all()
    product = get_object_or_404(Product, id=pk)
    reviews = product.reviews.all()
    average_rating = reviews.aggregate(models.Avg('rating'))['rating__avg'] or 0

    if request.method == 'POST':
        form = ProductReviewForm(request.POST)
        if form.is_valid():
            # Try to get an existing review for the product by the user
            existing_review = ProductReview.objects.filter(product=product, user=request.user).first()
            
            if existing_review:
                # Update the existing review
                existing_review.rating = form.cleaned_data['rating']
                existing_review.save()
            else:
                # Create a new review if none exists
                review = form.save(commit=False)
                review.product = product
                review.user = request.user
                review.save()
                
            return redirect('detail', pk=product.pk)  # Redirect after saving/updating
    else:
        form = ProductReviewForm()

    context = {
        'product': product,
        'reviews': reviews,
        'average_rating': average_rating,
        'form': form,
        'maincategories':maincategories,
    }
    return render(request, 'detail.html', context)


@login_required
def wishlist_view(request):
    wishlist_items = Wishlist.objects.filter(user=request.user)
    return render(request, 'wishlist.html', {'wishlist_items': wishlist_items})


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
    show_wishlist = request.GET.get('show') == 'wishlist_items'
    if not user_profile.profile_image:
        user_profile.profile_image = 'uploads/profile_pics/default.png'
    maincategories = MainCategory.objects.all()
    user_products = Product.objects.filter(user=user)
    following_list = user_profile.following.all() if show_following else []
    wishlist_items = Wishlist.objects.filter(user=user) if show_wishlist else []
    context = {
        'user_profile': user_profile, 
        'maincategories': maincategories, 
        'form': form, 
        'user_products': user_products, 
        'full_name': full_name, 
        'is_editing': is_editing,
        'following_list': following_list,
        'show_following': show_following,
        'wishlist_items': wishlist_items,
        'show_wishlist': show_wishlist,
    }
    return render(request, 'profile.html', context)


@login_required
def category_user(request, maincategory_id):
    maincategory = MainCategory.objects.get(id=maincategory_id)
    categories = Category.objects.filter(maincategory=maincategory)
    return render(request, 'category_user.html', {'categories': categories, 'maincategory': maincategory})

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
            return redirect('profile', username=request.user.username)  
    else:
        form = ProductForm()
    return render(request, 'add_product.html', {'form': form, 'category': category})

@login_required
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id, user=request.user)
    product.delete()
    messages.success(request, 'Product deleted successfully!')
    return redirect('profile', username=request.user.username)

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
    show_wishlist = request.GET.get('show') == 'wishlist_items'
    if not user_profile.profile_image:
        user_profile.profile_image = 'uploads/profile_pics/default.png'
    maincategories = MainCategory.objects.all()
    user_products = Product.objects.filter(user=user_profile.user)
    following_list = user_profile.following.all() if show_following else []
    wishlist_items = Wishlist.objects.filter(user=user) if show_wishlist else []
    context = {
        'user_profile': user_profile,
        'maincategories': maincategories,
        'form': form,
        'user_products': user_products,
        'full_name': full_name,
        'user': user, 
        'following_list': following_list,
        'show_following': show_following,
        'wishlist_items': wishlist_items,
        'show_wishlist': show_wishlist,
    }
    return render(request, 'userprofile.html', context)



@login_required
def follow_user(request, user_id):
    """Allow a user to follow another user."""
    user_to_follow = get_object_or_404(UserProfile, user__id=user_id)
    user_profile = request.user.userprofile

    if user_to_follow != user_profile:
        user_profile.follow(user_to_follow)
        messages.success(request, f"You've added {user_to_follow.user.username}.")
    else:
        messages.error(request, "You cannot add yourself.")

    return redirect('userprofile', user_id=user_to_follow.user.id)

@login_required
def unfollow_user(request, user_id):
    """Allow a user to unfollow another user."""
    user_to_unfollow = get_object_or_404(UserProfile, user__id=user_id)
    user_profile = request.user.userprofile

    if user_to_unfollow != user_profile:
        user_profile.unfollow(user_to_unfollow)
        messages.success(request, f"You have unadded {user_to_unfollow.user.username}.")
    else:
        messages.error(request, "You cannot add yourself.")

    return redirect('userprofile', user_id=user_to_unfollow.user.id)

@login_required
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist, created = Wishlist.objects.get_or_create(user=request.user, product=product)
    
    if created:
        messages.success(request, f'{product.name} has been added to your wishlist.')
    else:
        messages.info(request, f'{product.name} is already in your wishlist.')
    
    return redirect('detail', pk=product_id)  # Adjust the redirect as needed

@login_required
def wishlist_view(request):
    wishlist_items = Wishlist.objects.filter(user=request.user)
    return render(request, 'wishlist.html', {'wishlist_items': wishlist_items})


def maincategory_detail(request, id):
    maincategories = MainCategory.objects.all()
    maincategory = get_object_or_404(MainCategory, id=id)
    categories = maincategory.category_set.all()
    total_categories = categories.count()
    paginator = Paginator(categories, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'maincategory_detail.html', {'maincategory': maincategory, 'maincategories': maincategories, 'total_categories': total_categories, 'page_obj': page_obj})

def category_detail(request, id):
    maincategories = MainCategory.objects.all()
    category = get_object_or_404(Category, id=id)
    products = category.product_set.all()
    total_products = products.count()
    return render(request, 'category_detail.html', {'category': category, 'products': products, 'maincategories': maincategories, 'total_products': total_products,})


def search(request):
    query = request.GET.get('q')
    products = []
    
    if query:
        products = Product.objects.filter(name__icontains=query)  # Search by product name (or adapt for other fields)
    
    context = {
        'query': query,
        'products': products
    }
    
    return render(request, 'search.html', context)