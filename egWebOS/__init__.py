# -*- coding: utf-8 -*-
"""
WebOS support plugin for EventGhost
"""
from __future__ import print_function, unicode_literals

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

    def Configure(self, IP=''):  # TODO: Separate args or combined?
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

            sizer_1 = wx.BoxSizer(wx.VERTICAL)

            sizer_2 = wx.BoxSizer(wx.HORIZONTAL)
            sizer_1.Add(sizer_2, 1, wx.EXPAND, 0)

            IP_label = wx.StaticText(self, wx.ID_ANY, "IP address")
            sizer_2.Add(IP_label, 0, 0, 0)

            self.IP = wx.TextCtrl(self, wx.ID_ANY, IP)
            sizer_2.Add(self.IP, 0, 0, 0)

            self.Search = wx.Button(self, wx.ID_ANY, "Search")
            self.Search.Bind(wx.EVT_BUTTON, Search)
            sizer_2.Add(self.Search, 0, 0, 0)

            self.SetSizer(sizer_1)
            sizer_1.Fit(self)

            self.Layout()

        panel = eg.ConfigPanel()
        initPanel(panel)

        while panel.Affirmed():
            panel.SetResult(panel.IP.GetValue())

    def __start__(self, IP):  # TODO: Match Configure
        pass

    def __stop__(self):  # TODO:
        pass
