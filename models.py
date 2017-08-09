# -*- coding: utf-8 -*-
#!/usr/bin/env python

from app import db
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.orm import relationship,backref
from sqlalchemy import ForeignKey
from flask_security import UserMixin, RoleMixin


class Result(db.Model):

	__tablename__ = 'results'

	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer,ForeignKey('users.id'))
	last_name = db.Column(db.String(100))
	first_name = db.Column(db.String(100))
	personal_email = db.Column(db.String(255))
	position = db.Column(db.String(200))
	organization_name = db.Column(db.String(200))
	organization_url = db.Column(db.String(50))
	organization_activity = db.Column(db.String(200))
	discount_percent = db.Column(db.String(128))
	is_displayed = db.Column(db.Boolean, unique=False, server_default='f',default=False)
	created  = db.Column(db.DateTime,default=db.func.current_timestamp())
	updated = db.Column(db.DateTime,default=db.func.current_timestamp(),onupdate=db.func.current_timestamp())


	#created = db.Column(db.TIMESTAMP(timezone=False))
	#updated = db.Column(db.TIMESTAMP(timezone=False))

	#json_data = db.Column(JSON)
	#__table_args__ = (db.UniqueConstraint('url', name='_url_uc'),
    #            )

#	def __init__(self,url):
#		self.url = url

	def __repr__(self):
		return '<id {}>'.format(self.id)


class User(db.Model, UserMixin):
	
	__tablename__ = 'users'
	
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(255),unique=True)
	username = db.Column(db.String(255))
	password = db.Column(db.String(255))
	last_login_at = db.Column(db.DateTime())
	current_login_at = db.Column(db.DateTime())
	last_login_ip = db.Column(db.String(100))
	current_login_ip = db.Column(db.String(100))
	login_count = db.Column(db.Integer)
	active = db.Column(db.Boolean)#,server_default='t',default=True
	confirmed_at = db.Column(db.DateTime())
	roles = relationship('Role', secondary='roles_users', 
						backref=backref('users',lazy='dynamic'))
	cards = relationship('Result',backref=backref('users'))

class Role(db.Model, RoleMixin):
	
	__tablename__ = 'roles'
	
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(100), unique=True)
	description = db.Column(db.String(255))


class RolesUsers(db.Model):

	__tablename__ = 'roles_users'

	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column('user_id', db.Integer(), ForeignKey('users.id'))
	role_id = db.Column('role_id', db.Integer(), ForeignKey('roles.id'))
