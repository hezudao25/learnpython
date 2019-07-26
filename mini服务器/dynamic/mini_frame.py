import pymysql
import re
import logging


URL_FUNC_DICT = dict()


def route(url):
    """ 带参数的装饰器 装饰器是从函数读取就开始加载"""
    def get_func(func):
        URL_FUNC_DICT[url] = func

        def set_func(*args, **kwargs):
            return func(*args, **kwargs)
        return set_func
    return get_func


@route("/login.html")
def login(ret):
    with open("./templetes/login.html", "rb") as f:
        return f.read()


@route("/index.html")
def index(ret):
    with open("./templetes/index.html", "rb") as f:
        content = f.read()
    conn = pymysql.connect(host="localhost", port=3306, user="root", password="root", database="python01")
    cursor = conn.cursor()
    cursor.execute("select * from students;")
    stock_info = cursor.fetchall()
    cursor.close()
    conn.close()
    html_str = """<tr>
    <td width='25'>%s</td>
    <td width='25'>%s</td>
    <td width='25'>%s</td>
    <td width='25'>%s</td>    
    </tr>
    """
    html = ""
    for tem in stock_info:
        html += html_str % (tem[0], tem[1], tem[2], [3])


    content = re.sub(b"\{%content%\}", html.encode('utf-8'), content)

    return content







def application(environ, start_response):
    """"""
    start_response('200 OK', [('Content-Type', 'text/html; charset=utf-8')])
    file_name = environ["PATH_INFO"]
    #if environ["PATH_INFO"] == "/login.py":
    #    return login()
    #elif environ["PATH_INFO"] == "/index.py":
    #    return index()
    #else:
    #   return b"hahaha"
    logging.basicConfig(level=logging.INFO,
                        filename='./log.txt',
                        filemode='a',
                        format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')
    try:
        #return URL_FUNC_DICT[file_name]()
        for url, func in URL_FUNC_DICT.items():
            ret = re.match(url, file_name)
            if ret:
                return func(ret)
        else:
            logging.warning("没有对应的函数")
            return ("请求的url(%s)没有对应的函数..." % file_name).encode("utf-8")



    except Exception as rep:
        logging.warning("产生了异常: %s" % str(rep))
        return ("产生了异常: %s" % str(rep)).encode("utf-8")

