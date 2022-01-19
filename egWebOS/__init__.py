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

from functools import partial
from pywebostv.discovery import discover
from pywebostv.controls import MediaControl, TvControl, SystemControl, ApplicationControl, InputControl, SourceControl


def control_events(status_of_call, payload, control=None, self=None):
    if status_of_call:
        # Successful response from TV.
        # payload is a dict or an object (see API details)
        if isinstance(payload, type('')):
            self.TriggerEvent(control + '.' + payload)
        else:
            try:
                for key in payload:
                    if key is not 'callerId':
                        try:
                            self.TriggerEvent(control + '.' + key, payload[key])
                        except TypeError:
                            eg.PrintError("WebOS: Unknown event:", control, payload)
            except AttributeError:
                eg.PrintError("WebOS: Unknown event:", control, payload)
    else:
        # payload is the error string.
        eg.PrintError("Error message: ", control, payload)


class WebOS(eg.PluginClass):
    def __init__(self):  # TODO:
        pass

    def Configure(self, IP='', Code='', Subscriptions=[]):  # TODO: Separate args or combined?
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

            label_2 = wx.StaticText(self, wx.ID_ANY, "Choose what events to subscribe to from device")
            sizer_1.Add(label_2, 0, 0, 0)

            choices = []
            for control in ('MediaControl', 'TvControl', 'SystemControl', 'ApplicationControl', 'InputControl', 'SourceControl'):
                for key, value in globals()[control].COMMANDS.items():
                    if 'subscription' in value and value['subscription'] == True:
                        choices.append(control + '.' + key)

            self.Subscriptions = wx.ListBox(self, wx.ID_ANY, choices=choices, style=wx.LB_MULTIPLE)
            for i, s in enumerate(self.Subscriptions.GetStrings()):
                if s in Subscriptions:
                    self.Subscriptions.SetSelection(i)
            sizer_1.Add(self.Subscriptions, 0, 0, 0)

            self.SetSizer(sizer_1)
            sizer_1.Fit(self)

            self.Layout()

        panel = eg.ConfigPanel()
        initPanel(panel)

        while panel.Affirmed():
            selections = []
            for sel in panel.Subscriptions.GetSelections():
                selections.append(panel.Subscriptions.GetString(sel))
            panel.SetResult(panel.IP.GetValue(), panel.Code.GetValue(), selections)

    def __start__(self, IP, Code, Subscriptions):  # TODO: Match Configure
        if not Code:
            eg.PrintError("WebOS: Please get an access code in the config.")
            raise Exception('No access configured')

        self.client = WebOSClient(IP)
        self.client.connect()
        for status in self.client.register({'client_key': Code}):
            if status is not WebOSClient.REGISTERED:
                eg.PrintError("WebOS: Device registration problem", status)
                raise Exception('No access configured')

        self.controls = {}
        self.subscribed = []
        for control in Subscriptions:
            control, _, key = control.partition('.')
            self.controls[control] = globals()[control](self.client)
            self.controls[control].subscribe(key, self.controls[control].COMMANDS[key])(partial(control_events, control=control, self=self))
            self.subscribed.append(self.controls[control].unsubscribe(key, self.controls[control].COMMANDS[key]))

    def __stop__(self):  # TODO:
        for control in self.subscribed:
            control()
        self.client.close()
        del self.client
