#zh-tw
# ProjectPublicVariable.py

# 專案用全域變數、方法

import minimalmodbus

#region modbus RTU連線
# 定義Modbus裝置的串口及地址
# 第一個參數是串口，第二個參數是Modbus地址
instrument_1x = minimalmodbus.Instrument('COM4', 1) # Read Only :read f=1

instrument_3x = minimalmodbus.Instrument('COM4', 3) # Read Only :read f=3,4

instrument_4x = minimalmodbus.Instrument('COM4', 4) # Write Allow :read f=3,4; write f=6,16

# 設定串口波特率，Parity和Stop bits（這些參數需與Modbus設備一致）
for i in [instrument_1x, instrument_3x, instrument_4x]:
    i.serial.baudrate = 9600
    i.serial.parity = minimalmodbus.serial.PARITY_NONE
    i.serial.stopbits = 1
    i.serial.timeout = 1.0

#endregion

#region modbus RTU地址名稱及地址狀態

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
R3X_Mapping={0:'Gas',
             
             2:'Temperature',

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
R4X_Mapping={0:'Temp unit',
             1:'Date Formate',
             2:'Thermal Limit',
             3:'Thermal cut off',
             4:'Set Gas Unit',
             5:'Set Alarm flg1',
             6:'Set Alarm flg2',
             7:'Set Alarm flg3',
             8:'Set Alarm flg4',
             9:'set baudrate',
             10:'set ct range',
             11:'set CT1',
             12:'Set CT2',
             13:'Calibratile set',
             14:'configure set',
             15:'Member',
             16:'Set Pressur',
             
             18:'set CT1_1',
             19:'Set CT2_1',
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

#region R4X 地址狀態

#endregion
tempUnitDist={0:'°C',1:'°F'}


o2_GasUnitDist={0:'ppb',1:'PPM',2:'mg/l',3:'PPMV',4:'%',5:'PPM',6:'mg/l',7:'ppb',8:'PPMV',9:'kPa'}
#endregion


#region 圖表區域
plotTime='10秒' # 圖表週期
#endregion


#region 使用者
presentUser = None
#endregion