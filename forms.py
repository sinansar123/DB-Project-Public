from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField,FloatField,IntegerField
from wtforms.validators import DataRequired, Length, EqualTo,URL, Optional


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    name = StringField('Your Name',
                           validators=[DataRequired()])
    location = StringField('Location',
                        validators=[])
    genre = StringField('Favourite Genre',
                           validators=[])
    about = StringField('Tell us about yourself',
                           validators=[])
    submit = SubmitField('Sign Up')

class EditProfileForm(FlaskForm):
    username = StringField('Username',
                           validators=[Length(min=0, max=20)])
    password = PasswordField('Password', validators=[])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[ EqualTo('password')])
    name = StringField('Your Name',
                           validators=[])
    location = StringField('Location',
                        validators=[])
    genre = StringField('Favourite Genre',
                           validators=[])
    about = StringField('Tell us about yourself',
                           validators=[])
    submit = SubmitField('Edit Profile')

class AddAmpForm(FlaskForm):
    model = StringField('Model',validators=[])
    brand = StringField('Brand', validators=[])
    prod_year = StringField('Production Year',
                           validators=[])
    watts = StringField('Watts',
                        validators=[])
    tubes = StringField('Tubes',
                           validators=[])
    mic = StringField('Microphone Used',
                           validators=[])
    link = StringField('Link',
                      validators=[URL(message='Must be a valid URL'),Optional()])
    submit = SubmitField('Submit')


class AddInstrumentForm(FlaskForm):
    type = StringField('Type', validators=[])
    model = StringField('Model', validators=[])
    prod_year = StringField('Production Year',
                            validators=[])
    mods = StringField('Moifications',
                        validators=[])
    link = StringField('Link',
                       validators=[URL(message='Must be a valid URL'), Optional()])
    submit = SubmitField('Submit')

class AddSettingForm(FlaskForm):
    bass = FloatField('Bass', validators=[])
    mid = FloatField('Mid', validators=[])
    treble = FloatField('Treble',validators=[])
    volume = FloatField('Volume',validators=[])
    master = FloatField('Master',validators=[])
    gain = FloatField('Gain',validators=[])
    presence = FloatField('Presence', validators=[])
    spec_eq = FloatField('Special EQ',validators=[])
    effects = StringField('Effects',validators=[])
    genre = StringField('Genre', validators=[])
    submit = SubmitField('Submit')


class AddSoundForm(FlaskForm):
    name = StringField('Name', validators=[])
    genre = StringField('Genre', validators=[])
    amp_id = IntegerField('Amplifier ID',validators=[])
    instrument_id = IntegerField('Instrument ID',validators=[])
    setting_id = IntegerField('Setting ID',validators=[])
    descript = StringField('Description',validators=[])
    sample = StringField('Sample URL', validators=[URL(message='Must be a valid URL'), Optional()])
    submit = SubmitField('Submit')

class LoginForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

