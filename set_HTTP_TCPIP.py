#zh-tw
# set_HTTP_TCPIP.py
# 「HTTP \ TCPIP」

# 此程式碼為「設定」底下進入「HTTP \ TCPIP」並實作網路設定的頁面
    # 尚未能直接設定網路

try:
    
    from PyQt5.QtCore import Qt, QDateTime
    from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QScrollArea,\
          QHBoxLayout, QLineEdit, QPushButton, QMessageBox, QDialog
    from PyQt5.QtGui import QFont, QIntValidator
    # from datetime import datetime

    import os, traceback, json, psutil, socket, subprocess, platform

    import ProjectPublicVariable as PPV
    import PySQL

except Exception as e:
    print(f"An error occurred: {e}")
    traceback.print_exc()
    input("Press Enter to exit")

try:
    # 獲取腳本檔案的目錄
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # 讀取預設值的 JSON 檔案
    log_file = os.path.join(script_dir, 'record/Sentrak_set_ip.json')

    # 使用相對路徑構建檔案路徑
    default_ip_file = os.path.join(script_dir, 'record', 'Sentrak_default_ip.json')
except Exception as e:
    print(f"An error occurred: {e}")
    traceback.print_exc()

font = QFont()

default_ip_values=PPV.IPS
last_ip_values=PPV.IPS
set_ip_values={"使用者":"","時間":"",**PPV.IPS}


