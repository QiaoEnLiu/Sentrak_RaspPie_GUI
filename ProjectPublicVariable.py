#zh-tw
# ProjectPublicVariable.py

# 專案用全域變數、方法

import minimalmodbus, platform, serial
from PyQt5.QtCore import QTimer, QDateTime


timer = QTimer()
current_datetime = QDateTime.currentDateTime()

#region modbus RTU連線
# 埠號名稱依作業系統環境不一樣
port_names = {
    "Windows": "COM6",  # Windows環境的埠號
    "Linux": "/dev/ttyUSB0",  # Linux環境的埠號
}
it_Port=port_names[platform.system()]
try:
    # 定義Modbus裝置的串口及地址
    # 第一個參數是串口，第二個參數是Modbus地址
    instrument_ID1 = minimalmodbus.Instrument(it_Port, 1)

    # 設定串口波特率，Parity和Stop bits（這些參數需與Modbus設備一致）
    instrument_ID1.serial.baudrate = 9600
    instrument_ID1.serial.parity = minimalmodbus.serial.PARITY_NONE
    instrument_ID1.serial.stopbits = 1
    instrument_ID1.serial.timeout = 1.0

except serial.SerialException as e: # 略過未使用埠號、虛擬埠的錯誤
    pass


#endregion

#region R1X 地址名稱
R1X_Mapping={0:'Alarm2 , Alarm1',
             1:'x , Alarm3'}


def R1X_address(searchName):
    address= next((key for key, value in R1X_Mapping.items() if value == searchName), None)
    return address
#endregion

#region R1X 地址狀態

#endregion

#region R3X 地址名稱
R3X_Mapping={0:'Gas', # 已實作

             2:'Temperature', # 已實作

             4:'Calibration Gas %',

             6:'Calibration T',

             8:'Calibration CT1',

             10:'Calibration CT2',

             12:'Read V3 voltage',

             14:'Read V2 voltage',

             16:'Read BAT',
             17:'Read BAT %',
             18:'Read Valid Form Calibration',
             19:'Read Pooling cnt',
             20:'Read Current %'
             }


def R3X_address(searchName):
    address= next((key for key, value in R3X_Mapping.items() if value == searchName), None)
    return address

#endregion

#region R3X 地址狀態

#endregion

#region R4X 地址名稱


R4X_Mapping={0:'Temp unit', # 已實作
             1:'Date Formate', # 已實作
             2:'Thermal Limit', # 已實作
             3:'Thermal cut off', # 已實作
             4:'Set Gas Unit', # 已實作
             5:'Set Alarm flg0',
             6:'Set Alarm flg1',
             7:'Set Alarm flg NoSens',
             8:'Set Alarm flg Thermal',
             9:'set baudrate', # 已實作
             10:'set ct range',
             11:'set CT1',
             12:'Set CT2',
             13:'Calibratile set',
             14:'configure set',
             15:'Member',
             16:'Set Pressur',
             
             18:'set CT1_1', # 已實作
             19:'Set CT2_1', # 已實作
             20:'AD-CT1-Low',
             21:'AD-CT1-High',
             22:'AD-CT2-Low',
             23:'AD-CT2-High',
             24:'RTC_YearMonth',
             25:'RTC_DateHour',
             26:'RTC_Minute'
             }


def R4X_address(searchName):
    address= next((key for key, value in R4X_Mapping.items() if value == searchName), None)
    return address

#endregion

#region R4X 地址數值狀態

#region 'Temp unit'
tempUnitDist={0:'°C',
              1:'°F'}
#endregion

#region 'Date Formate'
dateFormat={0:["EU","dd-MM-yyyy"],
            1:["USA","MM-dd-yyyy"],
            2:["ISO","yyyy-MM-dd"]} #大寫M為月份，小寫m為分鐘
#endregion

#region 'Set Gas Unit'
o2_GasUnitDist={0:'ppb',
                1:'PPM',
                2:'mg/l',
                3:'PPMV',
                4:'%',
                5:'PPM',
                6:'mg/l',
                7:'ppb',
                8:'PPMV',
                9:'kPa'}
#endregion

#region 'set baudrate' (RS-485)

# |-8     |-7     |-6   |-5   |-4|-3|-2|-1       |
# |Byte                                          |
# |7      |6      |5    |4    |3 |2 |1 |0        |
# |DataBit|StopBit|ParityBits |BaudRate|act/deact|

# |-1       |
# |0        |
# |act/deact|
stateRS485={'停用':'0',
            '啟用':'1'}


# |-4|-3|-2|-1
# |3 |2 |1 |
# |BaudRate|
baudRate={'1200':'000',
          '2400':'001',
          '4800':'010',
          '9600':'011',
          '19200':'100',
          '38400':'101',
          '57600':'110',
          '115200':'111'}


# |-6   |-5   |-4
# |5    |4    |
# |ParityBits |
parityBit={'None':'00', 
           'Odd':'01',
           'Even':'10'}

# |-7     |-6
# |6      |
# |StopBit|
stopBit={'1':'0',
         '2':'1'}

# |-8     |-7
# |7      |
# |DataBit|
dataBit={'7':'0',
         '8':'1'}
#endregion


#region 'set CT1_1', 'Set CT2_1', 'AD-CT1-Low', 'AD-CT1-High', 'AD-CT2-Low', 'AD-CT2-High',
current_Min = 0
current_Max = 4095
#endregion

#region 進制轉換 'set baudrate', 'Calibratile set', 'configure set'
# 將二進制轉換為十進制（可接受只由0及1組成的字串）
def b2d(binary): # binary to decimal
    decimal = int(binary, 2)
    return decimal

# 將十進制轉換為二進制
def d2b(decimal): # decimal to binary
    binary = bin(decimal)[2:]
    return binary

#endregion

#endregion

#region 由值找索引（唯一值）
def get_keys_from_value(dictionary, target_value):
    return [key for key, value in dictionary.items() if value == target_value]
#endregion

#region 圖表區域
plotTime = None # 圖表週期
plotTimeDict = {1:'5秒',
                2:'10秒',
                3:'15秒'}
# ['1分','5分','10分','30分','1小時']
#endregion


#region 使用者
presentUser = None
#endregion