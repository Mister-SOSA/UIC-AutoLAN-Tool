from tracemalloc import start
import wx
import os
import requests
import eel
import keyring
import wx
import wx.adv
from requests.auth import HTTPBasicAuth


def authenticate():
    username, password = user_credentials()
    authentication = HTTPBasicAuth(username, password)
    r = requests.get('http://uic.edu', auth=authentication)
    status = r.status_code
    if status == 200:
        return True
    else:
        return False


def register_keyring(username, password):
    keyring.set_password('UIC_Ethernet', username, password)


def user_credentials():
    username = keyring.get_credential('UIC_Ethernet', None).username
    password = keyring.get_password('UIC_Ethernet', username)
    return [username, password]


def keyring_exists():
    if keyring.get_credential('UIC_Ethernet', None) is None:
        return False
    else:
        return True


def start_setup():
    eel.init('web')
    eel.start('index.html', size=(300, 250))


def create_menu_item(menu, label, func):
    item = wx.MenuItem(menu, -1, label)
    menu.Bind(wx.EVT_MENU, func, id=item.GetId())
    menu.Append(item)
    return item


class TaskBarIcon(wx.adv.TaskBarIcon):
    def __init__(self):
        super(TaskBarIcon, self).__init__()
        self.set_icon(wx.Icon('./ethernet.ico', wx.BITMAP_TYPE_ICO))
        self.Bind(wx.adv.EVT_TASKBAR_LEFT_DOWN, self.on_left_down)

    def CreatePopupMenu(self):
        menu = wx.Menu()
        create_menu_item(menu, 'Log out', self.on_logout)
        menu.AppendSeparator()
        create_menu_item(menu, 'Exit', self.on_exit)
        return menu

    def set_icon(self, icon):
        self.SetIcon(icon, 'UIC Auto-LAN')

    def on_left_down(self, event):
        print('Tray icon was left-clicked.')

    def on_logout(self, event):
        # Delete credentials in the keyring
        keyring.delete_password('UIC_Ethernet', user_credentials()[0])

    def on_exit(self, event):
        wx.CallAfter(self.Destroy)


def start_taskbar():
    app = wx.App()
    TaskBarIcon()
    app.MainLoop()


def main():
    if not keyring_exists():
        start_setup()
    else:
        start_taskbar()


if __name__ == '__main__':
    main()
