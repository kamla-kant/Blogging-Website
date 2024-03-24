'''
Refer Readme.txt
THIS IS EMPTY WEBSITE
'''

from datetime import datetime
from typing import Counter
import flask
from flask.templating import render_template
from flask import session

# Create App for our website
# ------------
my_website_app = flask.Flask(__name__)
my_website_app.secret_key = "MySecreteKey123"
# ------------
# ------------
# Handle 404 error
# ------------


@my_website_app.errorhandler(404)
def my_404_error_page(error):
    return "Page Under Construction"
# ------------

# ------------
# # END POINT - 1 : http://127.0.0.1:5000/
# # ------------
# @my_website_app.route('/') # '/' is mapped to url http://127.0.0.1:5000/
# def my_home_page():
#     return "Wel Come"
# # ------------

# ------------
# END POINT - 2 : http://127.0.0.1:5000/
# ------------


@my_website_app.route('/')
def my_home_page():
    return flask.render_template('home.html')
# ------------
# ------------
# END POINT - 3 : http://127.0.0.1:5000/about
# ------------


@my_website_app.route('/about')
def my_about_page():
    return flask.render_template('about.html')
# ------------
# ------------
# END POINT - 4 : http://127.0.0.1:5000/login
# ------------


@my_website_app.route('/login')
def my_login_page():
    return flask.render_template('login.html')
# ------------
# ------------
# END POINT - 5 : http://127.0.0.1:5000/createaccount
# ------------


@my_website_app.route('/createaccount')
def my_createaccount_page():
    return flask.render_template('newuser.html')


# ------------
# END POINT - 6 : http://127.0.0.1:5000/addnewuser
# ------------
@my_website_app.route('/addnewuser', methods=['POST'])
def my_addnewuser_page():
    # Whatever the data we are entering in front end,
    # all the data will be captured by framework
    # and stored in 'flask.request.form' variable in the
    # form of dictionary
    # flask.request.form = {'uname':'entered data', 'pw1': 'entered data' } etc
    entered_username = flask.request.form.get('uname')
    entered_password_1 = flask.request.form.get('pw1')
    entered_password_2 = flask.request.form.get('pw2')
    entered_email = flask.request.form.get('email')

    if entered_password_1 != entered_password_2:
        return "Password didn't match <a href='/createaccount'>Go Back</a>"
    else:
        # Store data in database

        # ------------------------
        # Connect to DB and create table if not exists
        # ------------------------
        import sqlite3

        print("Connect/Creating database 'my_website_db.sqlite3' ")
        my_db_connection = sqlite3.connect('my_website_db.sqlite3')
        print("Done")

        print("Get the cursor.(It help us to send query & retreive result)")
        my_db_cursor = my_db_connection.cursor()
        print("Done")

        print("Create a table if not exists")
        my_query = '''
        CREATE TABLE IF NOT EXISTS MYUSERS(
        NAME VARCHAR(100),
        PASSWORD VARCHAR(100),
        EMAIL VARCHAR(100)
        )
        '''

        print("Executing Query : ", my_query)
        my_db_cursor.execute(my_query)
        print("Done")
        # ------------------------

        # ------------------------
        # Check Whether username already exists
        # ------------------------
        my_query = f"SELECT NAME FROM MYUSERS WHERE NAME='{entered_username}' AND PASSWORD='{entered_password_1}'"
        print("Check Whether username already exists")
        print("Executing Query : ", my_query)
        my_db_cursor.execute(my_query)
        my_db_result = my_db_cursor.fetchall()
        if len(my_db_result) > 0:  # Then user record found
            print("Username already exists")
            return "Username already exists <a href='/createaccount'>Go Back</a>"
        else:
            print("Username Doesn't exists. Proceeding to account creation")
            # ------------------------

            # ------------------------
            # Create Account
            # ------------------------
            # Insert into table
            my_query = f"INSERT INTO MYUSERS VALUES('{entered_username}', '{entered_password_1}', '{entered_email}')"
            print("Executing Query : ", my_query)
            my_db_cursor.execute(my_query)
            print("Done")

            my_db_connection.commit()
            print("User account created")
            print("Closing DB")
            my_db_connection.close()
            print("Done")
            return flask.render_template("login.html")
# ------------

# ------------
# END POINT - 7 : http://127.0.0.1:5000/validatelogin
# ------------


@my_website_app.route("/validatelogin", methods=["POST"])
def my_validate_login_page():
    entered_username = flask.request.form.get('uname')
    entered_password = flask.request.form.get('pw')
    try:
        import sqlite3

        print("Connect/Creating database 'my_website_db.sqlite3' ")
        my_db_connection = sqlite3.connect('my_website_db.sqlite3')
        print("Done")

        print("Get the cursor.(It help us to send query & retreive result)")
        my_db_cursor = my_db_connection.cursor()
        print("Done")

        my_query = f"SELECT NAME FROM MYUSERS WHERE NAME='{entered_username}' AND PASSWORD='{entered_password}'"
        print("Check Whether username already exists")
        print("Executing Query : ", my_query)
        my_db_cursor.execute(my_query)
        my_db_result = my_db_cursor.fetchall()

        if len(my_db_result) > 0:  # Then user record found
            print("Username already exists. So Login Success")
            # return "Login Success <a href='/'>Go To Home Page</a>"
            # flask.flash('You were successfully logged in')
            session['username'] = entered_username
            return flask.redirect("/main")
            # return flask.render_template('main.html',len=0,result=[])
        else:
            return "Login Failed (Wrong Credentials) <a href='/login'>Goto Login</a>"

    except:
        # If table not present then error
        # also any other error as well
        return "Check whether you created the account <a href='/createaccount'>Create Account</a>"
