from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.db import IntegrityError
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from .forms import *
from django.conf import settings
from django.contrib.auth.decorators import login_required
from bs4 import BeautifulSoup
import requests
from django.core.paginator import Paginator, EmptyPage
import requests
from bs4 import BeautifulSoup
from django.shortcuts import render
import unicodedata
from .models import Recette,Ingredient
from rest_framework.decorators import api_view


def recette_detail(request, recette_id):
    recette = get_object_or_404(Recette, pk=recette_id)
    context = {'recette': recette}
    return render(request, 'recette_detail.html', context=context)

def get_recettes(page):
    src = page.content
    soup = BeautifulSoup(src, "lxml")

    recettes_title = soup.find_all("h3")
    recettes_title = recettes_title[1:]
    recettes_desc = soup.find_all("p")
    recettes_imgs = soup.find_all("img", {"decoding": "async"})
    
    # Use the hyphenate_text_list function to convert recettes_t to a list of URLs
    recettes_url = hyphenate_text_list([title.text for title in recettes_title])

    for i in range(len(recettes_title)):
        title = recettes_title[i].text
        # Check if a Recette object with the same title already exists in the database
        if Recette.objects.filter(title=title).exists():
            continue
        
        # Scrape recipe details
        page1 = requests.get(f"https://www.recettescooking.com/recettes/{recettes_url[i]}/")
        src = page1.content
        soup1 = BeautifulSoup(src, "lxml")
        recette_tit = soup1.find_all("div", {"class": "instructions"})
        recette_li = soup1.find_all("ol")
        recette_des_text = [li.text for li in recette_li]
        
        recette = Recette(
            title=title,
            description=recettes_desc[i].text,
            image_url=recettes_imgs[i].get("src"),
            text_desc=" ".join(recette_des_text)
        )
        recette.save()


