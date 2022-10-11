import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pprint as pp
import time
from datetime import datetime
import random

random.seed()
currentTime = datetime.now()
currentTime = currentTime.strftime("%H:%M:%S")

# token authentication API
cid = 'a958949a261f4d14a6be77f6c6083278'
secret = 'd3c477bda0994055a9202d0a6b1636df'

# access demand and limitation
scope = 'playlist-modify-private,playlist-read-private,playlist-modify-public,' \
        'user-read-currently-playing,user-modify-playback-state,user-read-recently-played'
limitQ = 50

# query to spotify API and get userId
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=cid, client_secret=secret,
                                               scope=scope, redirect_uri="http://127.0.0.1:8080/"))
userId = sp.me()["id"]
listening = False

# checking if user is listening (I need to handle when skipping but not playing the song
while not listening:
    if sp.currently_playing() is not None:
        actualProgress = (sp.currently_playing()["progress_ms"])
        time.sleep(1)
        if actualProgress != sp.currently_playing()[
            "progress_ms"]:  # spotify API can return smth but we're not listening to anything
            actualPlaylist = sp.current_user_playing_track()["context"]["uri"]
            if actualPlaylist[:17] != "spotify:playlist:":
                print("You're not listening to a playlist")
                time.sleep(2)
                exit()
            actualPlaylistId = actualPlaylist[17:]
            listening = True
            """for rssDescription in sp.playlist(actualPlaylistId)["description"].split(): # to only convert RSS allowed
                if rssDescription.upper() == "RSS":
                    listening = True
            if listening == False:
                print("You're not listening to a RSS allowed playlist, You need to add 'RSS' in the playlist description")
            """# get information of what playlist listening and Trim:
            actualPlaylistName = sp.playlist(actualPlaylistId)["name"]
            pp.pprint(actualPlaylistName)
        else:
            print("You're not listening to anything right now")
            time.sleep(5)
    else:
        print("You're not listening to anything right now")
        time.sleep(5)

# for the detection of a RSS playlist
playlist = None
namePlaylist = []
possible = False

# create a playlist named RSS test and doesn't if it already on available
author = None
rssPlaylistId = None
multipleRSS = False


def rssPlaylistCheck():
    global possible, author, rssPlaylistId, playlist
    playlist = sp.user_playlists(userId, limit=limitQ)
    for f in range(limitQ):
        name = playlist["items"][f]["name"]
        author = playlist["items"][f]["owner"]["display_name"]
        authorId = playlist["items"][f]["owner"]["id"]
        # pp.pprint("{pl} by {au}".format(pl=name, au=author))
        namePlaylist.append(name)
        if name.upper()[:3] == "RSS" and authorId == userId:
            print(name.upper()[:7] == "RSS RSS")
            if name.upper()[:7] == "RSS RSS":
                multipleRSS = True
            print("found a playlist compatible")
            rssPlaylistId = playlist["items"][f]["id"]
            possible = True
            break


rssPlaylistCheck()

if not possible:
    sp.user_playlist_create(userId, f"RSS {actualPlaylistName}")
    print("RSS playlist compatible playlist created")
    rssPlaylistCheck()

print(rssPlaylistId)

#get recently played track
recentlyTrack = []
recently = sp.current_user_recently_played()["items"]

for f in range(50):
    recentlyTrack.append(recently[f]["track"]["id"])


# checking and storing if a playlist have changed NEED TO HANDLE IF SOMEONE RSS THE SAME BUT DON'T WANT THE SAME TRACK
snapshotId = sp.playlist(actualPlaylistId)["snapshot_id"]

# handle if not existent
try:
    with open("snapshotId.txt", "r") as readSnap:
        prevSnap = readSnap.read()
except FileNotFoundError:
    with open("snapshotId.txt", "w") as createSnap:
        createSnap.write("")
    with open("snapshotId.txt", "r") as readSnap:
        prevSnap = readSnap.read()

if snapshotId != prevSnap:
    with open("snapshotId.txt", "w") as snap:
        snap.write(snapshotId)
    print("changed Snapshot ID")
    with open("tracklist.txt", "w") as tl:
        # to get every id in the playlist and shuffling
        x = 1
        offset = 0
        enum = 0
        tracklist = sp.playlist_tracks(actualPlaylistId, offset=offset)
        trackIdOrder = []

        for enum in range(tracklist["total"]):
            if enum == x * 100:
                offset = enum
                tracklist = sp.playlist_tracks(actualPlaylistId, offset=offset)
                x += 1
            tracklistAccess = tracklist["items"]  # Spport des PODCASTS !!!
            trackid = tracklistAccess[enum - offset]["track"]["id"]
            trackIdOrder.append(trackid)
        tl.write(str(trackIdOrder))
    print("whole tracklist saved")
    enum = len(trackIdOrder)
    for recentlyEach in recentlyTrack:
        if recentlyEach in trackIdOrder:
            trackIdOrder.remove(recentlyEach)
    print(enum)
    enum = len(trackIdOrder)
    print(enum)
    newOrder = random.sample(trackIdOrder, enum)  # shuffled songs
    print("Playlist Shuffled")
else:
    print("playlist unchanged, basing the shuffle on precedent tracklist")
    with open("tracklist.txt", "r") as clean:
        content = clean.read()
        content = content.strip("[]").split("',")
        new = []
        for f in content:
            f = f.strip("' ")
            new.append(f)
        trackIdOrder = new
        print("whole tracklist saved")
        enum = len(trackIdOrder)
        for recentlyEach in recentlyTrack:
            if recentlyEach in trackIdOrder:
                trackIdOrder.remove(recentlyEach)
        print(enum)
        enum = len(trackIdOrder)
        print(enum)

        newOrder = random.sample(trackIdOrder, enum)  # shuffled songs
        print("Playlist Shuffled")

# adding songs in the RSS playlist
playlistTag = rssPlaylistId
if multipleRSS == True:
    rssName = f"{actualPlaylistName}"
else:
    rssName = f"RSS {actualPlaylistName}"
    print(rssName)
sp.playlist_change_details(playlistTag, description=f"generated at {currentTime} UTC+1 from {actualPlaylistName}",
                           name=rssName)  # add responsive timezone
sp.playlist_replace_items(playlistTag, newOrder[:100])
