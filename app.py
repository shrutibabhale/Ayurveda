# Importing necessary Libraries
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, redirect, flash, url_for
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
import pickle
import numpy as np
import warnings 
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
login_manager.login_view = 'login'

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
    email = StringField(validators=[InputRequired(), Length(min=4, max=35)], render_kw={"placeholder": "Email", "class": "h-8 w-full rounded-md border border-slate-300 text-sm pl-2 bg-transparent shadow-sm"})

    password = PasswordField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Password", "class": "h-8 w-full rounded-md border border-slate-300 text-sm pl-2 bg-transparent  shadow-sm"})

    submit = SubmitField('Login', render_kw={"class": "bg-black w-full h-10 cursor-pointer text-white rounded-md text-sm"})

#Loading Diease Dectection Pickle File
f = open("DecisionTree-Model.sav", "rb")
model_N = pickle.load(f)
# Creating a Medical form to intergrate Medicine Recommendation Model

# Creating Symptoms dropdown Menu for selecting Symptoms
class serviceForm(FlaskForm):
    choices = [ ('', ' Select a Symptom'),
               (0,'abhighataja vedana'),
               (1,'abhishyanda'),
                (2,'adhamana'),
                (3,'agnidagdha'),	
                 (4,'agnimandhya'),
                  (5,'Agnimandya'),
                  (6,'agnimandya udararoga'),
                   (7,'ajirna'),
                   (8,'akshepa'),
                   (9,'ama'),(10,'amadosha'),	
(11,'amajirna'),
(12,'amashula'),
(13,'amatisara'),
(14,'amavata'),
(15,'amlapitta'),
(16,'amvata'),
(17,'anaha'),
(18,'angasthambha'),
(19,'angavedana'),
(20,'anidra'),
(21,'apachi'),
(22,'apasmara'),
(23,'apsmara'),
(24,'aptantrak'),
(25,'arbuda'),
(26,'ardhavbhedaka'),
(27,'ardita'),	
(28,'arma'),
(29,'arochaka'),
(30,'Arsha'),
(31,'arsha garbhasayaroga'),
(32,'aruchi'),
(33,'ashmari'),
(34,'asrigdara'),
(35,'asthibhagna'),
(36,'asthichyuti'),	
(37,'asthiruja'),
(38,'atisara'),
(39,'avabahuka'),	
(40,'badhirya'),
(41,'bahushosha'),	
(42,'bala Shosha'),	
(43,'balagraha'),
(44,'balakshaya'),	
(45,'balaroga'),
(46,'balya'),
(47,'bhagandar'),	
(48,'bhagandara'),	
(49,'bhrama'),
(50,'bhru-shankha-karna shula')	,
(51,'bhutonmada'),
(52,'budhidaurbalya'),	
(53,'charma vikara'),
(54,'charmkila'),
(55,'chhardi'),
(56,'dadru'),
(57,'dagdha vrana'),
(58,'daha')	,
(59,'danta roga'),	
(60,'daurbalya'),
(61,'dhatukshaya'),
(62,'drishtidaurbalya'),	
(63,'drishtimandya'),
(64,'dushta vrana')	,
(65,'galaganda'),
(66,'galaroga'),
(67,'gandamala'),
(68,'garadosha'),
(69,'garavisha'),	
(70,'garbhadosha'),	
(71,	'grahani'),
(72,'grahaniroga'),	
(73,'granthi'),
(74,'gridhrasi'),	
(75,'gudapaka'),
(76,'gulma'),
(77,'halimaka'),	
(78,'hanustambha'),
(79,'hikka'),	
(80,'hriddaha'),	
(81,'hriddaurbalya'),	
(82,'hriddrava'),
(83,'hridroga'),
(84,'hridya'),
(85,'hritshula'),	
(86,'indralupta'),
(87,'Janghashula'),
(88,'Jara')	,
(889,'Jirna Jvara'),	
(90,'Jirna Pratishaya'),	
(91,'Jirna Pravahika'),
(92,'jvara'),
(93,'jvaratisara'),
(94,'kamala'),
(95,'kampa'),
(96,'kandu'),	
(97,'kandu visphota'),
(98,'kaphaja vrana'),
(99,'kaphavataja nadivrana'),
(100,'karnagutha'),
(101,'karnanada'),
(102,'karnashula'),
(103,'karnasrava'),
(104,'karshya'),
(105,'kasa')	,
(106,'kasa shvasa'),
(107,'kastartava'),
(108,'katigraha')	,
(109,'katishula')	,
(110,'keshapata'),
(111,'keshashata'),	
(112,'khalitya'),	
(113,'khalli'),
(114,'Khanja'),	
(115,'klaivya'),
(116,'kotha'),
(117,'krichhrartav'),
(118,'krimi'),
(119,'krimiroga'),
(120,'kshata')	,
(121,'kshatakshina'),	
(122,'kshaya'),
(123,'kshudrakushtha'),
(124,'kushta'),
(125,'kushtha'),
(126,'kustha'),	
(127,'madhumeha')	,
(128,'mahakushtha'),
(129,'mahavataroga'),
(130,'malabandha'),
(131,'malavarodha'),
(132,'manasa dosha'),
(133,'mandagni'),
(134,'manodaurbalya'),
(135,'manodosha'),
(136,'Manodvega'),
(137,'Manoroga'),
(138,'manyastambha'),	
(139,'medhya'),
(140,'medoroga'),
(141,'moha'),
(142,'mukha roga'),
(143,'mukhapaka'),
(144,'mukhdaurgandhya'),
(145,'murchha'),
(146,'mutraghata'),	
(147,'mutrakriccha'),
(148,'mutrakricchra'),
(149,'mutraroga'),
(150,'mutrashmari'),
(151,'Mutrasthila'),	
(152,'nadi vrana'),
(153,'nadivrana'),
(154,'netraroga'),
(155,'netravrana'),	
(156,'ojakshya'),
(157,'padadaha'),
(158,'pakshaghat'),	
(159,'pakshaghata'),	
(160,'Pakshavadha'),
(161,'paktishula'),
(162,'palitya'),
(163,'pama')	,
(164,'pandu')	,
(165,'pandu duarbalya'),
(166,'pangu')	,
(167,'panguvata')	,
(168,'parinamashula'),	
(169,'parinamshula'),
(170,'parshva shula')	,
(171,'parshvashula')	,
(172,'pinasa')	,
(173,'pitta dushti'),
(174,'pitta jvara'),
(175,'pittaja netraroga'),	
(176,'pittaja netravyadhi'),
(177,'pittaja shirahshula'),
(178,'pittajaroga'),
(179,'pittaroga')	,
(180,'pliha'),
(181,'pliha- yakridroga'),
(182,'pliharoga')	,
(183,'pliharoga'),
(184,'prameha'),
(185,'pramehapidika'),	
(186,'prasavottara lakshana'),
(187,'prasavottara roga'),
(188,'praseka'),
(189,'pratishyaya'),
(190,'pravahika'),
(191,'prishashula'),	
(192,'rajayakshma'),
(193,'rajodosha'),
(194,'rajodushti'),
(195,'rajorodha'),
(196,'raktadushti'),	
(197,'raktaj pravahika'),	
(198,'raktajroga'),
(199,'raktanishthivana'),	
(200,'raktapitta'),
(201,'raktapradara'),
(202,'raktarsha')	,
(203,'raktasrava'),	
(204,'raktatisara'),
(205,'rasayana'),
(206,'sandhi shula'),
(207,'sandhigata vata'),
(208,'sandhigatavata'),
(209,'sandhigatvata'),
(210,'sandhigraha'),
(211,'sandhivedana')	,
(212,'sarpadamsha'),
(213,'sarvaJvara'),	
(214,'sharkara'),
(215,'shirahshula'),	
(216,'shirogatavata'),	
(217,'shirokampa'),
(218,'shiroroga'),
(219,'shitapitta'),	
(220,'shosha'),
(221,'shotha'),	
(222,'shukrameha'),	
(223,'shula')	,
(224,'shula yukta bradhna'),	
(225,'shulahara')	,
(226,'Shvasa'),
(227,'shveta pradara'),
(228,'shvitra'),
(229,'shwetapradara'),	
(230,'smriti and buddhi vardhaka'),
(231,'smriti daurbalya')	,
(232,'smritibhransha'),
(233,'smritidaurbalya'),	
(234,'smritikshaya'),
(235,'somaroga'),
(236,'sthanika'),
(237,'shotha'),
(238,'sthaulya'),
(239,'striroga'),
(240,'sukradosha'),
(241,'suryavarta'),	
(242,'sutika vata'),	
(243,'sutikadosha'),	
(244,'sutikaroga'),
(245,'svarabheda'),	
(246,'svarakshaya'),
(247,'svarbheda'),
(248,'timira'),
(249,'trikshula'),
(250,'trisha'),
(251,'trishna'),
(252,'tvak roga'),	
(253,'tvak vikara'),	
(254,'tvakroga'),
(255,'udara'),
(256,'Udararoga'),	
(257,'udarashula'),	
(258,'udarda'),
(259,'Udavarta'),
(260,'udvega'),
(261,'unmada'),
(262,'upadansha'),	
(263,'urahkshata'),	
(264,'urdhvaga raktapitta'),
(265,'urdhvajatrugataroga'),
(266,'urushula'),
(267,'urustambha'),
(268,'vandhyaroga'),	
(269,'Vandhyatva'),
(270,'vastigatas hula'),
(271,'vata rakta'),
(272,'vata roga'),
(273,'vata vikara'),
(274,'vata vyadhi'),
(275,'vatajashula'),
(278,'vatakaphaja roga'),	
(279,'vatarakta'),
(280,'vataraktaruja'),	
(281,'vataroga'),
(282,'vatashlaismika pratishyaya'),	
(283,'vatashonita'),
(284,'vatroga'),
(285,'Vibandha'),	
(286,'vicharchika'),
(287,'vidagdhajirna'),
(288,'vidarika'),
(289,'vidradhi'),	
(290,'vidvibandha'),
(291,'visarpa'),
(292,'visavikara'),	
(293,'vishama jvara'),	
(294,'vishma jvara'),
(295,'vishuchika'),
(296,'visuchika'),
(297,'vrana'),
(298,'vranaropana'),	
(299,'vranashotha'),
(300,'vriddhiroga'),	
(301,'vrishya'),
(302,'yakshma'),	
(303,'yonibhransha'),	
(304,'yonidosha'),
(305,'yoniroga'),
(306,'yonishula'),	
(307,'yonivyapat'),
]
   
    symptom1 = SelectField('1st Symptom', render_kw={"style":"width:190px;"},choices=choices, default= None,validators=[DataRequired ()])
    symptom2 = SelectField('2nd Symptom', render_kw={"style":"width:190px;"},choices=choices, default= None,validators=[DataRequired ()])
    symptom3 = SelectField('3rd Symptom', render_kw={"style":"width:190px;"},choices=choices, default= None,validators=[DataRequired ()])
    symptom4 = SelectField('4th Symptom',render_kw={"style":"width:190px;"}, choices=choices, default= None,validators=[DataRequired ()])

