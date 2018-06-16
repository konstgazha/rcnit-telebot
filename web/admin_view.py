from flask_admin import AdminIndexView, expose, helpers
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask import redirect


class FlaskAdminIndexView(AdminIndexView):
    @expose('/')
    def index(self):
        if not login.current_user.is_authenticated:
            return redirect(url_for('.login'))
        return super(MyAdminIndexView, self).index()


    # @app.route('/login', methods=['GET', 'POST'])
    # def login():
    #     form = LoginForm()
    #     if form.validate_on_submit():
    #         user = db.session.query(User).filter(User.username == form.username.data).first()
    #         if user:
    #             if user.validate_password(form.password.data):
    #                 return redirect(url_for('admin.index'))
    #         return 'Invlid username or password'
    #     return render_template('login.html', form=form)

    @expose('/login', methods=['GET', 'POST'])
    def login(self):
        form = LoginForm(request.form)
        if helpers.validate_form_on_submit(form):
            user = form.get_user()
            if user is not None and user.validate_password(form.password.data):
                login.login_user(user)
            else:
                flash('Invalid username or password.')
        if login.current_user.is_authenticated:
            return redirect(url_for('.index'))
        self._template_args['form'] = form
        return super(MyAdminIndexView, self).index()

    @expose('/logout')
    @login_required
    def logout(self):
        login.logout_user()
        return redirect(url_for('.login'))