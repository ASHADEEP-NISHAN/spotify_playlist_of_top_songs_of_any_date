from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os

SPOTIFY_CLIENT_ID=os.environ.get("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET=os.environ.get("SPOTIFY_CLIENT_SECRET")
REDIRECT_URI=os.environ.get("REDIRECT_URI")
SPOTIFY_DISPLAY_NAME=os.environ.get("SPOTIFY_DISPLAY_NAME")

# Scraping Billboard 100
date_input=input("which year you want to travel to? type date in this format yyyy-mm-dd:")
response=requests.get(url=f"https://www.billboard.com/charts/hot-100/{date_input}/")
billboard_website=response.text
soup=BeautifulSoup(billboard_website,"html.parser")
song_names=soup.select("li ul li h3")
song_list=[song.getText().strip() for song in song_names]
print(song_list)

#Spotify Authentication

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIFY_CLIENT_ID,
                                               client_secret=SPOTIFY_CLIENT_SECRET,
                                               redirect_uri=REDIRECT_URI,
                                               scope="playlist-modify-private",
                                               show_dialog=True,
                                               cache_path="token.txt",
                                               username=SPOTIFY_DISPLAY_NAME))

user_id= sp.current_user()["id"]
# print(user_id)

#Searching Spotify for songs by title
year = date_input.split("-")[0]
song_uri=[]
for song in song_list:
    result=sp.search(f"track: {song} year: {year}",type="track")
    try:
        uri=result['tracks']['items'][0]['uri']
        song_uri.append(uri)
    except IndexError:
        print(f"{song} is not available in spotify.Skipped")
# print(song_uri)

#Creating a new private playlist in Spotify
playlist=sp.user_playlist_create(name=f"{date_input} Billboard 100",public=False,user=user_id)
# print(playlist)

#Adding song to playlist
sp.playlist_add_items(playlist_id=playlist["id"],items=song_uri)