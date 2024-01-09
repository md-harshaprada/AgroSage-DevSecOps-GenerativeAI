from flask import Flask, jsonify, request, session, redirect
from passlib.hash import pbkdf2_sha256
from app import db
import uuid
import smtplib
from email.message import EmailMessage

class User:

  def start_session(self, user):
    del user['password']
    session['logged_in'] = True
    session['user'] = user
    return jsonify(user), 200

  def signup(self):
    print(request.form)

    # Create the user object
    user = {
      "_id": uuid.uuid4().hex,
      "name": request.form.get('name'),
      "email": request.form.get('email'),
      "password": request.form.get('password'),
      "location":request.form.get('location'),
      "profession":request.form.get('profession')
    }

    # Encrypt the password
    user['password'] = pbkdf2_sha256.encrypt(user['password'])

    # Check for existing email address
    if db.user.find_one({ "email": user['email'] }):
      return jsonify({ "error": "Email address already in use" }), 400

    if db.user.insert_one(user):
      senderemail="menthealthnd@gmail.com"
      recemail=user["email"]
      password='fjazggpptivmfvll'
      msg=EmailMessage()
      msg['Subject']="Mental Health - A new Direction"
      msg['From']=senderemail
      msg['To']=recemail
      message=f"Dear {user['name']}, \nWelcome to MentalHealth - A new Direction. We are concerned about the mental well-being of individuals and strive to offer guidance on how to cope with stress, anxiety, and other mental illnesses. It is possible to examine one's own personality by taking personality tests. On our website, we provide information on a wide range of mental health disorder causes. The contact information of the mental health specialists is also available here.\n You don't have to struggle in silence"
      msg.set_content(message)
      server=smtplib.SMTP_SSL('smtp.googlemail.com',465)
      server.login(senderemail,password)
      print("LOgin success")
      server.send_message(msg=msg)
      print("email has been sent to", recemail)
      return self.start_session(user)

    return jsonify({ "error": "Signup failed" }), 400
  
  def signout(self):
    session.clear()
    return redirect('/')
  
  def login(self):

    user = db.user.find_one({
      "email": request.form.get('email')
    })

    if user and pbkdf2_sha256.verify(request.form.get('password'), user['password']):
      return self.start_session(user)
    
    return jsonify({ "error": "Invalid login credentials" }), 401