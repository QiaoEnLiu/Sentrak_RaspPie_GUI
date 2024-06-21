import sqlite3
from flask import Flask ,render_template , request, jsonify
app = Flask(__name__)
SQLITE_DB_PATH = 'SentrakSQL/SentrakSQL.db'


def get_user():
    # 連接到SQLite數據庫（如果不存在，將創建一個新的）
    conn = sqlite3.connect(SQLITE_DB_PATH)

    # 設置 row_factory 為 sqlite3.Row，以便查詢結果以字典形式返回
    conn.row_factory = sqlite3.Row

    # 創建一個游標對象來執行SQL語句
    cursor = conn.cursor()

    # 查詢整個表格的數據
    cursor.execute('SELECT * FROM users')
    user_data = cursor.fetchall()

    # 關閉游標和連接
    cursor.close()
    conn.close()

    # return dict(user_data[0]) if user_data else {}
    user_list = [{'id': data[0],
                  'username': data[1],
                  'password': data[2],
                  'control': data[3],
                  'write': data[4],
                  'read': data[5],
                  'download': data[6]}
                   for data in user_data]
    return user_list


def get_R1X_Datas():
    conn = sqlite3.connect(SQLITE_DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM R1X')
    datas = cursor.fetchall()
    conn.close()

    data_list = [{'Reg': data[0],
                  'Name': data[1],
                  'Value': data[2]}
                  for data in datas]
    return data_list


def get_R3X_Datas():
    conn = sqlite3.connect(SQLITE_DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM R3X')
    datas = cursor.fetchall()
    conn.close()

    data_list = [{'Reg': data[0],
                  'Name': data[1],
                  'Value': data[2]}
                  for data in datas]
    return data_list

def get_R4X_Datas():
    conn = sqlite3.connect(SQLITE_DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM R4X')
    datas = cursor.fetchall()
    conn.close()

    data_list = [{'Reg': data[0],
                  'Name': data[1],
                  'Value': data[2]}
                  for data in datas]
    return data_list

@app.route('/', methods=['GET'])
def get():
    # return jsonify({'Sentrak PyQt5': 'Flask in Docker Success'})
    return jsonify(get_R3X_Datas())
    # return render_template('index.html',
    #                        user_data = get_user(),
    #                        data_R1X = get_R1X_Datas(),
    #                        data_R3X = get_R3X_Datas(),
    #                        data_R4X = get_R4X_Datas())
    # # return "<p>Sentrak Flask API Activate!</p>"


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port = 5000) # host='0.0.0.0'沒有這個，就算成功建置docker裡localhost也會連不到docker裡