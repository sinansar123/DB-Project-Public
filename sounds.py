class Sound:
    def __init__(self, name, user_id, genre, amp_id, instrument_id, setting_id, descript, sample,
                 song_id=None, up_date=None,id=None):
        self.id = id
        self.name = name
        self.user_id = user_id
        self.genre = genre
        self.amp_id = amp_id
        self.instrument_id = instrument_id
        self.setting_id = setting_id
        self.descript = descript
        self.sample= sample
        self.song_id = song_id
        self.up_date = up_date

        # db.add_sound(Sound(1,"Nick Johnston Lead",1,"rock/alternative",1,1,1,"20.12.2020","Awesome modern guitar sound",None,4.2,None))
        # db.add_sound(Sound(2, "Master of Puppets Rythm", 2, "Heavy metal/Thrash metal", 2, 2, 2, "21.12.2020", "Classic metal tone", None, 4.8,None))