"""A video player class."""

from .video_library import VideoLibrary
import random
from .video_playlist import Playlist


class VideoPlayer:
    """A class used to represent a Video Player."""

    def __init__(self):
        self._video_library = VideoLibrary()
        self._video_playing = False
        self._video_in_play = None
        self._video_paused = False
        self._video_playlist = {}

    def number_of_videos(self):
        num_videos = len(self._video_library.get_all_videos())
        print(f"{num_videos} videos in the library")

    def show_all_videos(self):
        """Returns all videos."""
        all_videos = self._video_library.get_all_videos()
        print("Here's a list of all available videos:")
        video_list = []
        for val in all_videos:
            ts = "["
            for t in val.tags:
                ts = ts + t + " "
            ts = ts + "]"

            if ts != "[]":
                ts = ts[0:len(ts)-2] + "]"

            video_list += [f"{val.title} ({val.video_id}) {ts}"]

        sort_list = sorted(video_list)
        for i in sort_list:
            print(i)
            
    def play_video(self, video_id):
        """Plays the respective video.

        Args:
            video_id: The video_id to be played.
        """
        
        id=[]
        for i in self._video_library.get_all_videos():
            id.append(i.video_id)

        video = self._video_library.get_video(video_id)

        if video_id in id:
            if self._video_playing == False and self._video_paused == False:
                print(f"Playing video: {video.title}")
                self._video_in_play = video
                self._video_playing = True
            elif self._video_paused == True:
                print(f"Stopping video: {self._video_in_play.title}")
                print(f"Playing video: {video.title}")
                self._video_in_play = video
                self._video_playing = True
                self._video_paused = False
            else:
                print(f"Stopping video: {self._video_in_play.title}")
                print(f"Playing video: {video.title}")
                self._video_in_play = video
                self._video_playing = True
        else:
            print(f"Cannot play video: Video does not exist")

        
    def stop_video(self):
        """Stops the current video."""
        if self._video_playing == True:
            print(f"Stopping video: {self._video_in_play.title}")
            self._video_playing = False
        elif self._video_paused == True:
            print(f"Stopping video: {self._video_in_play.title}")
            self._video_playing = False
            self._video_paused = False
        else:
            print("Cannot stop video: No video is currently playing")


        #print("stop_video needs implementation")

    def play_random_video(self):
        """Plays a random video from the video library."""
        id = self._video_library.get_all_videos()
        if self._video_playing == True:
            print(f"Stopping video: {self._video_in_play.title}")
            self._video_playing = False

        v = random.choice(id)
        print(f"Playing video: {v.title}")
        self._video_playing = True
        self._video_in_play = v

    

    def pause_video(self):
        """Pauses the current video."""
        if self._video_playing == True:
            print(f"Pausing video: {self._video_in_play.title}")
            self._video_paused = True
            self._video_playing = False
        elif self._video_paused == True:
            print(f"Video already paused: {self._video_in_play.title}")
        else:
            print("Cannot pause video: No video is currently playing")

    def continue_video(self):
        """Resumes playing the current video."""
        if self._video_paused == True:
            print(f"Continuing video: {self._video_in_play.title}")
            self._video_paused = False
            self._video_playing = True
        else:
            if self._video_playing == False:
                print(f"Cannot continue video: No video is currently playing")
                self._video_playing = False
            else:
                print(f"Cannot continue video: Video is not paused")

    def show_playing(self):
        """Displays video currently playing."""
        
        if self._video_playing == True:
            video = self._video_library.get_all_videos()
            video_list = []
            for val in video:
                if self._video_in_play.title == val.title:
                    ts = "["
                    for t in val.tags:
                        ts = ts + t + " "
                    ts = ts + "]"

                    if ts != "[]":
                        ts = ts[0:len(ts)-2] + "]"

                    video_list += [f"{val.title} ({val.video_id}) {ts}"]
            print(f"Currently playing: {video_list[0]}")
        elif self._video_paused == True:
            ts = "["
            for t in self._video_in_play.tags:
                ts = ts + t + " "
            ts = ts + "]"

            if ts != "[]":
                ts = ts[0:len(ts)-2] + "]"
            print(f"Currently playing: {self._video_in_play.title} ({self._video_in_play.video_id}) {ts} - PAUSED")
        else:
            print(f"No video is currently playing")


    def create_playlist(self, playlist_name):
        """Creates a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        if playlist_name.lower() not in (name.lower() for name in self._video_playlist.keys()):
            pl = Playlist(playlist_name)
            self._video_playlist[playlist_name] = pl
            print("Successfully created new playlist:",pl.name)
        else:
            print("Cannot create playlist: A playlist with the same name already exists")

    def add_to_playlist(self, playlist_name, video_id):
        """Adds a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be added.
        """
        playlist_name_old = playlist_name
        if playlist_name.lower() not in (name.lower() for name in self._video_playlist.keys()):
            print(f"Cannot add video to {playlist_name}: Playlist does not exist")
        else:
            for key in self._video_playlist.keys():
                if key.lower() == playlist_name.lower():
                    playlist_name = key
            video_list = self._video_playlist[playlist_name]._videos
            try:
                video_name = self._video_library.get_video(video_id).title
            except:
                video_name = ""
            if not video_name:
                print(f"Cannot add video to {playlist_name}: Video does not exist")
            elif video_id in video_list:
                print(f"Cannot add video to {playlist_name}: Video already added")
            else:
                video_list.append(video_id)
                obj = self._video_playlist[playlist_name]
                obj.x(video_list)
                self._video_playlist[playlist_name] = obj
                print(f"Added video to {playlist_name_old}: {video_name}")

    def show_all_playlists(self):
        """Display all playlists."""

        if self._video_playlist:
            print("Showing all playlists:")
            list = []
            for key in self._video_playlist.keys():
                list.append(self._video_playlist[key].name)
            for i in list[::-1]:
                print(i)

        else:
            print("No playlists exist yet")

    def show_playlist(self, playlist_name):
        """Display all videos in a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        playlist_name_old = playlist_name
        if playlist_name.lower() not in (name.lower for name in self._video_playlist.keys()):
            print(f"Cannot show playlist {playlist_name_old}: Playlist does not exist")
        else:
            print(f"Showing playlist: {playlist_name_old}")
            if self._video_playlist == 

    def remove_from_playlist(self, playlist_name, video_id):
        """Removes a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be removed.
        """
        playlist_name_old = playlist_name
        if playlist_name.lower() not in (name.lower() for name in self._video_playlist.keys()):
            print(f"Cannot remove video from {playlist_name}: Playlist does not exist")
        else:
            for key in self._video_playlist.keys():
                if key.lower() == playlist_name.lower():
                    playlist_name = key
            obj = self._video_playlist[playlist_name]
            video_list = obj._videos
            try:
                video_name = self._video_library.get_video(video_id).title
            except:
                video_name = ""
            if video_id in video_list:
                video_list.remove(video_id)
                obj.x(video_list)
                print(f"Removed video from {playlist_name_old}: {video_name}")
            else:
                if not video_name:
                    print(f"Cannot remove video from {playlist_name_old}: Video does not exist")
                else:
                    print(f"Cannot remove video from {playlist_name_old}: Video is not in playlist")

    def clear_playlist(self, playlist_name):
        """Removes all videos from a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        print("clears_playlist needs implementation")

    def delete_playlist(self, playlist_name):
        """Deletes a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        print("deletes_playlist needs implementation")

    def search_videos(self, search_term):
        """Display all the videos whose titles contain the search_term.

        Args:
            search_term: The query to be used in search.
        """
        print("search_videos needs implementation")

    def search_videos_tag(self, video_tag):
        """Display all videos whose tags contains the provided tag.

        Args:
            video_tag: The video tag to be used in search.
        """
        print("search_videos_tag needs implementation")

    def flag_video(self, video_id, flag_reason=""):
        """Mark a video as flagged.

        Args:
            video_id: The video_id to be flagged.
            flag_reason: Reason for flagging the video.
        """
        print("flag_video needs implementation")

    def allow_video(self, video_id):
        """Removes a flag from a video.

        Args:
            video_id: The video_id to be allowed again.
        """
        print("allow_video needs implementation")
