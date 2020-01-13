import spotipy
import pprint
from spotipy.oauth2 import SpotifyClientCredentials
from config import SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET

artist_name="Yo La Tengo"
album_name="I can hear the heart beating as one"


client_credentials_manager = SpotifyClientCredentials(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def search(album_name,artist_name,search_type,item_returned_limit):
    offset=0
    result_list=[]
    while True:
        if search_type=='album':
            results = sp.search(q='album:' + album_name, offset=offset)
        elif search_type=='artist':
            results = sp.search(q='artist:' + artist_name, offset=offset)
        elif search_type=='both':
            results = sp.search(q='album:' + album_name +' '+'artist:'+artist_name, offset=offset)

        if item_returned_limit=="All":
            item_returned_limit=int(results['tracks']['total'])

        for _, item in enumerate(results['tracks']['items']):
            result_list.append(item['album'])

        if (int(results['tracks']['limit'])+int(results['tracks']['offset']))>item_returned_limit:
            break
        offset+=10
    return result_list


def return_best(artist_name,album_name):
    best_result=''
    searches_performed=[]

    def search_attempt(search_type):
        return_list=search(album_name,artist_name,search_type=search_type,item_returned_limit=20)
        searches_performed.append(search_type)
        return return_list

    found_flag=False
    for search_type in ('both','album','artist'):
        return_list=search_attempt(search_type)
        try_count=0
        try_max=20
        print(search_type)
        for i in return_list:
            if try_count>=try_max:
                break
            #print(i['artists'][0]['name'])
            try:
                if str(i['name']).lower()==album_name.lower() and str(i['artists'][0]['name']).lower()==artist_name.lower():
                    print(i['name'],i['uri'])
                    best_result=i

                    found_flag=True
                    break
            except UnicodeEncodeError:
                continue
            try_count+=1
        if found_flag==True:
            break

    #default if no match found
    if found_flag==False:
        return_list=[]
        for search_type in ('both','album','artist'):
            return_list=search_attempt(search_type)
            try:
                best_result=return_list[0]
                print('default')
                print(best_result['name'],best_result['uri'])
                found_flag=True
                break
            except IndexError:
                continue


    #if no results found for each search, should be rare; only for bad search queries
    if found_flag==False:
        print("No Match Found")
        album_name='No Match'
        album_uri='No Match'
        release_date='No Match'
        album_artist='No Match'
        album_art='NA'
        return album_name,album_uri,album_artist,release_date,album_art

    if found_flag!=False:
        album_name=best_result['name']
        album_uri=best_result['uri']
        release_date=best_result['release_date']
        album_artist=best_result['artists'][0]['name']
        album_art=best_result['images'][0]['url']
        return album_name,album_uri,album_artist,release_date,album_art



