from flask import Flask, render_template, request, jsonify, session, redirect
import x
import uuid
import time
from flask_session import Session
from icecream import ic
ic.configureOutput(prefix=f'----- | ', includeContext=True)
 
app = Flask(__name__)
 
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

##############################
@app.get("/signup")
def show_signup():
    try:
        user = session.get("user", "")
        return render_template("page_signup.html", user=user)
    except Exception as ex:
        ic(ex)
        return "ups"
    
##############################
@app.post("/api-create-user")
def api_create_user():
    try:
        user_first_name = x.validate_user_first_name()
        user_last_name = x.validate_user_last_name()
    except Exception as ex:
        ic(ex)
        if "company_exception user_first_name" in str(ex):
            error_message = f"user_first_name {x.USER_FIRST_NAME_MIN} to {x.USER_FIRST_NAME_MAX} characters"
            ___tip = render_template("___tip.html", status="error", message=error_message)
            return f"""<browser mix-after-begin="#tooltip">{___tip}</browser>"""
        
        if "company_exception user_last_name" in str(ex):
            error_message = f"user_last_name {x.USER_LAST_NAME_MIN} to {x.USER_LAST_NAME_MAX} characters"
            ___tip = render_template("___tip.html", status="error", message=error_message)
            return f"""<browser mix-after-begin="#tooltip">{___tip}</browser>"""
        
        return "ups"
    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()