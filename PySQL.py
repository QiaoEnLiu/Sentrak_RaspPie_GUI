# SQL

import sqlite3

db_path = 'SentrakSQL/SentrakSQL.db'
regDFs={1: 'R1X',
        3: 'R3X',
        4: 'R4X'}

#region 連接資料庫
def execute_query(query, params=()):
        with sqlite3.connect(db_path) as conn: # 連接到SQLite數據庫
                conn.row_factory = sqlite3.Row # 設置 row_factory 為 sqlite3.Row，以便查詢結果以字典形式返回
                cursor = conn.cursor() # 創建一個游標對象來執行SQL語句
                cursor.execute(query, params)
                result = cursor.fetchall()
                cursor.close() # 關閉游標和連接
        return result

# 針對新增、刪除、修改的提交
def commit_SQL():
        with sqlite3.connect(db_path) as conn:
                conn.commit()   # 提交資料庫更改
                print("Commit To SQL Success\n")

#endregion

        
#region 查詢使用者
def selectSQL_user(username):
        query = 'SELECT * FROM users WHERE username = ?'
        result = execute_query(query, (username,))
        return dict(result[0]) if result else None
#endregion


#region 由reg地址
# 由暫存資料表查詢值
def selectSQL_Reg(regDF, regKey):
        dataFrame = regDFs[regDF]
        query = "SELECT Value FROM {} WHERE Reg = ?".format(dataFrame)
        result = execute_query(query, (regKey,))
        return result[0][0] if result else None

# 修改值存入暫存資料表
def updateSQL_Reg(regDF, regKey, updateValue):
        dataFrame = regDFs[regDF]
        query = "UPDATE {} SET Value = ? WHERE Reg = ?".format(dataFrame)
        # 嘗試執行更新查詢
        execute_query(query, (updateValue, regKey,))
        print(f"\nSQL Update Success:\n\r--{regDFs[regDF]} Address: {regKey}\n\r--Update Value: {updateValue}")
        commit_SQL()


#endregion


#region 由reg名稱（假設所有名稱都是唯一名稱）
# # 由暫存資料表查詢值
# def selectSQL_RegName(regDF, regName):
#         dataFrame = regDFs[regDF]
#         query = "SELECT Value FROM {} WHERE Name = ?".format(dataFrame)
#         result = execute_query(query, (regName,))
#         return result[0][0] if result else None

# # 修改值存入暫存資料表
# def updateSQL_RegName(regDF, regName, updateValue):
#         dataFrame = regDFs[regDF]
#         query = "UPDATE {} SET Value = ? WHERE Name = ?".format(dataFrame)
#         execute_query(query, (updateValue, regName,))
#         commit_SQL()
#         print("Update SQL Success")

#endregion
        
#region 其他需要暫存的變數
def selectSQL_Var(var):
        query = "SELECT Value FROM otherCacheVariable WHERE Variable = ?"
        result = execute_query(query, (var,))
        return result[0][0] if result else None

def updateSQL_Var(var, updateValue):
        query = "UPDATE otherCacheVariable SET Value = ? WHERE Variable = ?"
        execute_query(query, (updateValue, var,))
        commit_SQL()
        print(f"\nSQL Update Success:\n\r--otherCacheVariable Address: {var}\n\r--Update Value: {updateValue}")
#endregion
        
#region Alarm狀態暫存
def selectAlarmRelay(alarmID):
        query = "SELECT * FROM alarmRelay WHERE relayID = ?"
        result = execute_query(query, (alarmID,))
        return dict(result[0]) if result else None

def updateAlarmRelay(alarmID, status, value):
        query = "UPDATE alarmRelay SET status = ?, value = ? WHERE relayID = ?"
        execute_query(query, (status, value, alarmID,))
        print(f"\nSQL Update Success:\n\r--alarmRelay relayID: {alarmID}\n\r--Update:(status: {status}) ,(value: {value})")
#endregion