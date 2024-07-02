# SQL

import sqlite3

db_path = 'SentrakSQL/SentrakSQL.db'
regDFs={1: 'R1X',
        3: 'R3X',
        4: 'R4X'}
IPS={"User":"",
     "Time":"",
     "IPv4":"",
     "Subnet Mask":"",
     "Default Gateway":"",
     "Hostname":""}

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
    try:
        with sqlite3.connect(db_path) as conn:
            conn.commit()   # 提交資料庫更改
        #     print("Commit To SQL Success\n")
    except sqlite3.Error as e:
        print(f"Error connecting to SQLite database: {e}\n")

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
        print(f"\nSQL Update:\n\r--{regDFs[regDF]} Address: {regKey}\n\r--Update Value: {updateValue}")
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
        
#region R3X記錄
def insertSQL_R3X_Record(r3xRecordTuple):
        query = '''INSERT INTO R3X_Record (times, "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''
        execute_query(query, r3xRecordTuple)
        commit_SQL()
        print(r3xRecordTuple)
#endregion


#region 其他需要暫存的變數
def selectSQL_Var(var):
        query = "SELECT Value FROM otherCacheVariable WHERE Variable = ?"
        result = execute_query(query, (var,))
        # for i in result:
        #         for j in i:
        #                 print(j)
        return result[0][0] if result else None

def updateSQL_Var(var, updateValue):
        query = "UPDATE otherCacheVariable SET Value = ? WHERE Variable = ?"
        execute_query(query, (updateValue, var,))
        commit_SQL()
        print(f"\nSQL Update :\n\r--otherCacheVariable Address: {var}\n\r--Update Value: {updateValue}")
#endregion
        
#region Alarm狀態暫存
def selectAlarmRelay():
        # query = "SELECT * FROM alarmRelay WHERE relayID = ?"
        # result = execute_query(query, (alarmID,))
        # print(result)
        # return dict(result[0]) if result else None
        query = "SELECT * FROM alarmRelay"
        result = execute_query(query)
    
        # 將結果轉換為以relayID作為鍵的字典
        result_dict = {item['relayID']: dict(item) for item in result}
    
        return result_dict


def updateAlarmRelay(alarmID, status, value):
        if status[1] == 0:
                query = "UPDATE alarmRelay SET status = ?, value_o2 = ? WHERE relayID = ?"
                print(f"\nSQL Update:\n\r--alarmRelay relayID: {alarmID}\n\r--Update:(status: {status}) ,(value_o2: {value})")
        else:
                query = "UPDATE alarmRelay SET status = ?, value_temp = ? WHERE relayID = ?"
                print(f"\nSQL Update:\n\r--alarmRelay relayID: {alarmID}\n\r--Update:(status: {status}) ,(value_temp: {value})")
        execute_query(query, (status, value, alarmID,))
        
#endregion

#region IPv4
def selectDefaultNetSetting():
        query = "Select * FROM setInternet where User = 'Default'"
        result = execute_query(query)
        return dict(result[0])

def selectLastNetSetting():
        query = "SELECT * FROM setInternet ORDER BY Time DESC LIMIT 1"
        result = execute_query(query)
        return dict(result[0])

def updateNetSetting(ipInfo):
        IPS["User"]=ipInfo["使用者"]
        IPS["Time"]=ipInfo["時間"]
        IPS["IPv4"]=ipInfo["IPv4"]
        IPS["Subnet Mask"]=ipInfo["子網路遮罩"]
        IPS["Default Gateway"]=ipInfo["預設閘道"]
        IPS["Hostname"]=ipInfo["主機名稱"]

        # query = "Insert Into setInternet Values (?,?,?,?,?,?)"
        query = "Insert Into setInternet (User,Time,IPv4,SubnetMask,DefaultGateway,Hostname) Values (?,?,?,?,?,?)"
        execute_query(query, (IPS["User"], IPS["Time"], IPS["IPv4"], IPS["Subnet Mask"], IPS["Default Gateway"], IPS["Hostname"],))
        print(f"Insert SQL setInternet Table:\n\r{IPS}")



#endregion