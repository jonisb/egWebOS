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

class WebOS(eg.PluginClass):
    def __init__(self):  # TODO:
        pass

    def Configure(self, IP=''):  # TODO: Separate args or combined?
        def initPanel(self):
            sizer_1 = wx.BoxSizer(wx.VERTICAL)

            sizer_2 = wx.BoxSizer(wx.HORIZONTAL)
            sizer_1.Add(sizer_2, 1, wx.EXPAND, 0)

            IP_label = wx.StaticText(self, wx.ID_ANY, "IP address")
            sizer_2.Add(IP_label, 0, 0, 0)

            self.IP = wx.TextCtrl(self, wx.ID_ANY, IP)
            sizer_2.Add(self.IP, 0, 0, 0)

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
