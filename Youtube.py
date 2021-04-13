import googleapiclient.discovery
import googleapiclient.errors
import google.auth.exceptions
import google.oauth2.credentials
import google_auth_oauthlib.flow
from google.auth.transport.requests import Request
import csv
import pickle
import os.path


def get_user_authorization(valid_google_authorization_flow):
    """Process the google flow credentials, multi step with error checking"""

    #check if the authorization file exists
    #otherwise prompt the user
    if not os.path.isfile('token.pickle'):
        creds = valid_google_authorization_flow.run_console()
        with open('token.pickle', 'wb') as new_file:
            pickle.dump(creds, new_file)
    else:
        with open('token.pickle','rb') as f:
            creds = pickle.load(f)
            #check if the credentials are valid

            # verify that the token hasnt expired
            # otherwise prompt google for refresh
            if creds.expired:
                request = google.auth.transport.requests.Request()
                creds.refresh(request)
    return creds

def get_playlist_songs(youtube_response, videoID_list, nextPage):
    """Function to check grab video ID's from playlist


    Key Arguments.
    youtube_response: Here  the user is expected to pass the previous athorized youtube object to run the function

    videoID_list---Need to have an object to store the video ID's from youtube

    nextPage---Built this in for recursive calls, since youtube limits the length of requests, if there is another page
    music definately need to keep that in mind.
    """
    playlist_video_request = youtube.playlistItems().list(
        part="snippet",
        playlistId=youtube_response['items'][0]['id']['playlistId'],
        maxResults=50,
      pageToken = nextPage
    )
    playlist_videos = playlist_video_request.execute()

    for playlist_index in range(len(playlist_videos['items'])):
        videoID_list.append(
            ['youtube#video', playlist_videos['items'][playlist_index]['snippet']['resourceId']['videoId']])
    if 'nextPageToken' in playlist_videos.keys():
        get_playlist_songs(playlist_videos,video_ID,playlist_videos['nextPageToken'])
    return

#everything you need to start search
rap_list = 'tp_rap_list.csv'
API_KEY = '' #gotta build a key to
JSON = '' #google needs a way to check who you are
RAP_PLAYLIST = '' #the playlist ID for google to place the music in
songs = []
video_ID = []
with open(rap_list) as file:
    reader = csv.reader(file)
    for items in reader:
        songs += items


scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]
api_service_name = "youtube"

# Get credentials and create an API client
api_version = "v3"

flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(JSON, scopes)
credentials = get_user_authorization(flow)

#Let google know what service you want to make, what version, and the credentials to run this code
youtube = googleapiclient.discovery.build(api_service_name, api_version, credentials=credentials)

#lets process the videos to search
for items in range(103, 110):
    try:
        request = youtube.search().list(
                part="snippet",
                maxResults=5,
                q=songs[items]
            )
        response = request.execute()
        #check if the song is an album(i.e in a playlist)
        # if so run a function to extract the individual videos
        # and add to the personal list
        if response['items'][0]['id']['kind'] == 'youtube#playlist':
            get_playlist_songs(response,video_ID,nextPage="")
        else:
            video_ID.append(['youtube#video',response['items'][0]['id']['videoId']])
    except KeyError:
        print(format(KeyError))

#Now process the video ID list that we just created by loading it all into the playlist album
for items in range(len(video_ID)):
    request = youtube.playlistItems().insert(
        part='snippet',
            body={
              "snippet": {
                "playlistId": RAP_PLAYLIST,
                "resourceId": {
                    "kind":video_ID[items][0],
                    "videoId": video_ID[items][1]
                }
              }
            }
        )
    response = request.execute()
