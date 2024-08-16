import pickle
import streamlit as st
import requests

# Function to get anime poster using Jikan API
def get_anime_poster(anime_id):
    url = f"https://api.jikan.moe/v4/anime/{anime_id}"

    response = requests.get(url)

    if response.status_code == 200:
        anime_data = response.json()
        if 'data' in anime_data and 'images' in anime_data['data']:
            return anime_data['data']['images']['jpg']['large_image_url']
        else:
            print("Poster image not found in the API response.")
            return None
    else:
        print("Failed to retrieve anime details from API. Status code:", response.status_code)
        return None

def recommend(anime):
    index = animes[animes['name'] == anime].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_anime_names = []
    recommended_anime_posters = []
    for i in distances[1:9]:  # Get top 8 recommendations
        anime_id = animes.iloc[i[0]].anime_id
        poster_url = get_anime_poster(anime_id)
        if poster_url:
            recommended_anime_posters.append(poster_url)
        else:
            recommended_anime_posters.append("https://via.placeholder.com/150")  # Placeholder image URL
        recommended_anime_names.append(animes.iloc[i[0]]['name'])

    return recommended_anime_names, recommended_anime_posters

# Streamlit app
st.header('Anime Recommender System')
animes = pickle.load(open('anime_list.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

anime_list = animes['name'].values
selected_anime = st.selectbox(
    "Type or select an anime from the dropdown",
    anime_list
)

if st.button('Show Recommendation'):
    recommended_anime_names, recommended_anime_posters = recommend(selected_anime)
    
    # Ensure we don't exceed the number of available recommendations
    num_recommendations = min(len(recommended_anime_names), 9)
    
    for i in range(num_recommendations):
        st.text(recommended_anime_names[i])
        st.image(recommended_anime_posters[i])
