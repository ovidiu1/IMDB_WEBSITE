from flask import Flask, render_template, redirect, url_for, session, request, session, flash
from flask_oauth import OAuth
from functools import wraps
from imdb import IMDb


app = Flask(__name__)
app.secret_key = 'secret key'

def login_required(f):
	@wraps(f)
	def wrap(*args, **kwargs):
		if 'logged_in' in session:
			return f(*args, **kwargs)
		else:
			flash('You need to login to view this page.')
			return redirect(url_for('login'))
	return wrap

@app.route("/")
def home():
	if 'logged_in' in session:
		flash('You are logged in')
		return render_template("home.html")
	else:
		return render_template("home.html")

@app.route("/blog")
@login_required
def blog():
	if 'logged_in' in session:
		flash('You are logged in')
		return render_template("blog.html")
	else:
		return render_template("blog.html")

@app.route("/movies")
def movies():
	if 'logged_in' in session:
		flash('You are logged in')
		return render_template("movies.html")

	ia = IMDb()
	s_result = ia.search_movie('X')
	
	return render_template("movies.html", movies=s_result)


@app.route('/login', methods=['GET', 'POST'])
def login():
	error = None
	if request.method == 'POST':
		if request.form['username'] != 'admin' or request.form['password'] != 'admin':
			error = 'Invalid credentials. Please try again.'
		else:
			session['logged_in'] = True
			return redirect(url_for('home'))
	return render_template('login.html', error=error)

@app.route('/logout')
def logout():
	session.pop('logged_in', None)
	return redirect(url_for('home'))


'''

SECRET_KEY = 'development key'
DEBUG = True
FACEBOOK_APP_ID = '188477911223606'
FACEBOOK_APP_SECRET = '621413ddea2bcc5b2e83d42fc40495de'

app = Flask(__name__)
app.debug = DEBUG
app.secret_key = SECRET_KEY
oauth = OAuth()

facebook = oauth.remote_app('facebook',
    base_url='https://graph.facebook.com/',
    request_token_url=None,
    access_token_url='/oauth/access_token',
    authorize_url='https://www.facebook.com/dialog/oauth',
    consumer_key=FACEBOOK_APP_ID,
    consumer_secret=FACEBOOK_APP_SECRET,
    request_token_params={'scope': 'email'}
)

@app.route('/login')
def login():
    return facebook.authorize(callback=url_for('facebook_authorized',
        next=request.args.get('next') or request.referrer or None,
        _external=True))


@app.route('/login/authorized')
@facebook.authorized_handler
def facebook_authorized(resp):
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        )
    session['oauth_token'] = (resp['access_token'], '')
    me = facebook.get('/me')
    return render_template("home.html", value='Logged in as %s' % \
        (me.data['name']))


@facebook.tokengetter
def get_facebook_oauth_token():
    return session.get('oauth_token')
'''

if __name__ == "__main__":
    app.run()



