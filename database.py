import psycopg2
from users import User
from amps import Amp
from instruments import Instrument
from sounds import Sound
from settingscls import Setting
from passlib.hash import pbkdf2_sha256 as hasher

class Database:
    def __init__(self, dbname, dbuser, dbpassword):
        self.dbname = dbname
        self.dbuser = dbuser
        self.dbpassword = dbpassword

    #function to add user to database
    def add_user(self, user):
        with psycopg2.connect(dbname=self.dbname, user=self.dbuser, password=self.dbpassword) as connection:
            # create a person with given attributes
            cursor = connection.cursor()

            query = """INSERT INTO users(name, username, password, location, about,genre)
                        values ( %s, %s, %s, %s, %s ,%s)"""
            try:
                cursor.execute(query, (user.name,
                                       user.username, user.password, user.location,user.about, user.genre,))
                print("execute works")
                connection.commit()
                # created
                print("first commit works")
                # select the created person to find out its id
                query = "SELECT * FROM users WHERE (username = %s)"

                cursor.execute(query, (user.username,))
                user_attr = cursor.fetchone()
                print('Created user with id: {}'.format(user_attr[0]))
                ret_user = User(
                    user_attr[1], user_attr[2], user_attr[3], user_attr[4], user_attr[5], user_attr[6],
                    user_attr[7], user_attr[8], user_attr[0])
                return ret_user
            except:
                print(psycopg2.Error.pgerror)
                print('Error: User already exists.')
                pass

    #function to get user from table by username
    def get_user(self, username):
        with psycopg2.connect(dbname=self.dbname, user=self.dbuser, password=self.dbpassword) as connection:
            cursor = connection.cursor()

            try:
                # select the created person to find out its id
                query = "SELECT * FROM users WHERE (username = %s)"

                cursor.execute(query, (username,))
                user_attr = cursor.fetchone()
                ret_user = User(
                    user_attr[1], user_attr[2], user_attr[3], user_attr[4], user_attr[5], user_attr[6],
                    user_attr[7], user_attr[8], user_attr[0])
                return ret_user
            except:
                print('Error: User does not exist.')
                pass

    #edit user values. Takes in old user object and a new user object
    def edit_user(self,now_user,new_user):
        with psycopg2.connect(dbname=self.dbname, user=self.dbuser, password=self.dbpassword) as connection:
            cursor = connection.cursor()

            if new_user.username:
                username = new_user.username
            else:    username = now_user.username
            if new_user.name:
                name = new_user.name
            else:
                name = now_user.name
            if new_user.password:
                password = new_user.password
            else:
                password = now_user.password
            if new_user.genre:
                genre = new_user.genre
            else:
                genre = now_user.genre
            if new_user.about:
                about = new_user.about
            else:
                about = now_user.about
            if new_user.location:
                location = new_user.location
            else:
                location = now_user.location

            query = """UPDATE users SET name =%s , username=%s, password=%s, location=%s, about=%s,genre=%s
                                where (id = %s)"""

            try:
                cursor.execute(query, (name, username, password, location, about, genre,now_user.id))
                print("execute works")
                connection.commit()
            except:
                print('Error occured while editing profile')
                pass
    """
    # function to get user from table by username
    def get_user(self, username):
        with psycopg2.connect(dbname=self.dbname, user=self.dbuser, password=self.dbpassword) as connection:
            cursor = connection.cursor()

            try:
                # select the created person to find out its id
                query = "SELECT * FROM users WHERE (username = %s)"

                cursor.execute(query, (username,))
                user_attr = cursor.fetchone()
                ret_user = User(
                    user_attr[1], user_attr[2], user_attr[3], user_attr[4], user_attr[5], user_attr[6],
                    user_attr[7], user_attr[8], user_attr[0])
                return ret_user
            except:
                print('Error: User does not exist.')
                pass
    """
    # function to get user from table by username
    def delete_user(self, username):
        with psycopg2.connect(dbname=self.dbname, user=self.dbuser, password=self.dbpassword) as connection:
            cursor = connection.cursor()

            try:
                # delete user from database
                query = "DELETE FROM users WHERE (username = %s)"
                cursor.execute(query, (username,))
                print("Deleted user with username:{}".format(username))
                pass
            except:
                print('Error: User does not exist.')
                pass


    # method to add amp, takes user and amp object. Uses user for added_by
    #USES USERID
    def add_amp(self,amp,user):
        with psycopg2.connect(dbname=self.dbname, user=self.dbuser, password=self.dbpassword) as connection:
            cursor = connection.cursor()

            query = """INSERT INTO amps(model, brand, prod_year, watts, tubes,mic,link,added_by)
                                    values ( %s, %s, %s, %s, %s ,%s, %s ,%s)"""
            try:
                cursor.execute(query, (amp.model,amp.brand, amp.prod_year ,amp.watts,
                                       amp.tubes, amp.mic,amp.link, user.id))
                print("execute works!!!!!!!!!!!")
                connection.commit()
                pass
            except:
                print(psycopg2.Error.pgerror)
                print('Error occured while adding amp.')
                pass

    def edit_amp(self,now_amp,new_amp):
        with psycopg2.connect(dbname=self.dbname, user=self.dbuser, password=self.dbpassword) as connection:
            cursor = connection.cursor()

            if new_amp.model:
                model = new_amp.model
            else:
                model = now_amp.model
            if new_amp.brand:
                brand = new_amp.brand
            else:
                brand = now_amp.brand
            if new_amp.prod_year:
                prod_year = new_amp.prod_year
            else:
                prod_year = now_amp.prod_year
            if new_amp.watts:
                watts = new_amp.watts
            else:
                watts = now_amp.watts
            if new_amp.tubes:
                tubes = new_amp.tubes
            else:
                tubes = now_amp.tubes
            if new_amp.mic:
                mic = new_amp.mic
            else:
                mic = now_amp.mic
            if new_amp.link:
                link = new_amp.link
            else:
                link = now_amp.link


            query = """UPDATE amps SET model =%s , brand=%s, prod_year=%s, watts=%s, tubes=%s,mic=%s, 
                    link=%s, added_by=%s  where (id = %s)"""

            try:
                cursor.execute(query, (model, brand, prod_year, watts, tubes, mic,link,
                                        now_amp.added_by,now_amp.id))
                print("execute works")

                connection.commit()
                print("COMMIT NEW AMP")
            except:
                print('Error occured while editing amplifier')
                pass

    ###NEEDS FIX!!!! maybe change this to return amps and return all amps by a user.
    # USES USERID
    def get_amp_by_id(self, ampid):
        with psycopg2.connect(dbname=self.dbname, user=self.dbuser, password=self.dbpassword) as connection:
            cursor = connection.cursor()

            try:
                query = "SELECT * FROM amps WHERE (id = %s)"
                cursor.execute(query, (ampid,))
                amp_attr = cursor.fetchone()
                print('returned amp with id: {}'.format(amp_attr[0]))
                ret_amp = Amp(
                    amp_attr[1], amp_attr[2], amp_attr[3], amp_attr[4], amp_attr[5], amp_attr[6],
                    amp_attr[7], amp_attr[8],amp_attr[0])
                print(ret_amp.id,"RETID")
                return ret_amp
            except:

                print('Error occured while adding amp.')
                pass


    def get_all_amps_by_user(self, user):
        with psycopg2.connect(dbname=self.dbname, user=self.dbuser, password=self.dbpassword) as connection:
            cursor = connection.cursor()
            amp_array = []
            try:
                query = "SELECT * FROM amps WHERE (added_by = %s)"
                cursor.execute(query, (user.id,))
                user_amps = cursor.fetchall()
                print("done fetchall")
                for amp in user_amps:
                    amp_array.append(Amp(amp[1], amp[2], amp[3], amp[4], amp[5], amp[6],
                    amp[7], amp[8],amp[0]))
                return amp_array
            except:

                print('Error occured while adding amp.')
                pass

    # function to get delete amps
    def delete_amp(self, ampid):
        with psycopg2.connect(dbname=self.dbname, user=self.dbuser, password=self.dbpassword) as connection:
            cursor = connection.cursor()

            try:
                # delete user from database
                query = "DELETE FROM amps WHERE (id = %s)"
                cursor.execute(query, (ampid,))
                print("Deleted amp with id:{}".format(ampid))
                pass
            except:
                print('Error: User does not exist.')
                pass

    #function to add instrument
    def add_instrument(self, instru,user):
        with psycopg2.connect(dbname=self.dbname, user=self.dbuser, password=self.dbpassword) as connection:
            # create a person with given attributes
            cursor = connection.cursor()

            query = """INSERT INTO instruments(type, model, prod_year, mods, link,added_by)
                        values ( %s, %s, %s, %s, %s ,%s)"""
            try:
                cursor.execute(query, (instru.type,instru.model, instru.prod_year,
                                       instru.mods,instru.link, user.id,))
                print("execute works")
                connection.commit()
                # created
                print("first commit works")
            except:
                print(psycopg2.Error.pgerror)
                print('Error occured while adding instrument.')
                pass

    def edit_instrument(self,old_instru,new_instru):
        with psycopg2.connect(dbname=self.dbname, user=self.dbuser, password=self.dbpassword) as connection:
            cursor = connection.cursor()

            if new_instru.type:
                type = new_instru.type
            else:
                type = old_instru.type

            if new_instru.model:
                model = new_instru.model
            else:
                model = old_instru.model

            if new_instru.prod_year:
                prod_year = new_instru.prod_year
            else:
                prod_year = old_instru.prod_year

            if new_instru.mods:
                mods = new_instru.mods
            else:
                mods = old_instru.mods
            if new_instru.link:
                link = new_instru.link
            else:
                link = old_instru.link

            query = """UPDATE instruments SET type=%s , model=%s, prod_year=%s, mods=%s, link=%s,
                    added_by=%s  where (id = %s)"""

            try:
                cursor.execute(query, (type, model, prod_year, mods, link, old_instru.added_by, old_instru.id))
                print("execute works")

                connection.commit()
                print("COMMIT NEW Instruments")
            except:
                print('Error occured while editing instrument')
                pass



    #function to select instrument
    def get_instrument_by_id(self, instrumentid):
        with psycopg2.connect(dbname=self.dbname, user=self.dbuser, password=self.dbpassword) as connection:
            cursor = connection.cursor()

            try:
                query = "SELECT * FROM instruments WHERE (id = %s)"
                cursor.execute(query, (instrumentid,))
                instru_attr = cursor.fetchone()
                print('returned instrument with id: {}'.format(instru_attr[0]))
                ret_instru = Instrument(
                    instru_attr[1], instru_attr[2], instru_attr[3], instru_attr[4],
                    instru_attr[5], instru_attr[6],instru_attr[0])
                print(ret_instru.id, "RETID")
                return ret_instru
            except:

                print('Error occured while adding instrument.')
                pass

    def get_all_instruments_by_user(self, user):
        with psycopg2.connect(dbname=self.dbname, user=self.dbuser, password=self.dbpassword) as connection:
            cursor = connection.cursor()
            instrument_array = []
            try:
                query = "SELECT * FROM instruments WHERE (added_by = %s)"
                cursor.execute(query, (user.id,))
                user_instruments = cursor.fetchall()
                print("done fetchall")
                for instrument in user_instruments:
                    instrument_array.append(Instrument(instrument[1], instrument[2], instrument[3], instrument[4],
                                            instrument[5], instrument[6],instrument[0]))
                return instrument_array
            except:

                print('Error occured while fetching instruments.')
                pass

    def delete_instrument(self, instrumentid):
        with psycopg2.connect(dbname=self.dbname, user=self.dbuser, password=self.dbpassword) as connection:
            cursor = connection.cursor()

            try:
                # delete user from database
                query = "DELETE FROM instruments WHERE (id = %s)"
                cursor.execute(query, (instrumentid,))
                print("Deleted instrument with id:{}".format(instrumentid))
                pass
            except:
                print('Error: Instrument does not exist.')
                pass

    # method to add amp, takes user and amp object. Uses user for added_by
    # USES USERID
    def add_setting(self, setting, user):
        with psycopg2.connect(dbname=self.dbname, user=self.dbuser, password=self.dbpassword) as connection:
            cursor = connection.cursor()

            query = """INSERT INTO SETTINGS(bass, mid, treble, volume, master,gain,presence,spec_eq,effects,genre,
                        added_by) values ( %s, %s, %s, %s, %s ,%s, %s ,%s,%s, %s ,%s)"""
            try:
                cursor.execute(query, (setting.bass, setting.mid, setting.treble, setting.volume,
                                       setting.master, setting.gain, setting.presence,setting.spec_eq
                                       ,setting.effects,setting.genre, user.id))
                print("execute works!!!!!!!!!!!")
                connection.commit()
                pass
            except:
                print(psycopg2.Error.pgerror)
                print('Error occured while adding amp.')
                pass

    def edit_setting(self, old_setting, new_setting):
        with psycopg2.connect(dbname=self.dbname, user=self.dbuser, password=self.dbpassword) as connection:
            cursor = connection.cursor()

            if new_setting.bass:
                bass = new_setting.bass
            else:
                bass = old_setting.bass

            if new_setting.mid:
                mid = new_setting.mid
            else:
                mid = old_setting.mid

            if new_setting.treble:
                treble = new_setting.treble
            else:
                treble = old_setting.treble

            if new_setting.volume:
                volume = new_setting.volume
            else:
                volume = old_setting.volume
            if new_setting.master:
                master = new_setting.master
            else:
                master = old_setting.master
            if new_setting.gain:
                gain = new_setting.gain
            else:
                gain = old_setting.gain
            if new_setting.presence:
                presence = new_setting.presence
            else:
                presence = old_setting.presence
            if new_setting.spec_eq:
                spec_eq = new_setting.spec_eq
            else:
                spec_eq = old_setting.spec_eq
            if new_setting.effects:
                effects = new_setting.effects
            else:
                effects = old_setting.effects
            if new_setting.genre:
                genre = new_setting.genre
            else:
                genre = old_setting.genre
            query = """UPDATE SETTINGS SET bass=%s, mid=%s, treble=%s, volume=%s, master=%s,gain=%s,presence=%s
                    ,spec_eq=%s,effects=%s,genre=%s,added_by=%s where (id=%s)"""

            try:
                cursor.execute(query, (bass, mid, treble, volume, master, gain, presence,
                                       spec_eq,effects,genre,old_setting.added_by, old_setting.id))
                print("execute works")

                connection.commit()
                print("COMMIT NEW AMP")
            except:
                print('Error occured while editing amplifier')
                pass

    def delete_setting(self, settingid):
        with psycopg2.connect(dbname=self.dbname, user=self.dbuser, password=self.dbpassword) as connection:
            cursor = connection.cursor()

            try:
                # delete user from database
                query = "DELETE FROM settings WHERE (id = %s)"
                cursor.execute(query, (settingid,))
                print("Deleted setting with id:{}".format(settingid))
                pass
            except:
                print('Error: User does not exist.')
                pass

    def get_setting_by_id(self, settingid):
        with psycopg2.connect(dbname=self.dbname, user=self.dbuser, password=self.dbpassword) as connection:
            cursor = connection.cursor()

            try:
                query = "SELECT * FROM settings WHERE (id = %s)"
                cursor.execute(query, (settingid,))
                setting_attr = cursor.fetchone()
                print('returned setting with id: {}'.format(setting_attr[0]))
                ret_setting = Setting(
                    setting_attr[1], setting_attr[2], setting_attr[3], setting_attr[4], setting_attr[5], setting_attr[6],
                    setting_attr[7], setting_attr[8], setting_attr[9],setting_attr[10],setting_attr[11],setting_attr[0])
                return ret_setting
            except:
                print('Error occured while adding amp.')
                pass

    def get_all_settings_by_user(self, user):
        with psycopg2.connect(dbname=self.dbname, user=self.dbuser, password=self.dbpassword) as connection:
            cursor = connection.cursor()
            setting_array = []
            try:
                query = "SELECT * FROM settings WHERE (added_by = %s)"
                cursor.execute(query, (user.id,))
                user_settings = cursor.fetchall()
                print("done fetchall")
                for setting in user_settings:
                    setting_array.append(Setting(setting[1], setting[2], setting[3], setting[4], setting[5], setting[6],
                                         setting[7], setting[8], setting[9],setting[10],setting[11], setting[0]))
                return setting_array
            except:

                print('Error occured while fetching settings.')
                pass



    def add_sound(self, sound, user):
        with psycopg2.connect(dbname=self.dbname, user=self.dbuser, password=self.dbpassword) as connection:
            # create a person with given attributes
            cursor = connection.cursor()

            query = """INSERT INTO sounds(name,user_id,genre,amp_id,instrument_id,setting_id,descript,sample) 
                    values (%s, %s, %s, %s, %s ,%s,%s, %s )"""
            try:
                cursor.execute(query, (sound.name, user.id, sound.genre, sound.amp_id,
                                       sound.instrument_id, sound.setting_id, sound.descript,sound.sample))
                print("execute works")
                connection.commit()
                # created
            except:
                print(psycopg2.Error.pgerror)
                pass

    #function to select sound
    def get_sounds_by_userid(self, user):
        with psycopg2.connect(dbname=self.dbname, user=self.dbuser, password=self.dbpassword) as connection:
            cursor = connection.cursor()
            sound_array = []
            try:
                query = "SELECT * FROM sounds WHERE (user_id = %s)"
                cursor.execute(query,(user.id,))
                sounds = cursor.fetchall()
                for sound_attr in sounds:
                    sound_array.append(Sound(
                        sound_attr[1], sound_attr[2], sound_attr[3], sound_attr[4],
                        sound_attr[5], sound_attr[6], sound_attr[7], sound_attr[8], sound_attr[9]
                        , sound_attr[0]))
                return sound_array
            except:
                print('Error occured while fetching sound.')
                pass

    # function to select sound
    def get_sound_by_userid(self, soundid):
        with psycopg2.connect(dbname=self.dbname, user=self.dbuser, password=self.dbpassword) as connection:
            cursor = connection.cursor()
            try:
                query = "SELECT * FROM sounds WHERE (id = %s)"
                cursor.execute(query, (soundid,))
                sound_attr = cursor.fetchone()

                ret_sound =(Sound(
                        sound_attr[1], sound_attr[2], sound_attr[3], sound_attr[4],
                        sound_attr[5], sound_attr[6], sound_attr[7], sound_attr[8], sound_attr[9]
                        , sound_attr[0]))
                return ret_sound
            except:
                print('Error occured while fetching sound.')
                pass

    # function to select sound
    def get_sounds_by_username(self, name):
        with psycopg2.connect(dbname=self.dbname, user=self.dbuser, password=self.dbpassword) as connection:
            cursor = connection.cursor()
            setting_array = []
            modded_name = "%" + name + "%"
            try:
                query = "SELECT * FROM sounds WHERE (name LIKE %s)"
                cursor.execute(query, (modded_name,))
                sounds = cursor.fetchall()
                for sound_attr in sounds:
                    setting_array.append(Sound(
                        sound_attr[1], sound_attr[2], sound_attr[3], sound_attr[4],
                        sound_attr[5], sound_attr[6], sound_attr[7],sound_attr[8], sound_attr[9],
                        sound_attr[0]))
                return setting_array
            except:

                print('Error occured while adding sound.')
                pass

    # function to select all sound
    def get_all_sounds(self):
        with psycopg2.connect(dbname=self.dbname, user=self.dbuser, password=self.dbpassword) as connection:
            cursor = connection.cursor()
            setting_array = []
            try:
                query = "SELECT * FROM sounds"
                cursor.execute(query)
                sounds = cursor.fetchall()
                for sound_attr in sounds:
                    setting_array.append(Sound(
                        sound_attr[1], sound_attr[2], sound_attr[3], sound_attr[4],
                        sound_attr[5], sound_attr[6], sound_attr[7], sound_attr[8], sound_attr[9]
                        , sound_attr[0]))
                return setting_array
            except:
                print('Error occured while adding sound.')
                pass

    def delete_sound(self, soundid):
        with psycopg2.connect(dbname=self.dbname, user=self.dbuser, password=self.dbpassword) as connection:
            cursor = connection.cursor()

            try:
                # delete user from database
                query = "DELETE FROM SOUNDS WHERE (id = %s)"
                cursor.execute(query, (soundid,))
                print("Deleted setting with id:{}".format(soundid))
                pass
            except:
                print('Error: User does not exist.')
                pass
