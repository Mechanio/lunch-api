from datetime import date, datetime

from sqlalchemy import Column, String, Integer, DateTime, Date, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from passlib.hash import pbkdf2_sha256 as sha256

from app.database.database import base, session


class RestaurantModel(base):
    __tablename__ = "restaurant"
    id = Column(Integer, primary_key=True)
    name = Column(String(120), nullable=False)
    menus = relationship("MenusModel", uselist=False, backref='restaurant')

    @classmethod
    def find_by_id(cls, id_, to_dict=True):
        """
        Find restaurant by id
        :param id_: restaurant id
        :param to_dict: if True - returns dict representation of restaurant info, if False -
            returns model instance
        :return: dict representation of restaurant info or model instance
        """
        restaurant = session.query(cls).filter_by(id=id_).first()
        if not restaurant:
            return {}
        if to_dict:
            return cls.to_dict(restaurant)
        else:
            return restaurant

    @classmethod
    def find_by_name(cls, name, to_dict=True):
        """
        Find restaurant by name
        :param name: name of restaurant
        :param to_dict: if True - returns dict representation of restaurant info, if False -
            returns model instance
        :return: dict representation of restaurant info or model instance
        """
        restaurant = session.query(cls).filter_by(name=name).order_by(cls.id).first()
        if not restaurant:
            return {}
        if to_dict:
            return cls.to_dict(restaurant)
        else:
            return restaurant

    @classmethod
    def return_all(cls, offset, limit):
        """
        Return all restaurants
        :param offset: skip offset rows before beginning to return rows
        :param limit: determines the number of rows returned by the query
        :return: list of dict representations of restaurants
        """
        restaurants = session.query(cls).order_by(cls.id).offset(offset).limit(limit).all()

        return [cls.to_dict(restaurant) for restaurant in restaurants]

    @classmethod
    def delete_by_id(cls, id_):
        """
        Delete restaurant by id
        :param id_: restaurant id
        :return: code status (200, 404)
        """
        restaurant = session.query(cls).filter_by(id=id_).first()
        if restaurant:
            session.delete(restaurant)
            session.commit()
            return 200
        else:
            return 404

    def save_to_db(self):
        """
        Save model instance to database
        :return: None
        """
        session.add(self)
        session.commit()

    @staticmethod
    def to_dict(restaurant):
        """
        Represent model instance (restaurant) information
        :param restaurant: model instance
        :return: dict representation of restaurant info
        """
        return {
            "id": restaurant.id,
            "name": restaurant.name,
            "menus": MenusModel.find_by_restaurant_id(restaurant.id),
        }


class MenusModel(base):
    __tablename__ = "menu"
    id = Column(Integer, primary_key=True)
    restaurant_id = Column(Integer, ForeignKey('restaurant.id'), unique=True)
    monday = Column(String(500), nullable=False)
    tuesday = Column(String(500), nullable=False)
    wednesday = Column(String(500), nullable=False)
    thursday = Column(String(500), nullable=False)
    friday = Column(String(500), nullable=False)
    saturday = Column(String(500), nullable=False)
    sunday = Column(String(500), nullable=False)
    choices = relationship("ChoicesModel", lazy='dynamic', cascade="all, delete-orphan",
                           foreign_keys="ChoicesModel.menu_id")

    @classmethod
    def find_by_id(cls, id_, to_dict=True):
        """
        Find menu by id
        :param id_: menu id
        :param to_dict: if True - returns dict representation of menu info, if False -
            returns model instance
        :return: dict representation of menu info or model instance
        """
        menu = session.query(cls).filter_by(id=id_).first()
        if not menu:
            return {}
        if to_dict:
            return cls.to_dict(menu)
        else:
            return menu

    @classmethod
    def find_by_restaurant_id(cls, restaurant_id, to_dict=True):
        """
        Find menu by restaurant id
        :param restaurant_id: restaurant id
        :param to_dict: if True - returns dict representation of menu info, if False -
            returns model instance
        :return: dict representation of menu info or model instance
        """
        menu = session.query(cls).filter_by(restaurant_id=restaurant_id).first()
        if not menu:
            return {}
        if to_dict:
            return cls.to_dict(menu)
        else:
            return menu

    # #TODO
    # @classmethod
    # def find_by_day(cls, day, to_dict=True):
    #     """
    #     Find menu by day
    #     :param day: day of restaurant's menu
    #     :param to_dict: if True - returns dict representation of restaurant's menu info, if False -
    #         returns model instance
    #     :return: dict representation of restaurant's menu info or model instance
    #     """
    #     # menus = session.query(cls).filter_by(day=day).order_by(cls.id)
    #     # if not menus:
    #     #     return {}
    #     # if to_dict:
    #     #     return cls.to_dict(menus)
    #     # else:
    #     #     return menus

    @classmethod
    def return_all(cls, offset, limit):
        """
        Return all menus
        :param offset: skip offset rows before beginning to return rows
        :param limit: determines the number of rows returned by the query
        :return: list of dict representations of menus
        """
        menus = session.query(cls).order_by(cls.id).offset(offset).limit(limit).all()
        return [cls.to_dict(menu) for menu in menus]

    @classmethod
    def delete_by_id(cls, id_):
        """
        Delete menu by id
        :param id_: menu id
        :return: code status (200, 404)
        """
        menu = session.query(cls).filter_by(id=id_).first()
        if menu:
            session.delete(menu)
            session.commit()
            return 200
        else:
            return 404

    def save_to_db(self):
        """
        Save model instance to database
        :return: None
        """
        session.add(self)
        session.commit()

    @staticmethod
    def to_dict(menu):
        """
        Represent model instance (menu) information
        :param menu: model instance
        :return: dict representation of menus info
        """
        restaurant = RestaurantModel.find_by_id(menu.restaurant_id, to_dict=False)
        return {
            "id": menu.id,
            "restaurant_id": menu.restaurant_id,
            "restaurant": restaurant.name,
            "monday": menu.monday,
            "tuesday": menu.tuesday,
            "wednesday": menu.wednesday,
            "thursday": menu.thursday,
            "friday": menu.friday,
            "saturday": menu.saturday,
            "sunday": menu.sunday,
            "choices": [ChoicesModel.find_by_id(choice.id) for choice in menu.choices]
        }


