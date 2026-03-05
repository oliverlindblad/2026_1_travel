from flask import Flask, render_template, request, jsonify, session, redirect
import x
import uuid
import time
from flask_session import Session
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash

from icecream import ic
ic.configureOutput(prefix=f'______ | ', includeContext=True)

app = Flask(__name__)

app.config['SESSION_TYPE'] = 'filesystem'
Session(app)



##############################
@app.get("/signup")
@x.no_cache
def show_signup():
    try:
        user = session.get("user", "")
        return render_template("page_signup.html", user=user, x=x)
    except Exception as ex:
        ic(ex)
        return "ups"

##############################
@app.post("/api-create-user")
def api_create_user():
    try:
        user_first_name = x.validate_user_first_name()
        user_last_name = x.validate_user_last_name()
        user_email = x.validate_user_email()
        user_password = x.validate_user_password()
        user_hashed_password = generate_password_hash(user_password)
        # ic(user_hashed_password) # 'scrypt:32768:8:1$V0NLEqHQsgKyjyA7$3a9f6420e4e9fa7a4e4ce6c89927e7dcb532e5f557aee6309277243e5882cc4518c94bfd629b61672553362615cd5d668f62eedfe4905620a8c9bb7db573de31'

        user_pk = uuid.uuid4().hex
        user_created_at = int(time.time())

        db, cursor = x.db()
        q = "INSERT INTO users VALUES(%s, %s, %s, %s, %s, %s)"
        cursor.execute(q, (user_pk, user_first_name, user_last_name, user_email, user_hashed_password, user_created_at))
        db.commit()

        form_signup = render_template("___form_signup.html", x=x)

        return f"""
            <browser mix-replace="form">{form_signup}</browser>
            <browser mix-redirect="/login"></browser>
        """

    except Exception as ex:
        ic(ex)

        if "company_exception user_first_name" in str(ex):
            error_message = f"user first name {x.USER_FIRST_NAME_MIN} to {x.USER_FIRST_NAME_MAX} characters"
            ___tip = render_template("___tip.html", status="error", message=error_message)
            return f"""<browser mix-after-begin="#tooltip">{___tip}</browser>""", 400

        if "company_exception user_last_name" in str(ex):
            error_message = f"user last name {x.USER_LAST_NAME_MIN} to {x.USER_LAST_NAME_MAX} characters"
            ___tip = render_template("___tip.html", status="error", message=error_message)
            return f"""<browser mix-after-begin="#tooltip">{___tip}</browser>""", 400

        if "company_exception user_email" in str(ex):
            error_message = f"user email invalid"
            ___tip = render_template("___tip.html", status="error", message=error_message)
            return f"""<browser mix-after-begin="#tooltip">{___tip}</browser>""", 400

        if "company_exception user_password" in str(ex):
            error_message = f"user password {x.USER_PASSWORD_MIN} to {x.USER_PASSWORD_MAX} characters"
            ___tip = render_template("___tip.html", status="error", message=error_message)
            return f"""<browser mix-after-begin="#tooltip">{___tip}</browser>""", 400

        if "Duplicate entry" in str(ex) and "user_email" in str(ex):
            error_message = "Email already exists"
            ___tip = render_template("___tip.html", status="error", message=error_message)
            return f"""<browser mix-after-begin="#tooltip">{___tip}</browser>""", 400

        # Worst case
        error_message = "System under maintenance"
        ___tip = render_template("___tip.html", status="error", message=error_message)        
        return f"""<browser mix-after-begin="#tooltip">{___tip}</browser>""", 500


    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()



##############################
@app.get("/login")
@x.no_cache
def show_login():
    try:
        user = session.get("user", "")
        if not user: 
            return render_template("page_login.html", user=user, x=x)
        return redirect("/profile")
    except Exception as ex:
        ic(ex)
        return "ups"


##############################
@app.post("/api-login")
def api_login():
    try:
        user_email = x.validate_user_email()
        user_password = x.validate_user_password()

        db, cursor = x.db()
        q = "SELECT * FROM users WHERE user_email = %s"
        cursor.execute(q, (user_email,))
        user = cursor.fetchone()
        if not user:
            error_message = "Invalid credentials 1"
            ___tip = render_template("___tip.html", status="error", message=error_message)
            return f"""<browser mix-after-begin="#tooltip">{___tip}</browser>""", 400

        if not check_password_hash(user["user_password"], user_password):
            error_message = "Invalid credentials 2"
            ___tip = render_template("___tip.html", status="error", message=error_message)
            return f"""<browser mix-after-begin="#tooltip">{___tip}</browser>""", 400            

        user.pop("user_password")
        session["user"] = user

        return f"""<browser mix-redirect="/profile"></browser>"""

    except Exception as ex:
        ic(ex)


        if "company_exception user_email" in str(ex):
            error_message = f"user email invalid"
            ___tip = render_template("___tip.html", status="error", message=error_message)
            return f"""<browser mix-after-begin="#tooltip">{___tip}</browser>""", 400

        if "company_exception user_password" in str(ex):
            error_message = f"user password {x.USER_PASSWORD_MIN} to {x.USER_PASSWORD_MAX} characters"
            ___tip = render_template("___tip.html", status="error", message=error_message)
            return f"""<browser mix-after-begin="#tooltip">{___tip}</browser>""", 400

        # Worst case
        error_message = "System under maintenance"
        ___tip = render_template("___tip.html", status="error", message=error_message)        
        return f"""<browser mix-after-begin="#tooltip">{___tip}</browser>""", 500


    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()

##############################
@app.get("/profile")
@x.no_cache
def show_profile():
    try:
        user = session.get("user", "")
        if not user: return redirect("/login")
        return render_template("page_profile.html", user=user, x=x)
    except Exception as ex:
        ic(ex)
        return "ups"


##############################
@app.get("/logout")
def logout():
    try:
        session.clear()
        return redirect("/login")
    except Exception as ex:
        ic(ex)
        return "ups"        