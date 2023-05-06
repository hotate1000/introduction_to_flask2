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


# Flaskクラスをインスタンス化する。
app = Flask(__name__);
# SECRET_KEYを追加する。
app.config["SECRET_KEY"] = "2AZSMss3p5QPbcY2hBsJ";


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
        # メールを送る。
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

        flash("問い合わせありがとうございました。");

        return redirect(url_for("contact_complete"));
    return render_template("contact_complete.html");
