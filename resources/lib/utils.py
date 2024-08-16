#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, sys, xbmc, xbmcaddon, xbmcgui
import base64, gzip, xbmcvfs
import re, hashlib, json
import codecs, urllib, xbmcplugin, time

try:
	import StringIO
	loglevel = xbmc.LOGNOTICE
	py2 = True
except:
	import io
	loglevel = xbmc.LOGINFO
	py2 = False


#ISO639-2
langdict = {
	'Abkhazian': ['abk'],
	'Afrikaans': ['afr'],
	'Albanian': ['alb', 'sqi'],
	'Amharic': ['amh'],
	'Arabic': ['ara', 'arb'],
	'Aragonese': ['arg'],
	'Armenian': ['arm', 'hye'],
	'Assamese': ['asm'],
	'Asturian': ['ast'],
	'Azerbaijani': ['aze'],
	'Basque': ['baq', 'eus'],
	'Belarusian': ['bel'],
	'Bengali': ['ben'],
	'Bosnian': ['bos'],
	'Breton': ['bre'],
	'Bulgarian': ['bul'],
	'Burmese': ['bur', 'mya'],
	'Catalan': ['cat'],
	'Chinese': ['chi', 'zho', 'zhc', 'zht', 'zhe'],
	'Croatian': ['hrv'],
	'Czech': ['cze', 'ces'],
	'Danish': ['dan'],
	'Dari': ['prs'],
	'Dutch': ['dut', 'nld'],
	'English': ['eng'],
	'Esperanto': ['epo'],
	'Estonian': ['est'],
	'Extremaduran': ['ext'],
	'Finnish': ['fin'],
	'French': ['fre', 'fra'],
	'Gaelic': ['gla'],
	'Galician': ['glg'],
	'Georgian': ['geo', 'kat'],
	'German': ['ger'],
	'Greek': ['ell', 'gre', 'grc'],
	'Hebrew': ['heb'],
	'Hindi': ['hin'],
	'Hungarian': ['hun'],
	'Icelandic': ['ice', 'isl'],
	'Igbo': ['ibo'],
	'Indonesian': ['ind'],
	'Interlingua': ['ina'],
	'Irish': ['gle'],
	'Italian': ['ita'],
	'Japanese': ['jpn'],
	'Kannada': ['kan'],
	'Kazakh': ['kaz'],
	'Khmer': ['khm'],
	'Korean': ['kor'],
	'Kurdish': ['kur'],
	'Kyrgyz': ['kir'],
	'Latvian': ['lav'],
	'Lithuanian': ['lit'],
	'Luxembourgish': ['ltz'],
	'Macedonian': ['mac', 'mkd'],
	'Malay': ['may', 'msa'],
	'Malayalam': ['mal'],
	'Manipuri': ['mni'],
	'Marathi': ['mar'],
	'Mongolian': ['mon'],
	'Navajo': ['nav'],
	'Nepali': ['nep'],
	'Northern Sami': ['sme'],
	'Norwegian': ['nor'],
	'Occitan': ['oci'],
	'Odia': ['ori'],
	'Persian': ['per', 'fas'],
	'Polish': ['pol'],
	'Portuguese': ['por', 'pob', 'pom'],
	'Pushto': ['pus'],
	'Romanian': ['rum', 'ron', 'mol'],
	'Russian': ['rus'],
	'Santali': ['sat'],
	'Serbian': ['scc', 'srp', 'mne'],
	'Sindhi': ['snd'],
	'Sinhalese': ['sin'],
	'Slovak': ['slo', 'slk'],
	'Slovenian': ['slv'],
	'Somali': ['som'],
	'South Azerbaijani': ['azb'],
	'Spanish': ['spa', 'spn', 'spl'],
	'Swahili': ['swa'],
	'Swedish': ['swe'],
	'Syriac': ['syr'],
	'Tagalog': ['tgl'],
	'Tamil': ['tam'],
	'Tatar': ['tat'],
	'Telugu': ['tel'],
	'Tetum': ['tet'],
	'Thai': ['tha'],
	'Toki Pona': ['tok'],
	'Turkish': ['tur'],
	'Turkmen': ['tuk'],
	'Ukrainian': ['ukr'],
	'Urdu': ['urd'],
	'Uzbek': ['uzb'],
	'Vietnamese': ['vie'],
	'Welsh': ['wel', 'cym']
}


def addon():
	addon = xbmcaddon.Addon().getAddonInfo('id')
	return xbmcaddon.Addon(addon)


def name():
	return xbmcaddon.Addon().getAddonInfo('name')


def version():
	return xbmcaddon.Addon().getAddonInfo('version')


def localize(id):
	if py2:
		return addon().getLocalizedString(id).encode('utf-8')
	else:
		return addon().getLocalizedString(id)


def setting(setting):
	return addon().getSetting(setting)


def boolsetting(setting):
	return addon().getSetting(setting).lower() == "true"


def setsetting(setting, value):
	return addon().setSetting(setting, value)


def setboolsetting(setting, value):
	return addon().setSettingBool(setting, value)


def debug(msg, force = False):

	if force or boolsetting('debug'):
		try:
			xbmc.log("#####[SubLoader]##### " + msg, loglevel)
		except UnicodeEncodeError:
			xbmc.log("#####[SubLoader]##### " + msg, loglevel).encode( "utf-8", "ignore" )

debug('Loading %s version %s' % (name(), version()))


def videopath():
	return xbmc.Player().getPlayingFile()


def videosource():
	filepath = xbmc.getInfoLabel('Player.Filenameandpath')
	fileext = os.path.splitext(filepath)
	if fileext[1] == '.strm':
		file = xbmcvfs.File(filepath, 'r')
		source = file.read()
		file.close()
		return source # A .strm file contains actual source inside
	return xbmc.getInfoLabel('Player.Folderpath')


def fullvideosource():
	return xbmc.getInfoLabel('Player.Filenameandpath')


def debugsetting():

	if boolsetting('debug') != boolsetting('debugcheck'):
		return True
	return False
