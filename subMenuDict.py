#region 選單第一層子介面
# 設定 >>
# from setDisplayOption import displayOptionFrame # 「顯示」
# from setAlarmRelayMenu import setAlarmRelayMenuFrame # 「警報輸出」選項介面
# from setAnalogyOutputOption import analogyOutputOptionFrame # 「類比輸出」選項介面
from setSensorTempLimit import setSensorTempLimitFrame # 「感測器溫度保護」介面

# from setCommunicationOption import comOptionFrame # 「通訊」選項介面

from setTime import setTimeFrame # 「時間」選項介面
from setLanguage import setLanguageFrame # 「語言」選項介面

# 校正 >>
# from calibrateAirManualOption import calibrateAirManualOptionFrame # 「感測器校正」選頁介面
from calibrateAnalogyOutput import calibrateAnalogyOutputFrame # 「類比輸出校正」介面
from calibratePressure import calibratePressureFrame # 「大氣壓力校正」介面

# 記錄 >>
from records_DataStatistics import records_DataStatisticsFrame #「觀看記錄」、「統計表」介面 
from recordDownloadFile import recordDownloadFileFrame # 「下載記錄至隨身碟」介面
from record_AutoManual import record_AutoManualFrame # 「記錄方式設定」介面


# 識別 >>
from id_Frame import id_LogIn_Frame # 登入訊息
from id_DeviceSensorInfo import deviceSensorInfoFrame # 「儀器資訊」、「感測器資訊」介面

# 進入功能後有子功能選項的介面
from subOption import subOptionFrame
#endregion


#region 選單第二層子介面

# 設定 >>
from setUnit import setUnitFrame # 「介面」>>「單位」
from setPlotTime import setPlotTimeFrame # 「介面」>>「波形圖週期」

from setAlarmRelay import setAlarmRelayFrame # 「警報輸出」>>「Relay 1」、「Relay 2」、「Relay 3」
# from setAlarmRelay2 import setAlarmRelay2Frame
# from setAlarmRelay3 import setAlarmRelay3Frame

from setAnalogyOutput import setAnalogyOutputFrame # 「類比輸出」>>「類比濃度」、「類比溫度」
# from setAnalogyTemp import analogyTempFrame
# from setAnalogyConcentration import analogyConcentrationFrame

from set_HTTP_TCPIP import internetFrame # 「通訊」>>「HTTP / TCPIP」
from set_RS485 import rs485_Frame # 「通訊」>>「RS485」

# 校正 >>
from calibrateAirManual import calibrateAirManualFrame # 「感測器校正」>>「直接校正」、「空氣校正」

# 記錄 >>

# 識別 >>

#endregion

#region 未實作功能測試介面
from testEndFrame import testEndFrame
#endregion

#region 子功能在第一層選單選項後
subMenu = {
    '設定':{
        '顯示':['波形圖週期、單位',subOptionFrame,{ 
            '波形圖週期':['',setPlotTimeFrame],
            '單位':['',setUnitFrame]
        }],
        '警報輸出':['Relay 1、Relay 2、Relay 3…',subOptionFrame,{
            'Relay 1':['',setAlarmRelayFrame],
            'Relay 2':['',setAlarmRelayFrame],
            'Relay 3':['',setAlarmRelayFrame]
        }],
        '類比輸出':['濃度、溫度、類型',subOptionFrame,{
            '類比濃度':['',setAnalogyOutputFrame],
            '類比溫度':['',setAnalogyOutputFrame]
        }],
        '感測器溫度保護':['狀態、溫度設定',setSensorTempLimitFrame],
        '診斷':['觀看詳細數值',testEndFrame],
        '通訊':['RS-485、HTTP/TCPIP',subOptionFrame,{
            'RS485':['',rs485_Frame],
            'HTTP / TCPIP':['',internetFrame]
        }],
        '時間':['調整時間、日期格式',setTimeFrame],
        '語言':['多國語言',setLanguageFrame]},
          
    '校正':{
        '感測器校正':['空氣校正、直接校正',subOptionFrame,{
            "直接校正":["使用已知氧氣濃度之氣體、液體進行校正",calibrateAirManualFrame],
            "空氣校正":["將感測器置於空氣中校正",calibrateAirManualFrame]
            }],
        '大氣壓力校正':['大氣壓力校正',calibrateAnalogyOutputFrame],
        '類比輸出校正':['0 - 20 mA、4 - 20 mA',calibratePressureFrame]},

    '記錄':{'觀看記錄':['時間、數值',records_DataStatisticsFrame],
        '統計表':['最高值、平均值、最底值',records_DataStatisticsFrame],
        '下載記錄至隨身碟':['儲存格式：Excel、txt、json、csv',recordDownloadFileFrame],
        '記錄方式設定':['自動、手動',record_AutoManualFrame]},
          
    '識別':{'登入身份':['輸入密碼',id_LogIn_Frame],
        '儀器資訊':['型號、序號、生產日期……',deviceSensorInfoFrame],
        '感測器資訊':['型號、序號、生產日期……',deviceSensorInfoFrame]}
}

#endregion

#region 子功能在第二層選單選項後

'''#「設定」>>「介面」
subDisplay = { 
    '波形圖週期':['',setPlotTimeFrame],
    '單位':['',setUnitFrame]
}

#「設定」>>「警報輸出」
relays = {
    'Relay 1':['',setAlarmRelayFrame],
    'Relay 2':['',setAlarmRelayFrame],
    'Relay 3':['',setAlarmRelayFrame]
}

#「設定」>>「類比輸出」
subAnalogy = {
    '類比濃度':['',setAnalogyOutputFrame],
    '類比溫度':['',setAnalogyOutputFrame]
}

#「設定」>>「通訊」
subCommunication = {
    'RS485':['',rs485_Frame],
    'HTTP / TCPIP':['',internetFrame]
    }

#「校正」>>「感測器校正」
subCalibrateAirManual = {
    "直接校正":["使用已知氧氣濃度之氣體、液體進行校正",calibrateAirManualFrame],
    "空氣校正":["將感測器置於空氣中校正",calibrateAirManualFrame]
}'''


#endregion
