from flask import Flask, render_template, redirect,url_for,request
from flask_mail import Mail, Message
import pandas as pd
import os
from mailbot import Mailbot
import time

app = Flask(__name__)

app.config.update(dict(
    DEBUG = True,
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = 587,
    MAIL_USE_TLS = True,
    MAIL_USE_SSL = False,
    MAIL_USERNAME = 'admin@email.com',
    MAIL_PASSWORD = 'Password of admin'  
))

app.config['SECRET_KEY']= 'jhkjsmnbctyrWESTFVjhBJGXGJHBbojslazmYty2478uiH0898nkjjkv8932ink'
app.config['DEBUG']=True


@app.route('/')
@app.route('/<string:message>')
def home(message=""):
    return render_template('index.html',message=message)

@app.route('/submit',methods=['POST','GET'])
def submit():
    try:
        if request.method == "POST":
            rec_type = request.form['recievertype']
            file = request.files['inpfile']
            file.save('static/data.csv')
            df = sending(rec_type)

            return redirect(url_for('home',message="All mail has successfully send"))
        else:
            return redirect(url_for('home',message="Method not match"))
    except:
        return "<h1>Something went wrong...</h1>"
    

def sending(rec_type=""):
    try:
        df = pd.read_csv('static/data.csv')
        fname = "templates/mail-template/registered.html" if rec_type=="registered" else "templates/mail-template/unregistered.html"
        mail = Mail(app)
        print(f'\n\n\n{fname}\n\n\n')
        html_file = open(fname, 'r', encoding='utf-8')
        source_code = html_file.read()
        bot = Mailbot('admin@email.com',"password of admin's email")
        track_bounce=[]
        t1 = time.localtime()
        with mail.connect() as conn:
            for i in range (min(df.shape[0],2)):

                msg = Message(
                    'Subject-for-mail',
                    sender=('Sender-name','admin@email.com'),
                    recipients=[df['Email'][i]],
                    body=source_code.format(df['Name'][i].upper()),
                    html=source_code.format(df['Name'][i])
                )
                conn.send(msg)
                os.system('clear')

                if bot.is_email_bounced(df['Email'][i]):
                    track_bounce.append(1)
                    print("\n\n\nbounced\n\n\n")
                else:
                    track_bounce.append(0)
                    print(f"Mail to: {df['Name'][i]} : {df['Email'][i]}" )
                    print(f"total email send: {i+1} \n\n\n")
        t2 = time.localtime()
        tt = (abs(t2.tm_min-t1.tm_min)*60) + abs(t2.tm_sec-t1.tm_sec)
        df["Bounce Status"] = track_bounce  
        print(f"\nTotal time {tt}")
        return df
    except:
        return 0
    
    
if __name__=="__main__":
    app.run(debug=1,port=5000)