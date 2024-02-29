#zh-tw
# userPermissions.py

# 權限類別

class Permissions:
    def __init__(self, id, username, password, 
                 control=False, write=False, read=False, download=False):
        self._id = id
        self._username = username
        self._password = password
        self._control = control
        self._write = write
        self._read = read
        self._download = download

    # def __init__(self, user_dict):
    #     self._id = user_dict['id']
    #     self._username = user_dict['username']
    #     self._password = user_dict['password']
    #     self._control = user_dict.get('control', False)
    #     self._write = user_dict.get('write', False)
    #     self._read = user_dict.get('read', False)
    #     self._download = user_dict.get('download', False)

    @property
    def id(self):
        return self._id

    @property
    def username(self):
        return self._username

    @property
    def password(self):
        return self._password

    @property
    def control(self):
        return self.permissionEncode(self._control)

    @control.setter
    def control(self, value):
        self._control = value

    @property
    def read(self):
        return self.permissionEncode(self._read)

    @read.setter
    def read(self, value):
        self._read = value

    @property
    def write(self):
        return self.permissionEncode(self._write)

    @write.setter
    def write(self, value):
        self._write = value

    @property
    def download(self):
        return self.permissionEncode(self._download)

    @download.setter
    def download(self, value):
        self._download = value

    def permissionEncode(self, value):
        code = {0 : False,
                1 : True}   
        return code[value]

    def userInfo(self):
        text = f'''編號：{self.username} ({self.id})
            控制：{str(self.control)}
            寫入：{str(self.write)}
            讀取：{str(self.read)}
            下載：{str(self.download)}\n'''
        # print(text)
        return text
