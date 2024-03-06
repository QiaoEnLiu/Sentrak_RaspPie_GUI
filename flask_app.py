from flask import Flask

import sqlite3, logging

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'SentrakSQL/SentrakSQL.db'
sql_path = app.config['SQLALCHEMY_DATABASE_URI']
def check_flask_connection():
    if 'SQLALCHEMY_DATABASE_URI' in app.config:
        app.logger.info(f"Using Flask to connect to SQLite: {sql_path}")

    # if isinstance(app, Flask):
    #     app.logger.info("Flask App object found.")

class SQLiteLogHandler(logging.Handler):
    def emit(self, record):
        # 在這裡實現自訂的日誌處理邏輯
        log_message = self.format(record)
        # print(f"SQLite Log: {log_message}")

# 設定 Flask 的日誌等級
app.logger.setLevel(logging.DEBUG)
# 將 SQLiteLogHandler 加入到 Flask 的日誌處理器中
sqlite_log_handler = SQLiteLogHandler()
sqlite_log_handler.setLevel(logging.DEBUG)
app.logger.addHandler(sqlite_log_handler)


def init_db():
    conn = sqlite3.connect(sql_path)
    # cursor = conn.cursor()

    conn.commit()
    conn.close()


# @app.route('/', methods=['GET'])
def selectSQL_user(username):
    # 連接到SQLite數據庫（如果不存在，將創建一個新的）
    conn = sqlite3.connect(sql_path)

    # 設置 row_factory 為 sqlite3.Row，以便查詢結果以字典形式返回
    conn.row_factory = sqlite3.Row

    # 創建一個游標對象來執行SQL語句
    cursor = conn.cursor()

    # 查詢整個表格的數據
    cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
    user_data = cursor.fetchall()

    # 關閉游標和連接
    cursor.close()
    conn.close()

    return dict(user_data[0]) if user_data else {}

@app.route('/', methods=['GET'])
def flaskActivate():
    # check_flask_connection()
    return 'Flask API Activate'

@app.route('/', methods=['GET'])
def api_get_users(username):
    # check_flask_connection()
    # app.logger.info("Reading 'users' from SQLite database...")
    print(f'Flask Api Get Users:{username}')
    return selectSQL_user(username)


if __name__ == '__main__':
    print(flaskActivate())
    init_db()
    app.run(debug = True, port = 5000)