class EmployeeModel(base):
    __tablename__ = "employees"
    id = Column(Integer, primary_key=True)
    firstname = Column(String(30), nullable=False)
    lastname = Column(String(30), nullable=False)
    email = Column(String(50), nullable=False)
    hashed_password = Column(String(100), nullable=False)
    is_active = Column(Boolean(), nullable=False)
    is_admin = Column(Boolean(), default=False)
    choices = relationship("ChoicesModel", lazy='dynamic', cascade="all, delete-orphan",
                           foreign_keys="ChoicesModel.employee_id")

    @classmethod
    def find_by_id(cls, id_, to_dict=True, without_choices=False):
        """
        Find active employee by id
        :param id_: employee id
        :param to_dict: if True - returns dict representation of employee info, if False -
            returns model instance
        :return: dict representation of employee info or model instance
        """
        employee = session.query(cls).filter_by(id=id_).first()
        if not employee:
            return {}
        if employee.is_active:
            if to_dict:
                return cls.to_dict(employee, without_choices=without_choices)
            else:
                return employee
        else:
            return {}

    @classmethod
    def find_by_name(cls, firstname, lastname, to_dict=True):
        """
        Find active employee by name
        :param firstname: employee firstname
        :param lastname: employee lastname
        :param to_dict: if True - returns dict representation of employee info, if False -
            returns model instance
        :return: dict representation of employee info or model instance
        """
        employee = session.query(cls).filter_by(firstname=firstname, lastname=lastname) \
            .order_by(cls.id).first()
        if not employee:
            return {}
        if employee.is_active:
            if to_dict:
                return cls.to_dict(employee)
            else:
                return employee
        else:
            return {}

    @classmethod
    def find_by_email(cls, email, to_dict=True):
        """
        Find active employee by email
        :param email: employee email
        :param to_dict: if True - returns dict representation of employee info, if False -
            returns model instance
        :return: dict representation of employee info or model instance
        """
        employee = session.query(cls).filter_by(email=email).first()
        if not employee:
            return {}
        if employee.is_active:
            if to_dict:
                return cls.to_dict(employee)
            else:
                return employee
        else:
            return {}

    @classmethod
    def return_all(cls, offset, limit):
        """
        Return all active employees
        :param offset: skip offset rows before beginning to return rows
        :param limit: determines the number of rows returned by the query
        :return: list of dict representations of employees
        """
        employees = session.query(cls).order_by(cls.id).offset(offset).limit(limit).all()
        return [cls.to_dict(employee) for employee in employees if employee.is_active]

    @classmethod
    def return_all_inactive(cls, offset, limit):
        """
        Return all inactive employees
        :param offset: skip offset rows before beginning to return rows
        :param limit: determines the number of rows returned by the query
        :return: list of dict representations of employees
        """
        employees = session.query(cls).order_by(cls.id).offset(offset).limit(limit).all()
        return [cls.to_dict(employee) for employee in employees if not employee.is_active]

    @classmethod
    def delete_by_id(cls, id_):
        """
        Delete employee by id
        :param id_: employee id
        :return: code status (200, 404)
        """
        employee = session.query(cls).filter_by(id=id_).first()
        if employee:
            employee.is_active = False
            employee.save_to_db()
            return 200
        else:
            return 404

    def save_to_db(self):
        """
        Save model instance to database
        :return: None
        """
        session.add(self)
        session.commit()

    @staticmethod
    def to_dict(employee, without_choices=False):
        """
        Represent model instance (employee) information
        :param employee: model instance
        :return: dict representation of employee info
        """
        if without_choices:
            return {
                "id": employee.id,
                "firstname": employee.firstname,
                "lastname": employee.lastname,
                "email": employee.email,
                "is_active": employee.is_active,
                "is_admin": employee.is_admin,
            }
        else:
            return {
                "id": employee.id,
                "firstname": employee.firstname,
                "lastname": employee.lastname,
                "email": employee.email,
                "is_active": employee.is_active,
                "is_admin": employee.is_admin,
                "choices": [ChoicesModel.to_dict(choice) for choice in employee.choices],
            }

    @staticmethod
    def generate_hash(password):
        """
        Generate hashed password
        :param password: password to hash
        :return: hashed password
        """
        return sha256.hash(password)

    @staticmethod
    def verify_hash(password, hashed):
        """
        Verify hashed password with imputed one
        :param password: imputed password
        :param hashed: hashed password
        :return: True or False
        """
        return sha256.verify(password, hashed)


