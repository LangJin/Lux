from flask import Flask, request, jsonify, render_template
from concurrent.futures import ThreadPoolExecutor
from flask_cors import CORS
from tools import getmysqldata
from tools import config
from tools import gettoken
from tools import startplay
token_home = config.token_home
executor = ThreadPoolExecutor()
app = Flask(__name__)
CORS(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/test', methods=['POST', 'GET'])
def test():
    dict1 = request.get_json()
    response = jsonify(dict1)
    return response


@app.route('/reconfig', methods=['GET'])
def reconfig():
    '''读取配置'''
    key = ["env", "oid", "url", "token", "dbname", "ownerName"]
    configinfo = getmysqldata.returnmysqlall()
    configlist = []
    for config in configinfo:
        i = 0
        configdict = {}
        for con in config:
            configdict[key[i]] = con
            i += 1
        configlist.append(configdict)
    response = jsonify(configlist)
    return response


@app.route('/config', methods=['POST'])
def config():
    '''初始化用户金额'''
    dictdata = request.get_json()
    oid = dictdata["oid"]
    num = dictdata["num"]
    dbs = dictdata["datainfo"]
    hsql = "UPDATE t_user set balance = 99999999 WHERE oid = %s\
        and pass_word like 'e856dec846396b093d10ffdc28e4704f'\
        and isdelete = 0 and `status` = 1 and audit_status = 1\
        and istest = 0 AND balance < 9999999 LIMIT %s;" % (oid, num)
    a = getmysqldata.updatamysqldata(dbs, hsql)
    startplay.changex()
    if a == "0":
        response = {}
        response["code"] = 200
        response["msg"] = "初始化用户金额成功"
        response = jsonify(response)
        return response
    else:
        response = {}
        response["code"] = 500
        response["msg"] = "初始化用户金额失败"
        response = jsonify(response)
        return response


@app.route('/userlist', methods=['POST'])
def userlist():
    '''获取用户列表'''
    dictdata = request.get_json()
    oid = dictdata["oid"]
    num = dictdata["num"]
    dbs = dictdata["datainfo"]
    hsql = "SELECT * FROM t_user WHERE oid = %s\
    and pass_word like 'e856dec846396b093d10ffdc28e4704f'\
    and isdelete = 0 and `status` = 1 and istest = 0\
    and balance >= 9999999 and audit_status = 1 limit %s;" % (oid, num)
    userlist = getmysqldata.returnmysqlalldata(dbs, hsql, 2)
    if userlist is not None:
        response = {}
        response["code"] = 200
        response["msg"] = "获取用户列表成功"
        response["userlist"] = userlist
        return jsonify(response)
    else:
        response = {}
        response["code"] = 500
        response["msg"] = "查询数据库失败"
        response["userlist"] = userlist
        return jsonify(response)


@app.route('/crtoken', methods=['POST'])
def crtoken():
    '''创建token'''
    dictdata = request.get_json()
    hurl = dictdata["url"]
    filename = dictdata["token"]
    userlist = dictdata["userlist"]
    try:
        startplay.changez(0)
        executor.submit(hhhtoken, userlist, hurl, filename)
        response = {}
        response["code"] = 200
        response["msg"] = "正在生成token，请稍等..."
        return jsonify(response)
    except:
        response = {}
        response["code"] = 500
        response["msg"] = "检查下是不是登陆那里扯拐了"
        return jsonify(response)


def hhhtoken(userlist, hurl, filename):
    with open(token_home + filename + '.txt', 'w') as f:
        f.write('token:\n')
    for userName in userlist:
        code = gettoken.rancode()
        gettoken.userLogin(hurl, userName, code, filename)
    startplay.changez(1)


@app.route('/crtkstatus', methods=['GET'])
def crtkstatus():
    try:
        hsql = 'select * from status;'
        tcode = getmysqldata.returnmysqlcodez(hsql)
        response = {}
        response["code"] = 200
        response["tcode"] = tcode[0]
        response["msg"] = "生成的token的状态是%s！" % tcode[0]
        return jsonify(response)
    except:
        response = {}
        response["code"] = 500
        response["msg"] = "获取生成token的状态失败！"
        return jsonify(response)


@app.route('/readtoken', methods=['POST'])
def readtoken():
    '''读取token'''
    dictdata = request.get_json()
    filename = dictdata["token"]
    tokenlist = []
    try:
        with open(token_home + filename + '.txt', 'r') as f:
            while True:
                line = f.readline()  # 逐行读取
                if not line:
                    break
                line = line[:-1]
                tokenlist.append(line)
            del tokenlist[0]
        response = {}
        response["code"] = 200
        response["msg"] = "读取token成功！"
        response["tokens"] = tokenlist
        return jsonify(response)
    except:
        response = {}
        response["code"] = 500
        response["msg"] = "请检查是不是文件不存在！"
        return jsonify(response)


@app.route('/stoplotplay', methods=['GET'])
def stoplotplay():
    y = startplay.changey()
    if y == 0:
        response = {}
        response["code"] = 200
        response["msg"] = "正在停止..."
        return jsonify(response)
    else:
        response = {}
        response["code"] = 500
        response["msg"] = "请检查数据库是不是扯拐了"
        return jsonify(response)



if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True,  threaded=True)
