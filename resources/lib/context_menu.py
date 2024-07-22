# -*- coding: utf-8 -*-

import xbmc
import xbmcaddon
import xbmcgui

addon = xbmcaddon.Addon()
enable_context_menu = addon.getSettingBool('enable_context_menu')
xbmcgui.Window(10000).setProperty('enable_context_menu', str(enable_context_menu).lower())

if __name__ == '__main__':
	if enable_context_menu:
		xbmc.executebuiltin('ActivateWindow(subtitlesearch)')
	else:
		pass
