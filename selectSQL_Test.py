import sqlite3

def fetch_table_as_dict():
    # 連接到SQLite數據庫（如果不存在，將創建一個新的）
    conn = sqlite3.connect('SentrakSQL/SentrakSQL.db')

    # 設置 row_factory 為 sqlite3.Row，以便查詢結果以字典形式返回
    conn.row_factory = sqlite3.Row

    # 創建一個游標對象來執行SQL語句
    cursor = conn.cursor()

    # 查詢整個表格的數據
    cursor.execute('SELECT * FROM users')
    rows = cursor.fetchall()

    # 將查詢結果以字典形式打印
    for row in rows:
        user_dict = dict(row)
        print(user_dict)

    # 關閉游標和連接
    cursor.close()
    conn.close()

# 使用例子
fetch_table_as_dict()