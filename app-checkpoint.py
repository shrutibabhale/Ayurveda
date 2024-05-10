# Importing necessary Libraries
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, redirect, flash, url_for
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
import pickle
import numpy as np
import warningssudo apt-get install python-devsudo apt-get install python-devsudo apt-get install python-dev,
from sklearn.exceptions import DataConversionWarning
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, IntegerField
from wtforms.validators import InputRequired, Length, ValidationError, DataRequired
from flask_bcrypt import Bcrypt


# Ignoring User warnings and Data Conversion Warning
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=DataConversionWarning)

# Establishing Flask Connection
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'secretkey'

#
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'signin'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Defining the table columns
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(80), nullable=False)
    lastname = db.Column(db.String(80), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    email = db.Column(db.String(40), nullable=False, unique=True)
    address = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(80), nullable=False)
    pastcondition = db.Column(db.String(80), nullable=False)

#Defining a class called RegisterForm, which inherits from FlaskForm
class RegisterForm(FlaskForm):
    firstname = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "First Name", "class": "h-8 w-full rounded-md border border-slate-300 text-sm pl-2 bg-transparent shadow-sm"})
    lastname = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Last Name", "class": "h-8 w-full rounded-md border border-slate-300 text-sm pl-2 bg-transparent shadow-sm"})
    age = IntegerField(validators=[InputRequired()], render_kw={"placeholder": "Age", "class": "h-8 w-full rounded-md border border-slate-300 text-sm pl-2 bg-transparent shadow-sm"})
    gender = SelectField('Gender', choices=[('Male','Male'),('Female','Female')], render_kw={"class": "text-sm mx-1"})
    email = StringField(validators=[InputRequired(), Length(min=10, max=40)], render_kw={"placeholder": "Email", "class": "h-8 w-full rounded-md border border-slate-300 text-sm pl-2 bg-transparent shadow-sm"})
    address = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Enter your City", "class": "h-8 w-full rounded-md border border-slate-300 text-sm pl-2 bg-transparent  shadow-sm"})
    password = PasswordField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Password", "class": "h-8 w-full rounded-md border border-slate-300 text-sm pl-2 bg-transparent  shadow-sm"})
    pastcondition = StringField(validators=[InputRequired(), Length(min=4, max=80)], render_kw={"placeholder": "Past Conditions", "class": "h-20 w-full rounded-md border border-slate-300 text-sm pl-2 bg-transparent shadow-sm"})
    submit = SubmitField('Register', render_kw={"class": "bg-black w-full h-10 cursor-pointer text-white rounded-md text-sm"})

    # This is a validation method to check if a given email address already exists in the database.
    from flask import flash

    def validate_email(self, email):
        existing_user_email = User.query.filter_by(email=email.data).first()
        if existing_user_email:
            flash('That email already exists. Please choose a different one.', 'error')
            raise ValidationError('That email already exists. Please choose a different one.')


# Creating a login form for users to enter their email and password information, and submit it to the server for authentication..
class LoginForm(FlaskForm):
    email = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Email", "class": "h-8 w-full rounded-md border border-slate-300 text-sm pl-2 bg-transparent shadow-sm"})

    password = PasswordField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Password", "class": "h-8 w-full rounded-md border border-slate-300 text-sm pl-2 bg-transparent  shadow-sm"})

    submit = SubmitField('Login', render_kw={"class": "bg-black w-full h-10 cursor-pointer text-white rounded-md text-sm"})

#Loading Diease Dectection Pickle File
f = open("DecisionTree-Model.sav", "rb")
model_N = pickle.load(f)

#loading Medicine Recommendation Pickle file
f2 = open("drugTree.pkl", "rb")
model_med = pickle.load(f2)


