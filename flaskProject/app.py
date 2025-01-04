from flask import Flask

# 这里创建了一个 Flask 应用实例，赋值给变量 app。
# 参数 __name__ 是一个特殊变量，表示当前 Python 模块的名称。
app = Flask(__name__)

#url:http[默认端口80]/https[默认端口443]://www.qq.com:443/path

# 含义：这是一个装饰器，用于定义路由。
# 作用：告诉 Flask，当用户访问根路径 / 时，应该调用下面定义的函数（即 hello_world()）。
@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'

# 含义：启动 Flask 内置的开发服务器。
# 默认行为：
# 服务器会在本地运行，监听地址为 http://127.0.0.1:5000/。
# 默认端口为 5000，可以通过参数修改端口号，如 app.run(port=8080)。
# 作用：启动 Web 应用，使其可以接收用户的 HTTP 请求。
if __name__ == '__main__':
    app.run()

# 0.0.0.0让局域网所有机器都能访问