import random
import json

from flask import session, redirect, request, render_template
from flask_migrate import Migrate
from flask_admin import Admin
from werkzeug.security import generate_password_hash, check_password_hash
from collections import Counter

from Project5 import app, db
from Project5.forms import LoginForm, RegistrationForm, UserOrder, ChangePasswordForm
from Project5.models import User, Order, Meal, Category, meals_orders_association, \
    UserView, UserViewDisp, OrderViewAdmin, OrderViewSuperadmin, OrderViewDisp, \
    MealView, MealViewDisp, CategoryView, CategoryViewDisp, MyView, MyAdminView, AdminStatistic

migrate = Migrate(app, db)


# # Создание административной панели
admin = Admin(app, name='Панель администратора', template_mode='bootstrap3')
# User
admin.add_view(UserView(User, db.session, endpoint="admins_user"))
admin.add_view(UserViewDisp(User, db.session,endpoint="disp_user"))
# Meal
admin.add_view(MealView(Meal, db.session, endpoint="admins_meal"))
admin.add_view(MealViewDisp(Meal, db.session, endpoint="disp_meal"))
# Category
admin.add_view(CategoryView(Category, db.session, endpoint="admins_category"))
admin.add_view(CategoryViewDisp(Category, db.session, endpoint="disp_category"))
# Order
admin.add_view(OrderViewSuperadmin(Order, db.session, endpoint="superadmin_order"))
admin.add_view(OrderViewAdmin(Order, db.session, endpoint="admin_order"))
admin.add_view(OrderViewDisp(Order, db.session, endpoint="disp_order"))
# Other
admin.add_view(MyAdminView(name='Смена пароля'))
admin.add_view(AdminStatistic(name='Статистика'))
admin.add_view(MyView(name='Выйти'))


# Защита Административной панели
@app.before_request
def before_request():
    form = LoginForm()
    if request.full_path.startswith('/admin/'):
        if not session.get("is_auth"):
            err = 'Авторизуйтесь пожалуйста'
            return render_template('login.html', form = form, err = err)
        elif session.get("is_auth") and not session.get("admin"):
            err = 'Вы вошли в систему, однако у вас недостаточно прав для просмотра данной страницы. ' \
                  'Возможно, вы хотели бы войти в систему, используя другую учётную запись? '
            return render_template('login.html', form = form, err = err)


# Главная страница
@app.route('/')
def render_main():
    category = Category.query.all()
    randomcategory = random.choice(category)
    index_category = randomcategory.id
    meals = list(db.session.query(Meal).filter(Meal.categories_id == index_category))
    if len(meals) > 3:
        meals = random.sample(meals, 3)
    elif len(meals) <= 3:
        meals = meals
    sum = session.get('sum', 0)
    i = session.get('i', 0)
    session['del_meal'] = False
    return render_template("main.html", category = category, randomcategory = randomcategory, meals = meals,
                           i = i, sum = sum, header = True)


# Меню
@app.route('/menu/<categor>/')
def render_menu(categor):
    category = db.session.query(Category).filter(Category.title == categor).first()
    meals = list(db.session.query(Meal).filter(Meal.categories_id == category.id))
    sum = session.get('sum', 0)
    i = session.get('i', 0)
    session['del_meal'] = False
    return render_template("menu.html", category = category, meals = meals,
                            i = i, sum = sum, header = True)


# Корзина
@app.route('/cart/', methods=["GET", "POST"])
def render_cart():
    del_meal = session.get('del_meal')
    list_id = session.get('cart', [])
    i = session.get('i', 0)
    meals = {}
    sum = 0
    session['sum'] = sum
    meal_list = Counter(list_id)

    for meal_id, count_meal in meal_list.items():
        meal = db.session.query(Meal).filter(Meal.id == meal_id).first()
        sum = session.get('sum', 0)
        sum = sum + meal.price * count_meal
        session['sum'] = sum
        meals[meal]=count_meal

    form = UserOrder()
    if request.method == "POST":
        name_user = form.name_user.data
        address_user = form.address_user.data
        email_user = form.email_user.data
        phone_user = form.phone_user.data
        id = session.get("user_id")
        user = User.query.filter_by(id=id).first()
        if user.username == email_user:
            order = Order(name = name_user, summa = sum, status = "заявка принята", mail = email_user,
                          phone = phone_user, address = address_user, users_id = session.get("user_id"),
                          list_meal = meal_list)
            db.session.add(order)
            db.session.commit()
            return redirect("/ordered/")
        else:
            err = 'Электронная почта не совпадает с почтой авторизованного пользователя'
            return render_template("cart.html", meals = meals, sum = sum, i = i, header = True,
                           exitcart = True, del_meal = del_meal, form = form, err = err)
    else:
        return render_template("cart.html", meals = meals, sum = sum, i = i, header = True,
                           exitcart = True, del_meal = del_meal, form = form)


