Find movies and episodes on a Plex Media Server that match specific keywords, and add them to a playlist.
Searches the title and plot.

*An earlier version of this script used external metadata agents (i.e. TVDb). Those have been removed.* 

## Install
   1. ``git clone https://github.com/nwithan8/PlexHolidays.git``
   2. Enter "PlexHolidays" folder
   3. Install dependencies with ``python -m pip install -r requirements.txt``
    
## Usage

   Run with ``python run.py -u [SERVER_URL] -t [PLEX_TOKEN] -k [KEYWORD 1] [KEYWORD 2] ... -p [PLAYLIST_NAME] -s [SECTION_1_NAME] [SECTION_2_NAME] ...``
   
   Include ``--all`` if all the keywords must be present to be added to the playlist.
   
   See ``python run.py --help`` for more details.
