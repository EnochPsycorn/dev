from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Product, Category, Customer,Order
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import authenticate, login

def homePage(request):
    if request.method == 'POST':
        product = request.POST.get('product')
        remove = request.POST.get('remove')
        cart = request.session.get('cart')
        if cart:
            quantity = cart.get(product)
            if quantity:
                if remove:
                    if quantity <= 1:
                        cart.pop(product)
                    else:
                        cart[product] = quantity - 1
                else:
                    cart[product] = quantity + 1
            else:
                cart[product] = 1
        else:
            cart = {}
            cart[product] = 1

        request.session['cart'] = cart
        print(request.session['cart'])
        return redirect('home')

    else:
        products = None
        categories = Category.objects.all()
        category_id = request.GET.get('category')
        if category_id:
            products = Product.objects.filter(category=category_id)
        else:
            products = Product.objects.all()
            
        context = {'products': products, 'categories': categories}
        print("Your Email Address is: ", request.session.get('email'))
        return render(request, 'core/home.html', context)


def loginU(request):
    if request.method == "GET":
        return render(request, 'core/login.html')
    else:
        email = request.POST.get('email')
        password = request.POST.get('password')
        customer = Customer.get_customer_by_email(email)

        error_msg = None
        if customer:
            user = authenticate(request, customer=email, password=password)
            print(user)

            if user is not None:
                request.session['customer_id'] = customer.id
                request.session['email'] = customer.email
                
                login(request, user)
                # Redirect to a success page
                return redirect("home")
            else:
                error_msg = "Email or Password is Incorrect"
        else:
            error_msg = "Email or Password is incorrrect"

    return render(request, 'core/login.html', {'error_msg':error_msg})
    
def logout(request):
    request.session.clear()
    return redirect('login')

def validateCustomer(customer):
    err_msg = None
    if not customer.first_name:
        err_msg = "First Name Required."
    elif len(customer.first_name) < 3:
        err_msg = "First Name must be 3 characters long."
    elif not customer.last_name:
        err_msg = "Last Name Required."
    elif len(customer.last_name) < 3:
        err_msg = "Last Name must be 3 characters long."
    elif not customer.phone:
        err_msg = "Phone is Required."
    elif len(customer.phone) < 10:
        err_msg = "Phone Number must be 10 characters long."
    elif not customer.email:
        err_msg = "Email is Required."
    elif customer.does_exits():
        err_msg = "User with this email address already registered."
    return err_msg

def cart(request):
    cart_product_id = list(request.session.get('cart').keys())

    cart_product = Product.get_products_by_id(cart_product_id)
    return render(request, 'core/cart.html', {'cart_product': cart_product})

def checkout(request):

    if request.method == "POST":

        address = request.POST.get("address")
        phone = request.POST.get("phone")
        customer = request.session.get("customer_id")
        cart = request.session.get("cart")
        products = Product.get_products_by_id(list(cart.keys()))
        print(address, phone, customer, cart, products)
        
        
        for product in products:
            order = Order(customer=Customer(id=customer), product=product, price=product.price, address=address,
            phone=phone, quantity=cart.get(str(product.id)))
            order.save()

            request.session['cart'] = {}

        return redirect("cart")
    else:
        return render(request, 'core/checkout.html')

def signup(request):
    first_name = request.POST.get('firstname')
    last_name = request.POST.get('lastname')
    phone = request.POST.get('phone')
    email = request.POST.get('email')
    password = request.POST.get('password')

    values = {
        'firstname': first_name,
        'lastname': last_name,
        'phone': phone,
        'email': email,
    }
    customer = Customer(first_name=first_name, last_name=last_name, phone=phone, email=email, password=password)
    # customer.save()
    
    
    err_msg = validateCustomer(customer)

    if err_msg:
        return render(request, 'core/signup.html', {'error_msg': err_msg, 'values': values})
        
    else:
        customer.password = make_password(customer.password)
        customer.save()
        return redirect('home')
        
def orderpage(request):
    customer = request.session.get('customer_id')
    order = Order.get_order_by_customer(customer)
    print(order)
    return render(request, 'core/order.html', {'order': order})

# def signup(request):
#     if request.method == 'GET':
#         return render(request, 'core/signup.html')
#     else:
#         return registerCustomer(request)
