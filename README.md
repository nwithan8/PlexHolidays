Find movies and episodes on a Plex Media Server that match specific keywords, and add them to a playlist.
Searches the title and plot.

*An earlier version of this script used external metadata agents (i.e. TVDb). Those have been removed.* 

## Install
   1. ``git clone https://github.com/nwithan8/PlexHolidays.git``
   2. Enter "PlexHolidays" folder
   3. Install dependencies with ``python -m pip install -r requirements.txt``
    
## Usage

   Run with ``python run.py -u [SERVER_URL] -t [PLEX_TOKEN] -k [KEYWORD 1] [KEYWORD 2] ... -p [PLAYLIST_NAME] -s [SECTION_1_NAME] [SECTION_2_NAME] ...``
   
   Include ``--all`` if all the keywords must be present to be added to the playlist. Keywords are not case sensitive.
   
   If a playlist does not exist, one will be created automatically.
   
   This script only works on Movies and Show sections. Music, Clips, and Photos sections are not supported.
   
   See ``python run.py --help`` for more details.
   

## Example
``python run.py -u http://localhost:32400 -t thisisaplextoken -k christmas holiday --all -p "Christmas Movies" -s "Movies" "4K Movies"``
        
This would find all movies in the "Movies" and "4K Movies" sections that have BOTH "Christmas" and "holiday" in either the title or description, and add then to a playlist called "Christmas Movies".