# ------------


@my_website_app.route('/newpost')
def new_post():
    # If not loggeed in redirect to login page
    u = session.get('username')
    if u is None:  # Not logged in
        return flask.redirect("/login")
    else:
        return flask.render_template('newpost.html')


@my_website_app.route('/main')
def main():
    # If not loggeed in redirect to login page
    u = session.get('username')
    if u is None:  # Not logged in
        return flask.redirect("/login")
    else:
        import sqlite3
        print("Connect/Creating database 'my_website_db.sqlite3' ")
        my_db_connection = sqlite3.connect('my_website_db.sqlite3')
        print("Done")

        print("Get the cursor.(It help us to send query & retreive result)")
        my_db_cursor = my_db_connection.cursor()
        print("Done")
        try:
            my_query = "SELECT * FROM POSTS"
            print("Check Whether username already exists")
            print("Executing Query : ", my_query)
            my_db_cursor.execute(my_query)
            print("executed")
            my_db_result = my_db_cursor.fetchall()
            my_db_result = my_db_result[::-1]
            print("fetched")
            print(my_db_result)
            return flask.render_template('main.html', result=my_db_result)
        except:
            return flask.render_template('main.html', result=[])


@my_website_app.route('/post', methods=['GET', 'POST'])
def post_blog():
    # If not loggeed in redirect to login page
    u = session.get('username')
    if u is None:  # Not logged in
        return flask.redirect("/login")
    else:
        title = flask.request.form.get('title')
        content = flask.request.form.get('content')
        date = datetime.now().strftime("%d %b,%y ")
        u = str(session.get('username'))
        # Store data in database

        # ------------------------
        # Connect to DB and create table if not exists
        # ------------------------
        import sqlite3

        print("Connect/Creating database 'my_website_db.sqlite3' ")
        my_db_connection = sqlite3.connect('my_website_db.sqlite3')
        print("Done")

        print("Get the cursor.(It help us to send query & retreive result)")
        my_db_cursor = my_db_connection.cursor()
        print("Done")

        print("Create a table if not exists")
        my_query = '''
        CREATE TABLE IF NOT EXISTS POSTS(
        TITLE VARCHAR(100),
        CONTENT VARCHAR(1000),
        DATE VARCHAR(100),
        USERNAME VARCHAR(100)
        )
        '''
        my_db_cursor.execute(my_query)
        my_query = f"INSERT INTO POSTS VALUES('{title}', '{content}', '{date}','{u}')"
        print("Executing Query : ", my_query)
        my_db_cursor.execute(my_query)
        print("Done")

        my_db_connection.commit()
        print("User account created")
        print("Closing DB")
        my_query = "SELECT * FROM POSTS"
        print("Check Whether username already exists")
        print("Executing Query : ", my_query)
        my_db_cursor.execute(my_query)
        print("executed")
        my_db_result = my_db_cursor.fetchall()
        print("fetched")
        print(my_db_result)
        my_db_connection.close()
        print("Done")
        return flask.redirect('/main')


@my_website_app.route('/blogs')
def show_blogs():
    import sqlite3
    print("Connect/Creating database 'my_website_db.sqlite3' ")
    my_db_connection = sqlite3.connect('my_website_db.sqlite3')
    print("Done")

    print("Get the cursor.(It help us to send query & retreive result)")
    my_db_cursor = my_db_connection.cursor()
    print("Done")
    try:
        my_query = "SELECT * FROM POSTS ORDER BY DATE DESC"
        print("Check Whether username already exists")
        print("Executing Query : ", my_query)
        my_db_cursor.execute(my_query)
        print("executed")
        my_db_result = my_db_cursor.fetchall()
        my_db_result = my_db_result[::-1]
        print("fetched")
        print(my_db_result)
        return flask.render_template('blogs.html', result=my_db_result)
    except:
        return flask.render_template('blogs.html', result=[])


@my_website_app.route('/mypost')
def my_post():
    # If not loggeed in redirect to login page
    u = session.get('username')
    if u is None:  # Not logged in
        return flask.redirect("/login")
    else:
        import sqlite3
        print("Connect/Creating database 'my_website_db.sqlite3' ")
        my_db_connection = sqlite3.connect('my_website_db.sqlite3')
        print("Done")

        print("Get the cursor.(It help us to send query & retreive result)")
        my_db_cursor = my_db_connection.cursor()
        print("Done")
        try:
            u = str(u)
            my_query = f"SELECT * FROM POSTS WHERE USERNAME='{u}' ORDER BY DATE DESC"
            print("Check Whether username already exists")
            print("Executing Query : ", my_query)
            my_db_cursor.execute(my_query)
            print("executed")
            my_db_result = my_db_cursor.fetchall()
            # my_db_result = my_db_result[::-1]
            print("fetched")
            print(my_db_result)
            len = Counter(my_db_result)
            return flask.render_template('myposts.html', result=my_db_result, len=len)
        except:
            return flask.render_template('myposts.html', result=[])
# ------------
# Run Web Server
# ------------
# my_website_app.run()
# my_website_app.run(host='127.0.0.1', port=1234)


@my_website_app.route("/logout", methods=["GET", "POST"])
def my_logout_page():
    del session["username"]
    return flask.redirect('/')


# ------------
if __name__ == "__main__":
    my_website_app.run(debug=True)
