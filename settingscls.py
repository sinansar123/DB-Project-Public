class Setting():
    def __init__(self, bass, mid, treble, volume,master, gain, presence, spec_eq,effects,genre,added_by,id=None):
        self.id = id
        self.bass = bass
        self.mid = mid
        self.treble = treble
        self.volume = volume
        self.master = master
        self.gain = gain
        self.presence = presence
        self.spec_eq = spec_eq
        self.effects = effects
        self.genre = genre
        self.added_by = added_by

