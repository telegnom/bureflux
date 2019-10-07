from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from app import Config


class CreateAccount(FlaskForm):
    nickname = StringField(
        "nickname",
        validators=[
            DataRequired(message="Nickname required"),
            Length(min=3, message="Minimum nickname lenght: 3 chars"),
        ],
    )
    email = StringField(
        "email address", validators=[Email(message="Not a valid email address")]
    )
    repeat_email = StringField(
        "repeat email address",
        validators=[EqualTo("email", message="email addresses do not match")],
    )
    event_password = PasswordField(
        "event password",
        validators=[DataRequired(message="event passwort must not be empty")],
    )
    submit = SubmitField("create account")

    def validate_event_password(self, event_password):
        if Config.EVENT_PASSWORD != event_password.data:
            raise ValidationError("the event passwort is not correct")


class RequestVoucher(FlaskForm):
    nickname = StringField(
        "nickname",
        validators=[
            DataRequired(),
            Length(min=3, message="Minimum nickname length: 3 chars"),
        ],
    )
    request_type = SelectField(
        "request type",
        choices=[
            (None, "--- please select ---"),
            ("member", f"member of {Config.ERFA_NAME}"),
            ("significant", "significant other / own children"),
            ("friends", "friends and coworkers"),
            ("stranger", "strangers who asked"),
        ],
    )

    email = StringField(
        "email address", validators=[Email(message="Not a valid email address")]
    )
    repeat_email = StringField(
        "repeat email address",
        validators=[EqualTo("email", message="email addresses do not match")],
    )
    submit = SubmitField("request voucher")

    def validate_request_type(self, request_type):
        if request_type.data == None:
            raise ValidationError("please select the type of your request")


class AdminLogin(FlaskForm):
    email = StringField("email address", validators=[DataRequired()])
    password = PasswordField("password", validators=[DataRequired()])
    submit = SubmitField("Sign In")
