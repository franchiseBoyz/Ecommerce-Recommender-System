from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from .models import Product

# Load data from the database once, if your dataset is not huge
products = Product.objects.all()
df = pd.DataFrame(list(products.values(
    'category_1', 'category_2', 'category_3', 'title', 
    'product_rating', 'selling_price', 'mrp', 'seller_name', 
    'seller_rating', 'price_ratio', 'price_difference'
)))
df['combined_feature'] = df['category_2'].astype(str) + ' ' + df['title'].astype(str)

# Initialize TF-IDF vectorizer and fit it on the dataset
tfidf_vectorizer = TfidfVectorizer(stop_words='english')
tfidf_matrix_content = tfidf_vectorizer.fit_transform(df['title'])
cosine_similarities_content = cosine_similarity(tfidf_matrix_content, tfidf_matrix_content)

def get_recommendations(df, item_name, top_n=10):
    if item_name not in df['title'].values:
        return pd.DataFrame()  # Return an empty DataFrame if the item is not found

    item_index = df[df['title'] == item_name].index[0]
    similar_items = list(enumerate(cosine_similarities_content[item_index]))
    similar_items = sorted(similar_items, key=lambda x: x[1], reverse=True)
    top_similar_items = similar_items[1:top_n+1]
    recommended_item_indices = [x[0] for x in top_similar_items]
    return df.iloc[recommended_item_indices][['title', 'product_rating', 'selling_price']]

def search_view(request):
    item_name = request.GET.get('q', '').strip()
    if not item_name:
        return HttpResponse("No search query provided", status=400)

    recommendations = get_recommendations(df, item_name)
    if recommendations.empty:
        return HttpResponse("No recommendations found", status=404)
    
    return render(request, 'products/recommendations.html', {'recommendations': recommendations})

def home(request):
    top_rated_products = Product.objects.order_by('-product_rating')[:12]
    return render(request, 'products/home.html', {'top_rated_products': top_rated_products})