#Mapping Symptoms as indexes in dataset using dictionary
symptom_mapping = {
'Abhighataja Vedana':1,
'Abhishyanda':2,
'Adhamana':3,
'Agnidagdha':4,	
'Agnimandhya':5,
'Agnimandya':6,
'Agnimandya Udararoga':7,
'Ajirna':8,
'Akshepa':9,
'Ama':10,
'Amadosha':11,	
'Amajirna':	12,
'Amashula':13,
'Amatisara':14,
'Amavata':15,
'Amlapitta':16,
'Amvata':17,
'Anaha':18,
'Angasthambha':19,
'Angavedana':20,
'Anidra':21,
'Apachi':22,
'Apasmara':23,
'Apsmara':24,
'Aptantrak':25,
'Arbuda':26,
'Ardhavbhedaka':27,
'Ardita':28,	
'Arma':29,
'Arochaka':30,
'Arsha':31,
'Arsha Garbhasayaroga':32,
'Aruchi':33,
'Ashmari':34,
'Asrigdara':35,
'Asthibhagna':36,
'Asthichyuti':37,	
'Asthiruja':38,
'Atisara':	39,
'Avabahuka':40,	
'Badhirya':	41,
'Bahushosha':42,	
'Bala Shosha':43,	
'Balagraha':44,
'Balakshaya':45,	
'Balaroga':46,
'Balya':47,
'Bhagandar':48,	
'Bhagandara':49,	
'Bhrama':50,
'Bhru-shankha-Karna Shula':	51,
'Bhutonmada':52,
'Budhidaurbalya':53,	
'Charma Vikara':54,
'Charmkila':55,
'Chhardi':	56,
'Dadru':	57,
'Dagdha Vrana':58,
'Daha':	59,
'Danta Roga':60,	
'Daurbalya':61,
'Dhatukshaya':62,
'Drishtidaurbalya':63,	
'Drishtimandya':64,
'Dushta Vrana':	65,
'Galaganda':66,
'Galaroga':	67,
'Gandamala':68,
'Garadosha':69,
'Garavisha':70,	
'Garbhadosha':71,	
'Grahani':	72,
'Grahaniroga':73,	
'Granthi':	74,
'Gridhrasi':75,	
'Gudapaka':	76,
'Gulma':77,
'Halimaka':78,	
'Hanustambha':79,
'Hikka':80,	
'Hriddaha':81,	
'Hriddaurbalya':82,	
'Hriddrava':83,
'Hridroga':84,
'Hridya':85,
'Hritshula':86,	
'Indralupta':87,
'Janghashula':	88,
'Jara':	89,
'Jirna Jvara':90,	
'Jirna Pratishaya':91,	
'Jirna Pravahika':92,
'Jvara':93,
'Jvaratisara':94,
'Kamala':95,
'Kampa':96,
'Kandu':97,	
'Kandu Visphota':98,
'Kaphaja Vrana':99,
'Kaphavataja Nadivrana':100,
'Karnagutha':101,
'Karnanada':102,
'Karnashula':103,
'Karnasrava':104,
'Karshya':105,
'Kasa':	106,
'Kasa Shvasa':107,
'Kastartava':108,
'Katigraha':109	,
'Katishula':110	,
'Keshapata':111,
'Keshashata':112,	
'Khalitya':113,	
'Khalli':114,
'Khanja':115,	
'Klaivya':116,
'Kotha':117,
'Krichhrartav':	118,
'Krimi':119	,
'Krimiroga':120,
'Kshata':	121,
'Kshatakshina':122,	
'Kshaya':123,
'Kshudrakushtha':124,
'Kushta':125,
'Kushtha':126,
'Kustha':127,	
'Madhumeha':128	,
'Mahakushtha':129,
'Mahavataroga':	130,
'Malabandha':131,
'Malavarodha':132,
'Manasa Dosha':133,
'Mandagni':	134,
'Manodaurbalya':135,
'Manodosha':136,
'Manodvega':137,
'Manoroga':	138,
'Manyastambha':139,	
'Medhya':140,
'Medoroga':	141,
'Moha':142,
'Mukha Roga':143,
'Mukhapaka':144,
'Mukhdaurgandhya':145,
'Murchha':146,
'Mutraghata':147,	
'Mutrakriccha':148,
'Mutrakricchra':149,
'Mutraroga':150,
'Mutrashmari':151,
'Mutrasthila':152,	
'Nadi Vrana':153,
'Nadivrana':154,
'Netraroga':155,
'Netravrana':156,	
'Ojakshya':	157,
'Padadaha':	158,
'Pakshaghat':159,	
'Pakshaghata':160,	
'Pakshavadha':161,
'Paktishula':162,
'Palitya':163,
'Pama':164	,
'Pandu':165	,
'Pandu Duarbalya':166,
'Pangu':167	,
'Panguvata':168	,
'Parinamashula':169,	
'Parinamshula':	170,
'Parshva shula':171	,
'Parshvashula':172	,
'Pinasa':173	,
'Pitta Dushti':	174,
'Pitta Jvara':175,
'Pittaja Netraroga':176,	
'Pittaja Netravyadhi':177,
'Pittaja Shirahshula':178,
'Pittajaroga':179,
'Pittaroga':180	,
'Pliha':181,
'Pliha- Yakridroga':182,
'Pliharoga':183	,
'Pradara':184,
'Prameha':185,
'Pramehapidika':186,	
'Prasavottara Lakshana':187,
'Prasavottara roga':188,
'Praseka':189,
'Pratishyaya':190,
'Pravahika':191,
'Prishashula':192,	
'Rajayakshma':193,
'Rajodosha':194,
'Rajodushti':195,
'Rajorodha':196,
'Raktadushti':197,	
'Raktaj Pravahika':198,	
'Raktajroga':199,
'Raktanishthivana':200,	
'Raktapitta':201,
'Raktapradara':	202,
'Raktarsha':203	,
'Raktasrava':204,	
'Raktatisara':205,
'Rasayana':	206,
'Sandhi Shula':207,
'Sandhigata Vata':208,
'Sandhigatavata':209,
'Sandhigatvata':210,
'Sandhigraha':211,
'Sandhivedana':	212,
'Sarpadamsha':213,
'SarvaJvara':214,	
'Sharkara':	215,
'Shirahshula':216,	
'Shirogatavata':217,	
'Shirokampa':218,
'Shiroroga':219,
'Shitapitta':220,	
'Shosha':221,
'Shotha':222,	
'Shukrameha':223,	
'Shula':224	,
'Shula Yukta Bradhna':225,	
'Shulahara':226	,
'Shvasa':227	,
'Shveta Pradara':228,
'Shvitra':229,
'Shwetapradara':230,	
'Smriti and Buddhi Vardhaka':231,
'Smriti Daurbalya':	232,
'Smritibhransha':233,
'Smritidaurbalya':234,	
'Smritikshaya':235,
'Somaroga':236,
'Sthanika':237,
'Shotha':238,
'Sthaulya':	239,
'Striroga':	240,
'Sukradosha':241,
'Suryavarta':242,	
'Sutika Vata':243,	
'Sutikadosha':244,	
'Sutikaroga':245,
'Svarabheda':246,	
'Svarakshaya':247,
'Svarbheda':248,
'Timira':249,
'Trikshula':250,
'Trisha':251,
'Trishna':252,
'Tvak Roga':253,	
'Tvak Vikara':254,	
'Tvakroga':	255,
'Udara':256,
'Udararoga':257,	
'Udarashula':258,	
'Udarda':259,
'Udavarta':260,
'Udvega':261,
'Unmada':262,
'Upadansha':263,	
'Urahkshata':264,	
'Urdhvaga Raktapitta':265,
'Urdhvajatrugataroga':266,
'Urushula':267,
'Urustambha':268,
'Vandhyaroga':269,	
'Vandhyatva':270,
'Vastigatas hula':271,
'Vata Rakta':272,
'Vata Roga':273,
'Vata Vikara':274,
'Vata Vyadhi':275,
'Vatajashula':276,
'Vatakaphaja Roga':277,	
'Vatarakta':278,
'Vataraktaruja':279,	
'Vataroga':280,
'Vatashlaismika Pratishyaya':281,	
'Vatashonita':282,
'Vatroga':283,
'Vibandha':284,	
'Vicharchika':285,
'Vidagdhajirna':286,
'Vidarika':287,
'Vidradhi':288,	
'Vidvibandha':289,
'Visarpa':	290,
'Visavikara':291,	
'Vishama Jvara':292,	
'Vishma Jvara':293,
'Vishuchika':294,
'Visuchika':295,
'Vrana':296,
'Vranaropana':297,	
'Vranashotha':298,
'Vriddhiroga':299,	
'Vrishya':300,
'Yakshma':301,	
'Yonibhransha':302,	
'Yonidosha':303,
'Yoniroga':304,
'Yonishula':305,	
'Yonivyapat':306,

}
# Creating a Medical form to intergrate Medicine Recommendation Model
class medForm(FlaskForm):
    gender = SelectField('Gender :', render_kw={"style": "width: 170px;"},choices=[('', ' Select your gender'),(1,' Male'),(0,' Female')],default= None,validators=[DataRequired()])
    age = StringField(validators=[InputRequired()],render_kw={"style": "width: 60px;","placeholder": "Age"})
    severity = SelectField('Severity :',  render_kw={"style": "width: 220px;"},choices=[('', 'Select the level of severity'),(0,'Few days'),(1,'A week'),(2,'Few weeks or more')],default= None,validators=[DataRequired()])
    disease = SelectField('Disease :',  render_kw={"style": "width: 150px;"}, choices=[('', ' Select the diease'),(0, 'Diarrhea'), (1, 'Gastritis'),(2, 'Arthritis'),(3, 'Migraine')],default= None,validators=[DataRequired()])