class internetFrame(QWidget):
    def __init__(self, title, _style, stacked_widget, sub_pages):
        super().__init__()
        # print(title)
        
        self.title = title
        self.sub_pages=sub_pages

        # print(self.title, ProjectPublicVariable.presentUser.userInfo())

        # 標題列
        title_layout = QVBoxLayout()        
        self.title_label = QLabel(self.title, self)
        # title_label.setAlignment(Qt.AlignCenter)  
        font.setPointSize(18)
        self.title_label.setFont(font)
        # self.title_label.setStyleSheet(_style)
        title_layout.addWidget(self.title_label)

        # title_layout.setContentsMargins(0, 0, 0, 0)
        # title_layout.setSpacing(0)

        internetInfo_layout = QVBoxLayout()
        # internetInfo_layout.setContentsMargins(0, 0, 0, 0)
        # internetInfo_layout.setSpacing(0)


        self.ipconfig_texts = {
            "IPv4": [QLineEdit() for _ in range(4)],
            "子網路遮罩": [QLineEdit() for _ in range(4)],
            "預設閘道": [QLineEdit() for _ in range(4)],
            # "DNS 伺服器": [QLineEdit() for _ in range(4)]
        }
        self.input_boxes=None

        # 在這裡，取得 layout 和 input_boxes
        ip_layout, ipv4_input_boxes = self.ip_input_layout("IPv4")
        subnet_layout, subnet_input_boxes = self.ip_input_layout("子網路遮罩")
        gateway_layout, gateway_input_boxes = self.ip_input_layout("預設閘道")
        # dns_layout, dns_input_boxes = self.ip_input_layout("DNS 伺服器")
        hostname_layout = QVBoxLayout()

        # 將 input_boxes 賦值給對應的 ipconfig_texts 鍵
        self.ipconfig_texts["IPv4"] = ipv4_input_boxes
        self.ipconfig_texts["子網路遮罩"] = subnet_input_boxes
        self.ipconfig_texts["預設閘道"] = gateway_input_boxes
        # self.ipconfig_texts["DNS 伺服器"] = dns_input_boxes
        self.hostname_label = QLabel("主機名稱：")
        self.hostname_Input = QLineEdit()
        self.hostname_label.setFont(font)
        self.hostname_Input.setFont(font)

        hostname_layout.addWidget(self.hostname_label)
        hostname_layout.addWidget(self.hostname_Input)

        # 獲取預設的 IP 值
        print(self.get_main_network_info())
        last_ip_values["IPv4"] = self.get_main_network_info()["IPv4"].split('.')
        last_ip_values["子網路遮罩"] = self.get_main_network_info()["SubnetMask"].split('.')
        last_ip_values["預設閘道"] = self.get_main_network_info()["DefaultGateway"].split('.')
        last_ip_values["主機名稱"] = self.get_main_network_info()["Hostname"]

        # last_ip_values["IPv4"] = str(PySQL.selectLastNetSetting()["IPv4"]).split('.')
        # last_ip_values["子網路遮罩"] = str(PySQL.selectLastNetSetting()["SubnetMask"]).split('.')
        # last_ip_values["預設閘道"] = str(PySQL.selectLastNetSetting()["DefaultGateway"]).split('.')
        # last_ip_values["主機名稱"] = PySQL.selectLastNetSetting()["Hostname"]

        # 將預設值填入對應的 QLineEdit
        for name, input_boxes in self.ipconfig_texts.items():
            values = last_ip_values.get(name, [])  # 從 default_ip_values 取得對應名稱的值
            for input_box, value in zip(input_boxes, values):
                input_box.setText(value)
        self.hostname_Input.setText(last_ip_values["主機名稱"])


        set_button=QPushButton('設定', self)
        set_button.setFont(font)
        set_button.clicked.connect(lambda: self.setInternet())
        
        ip_default_button=QPushButton('預設IP組', self)
        ip_default_button.setFont(font)
        ip_default_button.clicked.connect(lambda: self.ip_to_default())

        network_stat_bt=QPushButton('網路狀態',self)
        network_stat_bt.setFont(font)
        network_stat_bt.clicked.connect(lambda: self.show_networt())

        setting_layout=QHBoxLayout()
        setting_layout.addWidget(set_button)
        setting_layout.addWidget(ip_default_button)
        setting_layout.addWidget(network_stat_bt)

        internetInfo_layout.addStretch()
        internetInfo_layout.addLayout(ip_layout)
        internetInfo_layout.addStretch()
        internetInfo_layout.addLayout(subnet_layout)
        internetInfo_layout.addStretch()
        internetInfo_layout.addLayout(gateway_layout)
        internetInfo_layout.addStretch()
        # internetInfo_layout.addLayout(dns_layout)
        # internetInfo_layout.addStretch()
        internetInfo_layout.addLayout(hostname_layout)
        internetInfo_layout.addStretch()
        internetInfo_layout.addLayout(setting_layout)


        # 整體佈局
        main_layout = QVBoxLayout(self)
        # main_layout.setContentsMargins(0, 0, 0, 0)
        # main_layout.setSpacing(0)
        main_layout.addLayout(title_layout)
        main_layout.addLayout(internetInfo_layout)

        print(title ,PPV.presentUser.userInfo())

        self.stacked_widget = stacked_widget
        deviceInfo_index = self.stacked_widget.addWidget(self)
        self.current_page_index = deviceInfo_index
        # 設定當前顯示的子畫面索引
        print(f'{title} Index: {self.stacked_widget.count()}')


    def ip_input_layout(self, name):
        # 創建水平佈局，包含標籤和輸入框
        font.setPointSize(16)
        layout = QVBoxLayout()

        label_layout = QVBoxLayout()
        ip_layout = QHBoxLayout()

        # 創建標籤，顯示名稱
        label = QLabel(f"{name}:")
        label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        label_layout.addWidget(label)

        label.setFont(font)


        # 創建輸入框，用小數點分隔
        # 用於存儲四個QLineEdit的列表
        input_boxes = [QLineEdit() for _ in range(4)]
        
        for input_box in input_boxes:
            # 創建一個QIntValidator，限制輸入範圍為0到255
            int_validator = QIntValidator(0, 255, self)

            # 將QIntValidator設置給QLineEdit
            input_box.setValidator(int_validator)
            input_box.setText('0')
        
        for input_box in input_boxes:
            # ip.append(input_box.text())
            input_box.setFont(font)
            ip_layout.addWidget(input_box)
            if input_box != input_boxes[-1]:  # 不是最後一個輸入框，添加小數點標籤
                dot_label = QLabel(".")
                dot_label.setFont(font)
                ip_layout.addWidget(dot_label)

        self.ipconfig_texts[name] = self.input_boxes
        # ip_text.append(ip)

        layout.addLayout(label_layout)
        layout.addLayout(ip_layout)

        return layout, input_boxes


    def setInternet(self):

        if PPV.presentUser.write == True:
            print('設定網路:', PPV.presentUser.write)

            # 建立一個字典，用於儲存各個類別的 IP 資訊
            ip_values = {}
        
            for name, input_boxes in self.ipconfig_texts.items():
                # 檢查每個輸入框是否有有效的文本
                values = [str(int(input_box.text())) for input_box in input_boxes]
                
                # 檢查是否有超出範圍的值，顯示提示並要求重新輸入
                if any(not 0 <= int(value) <= 255 if value else False for value in values):
                    QMessageBox.warning(self, '錯誤', f'請輸入有效的數字 (0 到 255) - {name}')
                    return  # 跳出迴圈，避免重複提示
                else:                   
                    ip_values[name] = values

            print("IP Config 文字框:")
            for name, values in ip_values.items():
                print(f"{name}: {values}")
            print(f"{self.hostname_label.text()}: {self.hostname_Input.text()}")


            reply = QMessageBox.question(self, '網路設定', '確定要儲存嗎？',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                QMessageBox.information(self, '設定成功', '設定後請注意是否連線成功')
                self.write_ip_info(PPV.presentUser.username)
            else:
                return

        else:
            print('您沒有權限設定網路:', PPV.presentUser.control)

    def ip_to_default(self):
        # print(PySQL.selectDefaultNetSetting())
        default_ip_values["IPv4"] = str(PySQL.selectDefaultNetSetting()["IPv4"]).split('.')
        default_ip_values["子網路遮罩"] = str(PySQL.selectDefaultNetSetting()["SubnetMask"]).split('.')
        default_ip_values["預設閘道"] = str(PySQL.selectDefaultNetSetting()["DefaultGateway"]).split('.')
        default_ip_values["主機名稱"] = PySQL.selectDefaultNetSetting()["Hostname"]
        

        # ips={default_ip_values["IPv4"], default_ip_values["子網路遮罩"], default_ip_values["預設閘道"]}
        # 將預設值填入對應的 QLineEdit
        for name, input_boxes in self.ipconfig_texts.items():
            values = default_ip_values.get(name, [])  # 從 default_ip_values 取得對應名稱的值
            for input_box, value in zip(input_boxes, values):
                input_box.setText(value)
        self.hostname_Input.setText(default_ip_values["主機名稱"])
        current_datetime = QDateTime.currentDateTime()
        formatted_datetime = current_datetime.toString(f"{PPV.dateFormat[2][1]} hh:mm:ss")
        print(f"{formatted_datetime}\n\r{default_ip_values}")


    def write_ip_info(self, username):
        # 將 QlineEdit 對象轉換為其文本值
        for name, input_boxes in self.ipconfig_texts.items():
            values = [input_box.text() for input_box in input_boxes]
            set_ip_values[name] = '.'.join(values)
        current_datetime = QDateTime.currentDateTime()
        formatted_datetime = current_datetime.toString(f"{PPV.dateFormat[2][1]} hh:mm:ss")
        set_ip_values["使用者"] = username
        set_ip_values["時間"] = formatted_datetime
        set_ip_values["主機名稱"] = self.hostname_Input.text() or username

        PySQL.updateNetSetting(set_ip_values)
        # print(f"{username}:{set_ip_values}")

    
        
    def show_networt(self):

        # network_info = '網路介面資訊:' + '暫未提供' + '\n'
        network_info = '網路介面資訊:' + '\n'
        for line in self.get_network_info():
            network_info += line + '\n'
        # print(network_info)
            
        MyDialog(network_info).exec_()
    
    def get_main_network_info(self):
        try:
            hostname = socket.gethostname()

            # 獲取IPv4地址、子網路遮罩和預設閘道（針對Windows）
            if platform.system() == "Windows":
                result = subprocess.getoutput("ipconfig | findstr IPv4")
                ip_line = [line for line in result.splitlines() if "IPv4 Address" in line][0]
                ip_address = ip_line.split(":")[1].strip()

                result = subprocess.getoutput("ipconfig | findstr Subnet")
                netmask_line = [line for line in result.splitlines() if "Subnet Mask" in line][0]
                netmask = netmask_line.split(":")[1].strip()

                result = subprocess.getoutput("ipconfig | findstr Default")
                gateway_line = [line for line in result.splitlines() if "Default Gateway" in line][0]
                gateway = gateway_line.split(":")[1].strip()

            # 獲取IPv4地址、子網路遮罩和預設閘道（針對Linux）
            elif platform.system() == "Linux":

                # 獲取IPv4地址和子網遮罩（針對Linux）
                result = subprocess.getoutput("ip addr show | grep 'inet ' | grep -v '127.0.0.1' | awk '{print $2}'")
                ip_subnet = result.split()[0]
                ip_address, cidr = ip_subnet.split("/")
                netmask = PPV.cidr_to_netmask(int(cidr))

                # 獲取預設閘道（針對Linux）
                result = subprocess.getoutput("ip route | grep default | awk '{print $3}'")
                gateway = result.splitlines()[0]

            return {"IPv4": ip_address, "SubnetMask": netmask, "DefaultGateway": gateway, "Hostname": hostname}

        except socket.gaierror:
            return {'error': '無法取得主機IP地址'}
        except IndexError:
            return {'error': '無法解析網絡輸出'}
        except Exception as e:
            return {'error': f'發生錯誤: {e}'}
    
    
    def get_network_info(self):
        try:
            addresses = psutil.net_if_addrs()
            stats = psutil.net_if_stats()
            result = []

            # 獲取當前連線的網路介面
            current_interface = psutil.net_connections(kind='inet')[0].laddr[0]

            # 獲取主機名稱
            hostname = socket.gethostname()
            result.append(f'Hostname: {hostname}')
            for interface, addrs in addresses.items():
                result.append(f' Interface: {interface} {"(Connected)" if interface == current_interface else ""}')
                for addr in addrs:
                    result.append(f'   Address Family: {addr.family}')
                    result.append(f'     Address: {addr.address}')
                    result.append(f'     Netmask: {addr.netmask}')
                    result.append(f'     Broadcast: {addr.broadcast}')
                
                # 添加預設閘道資訊
                if interface in stats:
                    gateway = 'N/A'
                    for addr in addrs:
                        if addr.family == socket.AF_INET:
                            gateway = addr.address
                            break
                    result.append(f'     Default Gateway: {gateway}')
                    
            return result
        except Exception as e:
            traceback.print_exc()
            return f'無法取得網路介面資訊: {e}'
    

        
class MyDialog(QDialog):
    def __init__(self, text):
        super().__init__()

        # 創建一個 QScrollArea 作為主要顯示區域
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        internetInfo_label = QLabel(text,self)
        font.setPointSize(12)
        internetInfo_label.setFont(font)
        # internetInfo_label.setStyleSheet(_style) 

        # internetInfo_label.setText(text)

        # 將內容設置為 QScrollArea 的可滾動部分
        scroll_area.setWidget(internetInfo_label)

        # 將 QScrollArea 添加到主佈局
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(scroll_area)

        # 設定 QDialog 的大小
        self.resize(400, 360)

#region IP <> Json File
    # def ip_to_default(self):

    #     try:
    #         with open(default_ip_file, 'r', encoding='utf-8') as file:
    #             json_str = file.read()
    #             default_values = json.loads(json_str)
    #             # print(default_values)
    #     except (FileNotFoundError, json.JSONDecodeError) as e:
    #         print(f"Error reading default values: {e}")
    #         default_values = {}

    #     # 獲取預設的 IP 值
    #     default_ip_values = default_values.get('default', {}).get('ip_values',{})
    #     # print(default_ip_values)

    #     # 將預設值填入對應的 QLineEdit
    #     for name, input_boxes in self.ipconfig_texts.items():
    #         values = default_ip_values.get(name, [])  # 從 default_ip_values 取得對應名稱的值
    #         for input_box, value in zip(input_boxes, values):
    #             input_box.setText(value)

    # def write_ip_info(self, username):
        
    #     # 讀取現有的使用者資訊或創建一個新的使用者資訊字典
    #     try:
    #         with open(log_file, 'r', encoding='utf-8') as file:
    #             ip_update_info = json.load(file)
    #     except (FileNotFoundError, json.JSONDecodeError):
    #         ip_update_info = {}

    #     # 將 QlineEdit 對象轉換為其文本值
    #     converted_ip_values = {}
    #     for name, input_boxes in self.ipconfig_texts.items():
    #         values = [input_box.text() for input_box in input_boxes]
    #         converted_ip_values[name] = values

    #     # 創建新的使用者資訊，包括使用者名稱和時間戳記
    #     user_info = {
    #         'username': username,
    #         'update_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    #         'ip_values': converted_ip_values
    #     }

    #     # 使用不同的時間戳記作為鍵，以確保每次都是新增獨立的紀錄
    #     timestamp_key = datetime.now().strftime('%Y%m%d%H%M%S')
    #     ip_update_info[timestamp_key] = user_info
            
    #     print(user_info)

    #     # 寫入更新後的使用者資訊到檔案
    #     with open(log_file, 'w', encoding='utf-8') as file:
    #         json_str = json.dumps(ip_update_info, ensure_ascii=False)
    #         json_string = json_str.replace(', "ip_values": ', ', "ip_values":\n').replace(']}},',']}},\n').replace('"],','"],\n')
    #         file.write(json_string)


    #     previous_sub_frame = self.stacked_widget.currentWidget()
    #     self.stacked_widget.removeWidget(previous_sub_frame)
    #     self.current_page_index = self.stacked_widget.currentIndex()

    #     for title, sub_page_index in list(self.sub_pages.items()):
    #         if sub_page_index not in range(self.stacked_widget.count()):
    #             del self.sub_pages[title]

    #     self.stacked_widget.setCurrentIndex(self.current_page_index)
        
    #endregion

#region 失敗作：查詢主要連線
    # def get_main_network_info(self):
    #     try:
    #         addresses = psutil.net_if_addrs()
    #         stats = psutil.net_if_stats()

    #         # 獲取當前連線的網路介面
    #         current_interface = psutil.net_connections(kind='inet')[0].laddr[0]

    #         # 獲取主機名稱
    #         hostname = socket.gethostname()

    #         main_network_info = {
    #             'Hostname': hostname,
    #             'Interfaces': {}
    #         }

    #         for interface, addrs in addresses.items():
    #             interface_info = {
    #                 'Connected': interface == current_interface,
    #                 'Addresses': [],
    #                 'DefaultGateway': 'N/A'
    #             }

    #             for addr in addrs:
    #                 addr_info = {
    #                     'Family': addr.family,
    #                     'Address': addr.address,
    #                     'Netmask': addr.netmask,
    #                     'Broadcast': addr.broadcast
    #                 }
    #                 interface_info['Addresses'].append(addr_info)

    #             if interface in stats:
    #                 for addr in addrs:
    #                     if addr.family == socket.AF_INET:
    #                         interface_info['DefaultGateway'] = addr.address
    #                         break

    #             main_network_info['Interfaces'][interface] = interface_info

    #         return main_network_info

    #     except Exception as e:
    #         return {'error': f'無法取得網路介面資訊: {e}'}
        
    # def filter_main_connection(self, network_info):
    #     main_connection = None
    #     other_connections = {}

    #     for interface, info in network_info['Interfaces'].items():
    #         if info['Connected']:
    #             main_connection = {
    #                 'Interface': interface,
    #                 'Connected': info['Connected'],
    #                 'Addresses': info['Addresses'],
    #                 'DefaultGateway': info['DefaultGateway']
    #             }
    #             break
    #         else:
    #             other_connections[interface] = {
    #                 'Connected': info['Connected'],
    #                 'Addresses': info['Addresses'],
    #                 'DefaultGateway': info['DefaultGateway']
    #             }

    #     filtered_info = {
    #         'Hostname': network_info['Hostname'],
    #         'MainConnection': main_connection,
    #         'OtherConnections': other_connections
    #     }

    #     return filtered_info
    #endregion

