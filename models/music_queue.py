class MusicQueue:
    playlist = []
    def __init__(self) -> None:
        pass

    def add_song(self, song):
        print("musique ajouté")
        self.playlist.append(song)
        print("playlist {}".format(self.playlist))

    def remove_playlist(self):
        self.playlist = []

    def print_playlist(self):
        return self.playlist
        # for music in self.playlist:
        #     ctx.send(music)