# Creating Symptoms dropdown Menu for selecting Symptoms
class serviceForm(FlaskForm):
    choices = [ ('', ' Select a Symptom'),
               ('Abhighataja Vedana','abhighataja vedana'),
               ('Abhishyanda','abhishyanda'),
                ('Adhamana','adhamana'),
                ('Agnidagdha','agnidagdha'),	
                 ('Agnimandhya','agnimandhya'),
                  ('Agnimandya','agnimandya'),
                  ('Agnimandya Udararoga','agnimandya udararoga'),
                   ('Ajirna','ajirna'),
                   ('Akshepa','akshepa'),
                   ('Ama','ama'),('Amadosha','amadosha'),	
('Amajirna','amajirna'),
('Amashula','amashula'),
('Amatisara','amatisara'),
('Amavata','amavata'),
('Amlapitta','amlapitta'),
('Amvata','amvata'),
('Anaha','anaha'),
('Angasthambha','angasthambha'),
('Angavedana','angavedana'),
('Anidra','anidra'),
('Apachi','apachi'),
('Apasmara','apasmara'),
('Apsmara','apsmara'),
('Aptantrak','aptantrak'),
('Arbuda','arbuda'),
('Ardhavbhedaka','ardhavbhedaka'),
('Ardita','ardita'),	
('Arma','arma'),
('Arochaka','arochaka'),
('Arsha','arsha'),
('Arsha Garbhasayaroga','arsha garbhasayaroga'),
('Aruchi','aruchi'),
('Ashmari','ashmari'),
('Asrigdara','asrigdara'),
('Asthibhagna','asthibhagna'),
('Asthichyuti','asthichyuti'),	
('Asthiruja','asthiruja'),
('Atisara','atisara'),
('Avabahuka','avabahuka'),	
('Badhirya','badhirya'),
('Bahushosha','bahushosha'),	
('Bala Shosha','bala Shosha'),	
('Balagraha','balagraha'),
('Balakshaya','balakshaya'),	
('Balaroga','balaroga'),
('Balya','balya'),
('Bhagandar','bhagandar'),	
('Bhagandara','bhagandara'),	
('Bhrama','bhrama'),
('Bhru-shankha-Karna Shula','bhru-shankha-karna shula')	,
('Bhutonmada','bhutonmada'),
('Budhidaurbalya','budhidaurbalya'),	
('Charma Vikara','charma vikara'),
('Charmkila','charmkila'),
('Chhardi','chhardi'),
('Dadru','dadru'),
('Dagdha Vrana','dagdha vrana'),
('Daha','daha')	,
('Danta Roga','danta roga'),	
('Daurbalya','daurbalya'),
('Dhatukshaya','dhatukshaya'),
('Drishtidaurbalya','drishtidaurbalya'),	
('Drishtimandya','drishtimandya'),
('Dushta Vrana','dushta vrana')	,
('Galaganda','galaganda'),
('Galaroga','galaroga'),
('Gandamala','gandamala'),
('Garadosha','garadosha'),
('Garavisha','garavisha'),	
('Garbhadosha','garbhadosha'),	
('Grahani',	'grahani'),
('Grahaniroga','grahaniroga'),	
('Granthi','granthi'),
('Gridhrasi','gridhrasi'),	
('Gudapaka','gudapaka'),
('Gulma','gulma'),
('Halimaka','halimaka'),	
('Hanustambha','hanustambha'),
('Hikka','hikka'),	
('Hriddaha','hriddaha'),	
('Hriddaurbalya','hriddaurbalya'),	
('Hriddrava','hriddrava'),
('Hridroga','hridroga'),
('Hridya','hridya'),
('Hritshula','hritshula'),	
('Indralupta','indralupta'),
('Janghashula','Janghashula'),
('Jara','Jara')	,
('Jirna Jvara','Jirna Jvara'),	
('Jirna Pratishaya','Jirna Pratishaya'),	
('Jirna Pravahika','Jirna Pravahika'),
('Jvara','jvara'),
('Jvaratisara','jvaratisara'),
('Kamala','kamala'),
('Kampa','kampa'),
('Kandu','kandu'),	
('Kandu Visphota','kandu visphota'),
('Kaphaja Vrana','kaphaja vrana'),
('Kaphavataja Nadivrana','kaphavataja nadivrana'),
('Karnagutha','karnagutha'),
('Karnanada','karnanada'),
('Karnashula','karnashula'),
('Karnasrava','karnasrava'),
('Karshya','karshya'),
('Kasa','kasa')	,
('Kasa Shvasa','kasa shvasa'),
('Kastartava','kastartava'),
('Katigraha','katigraha')	,
('Katishula','katishula')	,
('Keshapata','keshapata'),
('Keshashata','keshashata'),	
('Khalitya','khalitya'),	
('Khalli','khalli'),
('Khanja','Khanja'),	
('Klaivya','klaivya'),
('Kotha','kotha'),
('Krichhrartav','krichhrartav'),
('Krimi','krimi'),
('Krimiroga','krimiroga'),
('Kshata','kshata')	,
('Kshatakshina','kshatakshina'),	
('Kshaya','kshaya'),
('Kshudrakushtha','kshudrakushtha'),
('Kushta','kushta'),
('Kushtha','kushtha'),
('Kustha','kustha'),	
('Madhumeha','madhumeha')	,
('Mahakushtha','mahakushtha'),
('Mahavataroga','mahavataroga'),
('Malabandha','malabandha'),
('Malavarodha','malavarodha'),
('Manasa Dosha','manasa dosha'),
('Mandagni','mandagni'),
('Manodaurbalya','manodaurbalya'),
('Manodosha','manodosha'),
('Manodvega','Manodvega'),
('Manoroga','Manoroga'),
('Manyastambha','manyastambha'),	
('Medhya','medhya'),
('Medoroga','medoroga'),
('Moha','moha'),
('Mukha Roga','mukha roga'),
('Mukhapaka','mukhapaka'),
('Mukhdaurgandhya','mukhdaurgandhya'),
('Murchha','murchha'),
('Mutraghata','mutraghata'),	
('Mutrakriccha','mutrakriccha'),
('Mutrakricchra','mutrakricchra'),
('Mutraroga','mutraroga'),
('Mutrashmari','mutrashmari'),
('Mutrasthila','Mutrasthila'),	
('Nadi Vrana','nadi vrana'),
('Nadivrana','nadivrana'),
('Netraroga','netraroga'),
('Netravrana','netravrana'),	
('Ojakshya','ojakshya'),
('Padadaha','padadaha'),
('Pakshaghat','pakshaghat'),	
('Pakshaghata','pakshaghata'),	
('Pakshavadha','Pakshavadha'),
('Paktishula','paktishula'),
('Palitya','palitya'),
('Pama','pama')	,
('Pandu','pandu')	,
('Pandu Duarbalya','pandu duarbalya'),
('Pangu','pangu')	,
('Panguvata','panguvata')	,
('Parinamashula','parinamashula'),	
('Parinamshula','parinamshula'),
('Parshva shula','parshva shula')	,
('Parshvashula','parshvashula')	,
('Pinasa','pinasa')	,
('Pitta Dushti','pitta dushti'),
('Pitta Jvara','pitta jvara'),
('Pittaja Netraroga','pittaja netraroga'),	
('Pittaja Netravyadhi','pittaja netravyadhi'),
('Pittaja Shirahshula','pittaja shirahshula'),
('Pittajaroga','pittajaroga'),
('Pittaroga','pittaroga')	,
('Pliha','pliha'),
('Pliha- Yakridroga','pliha- yakridroga'),
('Pliharoga','pliharoga')	,
('Pradara','pliharoga'),
('Prameha','prameha'),
('Pramehapidika','pramehapidika'),	
('Prasavottara Lakshana','prasavottara lakshana'),
('Prasavottara roga','prasavottara roga'),
('Praseka','praseka'),
('Pratishyaya','pratishyaya'),
('Pravahika','pravahika'),
('Prishashula','prishashula'),	
('Rajayakshma','rajayakshma'),
('Rajodosha','rajodosha'),
('Rajodushti','rajodushti'),
('Rajorodha','rajorodha'),
('Raktadushti','raktadushti'),	
('Raktaj Pravahika','raktaj pravahika'),	
('Raktajroga','raktajroga'),
('Raktanishthivana','raktanishthivana'),	
('Raktapitta','raktapitta'),
('Raktapradara','raktapradara'),
('Raktarsha','raktarsha')	,
('Raktasrava','raktasrava'),	
('Raktatisara','raktatisara'),
('Rasayana','rasayana'),
('Sandhi Shula','sandhi shula'),
('Sandhigata Vata','sandhigata vata'),
('Sandhigatavata','sandhigatavata'),
('Sandhigatvata','sandhigatvata'),
('Sandhigraha','sandhigraha'),
('Sandhivedana','sandhivedana')	,
('Sarpadamsha','sarpadamsha'),
('SarvaJvara','sarvaJvara'),	
('Sharkara','sharkara'),
('Shirahshula','shirahshula'),	
('Shirogatavata','shirogatavata'),	
('Shirokampa','shirokampa'),
('Shiroroga','shiroroga'),
('Shitapitta','shitapitta'),	
('Shosha','shosha')
('Shotha','shotha'),	
('Shukrameha','shukrameha'),	
('Shula','shula')	,
('Shula Yukta Bradhna','shula yukta bradhna'),	
('Shulahara','shulahara')	,
('Shvasa','Shvasa'),
('Shveta Pradara','shveta pradara'),
('Shvitra','shvitra')
('Shwetapradara','shwetapradara'),	
('Smriti and Buddhi Vardhaka','smriti and buddhi vardhaka'),
('Smriti Daurbalya','smriti daurbalya')	,
('Smritibhransha','smritibhransha'),
('Smritidaurbalya','smritidaurbalya'),	
('Smritikshaya','smritikshaya'),
('Somaroga','somaroga'),
('Sthanika','sthanika'),
('Shotha','shotha'),
('Sthaulya','sthaulya'),
('Striroga','striroga'),
('Sukradosha','sukradosha'),
('Suryavarta','suryavarta'),	
('Sutika Vata','sutika vata'),	
('Sutikadosha','sutikadosha'),	
('Sutikaroga','sutikaroga'),
('Svarabheda','svarabheda'),	
('Svarakshaya','svarakshaya'),
('Svarbheda','svarbheda'),
('Timira','timira'),
('Trikshula','trikshula'),
('Trisha','trisha'),
('Trishna','trishna'),
('Tvak Roga','tvak roga'),	
('Tvak Vikara','tvak vikara'),	
('Tvakroga','tvakroga'),
('Udara','udara'),
('Udararoga','udararoga'),	
('Udarashula','udarashula'),	
('Udarda','udarda'),
('Udavarta','Udavarta'),
('Udvega','udvega'),
('Unmada','unmada'),
('Upadansha','upadansha'),	
('Urahkshata','urahkshata'),	
('Urdhvaga Raktapitta','urdhvaga raktapitta'),
('Urdhvajatrugataroga','urdhvajatrugataroga'),
('Urushula','urushula'),
('Urustambha','urustambha'),
('Vandhyaroga','vandhyaroga'),	
('Vandhyatva','Vandhyatva'),
('Vastigatas hula','vastigatas hula'),
('Vata Rakta','vata rakta'),
('Vata Roga','vata roga'),
('Vata Vikara','vata vikara'),
('Vata Vyadhi','vata vyadhi'),
('Vatajashula','vatajashula'),
('Vatakaphaja Roga','vatakaphaja roga'),	
('Vatarakta','vatarakta'),
('Vataraktaruja','vataraktaruja'),	
('Vataroga','vataroga'),
('Vatashlaismika Pratishyaya','vatashlaismika pratishyaya'),	
('Vatashonita','vatashonita'),
('Vatroga','vatroga'),
('Vibandha','vibandha'),	
('Vicharchika','vicharchika'),
('Vidagdhajirna','vidagdhajirna'),
('Vidarika','vidarika'),
('Vidradhi','vidradhi'),	
('Vidvibandha','vidvibandha'),
('Visarpa','visarpa'),
('Visavikara','visavikara'),	
('Vishama Jvara','vishama jvara'),	
('Vishma Jvara','vishma jvara'),
('Vishuchika','vishuchika'),
('Visuchika','visuchika'),
('Vrana','vrana'),
('Vranaropana','vranaropana'),	
('Vranashotha','vranashotha'),
('Vriddhiroga','vriddhiroga'),	
('Vrishya','vrishya'),
('Yakshma','yakshma'),	
('Yonibhransha','yonibhransha'),	
('Yonidosha','yonidosha'),
('Yoniroga','yoniroga'),
('Yonishula','yonishula'),	
('Yonivyapat','yonivyapat'),
]
   
    symptom1 = SelectField('1st Symptom', choices=choices, default= None,validators=[DataRequired()])
    symptom2 = SelectField('2nd Symptom', choices=choices, default= None,validators=[DataRequired()])
    symptom3 = SelectField('3rd Symptom', choices=choices, default= None,validators=[DataRequired()])
    symptom4 = SelectField('4th Symptom', choices=choices, default= None,validators=[DataRequired()])

