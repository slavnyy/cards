# -*- coding: utf-8 -*-
#!/usr/bin/env python
from datetime import datetime
from flask import Flask
from flask import render_template
from flask import request
from flask import url_for
from flask import redirect
from flask import flash
from flask_mail import Mail
from forms import ResultForm, UserForm
from flask_login import current_user
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemyUserDatastore, login_required, roles_required
card = Flask(__name__)


card.config.from_object("config.Config")

db = SQLAlchemy(card)

from models import *#import Result, User, Role, RolesUsers


mail = Mail(card)
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(card, user_datastore)



def can_user_edit_profile(current_user,id):
	user = Result.query.get_or_404(id)
	print current_user.email, user.personal_email
	if current_user.email == user.personal_email:
		return True
	return False

def can_user_edit_card(current_user,card_id):
	card = Result.query.get_or_404(card_id)
	print current_user.id, card.user_id
	if current_user.id == card.user_id:
		return True
	return False

@card.route("/")
def start_page():
	form = ResultForm()
	if current_user.is_authenticated:
		print "AUTHED",current_user,current_user.id
	return render_template("index.html",form=form)

@card.route("/about")
def about_page():
	return render_template("about.html")


@card.route('/cards',methods=['GET','POST'])
def list_result():
	results = Result.query.filter(Result.is_displayed.is_(True)).all()
	return render_template('results.html',results=results)


@card.route('/cards/edit/<int:id>',methods=['GET','POST'])
@roles_required('admin')
def edit_result(id):
	result = Result.query.get_or_404(id)
	form = ResultForm(obj=result)
	if form.validate_on_submit():
		form.populate_obj(result)
		db.session.commit()
	else:
		print form, form.errors
	print form.last_name.data
	return render_template("edit.html",result=form,id=id)


@card.route('/profile/add_card', methods=['GET','POST'])
@login_required
def card_create():
	form = ResultForm()
	if form.validate_on_submit():
		form.user_id.data = current_user.id
		result = Result()
		form.populate_obj(result)
		db.session.add(result)
		db.session.commit()
		return redirect(url_for('profile_show',id=current_user.id))
	else:
		print form.errors
	return render_template('add_card.html',form=form)


@card.route('/card/<int:card_id>/edit',methods=['GET','POST'])
@login_required
def card_edit(card_id):
	if can_user_edit_card(current_user,card_id):
		form = ResultForm(obj=Result.query.get_or_404(card_id))
		if form.validate_on_submit():
			form.populate_obj(Result.query.get_or_404(card_id))
			db.session.commit()
			return redirect(url_for('profile_show',id=current_user.id))
		else:
			print form.errors
		return render_template("card_edit.html",result=form,id=card_id)
	return redirect(url_for('start_page'))


@card.route('/profile/<int:id>',methods=['GET'])
@login_required
def profile_show(id):
	results = Result.query.filter(Result.user_id == id).all()
	return render_template("profile.html",results=results,profile_showid=id)




if __name__ == '__main__':
	card.run(debug=True,host="0.0.0.0")