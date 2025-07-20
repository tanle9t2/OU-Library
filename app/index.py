from app import app, login
from app.controller.AccountController import account_bp
from app.controller.HomeController import index_bp
from app.dao.UserDao import get_user_by_id

from flask_login import current_user

app.register_blueprint(account_bp, url_prefix='/account')
app.register_blueprint(index_bp, url_prefix='/')

@login.user_loader
def get_by_id(user_id):
    return get_user_by_id(user_id)


if __name__ == "__main__":
    app.run(debug=True)
