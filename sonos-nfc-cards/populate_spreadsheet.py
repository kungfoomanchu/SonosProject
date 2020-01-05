import gspread
import time
import urllib.request
from oauth2client.service_account import ServiceAccountCredentials
from spotify_api_call import return_best


# use creds to create a client to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)

# Find a workbook by name and open the first sheet
# Make sure you use the righto name here.
sheet = client.open("Media Database Project Example (For John)").sheet1

# Extract and print all of the values
list_of_sheet_records = sheet.get_all_records()

count=0
for record in list_of_sheet_records:
    #print(record['Artist (Search)'],record['Album (Search)'])
    if (record['Artist (Search)']+record['Album (Search)']!=''):
        art_file_name=record["Cover Art Image Filename"]
        album, uri, artist, release_date, album_art = return_best(record['Artist (Search)'],record['Album (Search)'])
        sheet.update_cell(count+2, 7, uri)
        time.sleep(1)
        sheet.update_cell(count+2, 8, artist)
        time.sleep(1)
        sheet.update_cell(count+2, 9, album)
        time.sleep(1)
        sheet.update_cell(count+2, 11, release_date[:4])
        time.sleep(1)
        if album_art!='No Match':
            urllib.request.urlretrieve(album_art, f'images/{art_file_name}.jpg')
        #print(album_art)
        
    count=count+1
