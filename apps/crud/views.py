from flask import Blueprint, render_template;


# Blueprintでcrudアプリを生成する。
crud = Blueprint(
    name="crud",
    import_name=__name__,
    template_folder="templates",
    static_folder="static",
    url_prefix="/crud",
)


@crud.route("/")
def index():
    return render_template("crud/index.html");
