# -*- coding: utf-8 -*-
# Module: default
# Author: M. M
# Created on: 13.07.2017
# License: GPL v.3 https://www.gnu.org/copyleft/gpl.html

import sys
from urlparse import parse_qsl
import urllib,urllib2
import xbmcgui
import xbmcplugin

_url = sys.argv[0]
_handle = int(sys.argv[1])
VIDEOS = {"EuroNews":[{'name': 'Euronews Live',
                       'thumb': 'https://upload.wikimedia.org/wikipedia/commons/3/39/Euronews._2016_alternative_logo.png',
                       'video': 'euronews',
                       'genre': 'TV'},
					   {'name': 'Euronews Live (Backup Stream)',
                       'thumb': 'https://upload.wikimedia.org/wikipedia/commons/3/39/Euronews._2016_alternative_logo.png',
                       'video': 'euronews_bak',
                       'genre': 'TV'},
					  ]
			}
		  
def get_categories():
    return VIDEOS.keys()
	
def get_json_paramval(url,param):
	req = urllib2.Request(url)
	response = urllib2.urlopen(req)
	the_page = response.read()
	
	paramext='"'+param+'":"'
	paramlen=len(paramext)
	marker=the_page.index(paramext)+paramlen
	the_page=the_page[marker:]
	marker=the_page.index('"')
	returnurl=the_page[:marker].replace('\\','')
	return returnurl

def get_euronews_bakurl():
	return get_json_paramval(get_json_paramval('http://www.euronews.com/api/watchlive.json','url'),'backup')

def get_euronews_url():
	return get_json_paramval(get_json_paramval('http://www.euronews.com/api/watchlive.json','url'),'primary')
	
def get_videos(category):
    return VIDEOS[category]


def list_categories():
    categories = get_categories()
    listing = []
    for category in categories:
        list_item = xbmcgui.ListItem(label=category)
        list_item.setArt({'thumb': 'https://upload.wikimedia.org/wikipedia/commons/3/39/Euronews._2016_alternative_logo.png',
                          'icon': 'https://upload.wikimedia.org/wikipedia/commons/3/39/Euronews._2016_alternative_logo.png',})
        list_item.setInfo('video', {'title': category, 'genre': category})
        url = '{0}?action=listing&category={1}'.format(_url, category)
        is_folder = True
        listing.append((url, list_item, is_folder))
    xbmcplugin.addDirectoryItems(_handle, listing, len(listing))
    xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    xbmcplugin.endOfDirectory(_handle)


def list_videos(category):
    videos = get_videos(category)
    listing = []
    for video in videos:
        list_item = xbmcgui.ListItem(label=video['name'])
        list_item.setInfo('video', {'title': video['name'], 'genre': video['genre']})
        list_item.setArt({'thumb': video['thumb'], 'icon': video['thumb']})
        list_item.setProperty('IsPlayable', 'true')
        url = '{0}?action=play&video="{1}"'.format(_url, video['video'])
        is_folder = False
        listing.append((url, list_item, is_folder))
    xbmcplugin.addDirectoryItems(_handle, listing, len(listing))
    xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    xbmcplugin.endOfDirectory(_handle)


def play_video(path):
    play_item = xbmcgui.ListItem(path=path)
    xbmcplugin.setResolvedUrl(_handle, True, listitem=play_item)

def router(paramstring):
    params = dict(parse_qsl(paramstring))
    if params:
        if params['action'] == 'listing':
            list_videos(params['category'])
        elif params['action'] == 'play':
			myparams = params['video'].replace('??','&')
			if myparams == '"euronews"':
				play_video(get_euronews_url())
			elif myparams == '"euronews_bak"':
				play_video(get_euronews_bakurl())
			else:
				play_video(myparams[1:-1])		
    else:
        list_categories()


if __name__ == '__main__':
    router(sys.argv[2][1:])
