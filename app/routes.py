import uuid
from app import app, db, login
from app.models import Accounts, Requests, Admins
from flask import render_template, flash, redirect, url_for
from app.forms import CreateAccount, RequestVoucher, AdminLogin
from flask_login import current_user, login_user, login_required, logout_user


@app.route("/", methods=["GET", "POST"])
def index():
    form = CreateAccount()
    if form.validate_on_submit():
        try:
            account = Accounts(nickname=form.nickname.data, email=form.email.data)
            db.session.add(account)
            db.session.commit()
        except BaseException as e:
            flash(f"An error occurred: {e}")
            return render_template("create_account.html", form=form)
        flash(f"Account created for nickname {form.nickname.data} with id {account.id}")
        return redirect(f"/account/{account.id}")

    return render_template("create_account.html", form=form)


@app.route("/account/<string:account_id>", methods=["GET", "POST"])
def account(account_id):
    form = RequestVoucher()
    voucher_requests = Requests.query.filter_by(requested_by=account_id, voucher=None)
    account = Accounts.query.filter_by(id=account_id).first()
    if voucher_requests.count() == 0:
        voucher_requests = False

    if form.validate_on_submit():
        request = Requests(
            id=str(uuid.uuid4()),
            nickname=form.nickname.data,
            email=form.email.data,
            request_type=form.request_type.data,
            requested_by=account.id,
        )
        db.session.add(request)
        db.session.commit()
        del request
        flash("voucher request created")
        voucher_requests = Requests.query.filter_by(requested_by=account_id)
    return render_template(
        "account.html", account=account, voucher_requests=voucher_requests, form=form
    )


@app.route(
    "/account/<string:account_id>/request/<string:request_id>/delete", methods=["GET"]
)
def voucher_request_delete(account_id, request_id):
    print(request_id)
    Requests.query.filter_by(id=request_id).delete()
    db.session.commit()
    flash("voucher request deleted")
    return redirect(f"/account/{account_id}")


@app.route("/login", methods=["GET", "POST"])
def admin_login():
    if current_user.is_authenticated:
        flash("User already logged in")
        return redirect(url_for("index"))
    form = AdminLogin()
    if form.validate_on_submit():
        admin = Admins.query.filter_by(email=form.email.data).first()
        if admin is None or not admin.check_password(form.password.data):
            flash("Invalid username or password")
            return redirect(url_for("admin_login"))
        login_user(admin, remember=False)
        return redirect(url_for("admin"))
    return render_template("admin_login.html", form=form)


@app.route("/admin", methods=["GET"])
@login_required
def admin():
    reqs = Requests.query.all()
    return render_template("admin.html", voucher_requests=reqs)


@app.route("/logout", methods=["GET"])
def logout():
    logout_user()
    return redirect(url_for("index"))
