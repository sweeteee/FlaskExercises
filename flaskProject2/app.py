# render_template: 这是 Flask 提供的一个函数，用来渲染模板（如 HTML 文件），并将数据传递到模板中。
from flask import Flask,render_template
from datetime import datetime

app = Flask(__name__)

# value 是传递给该函数的参数，通常是一个 datetime 对象。
# format 是一个可选的字符串参数，指定日期的格式。默认格式是 "%Y-%m-%d %H:%M"，表示年份-月份-日期 小时:分钟的格式（例如 2025-01-05 15:30）。
# value.strftime(format) 会将 datetime 对象格式化为指定格式的字符串。
def datetime_format(value,format="%Y-%m-%d %H:%M"):
    return value.strftime(format)

app.add_template_filter(datetime_format,"dformat")

# 类与对象
class User:
    def __init__(self,username,email):
        self.username = username
        self.email = email

# 渲染templates文件夹下的index.html文件
@app.route('/')
def hello_world():  # put application's code here
    user = User(username="知了",email="xx@qq.com")
    # 字典
    person = {
        "username":"张三",
        "email":"zhangsan@qq.com"
    }
    return render_template("index.html",user = user,person=person)

# 传参给html文件
@app.route("/blog/<blog_id>")
def blog_detail(blog_id):
    return render_template("blog_detail.html",blog_id=blog_id,username="小笼包好吃")

@app.route("/filter")
def filter_demo():
    user = User(username="知了传了个课",email="xx@qq.com")
    mytime = datetime.now()
    return render_template("filter.html",user=user,mytime=mytime)

@app.route("/control")
def control_statement():
    age = 18
    books = [{
        "name":"frontend",
        "author":"a"
    },{
        "name":"backend",
        "author":"b"
    },{
        "name":"database",
        "author":"c"
    },{
        "name":"model",
        "author":"d"
    }]
    return render_template("control.html",age=age,books=books)

@app.route("/child1")
def child1():
    return render_template("child1.html")

@app.route("/child2")
def child2():
    return render_template("child2.html")

@app.route('/static')
def static_demo():
    return render_template("static.html")

if __name__ == '__main__':
    app.run()
