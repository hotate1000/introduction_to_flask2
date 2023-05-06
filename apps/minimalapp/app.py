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
from email_validator import validate_email, EmailNotValidError;
from flask_debugtoolbar import DebugToolbarExtension;
import logging;
import os;
from flask_mail import Mail, Message;


# Flaskクラスをインスタンス化する。
app = Flask(__name__);
# SECRET_KEYを追加する。
app.config["SECRET_KEY"] = "2AZSMss3p5QPbcY2hBsJ";
# ログレベルを設定する。
app.logger.setLevel(logging.DEBUG);
# リダイレクトを中断しないようにする。
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False;
# DebugToolbarExtensionをアプリケーションにセットする。
toolbar = DebugToolbarExtension(app);
# Mail送信用の設定を追加する。
app.config["MAIL_SERVER"] = os.environ.get("MAIL_SERVER");
app.config["MAIL_PORT"] = os.environ.get("MAIL_PORT");
app.config["MAIL_USE_TLS"] = os.environ.get("MAIL_USE_TLS");
app.config["MAIL_USERNAME"] = os.environ.get("MAIL_USERNAME");
app.config["MAIL_PASSWORD"] = os.environ.get("MAIL_PASSWORD");
app.config["MAIL_DEFAULT_SENDER"] = os.environ.get("MAIL_DEFAULT_SENDER");
# flask-mail拡張をアプリケーションにセットする。
mail = Mail(app);


# メール送信用の関数
def send_email(to, subject, template, **kwargs):
    msg = Message(subject, recipients=[to]);
    # メールは、テキスト形式とHTML形式で作成する。
    # HTML形式が送信出来ない場合、テキスト形式が送信される。
    msg.body = render_template(template + ".txt", **kwargs);
    msg.html = render_template(template + ".html", **kwargs);
    mail.send(msg);


# URLと実行する関数をマッピングする。
@app.route("/")
def index():
    return "Hello World";


# 送信フォーム
@app.route("/contact")
def contact():
    return render_template("contact.html");


# 送信完了フォーム
@app.route("/contact/complete", methods=["GET", "POST"])
def contact_complete():
    print(request.method);
    if request.method == "POST":
        # フォームに入力した内容を受け取る。
        username = request.form["username"];
        email = request.form["email"];
        description = request.form["description"];

        # バリデーションのチェック
        is_valid = True;
        if not username:
            flash("ユーザー名は必須です。");
            is_valid = False;
        if not email:
            flash("メールアドレスは必須です。");
            is_valid = False;

        try:
            # メールアドレスの形式をチェック。
            validate_email(email);
        except EmailNotValidError:
            flash("メールアドレスの形式で入力してください。");
            is_valid = False;
        
        if not description:
            flash("問い合わせ内容は必須です。");
            is_valid = False;
        
        if not is_valid:
            # 入力がおかしかった場合、入力フォームを表示する。
            return redirect(url_for("contact"));

        # メールを送る。
        send_email(
            email,
            "問い合わせありがとうございました。",
            "contact_mail",
            username=username,
            description=description,
        );

        flash("問い合わせありがとうございました。");

        return redirect(url_for("contact_complete"));
    return render_template("contact_complete.html");