#
#       TODO : delete methods for everything, fix sound methods, add songs, implement different logintypes
#       TODO : survive?, Add better user interface, deploy
#
#
        """
            ###SONG QUERIES###
            
                Select * from Songs 
                Where (song_Id = song_id);
            
                SELECT * from SONGS
                WHERE (artist_id = user_id)
            
                INSERT INTO SONGS(id,name,album,release_date,label,artist_id)
            
                DELETE from SONGS WHERE (song_Id = song_id);
            
            ###ARTIST QUERIES###
                INSERT INTO ARTIST (band, label)
            
                SELECT * FROM ARTIST
                WHERE (ID = user.id
                
             ###ARTIST QUERIES###
                INSERT INTO ADMINISTRATOR (email. phone,section)   
        """

#db = Database('findyourtone', 'postgres', 'qweqweqwe')
#new_user = User('OLDNEWUser', 'newuser74','$pbkdf2-sha256$29000$sZayFmKMcU4JAeAc43zvnQ$iQaR7DLD43ahS1aL2MC7ayHgCvfi8MrAap.8ATLkXyw','USa','Love Death!:)!','POP')
#
#deneme = db.add_user(new_user)
#print(deneme.id, deneme.name, deneme.username,deneme.password, deneme.location, deneme.about,deneme.genre,deneme.category,deneme.reg_date)

