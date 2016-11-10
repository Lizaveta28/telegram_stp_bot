from flask import Flask, redirect, url_for, render_template
from flask_admin import Admin
from flask import request
from flask_login import LoginManager, login_user
from models.models import User, Section, Type, Stp, StpSection, SiteUser
from models.flask_models import UserAdmin, SectionAdmin, TypeAdmin, StpAdmin, StpSectionAdmin
import telebot
import config
from state_machines.utils import *

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
admin = Admin(app, name='СТП бот, административная панель', template_mode='bootstrap3')
# Add administrative views here
app.config['SECRET_KEY'] = 'Aogjaktsht%@%@%J@J=='
admin.add_view(SectionAdmin(Section))
admin.add_view(TypeAdmin(Type))
admin.add_view(UserAdmin(User))
admin.add_view(StpAdmin(Stp))
admin.add_view(StpSectionAdmin(StpSection))


@login_manager.user_loader
def load_user(user_id):
    return SiteUser.get(id=user_id)


@app.route("/promote_to_stp/<user>")
def promote_to_stp(user):
    tb = telebot.TeleBot(config.token)

    user = User.get(id=user)
    user.state = 'stp_main_menu'
    user.save()
    stp = Stp.get_or_create(user=user)[0]
    stp.is_active = True
    stp.save()
    try:
        keyboard = generate_custom_keyboard(types.ReplyKeyboardMarkup, buttons=[["Список запросов"],
                                                                                ["Мои активные запросы"],
                                                                                # ["Мои завершенные запросы"]
                                                                                ])
        tb.send_message(user.telegram_chat_id, "Вы были переведены в раздел СТП, команды находятся под полем ввода",
                        reply_markup=keyboard)
    except Exception as e:
        print("Cant promote to stp, reason: %s" % e)
    return redirect(url_for('stp.edit_view', id=stp.id))


@app.route("/")
def index():
    return render_template('login.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    # Here we use a class of some kind to represent and validate our
    # client-side form data. For example, WTForms is a library that will
    # handle this for us, and we use a custom LoginForm to validate.
    if request.method == 'POST':
        user = SiteUser.get(username=request.form.get('username'))
        password = request.form.get('password')
        if user.check_password(password):
            login_user(user)

            next = request.args.get('next')
            # next_is_valid should check if the user has valid
            # permission to access the `next` url

            return redirect(next or url_for('admin.index'))
    return render_template('login.html')


if __name__ == '__main__':
    import logging

    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)

    app.run(debug=True)