class ChoicesModel(base):
    __tablename__ = "choices"
    id = Column(Integer, primary_key=True)
    current_day = Column(Date())
    employee_id = Column(Integer, ForeignKey('employees.id'))
    menu_id = Column(Integer, ForeignKey('menu.id'))

    @classmethod
    def find_by_id(cls, id_, to_dict=True):
        """
        Find choice by id
        :param id_: choice id
        :param to_dict: if True - returns dict representation of choice info, if False -
            returns model instance
        :return: dict representation of choice info or model instance
        """
        choice = session.query(cls).filter_by(id=id_).first()
        if not choice:
            return {}
        if to_dict:
            return cls.to_dict(choice)
        else:
            return choice

    @classmethod
    def find_by_employee_id(cls, id_, to_dict=True):
        """
        Find choice by employee_id
        :param id_: employee id
        :param to_dict: if True - returns dict representation of choice info, if False -
            returns model instance
        :return: dict representation of choice info or model instance
        """
        choice = session.query(cls).filter_by(employee_id=id_, current_day=date.today().strftime("%Y-%m-%d")).first()
        if not choice:
            return {}
        if to_dict:
            return cls.to_dict(choice)
        else:
            return choice

    @classmethod
    def find_by_current_day(cls, offset, limit):
        """
        Find choices by current day
        :param offset: skip offset rows before beginning to return rows
        :param limit:  determines the number of rows returned by the query
        :return: list of dict representations of choices
        """
        choices = session.query(cls).filter_by(current_day=date.today().strftime("%Y-%m-%d")) \
            .order_by(cls.id).offset(offset).limit(limit).all()
        return [cls.to_dict(choice) for choice in choices]

    @classmethod
    def delete_by_id(cls, id_):
        """
        Delete choice by id
        :param id_: choice id
        :return: code status (200, 404)
        """
        choice = session.query(cls).filter_by(id=id_).first()
        if choice:
            session.delete(choice)
            session.commit()
            return 200
        else:
            return 404

    def save_to_db(self):
        """
        Save model instance to database
        :return: None
        """
        session.add(self)
        session.commit()

    @staticmethod
    def to_dict(choice):
        """
        Represent model instance (choice) information
        :param choice: model instance
        :return: dict representation of choice info
        """
        restaurant = MenusModel.find_by_id(choice.menu_id, to_dict=False)
        restaurant = RestaurantModel.find_by_id(restaurant.restaurant_id, to_dict=False)
        return {
            "id": choice.id,
            "current_day": choice.current_day,
            "employee": EmployeeModel.find_by_id(choice.employee_id, without_choices=True),
            "restaurant": restaurant.name,
        }


class RevokedTokenModel(base):
    __tablename__ = 'revoked_tokens'
    id_ = Column(Integer, primary_key=True)
    jti = Column(String(120))
    blacklisted_on = Column(DateTime, default=datetime.utcnow)

    def add(self):
        """
        Save model instance to database
        :return: None
        """
        session.add(self)
        session.commit()

    @classmethod
    def is_jti_blacklisted(cls, jti):
        """
        Check if jwt token is blocklisted
        :param jti: signature
        :return: True or False
        """
        query = session.query(cls).filter_by(jti=jti).first()
        return bool(query)
