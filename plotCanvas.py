#zh-tw
# PlotCanvas.py
# 初始子畫面折線圖

#!/usr/bin/python 在linux底下將此行置於第一行

try:
    import numpy, traceback, platform
    import matplotlib.pyplot as plt
    from matplotlib.font_manager import FontProperties, FontManager
    from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
    from unit_transfer import unit_transfer

    import ProjectPublicVariable as PPV
except Exception as e:
    print(f"An error occurred: {e}")
    traceback.print_exc()
    input("Press Enter to exit")

# matplotlib.use('Qt5Agg')
 
#region 針對Plot的中文字型
# fontPath='word_font/Chinese/zh/'

# 選擇一個字型
# 使用 FontManager 取得系統上所有可用的字型
font_manager = FontManager()
font_list = font_manager.ttflist
selected_font = None
for font in font_list:
    # print(font)
    if 'Microsoft JhengHei' in font.name:  # 這裡假設您想要使用名為 'SimHei'或'Microsoft JhengHei'的字型
        selected_font = font.fname
        break
    elif 'WenQuanYi Zen Hei' in font.name:
        selected_font = font.fname
        break
#end region

plotTime_limit=0


#region plotCanvas
class plotCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=75):
        fig, self.ax = plt.subplots(figsize=(width, height), dpi=dpi)
        super().__init__(fig)
        self.setParent(parent)

        self.x_data = []
        self.temperature_data = []
        self.oxygen_concentration_data = []        

        # 隱藏上側和右側的軸線
        self.ax.spines['right'].set_visible(False)
        self.ax.spines['top'].set_visible(False)

    def plot(self, temperature_unit, oxygen_concentration, temperature):
        global plotTime_limit
        # print(f'O2:{oxygen_concentration:.2f}, T:{temperature:.2f} {temperature_unit}')

        # 使用選擇的字型進行圖表繪製
        font = FontProperties(fname=selected_font, size=10)
        self.temperature_unit=unit_transfer.set_temperature_unit(unit=temperature_unit)

        # 生成溫度和氧氣濃度的數據
        # 更新數據
        if len(self.x_data) == 0:
            self.x_data.append(1)
        else:
            self.x_data.append(self.x_data[-1] + 1)
        self.temperature_data.append(temperature)
        self.oxygen_concentration_data.append(oxygen_concentration)

        # print(f'{self.x_data[-1]} O2:{oxygen_concentration:.2f}, T:{temperature:.2f} {temperature_unit}')
        if PPV.plotTime=='5秒':
            plotTime_limit=5
        elif PPV.plotTime=='10秒':
            plotTime_limit=10
        elif PPV.plotTime=='15秒':
            plotTime_limit=15
        else:
            plotTime_limit=10

        if len(self.x_data) > plotTime_limit:
            remove_count = len(self.x_data) - plotTime_limit
            # print(f'X軸溢出：{remove_count}')
            for _ in range(remove_count):
                self.x_data.pop(0)
                self.temperature_data.pop(0)
                self.oxygen_concentration_data.pop(0)

        # 繪製折線圖
        lineTemp, = self.ax.plot(self.x_data, self.temperature_data, label='溫度'+self.temperature_unit, color='blue')  # Temperature
        lineO2, = self.ax.plot(self.x_data, self.oxygen_concentration_data, label='氧氣濃度', color='green')  # Oxygen Concentration

        # 繪製散點圖
        scatterTemp = self.ax.scatter(self.x_data, self.temperature_data, label='溫度'+self.temperature_unit, color='blue')  # Temperature
        scatterO2 = self.ax.scatter(self.x_data, self.oxygen_concentration_data, label='氧氣濃度', color='green')  # Oxygen Concentration

        # 設定x軸的顯示範圍
        if len(self.x_data) > 1:
            self.ax.set_xlim(self.x_data[0], self.x_data[-1] + 1)

        self.ax.set_xticks(range(self.x_data[0], self.x_data[-1] + 2, 1))

        self.ax.set_ylim(0, 30)

        self.ax.set_title(
            '溫度、氧氣濃度時間狀態',
            fontdict={'fontsize': 18, 'fontweight': 'bold'},
            fontproperties=font)  # Temperature and Oxygen Concentration
        self.ax.set_xlabel(
            f'時間（每{PPV.plotTime}）',
            fontdict={'fontsize': 14, 'fontweight': 'bold'},
            fontproperties=font)
        # print(f'X時間軸：{self.ax.get_xlabel()}')
        # print(f'X時間軸最大值：{len(self.x_data)}')
        self.ax.set_ylabel(
            '溫度、氧氣濃度數值',
            fontdict={'fontsize': 14, 'fontweight': 'bold'},
            fontproperties=font)

        # 添加數值標籤
        for (i, j) in zip(self.x_data, self.temperature_data):
            self.ax.text(i, j, f'{j:.2f}', color='blue', ha='right', va='bottom')

        for (i, j) in zip(self.x_data, self.oxygen_concentration_data):
            self.ax.text(i, j, f'{j:.2f}', color='green', ha='left', va='top')

        # 添加圖例
        self.ax.legend(handles=[lineTemp, lineO2], labels=['溫度'+self.temperature_unit, '氧氣濃度'], prop=font)
        self.ax.legend(handles=[scatterTemp, scatterO2], prop=font)

        self.draw()

#endregion