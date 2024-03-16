import math
from .models import Post
from django.core.mail import send_mail
import os



def calculate_cosine_similarity(user_preference, post_descriptions,posts_pks):
    
    def tokenize(text):
        return text.lower().split()

    user_tokens = tokenize(user_preference)
    post_tokens_list = [tokenize(description) for description in post_descriptions]

    # Create a vocabulary of unique terms
    vocabulary = set(user_tokens)
    for tokens in post_tokens_list:
        vocabulary.update(tokens)


    # Calculate the Term Frequency (TF) for user preference
    user_tf = {term: user_tokens.count(term) / len(user_tokens) for term in vocabulary}

    # Calculate the Inverse Document Frequency (IDF) for each term
    num_documents = len(post_descriptions)
    user_idf = {term: math.log(1 + num_documents / (1 + sum(1 for tokens in post_tokens_list if term in tokens))) for term in vocabulary}

    # Calculate the TF-IDF vector for user preference
    user_tfidf_vector = [user_tf[term] * user_idf[term] for term in vocabulary]
    
    # Calculate the TF-IDF vectors for post descriptions
    post_tfidf_vectors = []
    for post_tokens in post_tokens_list:
        post_tf = {term: post_tokens.count(term) / len(post_tokens) for term in vocabulary}
        post_tfidf_vector = [post_tf[term] * user_idf[term] for term in vocabulary]
        post_tfidf_vectors.append(post_tfidf_vector)
    
    def cosine_similarity(vector1, vector2):
        dot_product = sum(a * b for a, b in zip(vector1, vector2))
        magnitude1 = math.sqrt(sum(a * a for a in vector1))
        magnitude2 = math.sqrt(sum(b * b for b in vector2))
        if magnitude1 == 0 or magnitude2 == 0:
            return 0  # Avoid division by zero
        return dot_product / (magnitude1 * magnitude2)


    # Calculate the cosine similarity between user preference and post descriptions
    similarities = [cosine_similarity(user_tfidf_vector, post_vector) for post_vector in post_tfidf_vectors]

    # Create a list of tuples with primary keys and similarity scores
    post_similarity_pairs = list(zip(posts_pks, similarities))

    # Sort the pairs based on similarity in descending order
    post_similarity_pairs.sort(key=lambda x: x[1], reverse=True)
    
    # Extract the sorted post primary keys
    sorted_post_primary_keys = [pk for pk, _ in post_similarity_pairs]

    print('\n Sorted pks')
    print(sorted_post_primary_keys)
    return sorted_post_primary_keys




def haversine(lat1,lon1,lat2,lon2):
    R = 6371 #radius of earth in km

    # distance between latitudes
    # and longitudes
    dLat = (lat2 - lat1) * math.pi / 180.0
    dLon = (lon2 - lon1) * math.pi / 180.0
 
    # convert to radians
    lat1 = (lat1) * math.pi / 180.0
    lat2 = (lat2) * math.pi / 180.0
 
    # apply formulae
    a = (pow(math.sin(dLat / 2), 2) + pow(math.sin(dLon / 2), 2) * math.cos(lat1) * math.cos(lat2))
    
    c = 2 * math.asin(math.sqrt(a))

    distance = R * c
    return distance

def find_nearest_dest(source_lat, source_lon):
    all_posts = Post.objects.all()
    nearest_destinations = []
    
    for post in all_posts:
        post_lat, post_lon = post.latitude,post.longitude
        print(post_lat)
        print(post_lon)
        distance = haversine(source_lat,source_lon,post_lat,post_lon)
        if distance <10:
            nearest_destinations.append({'post':post, 'distance':distance})
        # elif distance<10:
        #     nearest_destinations.append({'post':post, 'distance':distance})
    
    if len(nearest_destinations)>1:
        nearest_destinations.sort(key= lambda x :x[distance])

    return nearest_destinations

    
def send_mail_to_admin(post):
    subject = 'Report Count Exceeded for Room Post'
    message = f'The room post (ID:{post.pk}) has received 10 or more reports. Please review'
    from_email = os.environ.get('EMAIL_FROM')
    admin_email = os.environ.get('EMAIL_USER')

    send_mail(subject,message,from_email,[admin_email])


    