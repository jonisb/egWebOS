# -*- coding: utf-8 -*-
"""
WebOS support plugin for EventGhost
"""
from __future__ import print_function, unicode_literals

eg.RegisterPlugin(
    name="egWebOS",
    author="Joni Borén",
    version="0.0.0",
    kind="external",
    guid="{523fa3a6-f1a9-405d-a28a-8d211f76562b}",
    canMultiLoad=True,
    createMacrosOnAdd=False,
    url="http://www.eventghost.net/forum/viewforum.php?f=9&sid=291a5f7c46f3795101a0d34c17ad545c",  # TODO: Create support thread and link.
    description="""Adds actions to control WebOS devices like LG TVs.""",  # TODO: Add description, use <rst>?
)

class WebOS(eg.PluginClass):
    def __init__(self):  # TODO:
        pass

    def __start__(self):  # TODO:
        pass

    def __stop__(self):  # TODO:
        pass
