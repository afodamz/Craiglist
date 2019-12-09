from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from bs4 import BeautifulSoup
import requests
from requests.compat import quote_plus #This helps to put python tutor to python%20tutor
from .models import Search



BASE_CRAIGLIST_URL = 'https://losangeles.craiglist.org/search/?query{}'
BASE_IMAGE_URL = 'https://images.craiglist.org/{}_300x300.jpg'

# Create your views here.
def home(request):
    return render(request, 'home.html')

@csrf_exempt
def new_search(request):
    search = request.POST['search']
    Search.objects.create(search_text=search)

#Gets the all html data from the website
    # response = reuest.get('https://losangeles.craiglist.org/search/?query=python%20tutor')
    # data = response.text
    # print(data)

    final_url = BASE_CRAIGLIST_URL.format(quote_plus(search))
    response = requests.get(BASE_CRAIGLIST_URL)
    data = response.text
#Passing the source code to Beautiful soup to create a BeautifulSoup object
    soup = Beautifulsoup(data, features='html.parser')
#Extracting all the <a> tags whose class name is 'result-title' into a list
    # post_titles = soup.findall('a', {'class': 'result-title'})
    # print((post_titles)[0].text)

    final_postings = []
    for post in soup:
        post_title = post.find(class_='result-title').text
        post_url = post.find('a').get('href')

        if post.find(class_='result-price'):
            post_price = post.find(class_='result-price').text
        else:
            post_price = 'N/A'


        if post.find(class_='result-image'.get('data-ids')):
            post_image = post.find(class_='result-image').get('data-ids').split(',')[0].split(':')[1]
            post_image_url = BASE_IMAGE_URL.format(post_image)
        else:
            post_image_url = 'anyimage'



        final_postings.append((post_title, post_url, post_price, post_image_url))

    frontend_stuff = {'search': search,
    'final_postings': final_postings}
    return render(request, 'my_app/new_search.html', frontend_stuff)
