from flask_socketio import SocketIO
from flask.globals import current_app
import psycopg2
from forms import RegistrationForm, LoginForm, EditProfileForm, AddAmpForm, AddInstrumentForm,AddSettingForm
from flask import Flask, render_template, url_for, flash, redirect
from flask_login import login_user, current_user, logout_user, login_required
from database import Database
from flask_login import LoginManager
from authuser import  get_user
from users import User
from amps import  Amp
from settingscls import Setting
from instruments import Instrument
import sys
from passlib.hash import pbkdf2_sha256 as hasher

app = Flask(__name__)

"""
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
"""

login_manager = LoginManager()


@login_manager.user_loader
def load_user(user_id):
    return get_user(user_id)


db = Database('findyourtone', 'postgres', 'qweqweqwe')
app.config['SECRET_KEY'] = '18d76ffb6141d938eaab4ed46c3f41cd'


"""
@app.route('/')
def home():
    return render_template('main.html')
"""


@app.route('/')
def landing_page():
    if current_user.is_authenticated:
        return render_template('home.html')

    else:
        return render_template('landing_page.html')


@app.route('/home')
def home():
    sound_array = db.get_all_sounds()
    return render_template('home.html',sound_array=sound_array)

@app.route("/profile/", methods=['GET', 'POST'])
def profile():
    uname = current_user.username
    user = db.get_user(uname)
    return render_template('profile.html',user=user)

@app.route("/edit_profile/", methods=['GET', 'POST'])
def edit_profile():
    #get current user
    uname = current_user.username
    logged_user = db.get_user(uname)
    form = EditProfileForm()
    if form.validate_on_submit():
        #get data with form
        password = hasher.hash(form.password.data)
        user = User(form.name.data, form.username.data, password, form.location.data
                    , form.about.data, form.genre.data)
        #call method to change necessary values

        db.edit_user(logged_user, user)
        flash(f'Profile edited successfully!', 'success')
        return redirect(url_for('profile'))
    return render_template('edit_profile.html', title='Register', form=form)


@app.route("/amps/", methods=['GET', 'POST'])
def amps():
    uname = current_user.username
    user = db.get_user(uname)
    amp_array = db.get_all_amps_by_user(user)
    form = AddAmpForm()
    if form.validate_on_submit():
        # get data with form
        amp = Amp(form.model.data, form.brand.data, form.prod_year.data
                    , form.watts.data, form.tubes.data, form.mic.data, form.link.data,user.id)
        # call method to change necessary values
        db.add_amp(amp, user)
        flash(f'Amp added successfully!', 'success')
        return redirect(url_for('amps'))
    return render_template('amps.html',amp_array=amp_array,form=form)

@app.route("/amps/<int:amp_id>/delete", methods=['GET', 'POST'])
def delete_amp(amp_id):
    db.delete_amp(amp_id)
    return redirect(url_for('amps'))

@app.route("/instruments/<int:instrument_id>/delete", methods=['GET', 'POST'])
def delete_instrument(instrument_id):
    db.delete_instrument(instrument_id)
    return redirect(url_for('instruments'))

@app.route("/settings/<int:setting_id>/delete", methods=['GET', 'POST'])
def delete_setting(setting_id):
    db.delete_setting(setting_id)
    return redirect(url_for('settings'))

@app.route("/profile/delete", methods=['GET', 'POST'])
def delete_profile():
    db.delete_user(current_user.username)
    logout_user()
    flash("Your account has been deleted.", "success")
    return redirect(url_for('landing_page'))

@app.route("/amps/<int:amp_id>/", methods=['GET', 'POST'])
def edit_amps(amp_id):
    uname = current_user.username
    user = db.get_user(uname)
    now_amp = db.get_amp_by_id(amp_id)
    form = AddAmpForm()
    if form.validate_on_submit():
        # get data with form
        new_amp = Amp(form.model.data, form.brand.data, form.prod_year.data
                    , form.watts.data, form.tubes.data, form.mic.data, form.link.data,user.id)
        #print(form.model.data, form.brand.data, form.prod_year.data
        #          , form.watts.data, form.tubes.data, form.mic.data, form.link.data,user.id)
        # call method to change necessary values
        db.edit_amp(now_amp,new_amp)
        flash(f'Amp edited successfully!', 'success')
        return redirect(url_for('amps'))
    return render_template('edit_amps.html',amp_id=amp_id,form=form)



