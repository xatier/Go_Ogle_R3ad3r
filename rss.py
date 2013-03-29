#!/usr/bin/python

"""
RIP Google Reader Q______Q
"""

import wx, wx.html
import os
import sys
import urllib2



class HtmlWindow(wx.html.HtmlWindow):
    """
    the html show window
    """
    def __init__(self, parent, id, size=(600,400)):
        wx.html.HtmlWindow.__init__(self,parent, id, size=size)
        if "gtk2" in wx.PlatformInfo:
            self.SetStandardFonts()

    def OnLinkClicked(self, link):
        """goto link"""
        wx.LaunchDefaultBrowser(link.GetHref())


class ShowBox(wx.Dialog):
    def __init__(self, content):
        wx.Dialog.__init__(self, None, -1, "Show feed",
            style=wx.DEFAULT_DIALOG_STYLE | wx.THICK_FRAME | wx.RESIZE_BORDER |
                wx.TAB_TRAVERSAL)
        hwin = HtmlWindow(self, -1, size=(600,1800))

        hwin.SetPage(content)
        btn = hwin.FindWindowById(wx.ID_OK)
        self.CentreOnParent(wx.BOTH)
        self.SetFocus()


class Feed():
    def __init__(self, name):
        self.entry = []
        os.chdir(name)
        f = open('list')
        for line in f:
            title = line
            link = f.next()
            self.entry.append([title, link])
        f.close()
        os.chdir('../')

class feedBotton(wx.Button):
    def __init__(self, parent, label="", url=""):
        wx.Button.__init__(self, parent, label=label)
        self.url = url


class feedPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, style=wx.RAISED_BORDER)

        Sizer = wx.BoxSizer(wx.VERTICAL)
        iner_sizer = [] * len(parent.subscription)
        self.btn_list = []

        for sub in parent.subscription:
            Sizer.Add(wx.StaticText(self, label=("["+sub+"]")))
            iner_sizer.append(wx.BoxSizer(wx.VERTICAL))
            for e in Feed(sub).entry:
                feed_sizer = wx.BoxSizer(wx.HORIZONTAL)
                self.btn_list.append(feedBotton(self, label="Read Me", url=e[1]))
                feed_sizer.Add(self.btn_list[-1])
                feed_sizer.Add(wx.StaticText(self, label=("    "+e[0])))
                iner_sizer[-1].Add(feed_sizer)

            Sizer.Add(iner_sizer[-1])

        self.SetSizerAndFit(Sizer)



class MainWindow(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title)
        self.CreateStatusBar()
        self.Maximize()


        # read feed data
        self.feedsdir = os.listdir('feeds')
        os.chdir('feeds')
        self.subscription = []
        for feedname in self.feedsdir:
            self.subscription.append(feedname)

        # Setting up the menu
        filemenu= wx.Menu()

        menuAbout = filemenu.Append(wx.ID_ABOUT, '&About', 'about this program')
        menuExit  = filemenu.Append(wx.ID_EXIT, 'E&xit', 'ByeBye')

        # Creating the menubar
        menuBar = wx.MenuBar()
        menuBar.Append(filemenu,"&File")
        self.SetMenuBar(menuBar)

        self.mypanel = feedPanel(self)

        # Buttons
        self.sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        self.buttons = []
        self.buttons.append(wx.Button(self, -1, "bottom"))
        self.sizer2.Add(self.buttons[0], 1, wx.EXPAND)


        # Set events.
        self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)
        self.Bind(wx.EVT_MENU, self.OnExit, menuExit)
        self.Bind(wx.EVT_BUTTON, self.OnUpdate, self.buttons[0])
        self.Bind(wx.EVT_CLOSE, self.OnExit)

        for btn in self.mypanel.btn_list:
            self.Bind(wx.EVT_BUTTON, self.OnShow, btn)

        # add sizer2 to sizer
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.sizer2, 0, wx.EXPAND)
        self.sizer.Add(self.mypanel)

        # Layout the sizer
        self.SetSizer(self.sizer)
        self.SetAutoLayout(1)

        self.Show(True)

        # i don't want to see the anonyed error message dialog :(
        wx.Log_SetActiveTarget(wx.LogStderr())



    def OnAbout(self, e):
        dlg = wx.MessageDialog( self, "xatier's RSS reader", "About", wx.OK)
        dlg.ShowModal()
        dlg.Destroy()

    def OnExit(self, e):
        dlg = wx.MessageDialog(self,
                    "Do you really want make a contract with me?",
                    "Confirm Exit!", wx.OK|wx.ICON_QUESTION)
        dlg.ShowModal()
        dlg.Destroy()
        self.Destroy()

    def OnUpdate(self, e):
        c = urllib2.urlopen("http://tinyurl.com/cag6auj").read()
        dlg = ShowBox(c)
        dlg.ShowModal()
        dlg.Destroy()

    def OnShow(self, e):
        btn = e.GetEventObject()
        print (btn.url)
        c = urllib2.urlopen(btn.url).read()
        print ("done.")
        print c
        dlg = ShowBox(c)
        dlg.ShowModal()
        dlg.Destroy()


app = wx.App(False)
frame = MainWindow(None, "xatier's RSS feed reader")
app.MainLoop()


