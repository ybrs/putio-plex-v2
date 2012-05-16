from PMS import *
from PMS.Objects import *
from PMS.Shortcuts import *

import putio
import putio2


PLUGIN_TITLE = "Put.io"                         # The plugin Title
PLUGIN_PREFIX = "/video/putio"          # The plugin's contextual path within Plex

ICON_DEFAULT = "icon-default.png"       #
ART_DEFAULT = "art-default.jpg"         #


api = None


def Start():    
        # Register our plugins request handler
        Plugin.AddPrefixHandler(PLUGIN_PREFIX, MainMenu, PLUGIN_TITLE, ICON_DEFAULT, ART_DEFAULT)
        
        # Add in the views our plugin will support
        Plugin.AddViewGroup("InfoList", viewMode="InfoList", mediaType="items")
        Plugin.AddViewGroup("List", viewMode="List", mediaType="items")
        Plugin.AddViewGroup("Photos", viewMode="List", mediaType="photos")
        
        # Set up our plugin's container
        MediaContainer.art = R(ART_DEFAULT)
        MediaContainer.title1 = PLUGIN_TITLE
        DirectoryItem.thumb = R(ICON_DEFAULT)


def CreatePrefs():
        Prefs.Add(id='oauth_key', type='text', default='', label='Oauth Key')    

def MainMenu():
        global api
        dir = MediaContainer(noCache=True)        
        
        if Prefs.Get('oauth_key'):
            api = putio2.Client(Prefs.Get('oauth_key').replace('-', ''))
            try:
                listItems(id=None, dir=dir)
            except Exception as e:
                pass                
            dir.Append(Function(DirectoryItem(DoLogout, title='logout')))
        else:
            #dir.Append(Function(DirectoryItem(DoLogin, title='login')))
            dir.Append(PrefsItem(title='Enter your access token'))        
            dir.Append(Function(DirectoryItem(DoLogin, title="Sign in to Put.io", summary="", thumb=R(ICON_DEFAULT))))
        return dir

        
def listItems(id, dir):
        if id != None:
                items = api.File.list(parent_id=id)
        else:
                items = api.File.list(parent_id=0)
                
        for item in items:
            if item.content_type:
                if 'audio' in item.content_type:                    
                    dir.Append(Function(TrackItem(Files, title=item.name), url=item.stream_url ))
                elif 'video' in item.content_type:
                    dir.Append(Function(VideoItem(Files, title=item.name, thumb=item.screenshot), url=item.stream_url ))
                elif "application/x-directory" in item.content_type:
                    dir.Append(Function(DirectoryItem(Folders, title=item.name), id=item.id))
                else:
                    Log(item.id)

def Folders(sender, id):
        dir = MediaContainer(title2=sender.itemTitle)
        
        item = api.File.GET(id=id)
        if "application/x-directory" in item.content_type:
                listItems(id=id, dir=dir)
        
        return dir

def Files(sender, url):
        return Redirect(url)

def DoLogin(sender):
    if Prefs.Get('oauth_key'):        
        return Redirect(PLUGIN_PREFIX)
    else:
        return MessageContainer('Access Token', 'Please enter your access token!')


def DoLogout(sender):
        Prefs.Set('oauth_key', '')
        return Redirect(PLUGIN_PREFIX)
