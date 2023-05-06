from flask import (
    Flask,
    current_app,
    g,
    render_template,
    request,
    url_for,
    redirect,
    flash,
);


# Flaskクラスをインスタンス化する。
app = Flask(__name__);

# SECRET_KEYを追加追加する。
app.config["SECRET_KEY"] = "2AZSMss3p5QPbcY2hBsJ";


# URLと実行する関数をマッピングする。
@app.route("/")
def index():
    return "Hello World";
