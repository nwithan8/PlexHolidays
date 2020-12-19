import argparse
from typing import List, Union

from plexapi import server, media, video, library, playlist
from progress.bar import Bar


parser = argparse.ArgumentParser(description="Make or add to a Plex playlist based off keywords")
parser.add_argument("-u",
                    "--url",
                    type=str,
                    required=True,
                    help="URL of the Plex Media Server")
parser.add_argument("-t",
                    "--plex_token",
                    type=str,
                    required=True,
                    help="Token for the Plex Media Server")
parser.add_argument("-p",
                    "--playlist_name",
                    type=str,
                    required=True,
                    help="Name of the playlist to use. Will make a new playlist if not found.")
parser.add_argument("-k",
                    "--keywords",
                    nargs="+",
                    type=str,
                    required=True,
                    help="List of keywords to look for in media descriptions")
parser.add_argument('-a',
                    '--all',
                    action='store_true',
                    help="All keywords must be present in media description or title to be added."
                         "Otherwise, any keyword match will trigger an add.")
parser.add_argument("-s",
                    "--section_names",
                    nargs="+",
                    type=str,
                    required=True,
                    help="Names of the library sections to look in")
args = parser.parse_args()


class Plex:
    def __init__(self, url: str, token: str):
        self.server = server.PlexServer(url, token)

    @property
    def playlists(self) -> List[playlist.Playlist]:
        return self.server.playlists()

    def get_playlist(self, playlist_name: str) -> Union[playlist.Playlist, None]:
        for each in self.playlists:
            if each.title == playlist_name:
                return each
        return None

    def create_new_playlist(self, playlist_name: str, items: List[media.Media]):
        self.server.createPlaylist(title=playlist_name, items=items)

    def add_to_playlist(self, playlist_name: str, items: List[media.Media], create_if_not_found: bool = False) -> bool:
        playlist = self.get_playlist(playlist_name=playlist_name)
        if playlist:
            playlist.addItems(items=items)
            return True
        else:
            if create_if_not_found:
                self.create_new_playlist(playlist_name=playlist_name, items=items)
                return True
            return False

    @property
    def library_sections(self) -> List[library.LibrarySection]:
        return self.server.library.sections()

    def get_section(self, section_name: str) -> Union[library.LibrarySection, None]:
        for section in self.library_sections:
            if section.title == section_name:
                return section
        return None

    def get_all_section_items(self, section: library.LibrarySection) -> List[Union[video.Movie, video.Show]]:
        return section.all()


plex = Plex(url=args.url, token=args.plex_token)

def contains_keywords(item: Union[video.Video]) -> bool:
    all_keywords_present = True
    for keyword in args.keywords:
        if args.all and not all_keywords_present:
            return False
        if keyword.lower() in item.summary.lower():
            if not args.all:
                return True
        elif keyword.lower() in item.title.lower():
            if not args.all:
                return True
        else:
            all_keywords_present = False
    return all_keywords_present

def find_matching_items():
    matching_items = []

    for section_name in args.section_names:
        local_matching_items = []
        section = plex.get_section(section_name=section_name)
        if not section:
            print(f'Could not find section "{section_name}"')
            continue
        if section.type not in ['movie', 'show']:
            print(f'This script can only handle Movie and Show sections. "{section_name}" is a(n) {section.type} section.')
            continue
        print(f'Loading "{section_name}" items. This may take a while for large sections...')
        section_items = plex.get_all_section_items(section=section)
        if not section_items:
            print(f'Could not get any items from section "{section_name}"')
            continue
        if section.type == 'movie':
            bar = Bar(f'Analyzing movies...', max=len(section_items))
            for movie in section_items:
                if contains_keywords(item=movie):
                    local_matching_items.append(movie)
                bar.next()
            bar.finish()
        elif section.type == 'show':
            bar = Bar(f'Analyzing shows...', max=len(section_items))
            for show in section_items:
                for episode in show.episodes():
                    if contains_keywords(item=episode):
                        local_matching_items.append(episode)
                bar.next()
            bar.finish()
        if not local_matching_items:
            print(f'Did not find any matching items in "{section_name}"')
        else:
            print(f'Found {len(local_matching_items)} matching item(s) in "{section_name}"')
            matching_items.extend(local_matching_items)

    print(f'Adding {len(matching_items)} item(s) to playlist "{args.playlist_name}"...')
    if not plex.add_to_playlist(playlist_name=args.playlist_name, items=matching_items, create_if_not_found=True):
        raise Exception(f'"{args.playlist_name}" could not be updated.')
    print(f'"{args.playlist_name}" updated successfully!')

if __name__ == "__main__":
    find_matching_items()
