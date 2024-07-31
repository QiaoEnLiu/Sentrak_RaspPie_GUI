#zh-tw 此程式碼是用來產生折線圖的程式碼，每秒更新時使用此程式碼，當有新的數據進來時，圖表就以折線延伸
# plotCanvasPG.py
# 初始子畫面折線圖

try:
    import traceback
    from PyQt5.QtWidgets import QWidget, QVBoxLayout
    import pyqtgraph as pg
    from unit_transfer import unit_transfer

    import ProjectPublicVariable as PPV
    import PySQL
except Exception as e:
    print(f"An error occurred: {e}")
    traceback.print_exc()
    input("Press Enter to exit")

# matplotlib.use('Qt5Agg')
 


# plotTime_limit = PPV.plotTimeDefault[1]


#region plotCanvas
class PlotCanvasPG(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

        self.x_data = []
        self.temperature_data = []
        self.oxygen_concentration_data = []


    def initUI(self):
        self.layout = QVBoxLayout(self)
        self.setLayout(self.layout)

        self.plot_widget = pg.PlotWidget()  

        self.plot_widget.hideButtons()

        self.plot_widget.setMenuEnabled(False)
        self.plot_widget.setMouseEnabled(x=False, y=False)
        self.layout.addWidget(self.plot_widget)
        
        self.plot_widget.setBackground('w')
        self.plot_widget.showGrid(x=True, y=True)

        self.plot_curve_temperature = self.plot_widget.plot(pen='b', name='溫度')
        self.plot_curve_oxygen = self.plot_widget.plot(pen='g', name='氧氣濃度')

        self.plot_widget.setTitle('溫度、氧氣濃度時間狀態')
        
        # 設置 x 和 y 軸的顯示範圍從 0 開始
        # self.plot_widget.setXRange(0, plotTime_limit)
        self.plot_widget.setYRange(0, 30)

        self.x_axis = self.plot_widget.getAxis('bottom')
        self.y_axis = self.plot_widget.getAxis('left')



    def plot(self, plotTimeDictKey, temperature_unit, oxygen_concentration, temperature):
        # global plotTime_limit

        
        # 補充設定 plotTime_limit 的部分
        
        #region PlotTime判斷式
        # if PPV.plotTime == '5秒':
        #     plotTime_limit = 5
        # elif PPV.plotTime == '10秒':
        #     plotTime_limit = 10
        # elif PPV.plotTime == '15秒':
        #     plotTime_limit = 15
        # else:
        #     print('圖表週期未成功取得暫存值')
        #     plotTime_limit = 10
        #endregion
        plotTime_limit = PPV.plotTimeDict.get(plotTimeDictKey, PPV.plotTimeDict[3])[1]


        self.x_axis.setLabel(f'時間（每{PPV.plotTime}）')
        self.y_axis.setLabel('溫度、氧氣濃度數值')
        
        # 其餘部分保持不變
        self.x_data.append(self.x_data[-1] + 1 if self.x_data else 1)
        self.temperature_data.append(temperature)
        self.oxygen_concentration_data.append(oxygen_concentration)

        if len(self.x_data) > plotTime_limit:
            remove_count = len(self.x_data) - plotTime_limit
            
            self.x_data = self.x_data[remove_count:]
            self.temperature_data = self.temperature_data[remove_count:]
            self.oxygen_concentration_data = self.oxygen_concentration_data[remove_count:]

        # 設置 x 和 y 軸的顯示格式，只顯示正整數
        self.x_axis.setTicks([[(i, str(i)) for i in range(max(0, self.x_data[0]), self.x_data[-1] + 1)]])
        self.y_axis.setTicks([[(i, str(i)) for i in range(0, 30, 5)]])

        # self.x_axis.setTickSpacing(major=1, minor=None)
        # self.y_axis.setTickSpacing(major=5, minor=None)

        self.plot_curve_temperature.setData(self.x_data, self.temperature_data)
        self.plot_curve_oxygen.setData(self.x_data, self.oxygen_concentration_data)

        # 更新 x 軸的顯示範圍
        if self.x_data:
            self.plot_widget.setXRange(max(1, self.x_data[0]), self.x_data[-1])
            # self.plot_widget.getAxis('top').setTicks(None)
#endregion