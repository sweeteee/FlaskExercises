from flask import Flask,request

app = Flask(__name__)

@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'

@app.route("/profile")
def profile():
    return "我是个人中心"

@app.route("/blog/list")
def blog_list():
    return "我是博客列表"

# 带参数的url
# @app.route("/blog/<blog_id>")
@app.route("/blog/<int:blog_id>") #限定数字参数
def blog_detail(blog_id):
    return "您访问的博客是：%d" %blog_id

###带参数的url（单参数）###

# /book/list 返回第一页数据
# /book/list?page=2 获取第二页的数据
# request需要从flask中导入
@app.route("/book/list")
def book_list():
    # 需要page的参数 默认是1 参数类型整型
    page = request.args.get("page",default=1,type=int)
    return f"您获取的是第{page}页的图书列表"

###带参数的url（多参数）###
# 例如在地址栏输入：
# /book/search?page=2&genre=fiction&author=Jane
@app.route("/book/search")
def book_search():
    page = request.args.get("page",default=1,type=int)
    genre = request.args.get("genre",default="all",type=str)
    author = request.args.get("author",default="",type=str)

    return f"您搜索的是第{page}页的图书列表，类别：{genre}，作者：{author}"

if __name__ == '__main__':
    app.run()