def hyphenate_text_list(text_list):
    hyphenated_list = []
    for text in text_list:
        # remove accents
        text = ''.join(c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn')
        # replace spaces with hyphens
        hyphenated_text = '-'.join(text.split())
        hyphenated_list.append(hyphenated_text)
    return hyphenated_list

 

page = requests.get("https://www.recettescooking.com/")
get_recettes(page)





def recettes_view(request):
    recettes = Recette.objects.all()

    per_page = 6

    paginator = Paginator(recettes, per_page)

    page_number = request.GET.get('page')

    try:
        page = paginator.get_page(page_number)
    except EmptyPage:
        page = paginator.get_page(paginator.num_pages)

    context = {
        'recettes': page,
    }

    return render(request, 'index.html', context)


# Create your views here.
class MyPasswordResetView(PasswordResetView):
    template_name = 'password_reset_form.html'
    email_template_name = 'password_reset_email.html'
    success_url = reverse_lazy('password_reset_done')
    
    
class MyPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'password_reset_done.html'
    
class MyPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'password_reset_confirm.html'
    success_url = reverse_lazy('login')
    
class MyPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'password_reset_complete.html'


def logOut(request):
    logout(request)
    return redirect('login')


def signUp(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        passwordConf = request.POST.get('passwordConf')
        if password != passwordConf:
            messages.error(request, 'Passwords do not match.')
        elif username == '' or email == '' or password == '' or passwordConf == '':
            messages.error(request, 'Enter all informations.')
        else:
            try:
                myUser = User.objects.create_user(username,email,password)
                myUser.save()
                return redirect('login')
            except IntegrityError:
                messages.error(request, 'This username is already taken. Please choose a different username.')
    return render(request,'signup.html')

def logIn(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        pass1 = request.POST.get('pass')
        user = authenticate(request,username=username,password=pass1)
        if user is not None:
            login(request,user)
            if user.is_superuser:
                return redirect('dashboard')
            else : 
                return redirect('index')
        else:
            messages.error(request, "Invalid username or password.")
    return render(request,'login.html')

def Index(request):
    #context = recettes_view(request)
    #return render(request,'index.html', context)
    return recettes_view(request)
    
def aboutUs(request):
    return render(request,'about.html')

def userAccount(request):
    return render(request, 'user_account.html')



@login_required
def user_profile(request):
    user = request.user
    return render(request, 'user_account.html', {'user': user})


def search_recipes(request):
    query = request.GET.get('keyword')
    if query:
        #recipes = Recette.objects.filter(title__contains=query).distinct()
        recipes = Recette.objects.filter(title__icontains=query).distinct()
    else:
        recipes = Recette.objects.none()

    paginator = Paginator(recipes, 9)  # Modifier le nombre d'éléments par page selon vos besoins
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'recettes': page_obj,
        'keyword': query,
    }

    return render(request, 'index.html', context)

from .models import Commentaire

@login_required
def ajouter_commentaire(request):
    if request.method == 'POST':
        opinion = request.POST.get('opinion')  
        utilisateur = request.user  
        recette_id = request.POST.get('recette_id') 

        try:
            recette = Recette.objects.get(id=recette_id)
        except Recette.DoesNotExist:
            pass

        if opinion:
            commentaire = Commentaire(texte=opinion, utilisateur=utilisateur, recette=recette)
            commentaire.save()
            messages.success(request, "opinion add successfuly.")    
        else:
            messages.warning(request, "Please enter your opinion.")   
        return redirect('index')  

    return render(request, 'index.html') 

from .models import Ranking

def ajouter_rank(request, recette_id):
    recette = get_object_or_404(Recette, pk=recette_id)

    if request.method == 'POST':
        rank = request.POST.get('rank')
        if rank and rank.isdigit():  
            user = request.user
            ranking = Ranking.objects.create(user=user, recette=recette, rank=rank)
            ranking.save()
            messages.success(request, "rank add successfuly.")
            return redirect('index')
        else:
            messages.warning(request, "Please enter your rank.")
            #HttpResponseBadRequest("Le champ de note est invalide.")
            return redirect('index')
            
    
    context = {'recette': recette}
    return render(request, 'index.html', context)



def commentaires(request):
    commentaires = Commentaire.objects.all()
    context = {'commentaires': commentaires}
    return render(request, 'commentaires.html', context)



def recette_detail(request, recette_id):
    recette = get_object_or_404(Recette, pk=recette_id)
    commentaires = Commentaire.objects.filter(recette=recette)
    context = {'recette': recette, 'commentaires': commentaires}
    return render(request, 'recette_detail.html', context)



def administration(request):
    data = Recette.objects.all()
    return render(request,'administration.html',{'recettes' : data}) 


def add_recipe_view(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        image = request.POST.get('image')
        ingredients = request.POST.get('ingredients')

        # Create a new instance of YourRecetteModel and save it to the database
        Recette.objects.create(
            title=title,
            description=description,
            image_url=image,
            text_desc=ingredients
        )
        messages.success(request, "recipe add successfuly.")
        return redirect('administration')  # Redirect to the view that displays the list of recipes

    return render(request, 'administration.html')


def add_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        issuperuser = request.POST.get('superuser')

        User.objects.create(
            username = username,
            email = email,
            password = password,
            is_superuser = issuperuser
        )
        messages.success(request, "user add successfuly.")
        return redirect('users')
    return render(request, 'users.html')


def deleteRecipe(request,pk):
    recette = Recette.objects.get(pk=pk)
    recette.delete()
    messages.success(request, "recipe deleted successfuly.")
    return redirect('administration')

def updateRecipe(request, pk):
    recipe = get_object_or_404(Recette, pk=pk)

    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        image_url = request.POST.get('image')
        text_desc = request.POST.get('ingredients')

        # Update the fields of the existing recipe
        recipe.title = title
        recipe.description = description
        recipe.image_url = image_url
        recipe.text_desc = text_desc
        recipe.save()
        messages.success(request, "recipe updated successfuly.")
        return redirect('administration')  # Redirect to the view that displays the list of recipes
    else:
        return render(request, 'updateRecette.html', {'recipe': recipe})


def dashboard(request):
    recette_count = Recette.objects.count()
    commentaire_count = Commentaire.objects.count()
    ranking_count = Ranking.objects.count()
    user_count = User.objects.count()
    return render(request, 'dashboard.html', {
        'recette_count': recette_count,
        'commentaire_count': commentaire_count,
        'ranking_count': ranking_count,
        'user_count' : user_count
    })


def users(request):
    data = User.objects.all()
    return render(request,'users.html',{'users' : data}) 

def deleteUser(request,pk):
    user = User.objects.get(pk=pk)
    user.delete()
    messages.success(request, "user deleted successfuly.")
    return redirect('users')

def updateUser(request, pk):
    user = get_object_or_404(User, pk=pk)

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        issuperuser = request.POST.get('superuser')

        # Update the fields of the existing recipe
        user.username = username
        user.email = email
        user.password = password
        user.is_superuser = issuperuser
        user.save()
        messages.success(request, "user updated successfuly.")
        return redirect('users')  # Redirect to the view that displays the list of recipes
    else:
        return render(request, 'updateUser.html', {'user': user})