#Defining a fucntion to convert user inputs and predict
def serviceValidation(selected_symptoms):

    # Convert the selected symptoms to a 30-element list of 1s and 0s
    inputs = [ 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,00,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0] 
    for symptom in selected_symptoms:
        if symptom:
            inputs[symptom_mapping[symptom]] = 1

    # convert list to NumPy array
    inputs = np.array(inputs)
    inputs = inputs.reshape(1, -1)


    # Pass the inputs to your machine learning model and retrieve the predicted result
    predicted_result = model_N.predict(inputs)
    print(predicted_result[0])

    # Return the predicted result to the user
    return predicted_result[0]


def medicineValidation(selectedOptions):
    """Defining a function to recommend medicine"""
    inputs = np.array(selectedOptions)  # convert list to NumPy array
    inputs = inputs.reshape(1, -1)
    # Pass the inputs to your machine learning model and retrieve the predicted result
    recommend_Med = model_med.predict(inputs)
    # Return the predicted result to the user
    return recommend_Med[0]


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/signin', methods=['GET', 'POST'])
def signin():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('service'))
        else:
            # login failed, display error message
            flash('Invalid email or password. Please try again.', 'error')
    return render_template('signin.html', form=form)



@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        print(form.password.data)
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User( firstname=form.firstname.data, lastname=form.lastname.data, age=form.age.data, gender=form.gender.data,email=form.email.data, address=form.address.data, password=hashed_password, pastcondition=form.pastcondition.data)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('signin'))

    return render_template('register.html', form=form)

