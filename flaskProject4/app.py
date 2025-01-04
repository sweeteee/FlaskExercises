from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

# 更强大的表数据更新包
from flask_migrate import Migrate

# app 是 Flask 应用的核心对象，它代表了整个 Web 应用程序的实例。
# 1.配置应用
# Flask 是一个类，app 是这个类的一个实例，表示当前的 Flask 应用程序。
# 从底层来看，Flask 是一个继承自 Python 标准库 Werkzeug 的 WSGI 应用类。
# from flask import Flask
# app = Flask(__name__)

# 2.注册路由
# app 用于定义路由（URL 与函数的映射），当用户访问某个 URL 时，app 会调用对应的函数
# @app.route('/')
# def index():
#     return "Hello, Flask!"

# 3.处理请求与响应
# Flask 框架会将所有 HTTP 请求交给 app 对象处理，它根据路由找到对应的函数，运行函数后返回响应。

# 4.加载扩展
# 许多第三方扩展（例如 Flask-SQLAlchemy、Flask-Migrate）需要通过 app 进行初始化：
# from flask_sqlalchemy import SQLAlchemy
# db = SQLAlchemy(app)  # 将数据库扩展与 app 绑定
app = Flask(__name__)

# 在 Python 中，__name__ 是一个内置变量，每个模块都会有它。
# 它的作用是指示当前模块的名称，它可以帮助我们区分一个模块是被直接运行还是被导入。具体来说：
# (1) 当模块被直接运行时
# __name__ 的值会被设置为 "__main__"
# (2) 当模块被导入时
# 如果一个 Python 文件被其他模块导入，__name__ 的值会是该模块的名称（通常是文件名，不包括扩展名）。

# 为什么要传入 __name__？
# Flask 类需要知道当前应用的模块名称，__name__ 帮助它定位应用的 根目录，以便：
#
# 加载静态文件（默认目录是 static）。
# 加载模板文件（默认目录是 templates）。
# 调试时更容易定位问题。
# 举例：假设 Flask 启动时需要查找静态文件和模板文件，它会根据 __name__ 定位到当前模块的文件路径，确保文件可以被正确加载。

# MySQL所在的主机名
HOSTNAME = "127.0.0.1"
# MySQL监听的端口号，默认3306
# 不同数据库管理系统有自己的默认端口号，例如：
# PostgreSQL：5432
# SQL Server：1433
# MongoDB：27017
PORT = 3306
# 连接MySQL的用户名，读者用自己设置的
USERNAME = "root"
# 连接MySQL的密码，读者用自己的
PASSWORD = "0000"
# MySQL上创建的数据库名称
DATABASE = "database_learn"

app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}?charset=utf8mb4"


# 在app.config中设置好连接数据库的信息
# 然后使用SQLAlchemy(app)创建一个db对象
# SQLAlchemy会自动读取app.config中连接数据库的信息

db = SQLAlchemy(app)

migrate = Migrate(app, db)

# with app.app_context():
#     with db.engine.connect() as conn:
#         rs = conn.execute(text("select 1"))
#         print(rs.fetchone())

class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer,primary_key=True, autoincrement=True)
    # varchar, null = 0
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100))

user = User(username = "法外狂徒张三", password = '111111')
# 底层映射的是sql: insert user(username, password) vlaues('法外狂徒张三', '111111')

class Article(db.Model):
    __tablename__ = "article"
    id = db.Column(db.Integer,primary_key=True, autoincrement=True)
    title = db.Column(db.String(200), nullable=False)
    # string类型最多存储256个字符
    content = db.Column(db.Text, nullable=False)

    # 添加作者的外键（引用了user表中的id字段）
    author_id = db.Column(db.Integer,db.ForeignKey("user.id"))
    # ******方法一不需要******
    author = db.relationship("User")
    # ******************

article = Article(title="Flask学习大纲",content="Flaskxxxx")
# 方法一：
# 给article的外键赋值
# article.author_id = user.id
# 即可通过article.author_id查到原表User中的条目
# user = User.query.get(article.author_id)
# 缺陷：不够对象化

# 方法二：使用sqlalchemy的特性 对象化
article.author = user  # 关联用户到文章
# 通过 article.author 自动访问到 User 对象
print(article.author.username)  # 输出：法外狂徒张三

# 将所有表同步到数据库中
# 局限性：只能识别新增的模型，不能识别模型中新增的字段，字段类型的改变
# with app.app_context():
#     db.create_all()

@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'

@app.route('/user/add')
def add_user():
    # 1.创建ORM对象
    user = User(username="法外狂徒张三", password='111111')
    # 2.将ORM对象添加到db.session中
    db.session.add(user)

    # 1.创建ORM对象
    user = User(username="荒漠屠夫雷克顿", password='111111')
    # 2.将ORM对象添加到db.session中
    db.session.add(user)

    # 3.将db.session()中的改变同步到数据库中
    db.session.commit()
    return "用户创建成功！"

@app.route('/user/query')
def query_user():
    # 1.get查找，根据主键查找（找一个）
    user = User.query.get(1)
    print(f"{user.id}:{user.username}-{user.password}")
    # 2.filter_by查找（找一群）
    # 得到Query对象:类数组
    users = User.query.filter_by(password='111111')
    print(type(users))
    for user in users:
        print(f"{user.id}:{user.username}-{user.password}")
    return "数据查找成功！"

@app.route('/user/update')
def update_user():
    user=User.query.filter_by(username="法外狂徒张三").first() # 索引不存在不报错 仅返回none
    # user = User.query.filter_by(username="法外狂徒张三")[0]  # 索引不存在报错
    user.password="222222"
    db.session.commit()
    return "数据修改成功！"

@app.route('/user/delete')
def delete_user():
    # 1.查找id为1的项
    user=User.query.get(1)
    # 2.从db.session中删除，不改变其他项的id
    db.session.delete(user)
    # 3.将db.session的修改，同步到数据库中
    db.session.commit()
    return "数据删除成功！"

if __name__ == '__main__':
    app.run()
