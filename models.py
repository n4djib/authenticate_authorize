from flask_login import UserMixin
from flask_rbac import RoleMixin
from app import db


roles_parents = db.Table(
    'roles_parents',
    db.Column('role_id', db.Integer, db.ForeignKey('role.id')),
    db.Column('parent_id', db.Integer, db.ForeignKey('role.id'))
)


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    parents = db.relationship(
        'Role',
        secondary=roles_parents,
        primaryjoin=(id == roles_parents.c.role_id),
        secondaryjoin=(id == roles_parents.c.parent_id),
        backref=db.backref('children', lazy='dynamic')
    )

    def __init__(self, name):
        RoleMixin.__init__(self)
        self.name = name

    # def add_parent(self, parent):
    #     # You don't need to add this role to parent's children set,
    #     # relationship between roles would do this work automatically
    #     self.parents.append(parent)

    # def add_parents(self, *parents):
    #     for parent in parents:
    #         self.add_parent(parent)

    # @staticmethod
    # def get_by_name(name):
    #     return Role.query.filter_by(name=name).first()


users_roles = db.Table(
    'users_roles',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer, db.ForeignKey('role.id'))
)


@rbac.as_user_model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    # username = db.Column(db.String(100), unllable=True)
    username = db.Column(db.String(100))
    is_active = db.Column(db.Boolean)
    articles = db.relationship("Article", back_populates="author")

    roles = db.relationship(
        'Role',
        secondary=users_roles,
        backref=db.backref('roles', lazy='dynamic')
    )

    # def __init__(self, email, username, password):
    #     self.email = email
    #     self.username = username
    #     self.password = password

    # def add_role(self, role):
    #     self.roles.append(role)

    # def add_roles(self, roles):
    #     for role in roles:
    #         self.add_role(role)

    # def get_roles(self):
    #     for role in self.roles:
    #         yield role


class Article(db.Model):
    __tablename__ = 'articles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), index=True, nullable=False)
    content = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    author = db.relationship("User", back_populates="articles")