@app.route('/service', methods=['GET','POST'])
@login_required
def service():
    global predicted_result
    user = User.query.filter_by(id=current_user.id).first()


    form = serviceForm()
    if form.validate_on_submit():
        selectedSymptoms = [form.symptom1.data, form.symptom2.data, form.symptom3.data, form.symptom4.data]
        predicted_result = serviceValidation(selectedSymptoms)

        return render_template('service.html', form=form, predicted_result=predicted_result, id=user.id, name=user.firstname.upper(), age=user.age, gender=user.gender)
    return render_template('service.html', form=form, id=user.id, name=user.firstname.upper(), age=user.age, gender=user.gender)


@app.route('/med_service', methods=['GET','POST'])
@login_required
def med_service():

    form = medForm()
    user = User.query.filter_by(id=current_user.id).first()

    if form.validate_on_submit():
        selectedOptions = [form.disease.data, form.age.data, form.gender.data, form.severity.data]
        recommend_Med = medicineValidation(selectedOptions)
        return render_template("med_service.html", form=form, predicted_result=recommend_Med.upper(), id=user.id, name=user.firstname.upper(), age=user.age, gender=user.gender)

    return render_template("med_service.html", form=form, id=user.id, name=user.firstname.upper(), age=user.age, gender=user.gender)


@app.route('/doc_service')
def doc_service():  # put application's code here
    user = User.query.filter_by(id=current_user.id).first()

    return render_template("doc_service.html",id=user.id, name=user.firstname.upper(), age=user.age, gender=user.gender)

@app.route('/faq')
def faq():  # put application's code here
    return render_template("faq.html")

if __name__ == '__main__':
    app.run(debug=True)
