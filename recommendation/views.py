from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import UserRegistrationForm
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle

from django.shortcuts import render
from .models import Movie  # Assuming you have a Movie model or you are fetching data from another source


def user_dashboard(request):
    suggestions = get_suggestions()  # Replace with actual logic to get suggestions
    return render(request, 'userDashboard.html', {'suggestions': suggestions})


# Load ML models
def load_models():
    clf = pickle.load(open('nlp_model.pkl', 'rb'))
    vectorizer = pickle.load(open('tranform.pkl', 'rb'))
    return clf, vectorizer


clf, vectorizer = load_models()


# Create similarity matrix
def create_similarity():
    data = pd.read_csv('main_data.csv')
    cv = CountVectorizer()
    count_matrix = cv.fit_transform(data['comb'])
    similarity = cosine_similarity(count_matrix)
    return data, similarity

# Movie recommendation logic
def rcmd(movie_name):
    movie_name = movie_name.lower()
    try:
        data.head()
        similarity.shape
    except:
        data, similarity = create_similarity()
    if movie_name not in data['movie_title'].unique():
        return 'Sorry! Try another movie name.'
    else:
        i = data.loc[data['movie_title'] == movie_name].index[0]
        lst = list(enumerate(similarity[i]))
        lst = sorted(lst, key=lambda x: x[1], reverse=True)
        lst = lst[1:11]  # Exclude the requested movie itself
        recommendations = [data['movie_title'][item[0]] for item in lst]
        return recommendations

# Convert string to list
def convert_to_list(my_list):
    my_list = my_list.split('","')
    my_list[0] = my_list[0].replace('["', '')
    my_list[-1] = my_list[-1].replace('"]', '')
    return my_list

# Get movie suggestions
def get_suggestions():
    data = pd.read_csv('main_data.csv')
    return list(data['movie_title'].str.capitalize())



def landing_page(request):
    suggestions = get_suggestions()
    return render(request, 'index.html', {'suggestions': suggestions})

def similarity_view(request):
    if request.method == "POST":
        movie = request.POST.get('name')
        recommendations = rcmd(movie)
        if isinstance(recommendations, str):
            return JsonResponse({'error': recommendations})
        else:
            return JsonResponse({'similarity': recommendations})

def user_dashboard(request):
    return render(request, 'userDashboard.html')

# Authentication views
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f"Account created for {user.username}!")
            login(request, user)
            return redirect('user_dashboard')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome to Evoflicks, {user.username}!")
            return redirect('user_dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect('login')
