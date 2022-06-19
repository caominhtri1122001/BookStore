from django.shortcuts import get_object_or_404, render, redirect
from django.http import JsonResponse
from requests import Response
from .forms import BookForm
from .models import *
import json
import datetime
from .utils import cartData, guestOrder
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.forms import AuthenticationForm


# Create your views here.
def store(request):
    data = cartData(request)
    cartItems = data['cartItems']

    books = Book.objects.all()
    context = {
        'books': books,
        'cartItems': cartItems,
    }
    return render(request, 'store/store.html', context)


def cart(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/cart.html', context)


@csrf_exempt
def checkout(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/checkout.html', context)


def detail(request, id):
    book = get_object_or_404(Book, id=id)
    context = {
        'book': book
    }
    return render(request, 'store/detail.html', context)


def login(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            return redirect('list')
    else:
        form = AuthenticationForm()
    return render(request, 'store/login.html', {'form': form})


def list(request):
    keyword = request.GET.get('keyword')
    select = request.GET.get('drop-down')
    if keyword:
        if select == '0':
            books = Book.objects.filter(id__icontains=keyword)
        if select == '1':
            books = Book.objects.filter(name__icontains=keyword)
        if select == '2':
            books = Book.objects.filter(price__icontains=keyword)
        if select == '3':
            books = Book.objects.filter(category__name__icontains=keyword)
    else:
        books = Book.objects.all()
    context = {
        "keyword": keyword,
        'books': books,
        '1': select
    }
    return render(request, 'store/list.html', context)


# def create_view(request):
#     form = BookForm(request.POST or None, request.FILES or None)
#     if (form.is_valid()):
#         form.save()
#         form = BookForm()
#         return redirect('/list')
#     context = {
#         'form': form
#     }
#     return render(request, 'store/create.html', context)


def create_view(request):
    select = request.POST.get('category')
    category = Category.objects.all()
    context = {
        'category': category
    }
    if request.method == 'POST':
        # name = request.POST['name']
        # price = request.POST['price']
        # image = request.FILES['image']
        # print('name',name,price,image)
        Book.objects.create(name=request.POST['name'],
                            price=request.POST['price'],
                            image=request.FILES['image'],
                            category=Category(select))
        return redirect('list')
    else:
        return render(request, 'store/create.html', context)


# def update_view(request, id):
#     book = get_object_or_404(Book, id=id)
#     # book = get_object_or_404(Book, id=id)
#     # form = BookForm(request.POST or None, instance=book)
#     if request.method == 'POST':
#         book.delete()
#         Book.objects.create(name=request.POST['name'],
#                             price=request.POST['price'],
#                             image=request.FILES['image'], )
#         return redirect('/list')
#     context = {
#         'book': book
#     }
#     return render(request, 'store/update.html', context)

def update_view(request, id):
    select = request.POST.get('drop-down')
    print(Category(select))
    book = get_object_or_404(Book, id=id)
    category = Category.objects.all()
    context = {
        'book': book,
        'category': category,
    }
    if request.method == 'POST':
        # Book.objects.update(name=request.POST['name'],
        #     price=request.POST['price'],
        #     image=request.FILES['image'], )
        book.name = request.POST['name']
        book.price = request.POST['price']
        book.category = Category(select)
        # book.category.name = request.POST['']
        # print(request.POST['category'])
        book.image = request.FILES['image']
        book.save()
        return redirect('/list')
    else:
        return render(request, 'store/update.html', context)

def delete_view(request, id):
    book = get_object_or_404(Book, id=id)
    if request.method == 'POST':
        book.delete()
        return redirect('/list')
    context = {
        'book': book
    }
    return render(request, 'store/delete.html', context)


def updateItem(request):
    data = json.loads(request.body)
    bookID = data['bookID']
    action = data['action']

    print('Action : ', action)
    print('BookID : ', bookID)

    customer = request.user.customer
    book = Book.objects.get(id=bookID)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=book)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)


def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)

    else:
        customer, order = guestOrder(request, data)

    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == order.get_cart_total:
        order.complete = True
    order.save()

    if order.shipping is True:
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            zipcode=data['shipping']['zipcode']
        )

    return JsonResponse('Payment completed', safe=False)
