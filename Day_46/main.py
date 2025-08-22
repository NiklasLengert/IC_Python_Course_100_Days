from bs4 import BeautifulSoup
import requests
import os
import spotipy
import spotipy.oauth2 as oauth2

# input_year = input("Enter a date in YYYY-MM-DD format from which we show the top 100 songs: ")
input_year = "2023-10-01"
URL = f"https://www.billboard.com/charts/hot-100/{input_year}/"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}

response = requests.get(URL, headers=headers)
response.raise_for_status()
soup = BeautifulSoup(response.text, "html.parser")
songs = []

tag_list = soup.select(selector="li h3")
for tag in tag_list:
    if tag["id"] == "title-of-a-story":
        s_name = tag.getText()
        songs.append(s_name.replace("\n", "").replace("\t", ""))
print(songs)


# Spotify API setup
CLIENT_ID = ""
CLIENT_SECRET = ""
REDIRECT_URI = "https://example.com"
USERNAME = "Niklas Lengert"

scope = "playlist-modify-private"
sp = spotipy.Spotify(auth_manager=oauth2.SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope=scope,
    show_dialog=True,
    cache_path="token.txt"
))

user_id = sp.current_user()["id"]

song_uris = []
year = input_year.split("-")[0]
for song in songs:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

playlist = sp.user_playlist_create(
    user=user_id,
    name=f"Top 100 Songs from {input_year}",
    public=False,
    description=f"Top 100 songs from Billboard Hot 100 on {input_year}"
)

sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)
print(f"Added {len(song_uris)} songs to the playlist: {playlist['name']}")
