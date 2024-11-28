import streamlit as st
from yt_dlp import YoutubeDL
import requests
from PIL import Image
from io import BytesIO
import os
import subprocess
import sys

# Ensure dependencies are installed
REQUIRED_PACKAGES = [
    "streamlit",
    "yt-dlp",
    "pillow",
    "requests"
]

for package in REQUIRED_PACKAGES:
    try:
        __import__(package)
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])


# Set page configuration with custom theme
st.set_page_config(
    page_title="🎵 Rasa by ServerSync", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# Apply the theme configuration
st.markdown(
    """
    <style>
    body {
        background-color: #0a0a0a;
        color: #b7ec95;
        font-family: 'monospace';
    }

    .sidebar .sidebar-content {
        background-color: #3c3e50;
    }

    .main-title {
        font-family: 'Raleway', sans-serif;
        font-size: 52px;
        font-weight: 700;
        text-align: center;
        color: #b7ec95;
        margin-top: 30px;
        letter-spacing: 2px;
    }

    .subtitle {
        font-family: 'Roboto Mono', monospace;
        font-size: 22px;
        font-weight: 400;
        text-align: center;
        color: #b7ec95;
        margin-bottom: 40px;
        letter-spacing: 1px;
    }

    /* Centered footer at the bottom */
    .bottom-center-section {
        font-family: 'Roboto Mono', monospace;
        font-size: 14px;
        color: #b7ec95;
        position: fixed;
        bottom: 10px;
        left: 50%;
        transform: translateX(-50%);
        text-align: center;
        z-index: 999;
    }

    .bottom-center-section a {
        color: #b7ec95;
        text-decoration: none;
    }

    .bottom-center-section a:hover {
        text-decoration: underline;
    }

    .bottom-center-section .social-icons {
        display: flex;
        justify-content: center;
        gap: 10px;
        font-size: 18px;
    }

    .bottom-center-section .social-icons a {
        color: #b7ec95;
        text-decoration: none;
    }

    .bottom-center-section .social-icons a:hover {
        color: #fff;
    }

    .song-card {
        background-color: #1c1c1c;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }

    .play-button {
        background-color: #1DB954;
        color: white;
        padding: 10px;
        border: none;
        border-radius: 5px;
        cursor: pointer;
        width: 100%;
        text-align: center;
        font-size: 18px;
    }
    </style>
    """, 
    unsafe_allow_html=True
)

# Function to search for songs using yt-dlp with caching
@st.cache_data(show_spinner=False)
def search_songs(query):
    try:
        ydl_opts = {
            'format': 'bestaudio/best',
            'noplaylist': True,
            'quiet': True,
            'default_search': 'ytsearch10',  # Fetch top 10 matching results
        }
        with YoutubeDL(ydl_opts) as ydl:
            results = ydl.extract_info(query, download=False)
            if 'entries' in results:
                return [
                    {
                        'title': entry.get('title', 'Unknown Title'),
                        'url': entry.get('url'),
                        'thumbnail': entry.get('thumbnail'),
                        'webpage_url': entry.get('webpage_url'),
                        'duration': entry.get('duration', 0)
                    }
                    for entry in results['entries'] if entry
                ]
            else:
                return []  # No results found
    except Exception as e:
        st.error(f"An error occurred while fetching results: {str(e)}")
        return []


# Function to format duration (seconds to MM:SS)
def format_duration(duration):
    mins, secs = divmod(duration, 60)
    return f"{mins}:{secs:02d}"


# Add the main title and subtitle of the app
st.markdown(
    """
    <div class="main-title">𝓡𝓪𝓼𝓪</div>
    <div class="subtitle">by ServerSync</div>
    """,
    unsafe_allow_html=True
)

# Input field for song name
song_query = st.text_input("Start typing the song name:")

# Show suggestions and allow the user to select and play songs
if song_query:
    with st.spinner("Fetching suggestions..."):
        song_suggestions = search_songs(song_query)

    if song_suggestions:
        suggestion_titles = [song['title'] for song in song_suggestions]
        selected_song_title = st.selectbox("Select a song from the suggestions:", suggestion_titles)

        # Display selected song details
        selected_song = next(song for song in song_suggestions if song['title'] == selected_song_title)

        st.markdown("### Selected Song")
        col1, col2 = st.columns([1, 3])

        # Display thumbnail in the first column
        with col1:
            if selected_song['thumbnail']:
                try:
                    response = requests.get(selected_song['thumbnail'])
                    if response.status_code == 200:
                        image = Image.open(BytesIO(response.content))
                        st.image(image, use_column_width=True)
                    else:
                        st.warning("Thumbnail not available.")
                except Exception:
                    st.warning("Error loading thumbnail.")
            else:
                st.warning("Thumbnail not available.")

        # Display song details in the second column
        with col2:
            st.markdown(f"**Title:** {selected_song['title']}")
            st.markdown(f"**Duration:** {format_duration(selected_song['duration'])}")
            st.markdown(f"[Watch on YouTube]({selected_song['webpage_url']})")

        # Play the selected song
        audio_url = selected_song.get('url')
        if audio_url:
            if st.button("🎵 Play Selected Song"):
                st.audio(audio_url, format="audio/mp3")
        else:
            st.warning("Audio URL not available.")
    else:
        st.warning("No suggestions available. Please refine your search.")
else:
    st.info("Start typing to see song suggestions...")

# Bottom center section with social media links
st.markdown(
    """
    <div class="bottom-center-section">
        <div><strong>Made by Aditya Kumar Jha</strong></div>
        <div class="social-icons">
            <a href="https://www.instagram.com/aditya_kr_jha_29/" target="_blank">Instagram</a>
            <a href="https://in.linkedin.com/in/aditya-kumar-jha-b0b669252" target="_blank">LinkedIn</a>
        </div>
    </div>
    """, 
    unsafe_allow_html=True
)