#Defining a fucntion to convert user inputs and predict
def serviceValidation(selected_symptoms):

    
    # convert list to NumPy array
    inputs = np.array([selected_symptoms])
    inputs = inputs.reshape(1, -1)


    # Pass the inputs to your machine learning model and retrieve the predicted result
    predicted_result = model_N.predict(inputs)
    print(predicted_result[0])

    # Return the predicted result to the user
    return predicted_result[0]





@app.route('/')
def index():
    return render_template("index.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('service'))
        else:
            # login failed, display error message
            flash('Invalid email or password. Please try again.', 'error')
    return render_template('login.html', form=form)



@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        print(form.password.data)
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User( firstname=form.firstname.data, lastname=form.lastname.data, age=form.age.data, gender=form.gender.data,email=form.email.data, address=form.address.data, password=hashed_password, pastcondition=form.pastcondition.data)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('register.html', form=form)

@app.route('/service', methods=['GET','POST'])
@login_required
def service():
    global predicted_result
    user = User.query.filter_by(id=current_user.id).first()
    form = serviceForm()
    if current_user.is_authenticated:
        if form.validate_on_submit():
            flash(f'WELCOME {current_user.firstname} ')
            selectedSymptoms = [form.symptom1.data, form.symptom2.data, form.symptom3.data, form.symptom4.data]
            predicted_result = serviceValidation(selectedSymptoms)

            return render_template('service.html', form=form, predicted_result=predicted_result, id=user.id, name=user.firstname.upper(), age=user.age, gender=user.gender)
        return render_template('service.html', form=form, id=user.id, name=user.firstname.upper(), age=user.age, gender=user.gender)
    
    else:
        return redirect(url_for('login'))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You logged out successfully!!")
    return render_template("index.html")

@app.route('/doc_service')
@login_required
def doc_service():
    user= User.query.filter_by(id=current_user.id).first()
    return render_template("doc_service.html",id=user.id,name=user.firstname.upper(),age=user.age,gender=user.gender)

   
    
@app.route('/druglist')
def druglist():  # put application's code here
    return render_template("druglist.html")

@app.route('/DrugInformation')
def DrugInformation():  # put application's code here
    return render_template("Druginformation.html")




@app.route('/faq')
def faq():  # put application's code here
    return render_template("faq.html")

@app.route('/termsconditon')
def termscondition(): # put application's code here
    return render_template("termscondition.html")



if __name__ == '__main__':
    app.run(debug=True)


