# -*- coding: utf-8 -*-
#!/usr/bin/env python
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField,IntegerField, PasswordField, FormField, FieldList
from wtforms.fields.html5 import TelField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, InputRequired, EqualTo, Email


class ResultForm(FlaskForm):
	id = IntegerField('id')
	user_id = IntegerField('user_id')
	last_name = StringField(u'Фамилия')
	first_name = StringField(u'Имя',validators=[DataRequired()])
	middle_name = StringField(u'Отчество')
	personal_email = StringField('E-mail')
	position = StringField(u'Должность',validators=[DataRequired()])
	organization_name = StringField(u'Название организации')
	organization_url = StringField(u'Сайт организации')
	organization_activity = StringField(u'Вид деятельности', validators=[DataRequired()])
	discount_percent = StringField(u'Процент скидки')
	address_activity = StringField(u'Адрес деятельности')
	address_official = StringField(u'Адрес юридический')
	phone_work = TelField(u'Телефон рабочий')
	phone_mobile = TelField(u'Телефон мобильный')
	phone_organization = TelField(u'Телефон организации')
	is_displayed = BooleanField('is_displayed')
	#submit = SubmitField('Submit')


class UserForm(FlaskForm):
	email = StringField('email',validators=[Email(message=u'Введите правильный email')])
	password = PasswordField('password',validators=[InputRequired(message=u'Введите пароль'), EqualTo('password_confirm', message=u'Пароль не совпадает')])
	password_confirm = PasswordField('password_confirm')

