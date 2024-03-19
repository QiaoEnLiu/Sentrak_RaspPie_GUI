# SQL

import sqlite3

db_path = 'SentrakSQL/SentrakSQL.db'
regDFs={1: 'R1X',
        3: 'R3X',
        4: 'R4X'}

# 查詢使用者
def selectSQL_user(username):
        # 連接到SQLite數據庫（如果不存在，將創建一個新的）
        conn = sqlite3.connect(db_path)

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


#region 由reg地址
# 由暫存資料表查詢值
def selectSQL_Reg(regDF, regKey):

        # 連接到SQLite數據庫（如果不存在，將創建一個新的）
        conn = sqlite3.connect(db_path)

        # 設置 row_factory 為 sqlite3.Row，以便查詢結果以字典形式返回
        conn.row_factory = sqlite3.Row

        # 創建一個游標對象來執行SQL語句
        cursor = conn.cursor()

        query = f"SELECT Value FROM {regDFs[regDF]} WHERE Reg = {regKey}"

        # 查詢整個表格的數據
        cursor.execute(query)
        data = cursor.fetchall()

        # 關閉游標和連接
        cursor.close()
        conn.close()
        return data[0][0]

# 修改值存入暫存資料表
def updateSQL_Reg(regDF, regKey, updateValue):
        # 連接到SQLite數據庫（如果不存在，將創建一個新的）
        conn = sqlite3.connect(db_path)

        # 設置 row_factory 為 sqlite3.Row，以便查詢結果以字典形式返回
        conn.row_factory = sqlite3.Row

        # 創建一個游標對象來執行SQL語句
        cursor = conn.cursor()

        query = f"UPDATE {regDFs[regDF]} SET Value = {updateValue} Where Reg = {regKey}"

        # 查詢整個表格的數據
        cursor.execute(query)

        # 提交變更
        conn.commit()

        # 關閉游標和連接
        cursor.close()
        conn.close()

        print("Update SQL Success")

#endregion


#region 由reg名稱（假設所有名稱都是唯一名稱）
# 由暫存資料表查詢值
def selectSQL_RegName(regDF, regName):

        # 連接到SQLite數據庫
        conn = sqlite3.connect(db_path)

        # 設置 row_factory 為 sqlite3.Row，以便查詢結果以字典形式返回
        conn.row_factory = sqlite3.Row

        # 創建一個游標對象來執行SQL語句
        cursor = conn.cursor()

        query = f"SELECT Value FROM {regDFs[regDF]} WHERE Name = {regName}"

        # 查詢整個表格的數據
        cursor.execute(query)
        data = cursor.fetchall()

        # 關閉游標和連接
        cursor.close()
        conn.close()
        return data[0][0]

# 修改值存入暫存資料表
def updateSQL_RegName(regDF, regName, updateValue):
        # 連接到SQLite數據庫
        conn = sqlite3.connect(db_path)

        # 設置 row_factory 為 sqlite3.Row，以便查詢結果以字典形式返回
        conn.row_factory = sqlite3.Row

        # 創建一個游標對象來執行SQL語句
        cursor = conn.cursor()

        query = f"UPDATE {regDFs[regDF]} SET Value = {updateValue} Where Name = {regName}"

        # 查詢整個表格的數據
        cursor.execute(query)

        # 提交變更
        conn.commit()

        # 關閉游標和連接
        cursor.close()
        conn.close()

        print("Update SQL Success")

#endregion
        
