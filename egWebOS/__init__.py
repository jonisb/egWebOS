# -*- coding: utf-8 -*-
"""
WebOS support plugin for EventGhost
"""
from __future__ import print_function, unicode_literals
from pywebostv.connection import WebOSClient

eg.RegisterPlugin(
    name="WebOS connect",
    author="Joni Borén",
    version="0.0.0",
    kind="external",
    guid="{523fa3a6-f1a9-405d-a28a-8d211f76562b}",
    canMultiLoad=True,
    createMacrosOnAdd=False,
    url="https://github.com/jonisb/egWebOS/issues",  # TODO: Create support thread and link.
    description="""Adds actions to control WebOS devices like LG TVs.""",  # TODO: Add description, use <rst>?
)

from pywebostv.discovery import discover


class WebOS(eg.PluginClass):
    def __init__(self):  # TODO:
        pass

    def Configure(self, IP='', Code=''):  # TODO: Separate args or combined?
        def initPanel(self):
            def Search(event):
                import threading, Queue
                pipe = Queue.Queue()
                class myThread(threading.Thread):
                    def __init__(self, IP, retries):
                        #threading.Thread.__init__(self)
                        super(myThread, self).__init__()
                        self.IP = IP
                        self.retries = retries
                    def run(self):
                        for retry in range(self.retries):
                            pipe.put(retry)
                            try:
                                IP = discover("urn:schemas-upnp-org:device:MediaRenderer:1", keyword="LG", hosts=True, retries=1).pop()
                            except KeyError:
                                pass
                            else:
                                print('Found IP: {0} try {1}'.format(IP, retry+1))
                                self.IP.SetValue(IP)
                                break
                        else:
                            eg.PrintError('WebOS Connect: was not able to find any compatiple devices.')

                retries = 5
                t1 = myThread(self.IP, retries)
                t1.start()
                try:
                    dlg = wx.ProgressDialog("Searchin for WebOS devices", 'Please wait..', retries, style=wx.PD_APP_MODAL | wx.PD_ELAPSED_TIME | wx.PD_CAN_ABORT | wx.STAY_ON_TOP | wx.PD_AUTO_HIDE)
                    while t1.isAlive():
                        try:
                            retry = pipe.get_nowait()
                            pipe.task_done()
                        except Queue.Empty:
                            pass
                        dlg.Update(retry+1, "Waiting for device... try {0}".format(retry+1))
                        wx.MilliSleep(100)
                except Exception: # todo: better exception
                    pass
                else:
                    dlg.Destroy()
                t1.join()

            def Register(event):
                store = {'client_key': self.Code.GetValue()}
                client = WebOSClient(self.IP.GetValue())
                try:
                    client.connect()
                except Exception: # todo: better exception
                    eg.PrintError("Can't connect to device") # todo:
                else:
                    try:
                        for status in client.register(store):
                            if status == WebOSClient.PROMPTED:
                                print("Please accept the connect on the TV!") # todo: show dialog
                            elif status == WebOSClient.REGISTERED:
                                print("Registration successful!")
                                self.Code.SetValue(store['client_key'])
                    except Exception: # todo: better exception
                        eg.PrintError("Failed to register.") # todo:
                    client.close()

            sizer_1 = wx.BoxSizer(wx.VERTICAL)

            sizer_2 = wx.BoxSizer(wx.HORIZONTAL)
            sizer_1.Add(sizer_2, 1, wx.EXPAND, 0)

            IP_label = wx.StaticText(self, wx.ID_ANY, "IP address")
            sizer_2.Add(IP_label, 0, 0, 0)

            self.IP = wx.TextCtrl(self, wx.ID_ANY, IP)
            sizer_2.Add(self.IP, 0, 0, 0)

            self.Search = wx.Button(self, wx.ID_ANY, "Search")
            self.Search.SetToolTipString("Search for devices to control over the network")
            self.Search.Bind(wx.EVT_BUTTON, Search)
            sizer_2.Add(self.Search, 0, 0, 0)

            sizer_3 = wx.BoxSizer(wx.HORIZONTAL)
            sizer_1.Add(sizer_3, 1, wx.EXPAND, 0)

            label_code = wx.StaticText(self, wx.ID_ANY, "Code")
            sizer_3.Add(label_code, 0, 0, 0)

            self.Code = wx.TextCtrl(self, wx.ID_ANY, Code)
            self.Code.SetToolTipString("This code is used to access the WebOS device")
            sizer_3.Add(self.Code, 0, 0, 0)

            self.Register = wx.Button(self, wx.ID_ANY, "Register")
            self.Register.SetToolTipString("Connect using code or request a new code from device")
            self.Register.Bind(wx.EVT_BUTTON, Register)
            sizer_3.Add(self.Register, 0, 0, 0)

            self.SetSizer(sizer_1)
            sizer_1.Fit(self)

            self.Layout()

        panel = eg.ConfigPanel()
        initPanel(panel)

        while panel.Affirmed():
            panel.SetResult(panel.IP.GetValue(), panel.Code.GetValue())

    def __start__(self, IP, Code):  # TODO: Match Configure
        pass

    def __stop__(self):  # TODO:
        pass