# Заказ выполнен
@app.route('/ordered/', methods=["GET", "POST"])
def render_ordered():
    sum = 0
    session['sum'] = sum
    i = 0
    session['i'] = i
    cart = []
    session['cart'] = cart
    return render_template("ordered.html", ord = True, sum = sum, i = i)


# Личный кабинет
@app.route('/account/')
def render_account():
    i = session.get('i', 0)
    id = session.get('user_id')
    sum = session.get('sum', 0)
    orders_list = Order.query.filter(Order.users_id == id).order_by(Order.date.desc())
    orders = []
    for order in orders_list:
        order_list = []
        order.date = order.date.strftime('%d-%m-%Y %H:%M')
        for key, value in order.list_meal.items():
            meal = Meal.query.filter_by(id=key).first()
            order_list.append([meal.title, value, meal.price])
            order.list_meal = order_list
        orders.append(order)
    return render_template("account.html", lg = True, i = i, orders = orders, sum = sum, header = True)


# Авторизация
@app.route('/login/', methods=["GET", "POST"])
def render_login():
    err = ""
    form = LoginForm()
    if request.method == "POST":
        username = form.username.data
        password = form.password.data
        user = User.query.filter_by(username=username).first()
        if user and user.role == 'superadmin' and check_password_hash(user.password_hash, password):
            session['user_id']=user.id
            session["is_auth"] = True
            session["admin"] = True
            session['role'] = "superadmin"
            return redirect("/admin/")
        elif user and user.role == 'admin' and check_password_hash(user.password_hash, password):
            session['user_id']=user.id
            session["is_auth"] = True
            session["admin"] = True
            session['role'] = "admin"
            return redirect("/admin/")
        elif user and user.role == 'disp' and check_password_hash(user.password_hash, password):
            session['user_id']=user.id
            session["is_auth"] = True
            session["admin"] = True
            session['role'] = "disp"
            return redirect("/admin/")
        elif user and check_password_hash(user.password_hash, password):
            session['user_id']=user.id
            session["is_auth"] = True
            session["admin"] = False
            session['role'] = "user"
            return redirect("/account/")
        else:
            err = "Неверное имя или пароль"
            return render_template("login.html", form = form, err = err)
    else:
        return render_template("login.html", form = form, err = err)


# Регистрация
@app.route('/register/', methods=["GET", "POST"])
def render_register():
    err = ""
    form = RegistrationForm()
    if request.method == "POST":
        username = form.username.data
        password = form.password.data
        user = User.query.filter_by(username=username).first()
        if user:
            err = "Пользователь с указанным именем уже существует"
            return render_template("login.html", err = err, form = form)
        else:
            if form.validate_on_submit():
                session['role'] = "user"
                role = session.get('role')
                user = User(username = username, password_hash = generate_password_hash(password), role = role)
                db.session.add(user)
                db.session.commit()
                session['user_id']=user.id
                session["is_auth"] = True
                return redirect("/cart/")
            else:
                return render_template("register.html", form = form, err = err)
    else:
        return render_template("register.html", form = form, err = err)


# Добавить 1 блюдо в корзину
@app.route('/addmeal/<int:id>/')
def render_addmeal(id):
    cart = session.get("cart",[])
    cart.append(id)
    session['cart'] = cart
    counter = session.get("i", 0)
    session["i"] = counter + 1
    sum = session.get("sum", 0)
    meal = db.session.query(Meal).filter(Meal.id == id).first()
    session["sum"] = sum + meal.price
    session['del_meal'] = False
    return redirect('/cart/')


# Увеличить количество в корзине
@app.route('/addtocart/<int:id>/')
def render_addtocart(id):
    cart = session.get("cart",[])
    cart.append(id)
    session['cart'] = cart
    counter = session.get("i", 0)
    session["i"] = counter + 1
    sum = session.get("sum", 0)
    meal = db.session.query(Meal).filter(Meal.id == id).first()
    session["sum"] = sum + meal.price
    session['del_meal'] = False
    return redirect('/')


# Удалить блюдо из корзины
@app.route('/deletefromcart/<int:id>/')
def render_deletefromcart(id):
    list_id = session.get('cart', [])
    list_id.remove(id)
    session['cart'] = list_id
    counter = session.get("i", 0)
    session['i'] = counter - 1
    session['del_meal'] = True
    return redirect('/cart/')


# Разлогинить
@app.route('/logout/')
def render_logout():
    if session.get("is_auth"):
        session.pop("is_auth")
        session['admin'] = False
        session['role'] = None
    return redirect('/login/')


# Поменять пароль
@app.route("/change-password/", methods=["GET", "POST"])
def change_password():
    form = ChangePasswordForm()
    if request.method == "POST":
        if form.validate_on_submit():
            user = User.query.filter_by(id=session.get("user_id")).first()
            user.password_hash = generate_password_hash(form.password.data)
            db.session.add(user)
            db.session.commit()
            return redirect("/login/")
    return render_template("change_password.html", form=form)


# Ошибка 404
@app.errorhandler(404)
def pageNotFound(error):
    return render_template("404.html")