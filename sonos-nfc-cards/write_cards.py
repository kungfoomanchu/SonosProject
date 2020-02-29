import gspread
from oauth2client.service_account import ServiceAccountCredentials
from def__sonos_nfc_write_loop import write_card

# use creds to create a client to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)

# Find a workbook by name and open the first sheet
# Make sure you use the righto name here.
sheet = client.open("NFC Cards Database").sheet1

list_of_sheet_records = sheet.get_all_records()
for record in list_of_sheet_records:
    uri_to_write=record['Spotify URI (Result)']
    artist_to_write=record['Artist (Result)']
    album_to_write=record['Album (Result)']
    year_to_write=record['Year (Result)']
    skip_or_print=record['Skip vs Print']
    if uri_to_write!='No Match':
        if skip_or_print!='Skip':
            write_card(uri_to_write,artist_to_write,album_to_write,year_to_write)
