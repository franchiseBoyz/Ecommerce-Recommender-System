from django.shortcuts import render
from .models import Product
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

def create_recommendation_model():
    products = Product.objects.all()
    df = pd.DataFrame(list(products.values(
        'category_1', 'category_2', 'category_3', 'title', 'product_rating', 
        'selling_price', 'mrp', 'seller_name', 'seller_rating', 
        'price_ratio', 'price_difference', 'product_id'
    )))
    
    df['combined_features'] = (
        df['category_1'] + " " + df['category_2'] + " " + 
        df['category_3'] + " " + df['title']
    )
    
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(df['combined_features'])
    
    cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)
    
    return df, cosine_sim

def recommend_products(query):
    df, cosine_sim = create_recommendation_model()
    
    # Preprocess query
    query = query.lower()
    query_index = df[df['title'].str.contains(query, case=False, na=False)].index.tolist()
    
    if not query_index:
        return pd.DataFrame()
    
    query_index = query_index[0]
    sim_scores = list(enumerate(cosine_sim[query_index]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    
    # Get top 10 recommendations
    sim_scores = sim_scores[1:11]
    product_indices = [i[0] for i in sim_scores]
    
    recommended_products = df.iloc[product_indices]
    return recommended_products[['title', 'product_rating']]

def search_view(request):
    query = request.GET.get('q', '')
    recommendations = recommend_products(query)
    return render(request, 'products/search_results.html', {'recommendations': recommendations})

def home(request):
    return render(request, 'products/home.html')  # Adjust the template path as needed
