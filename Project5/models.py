from flask_sqlalchemy import SQLAlchemy
from flask_admin import BaseView, expose
from flask import redirect, session
from flask_admin.contrib.sqla import ModelView
from sqlalchemy.dialects.postgresql import JSON

db = SQLAlchemy()


# Модель Пользователь
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    password_hash = db.Column(db.String, nullable=False)
    role = db.Column(db.String(32), nullable=False)
    orders = db.relationship("Order", back_populates='users')


# Модель Ассоциативная таблица Блюда - Заказы
meals_orders_association = db.Table('meals_orders', db.metadata,
    db.Column('order_id', db.Integer, db.ForeignKey('orders.id')),
    db.Column('meal_id', db.Integer, db.ForeignKey('meals.id')))


# Модель Заказы
class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    date = db.Column(db.DateTime(timezone=False), default = db.func.now())
    summa = db.Column(db.Float, nullable=False)
    status = db.Column(db.String, nullable=False)
    mail = db.Column(db.String, nullable=False)
    phone = db.Column(db.String, nullable=False)
    address = db.Column(db.String, nullable=False)
    users = db.relationship("User", back_populates='orders')
    users_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    list_meal = db.Column(JSON)
    orders_meals = db.relationship("Meal", secondary=meals_orders_association, back_populates='orders')


# Модель Блюда
class Meal(db.Model):
    __tablename__ = 'meals'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.String, nullable=False)
    picture = db.Column(db.String, nullable=False)
    categories = db.relationship("Category", back_populates='meals')
    categories_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    orders = db.relationship("Order", secondary=meals_orders_association, back_populates='orders_meals')


# Модель Категории
class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    meals = db.relationship("Meal", back_populates='categories')


# Административная панель-Статистика(проба)
class AdminStatistic(BaseView):
    def is_accessible(self):
        if session.get("role") == 'superadmin':
            return True
    @expose('/')
    def statistic(self):
        statistic = '10'
        return self.render('adminstatistic.html', statistic=statistic)


# Выход из административной панели
class MyView(BaseView):
    @expose('/')
    def exit_admin(self):
        return redirect('/logout/')


# Смена пароля администратора
class MyAdminView(BaseView):
    def is_accessible(self):
        if session.get("role") == 'superadmin':
            return True
    @expose('/')
    def change_password_admin(self):
        return redirect('/change-password/')


# Модели Администраторов- Заказы
# Модель для роли superadmin- Заказы
class OrderViewSuperadmin(ModelView):
    column_searchable_list = ['id', 'name', 'date', 'summa', 'phone', 'status', 'mail', 'address', 'users_id', 'list_meal']
    column_filters = ['id', 'name', 'date', 'summa', 'phone', 'status', 'mail', 'address', 'users_id']
    column_list = ['id', 'name', 'date', 'summa', 'phone', 'status', 'mail', 'address', 'users_id', 'list_meal']
    column_sortable_list = ['id', 'name', 'date', 'summa', 'phone', 'status', 'mail', 'address', 'users_id', 'list_meal']
    page_size = 10
    edit_modal = True
    def is_accessible(self):
        if session.get("role") == 'superadmin':
            return True


# Модель для роли admin- Заказы
class OrderViewAdmin(ModelView):
    column_searchable_list = ['id', 'name', 'date', 'summa', 'phone', 'status', 'mail', 'address', 'users_id', 'list_meal']
    column_filters = ['id', 'name', 'date', 'summa', 'phone', 'status', 'mail', 'address', 'users_id']
    column_list = ['id', 'name', 'date', 'summa', 'phone', 'status', 'mail', 'address', 'users_id', 'list_meal']
    column_sortable_list = ['id', 'name', 'date', 'summa', 'phone', 'status', 'mail', 'address', 'users_id', 'list_meal']
    can_set_page_size = True
    edit_modal = True
    can_delete = False
    def is_accessible(self):
        if session.get("role") == 'admin':
            return True


# Модель для роли disp - Заказы
class OrderViewDisp(ModelView):
    column_searchable_list = ['id', 'name', 'date', 'summa', 'phone', 'status', 'mail', 'address', 'users_id', 'list_meal']
    column_filters = ['id', 'name', 'date', 'summa', 'phone', 'status', 'mail', 'address', 'users_id']
    column_list = ['id', 'name', 'date', 'summa', 'phone', 'status', 'mail', 'address', 'users_id', 'list_meal']
    column_sortable_list = ['id', 'name', 'date', 'summa', 'phone', 'status', 'mail', 'address', 'users_id', 'list_meal']
    can_set_page_size = True
    can_edit = True
    can_delete = False
    form_edit_rules = {'status', 'phone', 'address'}
    def is_accessible(self):
        if session.get("role") == 'disp':
            return True


# Модель Администраторов - Блюда
# Модель для роли superadmin, admin - Блюда
class MealView(ModelView):
    column_searchable_list = ['id', 'title', 'price', 'description', 'picture', 'categories_id']
    column_filters = ['id', 'title', 'price', 'description', 'picture', 'categories_id']
    column_list = ['id', 'title', 'price', 'description', 'picture', 'categories_id']
    column_sortable_list = ['id', 'title', 'price', 'description', 'picture', 'categories_id']
    can_set_page_size = True
    def is_accessible(self):
        if session.get("role") == 'superadmin' or session.get("role") == 'admin':
            return True

# Модель для роли disp - Блюда
class MealViewDisp(ModelView):
    column_searchable_list = ['id', 'title', 'price', 'description', 'picture', 'categories_id']
    column_filters = ['id', 'title', 'price', 'description', 'picture', 'categories_id']
    column_list = ['id', 'title', 'price', 'description', 'picture', 'categories_id']
    column_sortable_list = ['id', 'title', 'price', 'description', 'picture', 'categories_id']
    can_set_page_size = True
    can_edit = False
    can_delete = False
    def is_accessible(self):
        if session.get("role") == 'disp':
            return True


# Модель Администраторов - Категории
# Модель для роли superadmin, admin - Категории
class CategoryView(ModelView):
    column_searchable_list = ['id', 'title']
    column_filters = ['id', 'title']
    column_list = ['id', 'title']
    column_sortable_list = ['id', 'title']
    page_size = 10
    def is_accessible(self):
        if session.get("role") == 'admin' or session.get("role") == 'superadmin':
            return True


# Модель для роли disp  - Категории
class CategoryViewDisp(ModelView):
    column_searchable_list = ['id', 'title']
    column_filters = ['id', 'title']
    column_list = ['id', 'title']
    column_sortable_list = ['id', 'title']
    page_size = 10
    can_edit = False
    can_delete = False
    def is_accessible(self):
        if session.get("role") == 'disp':
            return True


# Модель Администраторов - Пользователь
# Модель для роли superadmin- Пользователь
class UserView(ModelView):
    column_searchable_list = ['id', 'username', 'password_hash', 'role']
    column_filters = ['id', 'username', 'password_hash', 'role']
    column_list = ['id', 'username', 'password_hash', 'role']
    column_sortable_list = ['id', 'username', 'password_hash', 'role']
    can_set_page_size = True
    def is_accessible(self):
        if session.get("role") == 'superadmin':
            return True


# Модель для ролей disp, admin   - Пользователь
class UserViewDisp(ModelView):
    column_searchable_list = ['id', 'username', 'role']
    column_filters = ['id', 'username', 'role']
    column_list = ['id', 'username', 'role']
    column_sortable_list = ['id', 'username', 'role']
    can_set_page_size = True
    can_edit = False
    can_delete = False
    def is_accessible(self):
        if session.get("role") == 'disp' or session.get("role") == 'admin':
            return True