#deneme = db.get_user('newuser')
#print(deneme.id, deneme.name, deneme.username,deneme.password, deneme.location, deneme.about,deneme.genre,deneme.category,deneme.reg_date)

#new_amp = Amp("Angel", "Randall","2010","100","6l6","SM57","a link","")
#db.add_amp(new_amp,deneme)
#yeni_amfi = db.get_amp_by_user(deneme)
#print(yeni_amfi.id,yeni_amfi.model,yeni_amfi.brand,yeni_amfi.added_by)
#db.delete_user("newuser3")

#db.edit_user(deneme,new_user)


#new_instrument= Instrument("guitar","Telecaster","61","Neck broken and repaired","Nolink,too rare","someuser")
#db.add_Instrument(new_instrument,deneme)
#res =db.get_instrument_by_id("1")
#print(res.id,res.type,res.model,res.prod_year,res.mods,res.link,res.added_by)



#ses = Sound("Nick Johnston Lead", 1,"rock/alternative",1,1,1,"Awesome modern guitar sound",
#      "https://www.youtube.com/watch?v=GZ7W3JvZBJQ&ab_channel=NickJohnston","4","2","1","20.12.2020")

#db.add_sound(ses,deneme, yeni_amfi,res,deneme)
#db.get_sound_by_user(deneme)

#yeni_amfi = Amp("model","marka","tarih","wat","tüp","mic")
##amp = db.get_amp_by_id("4")
#new_amp= db.get_amp_by_id("1")
#db.edit_amp(amp,new_amp)
#for amp in amps:
#print(amp.id, amp.model, amp.brand, amp.prod_year,amp.watts,amp.tubes,amp.mic,amp.link,amp.added_by)

##instrument = db.get_instrument_by_id("3")
#for instrument in instruments:
#    print(instrument.id,instrument.type,instrument.model,instrument.prod_year,instrument.mods,instrument.link,
#         instrument.added_by)

#setting = Setting("1","1","1","1","1","1","1","1","1""1","metal","1")
##db.get_setting_by_id("10")
#print("")
#sound = db.get_sounds_by_userid(deneme)
#print(sound[1])
##db.add_sound(sound,deneme)