import streamlit as st
import requests,os
from dotenv import load_dotenv

load_dotenv()

API_URL = os.getenv("app_url")

st.set_page_config(
    page_title="Movie Recommender",
    page_icon="🎬",
    layout="wide"
)

st.title("🎬 Movie Recommender")
st.markdown("*Powered by Neo4j Knowledge Graph*")

# ---- Search Box ----
search_query = st.text_input("Search for a movie", placeholder="e.g. Inception, Avatar...")

movie_selected = None

if search_query:
    try:
        res = requests.get(f"{API_URL}/movies/search", params={"q": search_query})
        suggestions = res.json().get("results", [])

        if suggestions:
            movie_selected = st.selectbox("Select a movie", suggestions)
        else:
            st.warning("No movies found. Try a different name.")
    except Exception as e:
        st.error(f"Could not connect to API: {e}")

# ---- Recommendations ----
if movie_selected:
    st.markdown(f"### Recommendations for **{movie_selected}**")

    tab1, tab2, tab3, tab4 = st.tabs([
        "⭐ Combined", "🎭 By Genre", "🎬 By Director", "🏢 By Company"
    ])

    def show_recommendations(recs):
        for i, rec in enumerate(recs, 1):
            st.write(f"**{i}.** {rec['title']}")
            st.divider()

    # ---- Combined ----
    with tab1:
        try:
            res = requests.get(f"{API_URL}/recommend", params={"movie": movie_selected, "limit": 10})
            if res.status_code == 404:
                st.warning("No recommendations found.")
            else:
                show_recommendations(res.json()["recommendations"])
        except Exception as e:
            st.error(f"Error: {e}")

    # ---- Genre ----
    with tab2:
        try:
            res = requests.get(f"{API_URL}/recommend/genre", params={"movie": movie_selected, "limit": 10})
            if res.status_code == 404:
                st.warning("No recommendations found.")
            else:
                show_recommendations(res.json()["recommendations"])
        except Exception as e:
            st.error(f"Error: {e}")

    # ---- Director ----
    with tab3:
        try:
            res = requests.get(f"{API_URL}/recommend/director", params={"movie": movie_selected, "limit": 10})
            if res.status_code == 404:
                st.warning("No recommendations found.")
            else:
                show_recommendations(res.json()["recommendations"])
        except Exception as e:
            st.error(f"Error: {e}")

    # ---- Company ----
    with tab4:
        try:
            res = requests.get(f"{API_URL}/recommend/company", params={"movie": movie_selected, "limit": 10})
            if res.status_code == 404:
                st.warning("No recommendations found.")
            else:
                show_recommendations(res.json()["recommendations"])
        except Exception as e:
            st.error(f"Error: {e}")