from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo, Email


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=50)],
                           render_kw={'placeholder': 'Username'})
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=40)],
                             render_kw={'placeholder': 'Password'})
    confirm_password = PasswordField('Repeat password', validators=[DataRequired(),
                                                                    EqualTo('password')],
                                     render_kw={'placeholder': 'Repeat password'})
    last_name = StringField('Last name', validators=[DataRequired(), Length(min=2, max=50)],
                            render_kw={'placeholder': 'Last name'})
    first_name = StringField('First name', validators=[DataRequired(), Length(min=2, max=50)],
                             render_kw={'placeholder': 'First name'})
    email = StringField('Email', validators=[DataRequired(), Email(), Length(min=2, max=50)],
                        render_kw={'placeholder': 'Email'})
    telephone = StringField('Telephone number', validators=[DataRequired(), Length(min=10, max=20)],
                            render_kw={'placeholder': 'Telephone number'})
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=50)],
                           render_kw={'placeholder': 'Username'})
    password = PasswordField('Password', validators=[DataRequired()],
                             render_kw={'placeholder': 'Password'})
    submit = SubmitField('Login')
