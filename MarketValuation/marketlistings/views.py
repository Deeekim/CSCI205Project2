import csv
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.db.models import Q

from .models import Listing
from .forms import CSVUploadForm, ListingsForm

def home(request):
    return render(request, 'marketlistings/base_template.html')

def upload_csv(request):
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = form.cleaned_data['csv_file']
            decoded_file = csv_file.read().decode('utf-8').splitlines()
            reader = csv.DictReader(decoded_file)

            CATEGORY_MAPPING = {
                'House': 'hos',
                'Apartment': 'apt',
                'Condominium': 'cdm',
                'Commercial': 'cml',
            }
            TEMPORARY_ROW_COUNT = 0 # DELETE BEFORE SUBMISSION
            for row in reader:
                if TEMPORARY_ROW_COUNT > 10: # DELETE BEFORE SUBMISSION
                    break
                try:
                    category_key = CATEGORY_MAPPING.get(row['Category'], None) 

                    # Convert numeric fields to Decimal or float, or set to None if empty
                    land_size = float(row.get('Land Size(M2)', 0)) if row.get('Land Size(M2)') else None
                    building_size = float(row.get('Building Size(M2)', 0)) if row.get('Building Size(M2)') else None
                    bedrooms = int(row.get('Bedrooms', 0)) if row.get('Bedrooms') else None
                    bathrooms = int(row.get('Bathrooms', 0)) if row.get('Bathrooms') else None
                    latitude = float(row.get('Latitude', 0)) if row.get('Latitude') else None
                    longitude = float(row.get('Longitude', 0)) if row.get('Longitude') else None
                    price = float(row.get('Price(Php)', 0)) if row.get('Price(Php)') else None

                    if not category_key:
                        print(f"Skipping row with invalid category: {row['Category']}")
                        continue

                    Listing.objects.create(
                        description=row['Description'],
                        address=row['Location'],
                        category=category_key,
                        land_size=land_size,
                        building_size=building_size,
                        bedrooms=bedrooms,
                        bathrooms=bathrooms,
                        latitude=latitude,
                        longitude=longitude,
                        price=price,
                    )

                    TEMPORARY_ROW_COUNT += 1 # DELETE BEFORE SUBMISSION

                except ValueError as e:
                    print(f"Skipping row due to value error: {e}")

            return redirect('marketlistings:view-all')
    else:
        form = CSVUploadForm()

    return render(request, 'marketlistings/upload_csv.html', {'form': form})

def viewall(request):
    '''
    This function views all the listings available. Listings segmented into pages using Paginator.
    Source: https://docs.djangoproject.com/en/5.1/ref/paginator/#:~:text=Paginator¶,see%20the%20Pagination%20topic%20guide.
    '''
    query = request.GET.get('q', '')
    category = request.GET.get('category', '')
    price_range = request.GET.get('price_range',  '')
    sort = request.GET.get('sort', '')
    listings = Listing.objects.all()

    # Search Query
    if query:
        listings = listings.filter(
            Q(description__icontains=query) | 
            Q(address__icontains=query)
        )

    # Category selecting
    if category:
        listings = listings.filter(category = category)

    # Price range filter
    if price_range:
        try:
            min_price, max_price = map(float, price_range.split('-'))
            listings = listings.filter(price__gte=min_price, price__lte=max_price)
        except ValueError:
            pass

    # Sorting
    if sort == "price_asc":
        listings = listings.order_by("price")
    elif sort == "price_desc":
        listings = listings.order_by("-price")

    listings_per_page = 6
    paginator = Paginator(listings, listings_per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    elided_page_range = paginator.get_elided_page_range(page_obj.number, on_each_side =2, on_ends =2)

    context = {
        'page_obj': page_obj, 
        'elided_page_range': elided_page_range,
        'query': query,
        'category': category,
        'price_range': price_range,
        'sort': sort,
    }

    return render(request, 'marketlistings/view_all.html', context)


def addlistings(request):
    '''
    This function allows the user to create a listing by filling up a form of parameters.
    '''
    if request.method == "GET":
        lf = ListingsForm()
    elif request.method == "POST":
        lf = ListingsForm(request.POST)
        if lf.is_valid():
            lf.save()
            return redirect('marketlistings:view-all')

    context = { 'form': lf }
    return render(request, 'marketlistings/add_listings.html', context)

def view_listing(request, pk):
    '''
    This functions prints out more information on a selected listing.
    '''
    listing = Listing.objects.get(id = pk)
    context = { 'listing': listing }
    return render(request, 'marketlistings/view_listing.html', context)

def edit_listing(request, pk):
    '''
    This function allows the user 
    '''
    listing = Listing.objects.get(id = pk)
    if request.method == "GET":
        form = ListingsForm(instance = listing)
    elif request.method == "POST":
        form = ListingsForm(request.POST, instance = listing)
        if form.is_valid():
            form.save()
            return redirect('marketlistings:view-all')
    context = { 'form': form , 'listing': listing }
    return render(request, 'marketlistings/edit_listing.html', context)

def delete_listing(request, pk):
    listing = Listing.objects.get(id = pk)
    if request.method == "GET":
        context = { 'listing' : listing }
        return render(request, "marketlistings/delete_listing.html", context)
    elif request.method == "POST":
        listing.delete()
        return redirect('marketlistings:view-all')