@app.route("/instruments/", methods=['GET', 'POST'])
def instruments():
    uname = current_user.username
    user = db.get_user(uname)
    instrument_array = db.get_all_instruments_by_user(user)
    form = AddInstrumentForm()
    if form.validate_on_submit():
         try:
            # get data with form
            instru = Instrument(form.type.data, form.model.data, form.prod_year.data
                      , form.mods.data, form.link.data, user.id)
            # call method to change necessary values
            db.add_instrument(instru, user)
            flash(f'Amp added successfully!', 'success')
            return redirect(url_for('instruments'))
         except:
             flash(f'An error occured while adding, try again.', "danger")
    return render_template('instruments.html',instrument_array=instrument_array,form=form)


@app.route("/instruments/<int:instrument_id>/", methods=['GET', 'POST'])
def edit_instruments(instrument_id):
    uname = current_user.username
    user = db.get_user(uname)
    res = db.get_instrument_by_id(instrument_id)
    print(res.id, res.type, res.model, res.prod_year, res.mods, res.link, res.added_by)
    form = AddInstrumentForm()
    if form.validate_on_submit():
        try:
            # get data with form
            new_instru = Instrument(form.type.data, form.model.data, form.prod_year.data
                          , form.mods.data, form.link.data, user.id)
            # print(form.model.data, form.brand.data, form.prod_year.data
            #          , form.watts.data, form.tubes.data, form.mic.data, form.link.data,user.id)
            # call method to change necessary values
            db.edit_instrument(res, new_instru)
            flash(f'Instrument edited successfully!', 'success')
            return redirect(url_for('instruments'))
        except:
            flash(f'An error occured while editing, try again.', "danger")
    return render_template('edit_instruments.html', instrument_id=instrument_id, form=form)

@app.route("/settings/", methods=['GET', 'POST'])
def settings():
    uname = current_user.username
    user = db.get_user(uname)
    setting_array = db.get_all_settings_by_user(user)
    form = AddSettingForm()
    if form.validate_on_submit():
        try:
            # get data with form
            setting = Setting(form.bass.data, form.mid.data, form.treble.data
                      , form.volume.data, form.master.data, form.gain.data,
                              form.presence.data,form.spec_eq.data,form.effects.data,
                              form.genre.data,user.id)
            # call method to change necessary values
            db.add_setting(setting, user)
            flash(f'Setting added successfully!', 'success')
            return redirect(url_for('settings'))
        except:
            flash(f'An error occured while adding, try again.', "danger")
    return render_template('settings.html',setting_array=setting_array,form=form)


@app.route("/settings/<int:setting_id>/", methods=['GET', 'POST'])
def edit_settings(setting_id):

    uname = current_user.username
    user = db.get_user(uname)
    res = db.get_setting_by_id(setting_id)

    form = AddSettingForm()
    if form.validate_on_submit():
        try:
            # get data with form
            new_setting = Setting(form.bass.data, form.mid.data, form.treble.data
                          , form.volume.data, form.master.data, form.gain.data, form.presence.data, form.spec_eq.data
                                  , form.effects.data, form.genre.data, user.id)

            # call method to change necessary values
            db.edit_setting(res, new_setting)
            flash(f'Setting edited successfully!', 'success')

            return redirect(url_for('settings'))
        except:
            flash(f'An error occured while editing, try again.', "danger")
    return render_template('edit_settings.html', setting_id=setting_id, form=form)

@app.route("/register/", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        try:
            password = hasher.hash(form.password.data)
            user = User(form.name.data,form.username.data,password,form.location.data
                            ,form.about.data,form.genre.data)
            #print(deneme.id, deneme.name, deneme.username,deneme.password, deneme.location, deneme.category,deneme.genre,deneme.about)

            temp = db.add_user(user)

            #
            flash(f'Account created for {form.username.data}!', 'success')
            return redirect(url_for('login'))
        except:
            flash(f'An error occured while registering, try again.',"danger")
    return render_template('register.html', title='Register', form=form)



@app.route("/login/", methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        print(form.username.data, form.password.data, file=sys.stderr)

        # get the correct person from the database
        user = get_user(form.username.data)
        # check if the current_person is successfully returned
        if user:
            # check if the password is correct
            if hasher.verify(form.password.data, user.password):
                # log the user in
                login_user(user)
                print("The current persons activeness status:")
                print(current_user.is_active)
                print("The current persons authentication status:")
                print(current_user.is_authenticated)
                flash('You have been logged in!', 'success')
                return redirect(url_for('home'))
            else:
                print("The current persons activeness status:")
                print(current_user.is_active)
                print("The current persons authentication status:")
                print(current_user.is_authenticated)
                flash('Login Unsuccessful. Please check password', 'danger')

        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    flash("You have logged out.","success")
    return redirect(url_for("landing_page"))


# check if user disconnected from site,if they did log them out.
socketio = SocketIO(app)
@socketio.on('disconnect')
def disconnect_user():
    logout_user()




login_manager.init_app(app)
if __name__ == '__main__':
    app.run(debug=True)
