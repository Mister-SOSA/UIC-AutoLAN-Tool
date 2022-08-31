import wx
import requests
import eel
import keyring
import wx.adv
from requests.auth import HTTPBasicAuth
from win10toast import ToastNotifier

toaster = ToastNotifier()
eel.init('web')


@eel.expose
def authenticate():
    username, password = user_credentials()
    # authentication = HTTPBasicAuth('agocma2', 'Mojezeljice.1')
    authentication = HTTPBasicAuth(username, password)
    r = requests.get('http://uic.edu', auth=authentication)
    status = r.status_code
    if status == 200:
        toaster.show_toast("Connected!",
                           f"Authenticated to LAN as {username}",
                           icon_path="./ethernet.ico",
                           duration=10, threaded=True)
        start_taskbar()
        return True
    else:
        return False


def is_authenticated():
    print('Checking authentication')
    r = requests.get('http://uic.edu')
    status = r.status_code
    if status == 200:
        return True
    elif status == 401:
        return False


@eel.expose
def register_keyring(username, password):
    keyring.set_password('UIC_Ethernet', username, password)
    if authenticate():
        return True
    else:
        eel.show_error()
        return False


def user_credentials():
    print('Getting credentials')
    username = keyring.get_credential('UIC_Ethernet', None).username
    password = keyring.get_password('UIC_Ethernet', username)
    return [username, password]


def keyring_exists():
    if keyring.get_credential('UIC_Ethernet', None) is None:
        return False
    else:
        return True


def start_setup():
    eel.start('index.html', size=(300, 250), shutdown_delay=0)


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
        pass

    def on_logout(self, event):
        # Delete credentials in the keyring
        try:
            username = keyring.get_credential('UIC_Ethernet', None).username
            keyring.delete_password('UIC_Ethernet', user_credentials()[0])
            toaster.show_toast("Logged out",
                               f"The user {username} has been removed from the keychain.",
                               icon_path="./ethernet.ico")
            start_setup()
        except Exception as e:
            print(e)

    def on_exit(self, event):
        wx.CallAfter(self.Destroy)


@eel.expose
def start_taskbar():
    print('starting taskbar')
    app = wx.App()
    TaskBarIcon()
    app.MainLoop()


def main():
    if not keyring_exists():
        start_setup()
    elif keyring_exists() and not is_authenticated():
        authenticate()
    elif is_authenticated() and keyring_exists():
        start_taskbar()


if __name__ == '__main__':
    main()
