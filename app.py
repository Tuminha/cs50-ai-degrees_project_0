import streamlit as st
import sys
import os
import time

# Add the current directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from degrees import load_data, shortest_path, person_id_for_name, people, movies

st.set_page_config(page_title="Six Degrees of Kevin Bacon", layout="wide")

st.title("🎬 Six Degrees of Kevin Bacon 🎬")

# Use st.context to get headers information
headers = st.context.headers
st.sidebar.write(f"User Agent: {headers.get('User-Agent', 'Unknown')} 🔑")

# Dataset selection
dataset = st.sidebar.selectbox(
    "📂 Choose dataset",
    ("small", "large")
)

# Load data
@st.cache_data
def cached_load_data(dataset):
    load_data(dataset)
    return "Data loaded"

data_load_state = st.text('Loading data... ⏳')
cached_load_data(dataset)
data_load_state.text(f"Data loaded from {dataset} dataset. ✅")

# Input fields for source and target actors
col1, col2 = st.columns(2)
with col1:
    source_name = st.text_input("Enter the name of the first actor: 🎭")
with col2:
    target_name = st.text_input("Enter the name of the second actor: 🎭")

if st.button("🔍 Find Connection"):
    if source_name and target_name:
        source = person_id_for_name(source_name)
        if source is None:
            st.error(f"Person '{source_name}' not found. ❌")
        else:
            target = person_id_for_name(target_name)
            if target is None:
                st.error(f"Person '{target_name}' not found. ❌")
            else:
                with st.spinner('Searching for connection... 🔄'):
                    start_time = time.time()
                    path = shortest_path(source, target)
                    end_time = time.time()
                
                if path is None:
                    st.write("Not connected. 🚫")
                else:
                    degrees = len(path)
                    st.success(f"{degrees} degrees of separation found in {end_time - start_time:.2f} seconds. 🎉")
                    
                    # Use st.expander to show the path
                    with st.expander("View Connection Path 📈"):
                        st.write("FINAL PATH:")
                        for i, (movie_id, person_id) in enumerate(path, 1):
                            person1 = people[source]["name"] if i == 1 else people[path[i-2][1]]["name"]
                            person2 = people[person_id]["name"]
                            movie = movies[movie_id]["title"]
                            st.write(f"{i}: {person1} and {person2} starred in {movie} 🎬")
                    
                    # Bar chart for visualizing the degrees of separation
                    st.bar_chart({
                        "Degrees of Separation": degrees,
                        "Maximum Degrees": 6  # Based on the "Six Degrees" theory
                    }, use_container_width=True)

# Replace the st.feedback section with this:
st.write("How satisfied are you with the search results? 👍👎")
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("👍 Satisfied"):
        st.success("Thank you for your positive feedback!")
with col2:
    if st.button("👎 Not Satisfied"):
        st.error("We're sorry to hear that. We'll work on improving!")
with col3:
    if st.button("😐 Neutral"):
        st.info("Thank you for your feedback!")

# Keep the fun fact and footer as they are
st.info("Did you know? The 'Six Degrees of Kevin Bacon' game was invented by three college students in 1994! 🎓")

# Footer
st.sidebar.markdown("---")
st.sidebar.info("This app uses Streamlit features! 🚀")