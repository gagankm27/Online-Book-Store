import csv
import os
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from datetime import datetime
from .models import Book,UserDetails, Purchase

# LOGIN PAGE → Collect user details
def login_page(request):
    error = None

    if request.method == "POST":
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        email = request.POST.get("email")

        # Save data
        UserDetails.objects.create(
            name=name,
            phone=phone,
            email=email
        )

        # Redirect clears the form
        return redirect("home")

    # GET request - fresh empty form
    return render(request, "login.html", {"error": error})


# ADMIN LOGIN PAGE
def admin_login_page(request):
    error_message = None  # Initialize error message

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        # Admin Login
        if username == "admin@gmail.com" and password == "Admin@123":
            return redirect("crud")  # URL name of CRUD page
        # Invalid credentials
        else:
            error_message = "Invalid username or password."

    return render(request, "admin_login.html", {"error_message": error_message})


# HOME PAGE → Displays books to customer
def home(request):
    books = Book.objects.all()
    return render(request, "home.html", {"books": books})


# CRUD PAGE → Add/Delete books & View purchase records
def crud(request):
    books = Book.objects.all()

    # Add Book
    if request.method == "POST":
        name = request.POST.get("name")
        price = request.POST.get("price")
        Book.objects.create(name=name, price=price)
        return redirect("crud")

    # ----- Load CSV purchase data -----
    csv_path = os.path.join(settings.BASE_DIR, "bills", "Users_purchase_details.csv")
    bills = []

    if os.path.exists(csv_path):
        with open(csv_path, mode="r", encoding="utf-8") as file:
            reader = list(csv.DictReader(file))  # list so we can access by index
            # --- Apply search filter ---
            search_query = request.GET.get("search", "").lower()
            for row in reader:
                if search_query:
                    if search_query not in row["Name"].lower() \
                       and search_query not in row["Email"].lower() \
                       and search_query not in row["Phone"].lower():
                        continue
                bills.append({
                    "name": row["Name"],
                    "email": row["Email"],
                    "phone": row["Phone"],
                    "total_books": row["Total Books Purchased"],
                    "book_names": row["Book Names"],
                    "total_amount": row["Total Amount"]
                })

    return render(request, "crud.html", {"books": books, "bills": bills})


# DELETE PURCHASE ENTRY FROM CSV
def delete_purchase(request, index):
    """
    Deletes a purchased record from the CSV based on row index.
    """
    csv_path = os.path.join(settings.BASE_DIR, "bills", "Users_purchase_details.csv")
    if os.path.exists(csv_path):
        with open(csv_path, mode="r", encoding="utf-8") as file:
            rows = list(csv.DictReader(file))
            if 0 <= index < len(rows):
                rows.pop(index)  # remove row

        # Rewrite CSV
        if rows:
            with open(csv_path, mode="w", newline="", encoding="utf-8") as file:
                writer = csv.DictWriter(file, fieldnames=rows[0].keys())
                writer.writeheader()
                writer.writerows(rows)

    return redirect("crud")


# DELETE BOOK
def delete_book(request, id):
    book = get_object_or_404(Book, id=id)
    book.delete()
    return redirect("crud")


# CART FUNCTIONALITY
def add_to_cart(request, id):
    book = get_object_or_404(Book, id=id)

    cart = request.session.get('cart', [])

    cart.append({
        'id': book.id,
        'name': book.name,
        'price': float(book.price)
    })

    request.session['cart'] = cart

    return redirect("cart")  # Go to cart page


# VIEW CART PAGE
def cart_page(request):
    cart = request.session.get('cart', [])
    total = sum(item['price'] for item in cart)

    return render(request, "cart.html", {"cart": cart, "total": total})


# REMOVE ITEM FROM CART
def remove_from_cart(request, index):
    cart = request.session.get('cart', [])

    if 0 <= index < len(cart):
        cart.pop(index)

    request.session['cart'] = cart

    return redirect("cart")


# CHECKOUT - Generate CSV Bill and Clear Cart
def checkout(request):

    # ---- Get User Details (latest entry) ----
    try:
        user = UserDetails.objects.latest('id')
    except UserDetails.DoesNotExist:
        user = None

    # ---- Get cart data from session ----
    cart = request.session.get('cart', [])

    total_books = len(cart)
    book_names = [item['name'] for item in cart]
    total_amount = sum(item['price'] for item in cart)

    # ---- CSV File Path (single file) ----
    bill_folder = os.path.join(settings.BASE_DIR, "bills")
    os.makedirs(bill_folder, exist_ok=True)

    filepath = os.path.join(bill_folder, "Users_purchase_details.csv")

    # ---- Check if file already exists (to add header only once) ----
    file_exists = os.path.isfile(filepath)

    # ---- Append purchase record to CSV ----
    with open(filepath, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        # Write header only for first time
        if not file_exists:
            writer.writerow([
                "Name", "Email", "Phone",
                "Total Books Purchased",
                "Book Names",
                "Total Amount",
                "Purchase Time"
            ])

        writer.writerow([
            user.name if user else "Unknown",
            user.email if user else "Unknown",
            user.phone if user else "Unknown",
            total_books,
            ", ".join(book_names),
            total_amount,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ])

    # ---- Clear Cart ----
    request.session['cart'] = []

    return redirect('/')  # Redirect to login or home page after checkout
