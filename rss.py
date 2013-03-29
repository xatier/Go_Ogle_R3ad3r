#!/usr/bin/python

"""
RIP Google Reader Q______Q
"""

import wx, wx.html, wx.lib.scrolledpanel
import os
import sys
import urllib2

class HtmlWindow(wx.html.HtmlWindow):
    """
    html rendering window
    """
    def __init__(self, parent, id, size=(600,800)):
        wx.html.HtmlWindow.__init__(self,parent, id, size=size)
        if "gtk2" in wx.PlatformInfo:
            self.SetStandardFonts()

    def OnLinkClicked(self, link):
        """goto link"""
        wx.LaunchDefaultBrowser(link.GetHref())

class DisplayPanel(wx.Panel):
    """
    the panel where Feed body display
    """
    def __init__(self, parent, content):
        wx.Panel.__init__(self, parent, style=wx.RAISED_BORDER)
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.hwin = HtmlWindow(self, -1)
        if not content:
            content = "<h1>None</h1>"
        self.hwin.SetPage(content)
        sizer.Add(self.hwin, wx.EXPAND)
        self.SetSizerAndFit(sizer)

    def updateContent(self, content):
        self.hwin.SetPage(content)


class Subscription():
    def __init__(self, name):
        self.entry = []
        os.chdir(name)
        f = open('list')
        for line in f:
            title = line
            link = f.next().rstrip('\n')
            self.entry.append([title, link])
        f.close()
        os.chdir('../')



class FeedBotton(wx.Button):
    def __init__(self, parent, label="", url=""):
        wx.Button.__init__(self, parent, label=label)
        self.url = url


class SubscriptionPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, style=wx.RAISED_BORDER)

        sizer = wx.BoxSizer(wx.VERTICAL)
        iner_sizer = [] * len(parent.subscriptions)
        self.btn_list = []

        for sub in parent.subscriptions:
            sizer.Add(wx.StaticText(self, label=("["+sub+"]")))
            iner_sizer.append(wx.BoxSizer(wx.VERTICAL))
            for e in Subscription(sub).entry:
                feed_sizer = wx.BoxSizer(wx.HORIZONTAL)
                self.btn_list.append(FeedBotton(self, label="Read Me", url=e[1]))
                feed_sizer.Add(self.btn_list[-1])
                feed_sizer.Add(wx.StaticText(self, label=("    "+e[0])))
                iner_sizer[-1].Add(feed_sizer)

            sizer.Add(iner_sizer[-1])

        # set panel color for debugging
        #self.SetBackgroundColour(wx.Colour(128,128,128))
        self.SetSizerAndFit(sizer)
        self.SetAutoLayout(1) 



class MainWindow(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title)
        self.CreateStatusBar()
        self.Maximize()

        #os.system("./fetch.pl")

        # read feed data
        self.feedsdir = os.listdir('feeds')
        os.chdir('feeds')
        self.subscriptions = []
        for feedname in self.feedsdir:
            self.subscriptions.append(feedname)

        # Setting up the menu
        filemenu= wx.Menu()

        menuAbout = filemenu.Append(wx.ID_ABOUT, '&About', 'about this program')
        menuExit  = filemenu.Append(wx.ID_EXIT, 'E&xit', 'ByeBye')

        # Creating the menubar
        menuBar = wx.MenuBar()
        menuBar.Append(filemenu,"&File")
        self.SetMenuBar(menuBar)

        """
        XXX: try to add scrolling bar to the left panel Q_Q
        """
        # self.sp = wx.lib.scrolledpanel.ScrolledPanel(self, style=wx.ALWAYS_SHOW_SB)
        # self.sp.SetupScrolling()
        # tsizer = wx.BoxSizer(wx.VERTICAL)
        # self.text_panel = SubscriptionPanel(self)
        # tsizer.Add(self.text_panel)
        # self.sp.SetSizer(tsizer)
        # self.sp.SetAutoLayout(1)

        self.text_panel = SubscriptionPanel(self)

        self.display_panel = DisplayPanel(self, None)

        # Set events.
        self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)
        self.Bind(wx.EVT_MENU, self.OnExit, menuExit)
        self.Bind(wx.EVT_CLOSE, self.OnExit)

        for btn in self.text_panel.btn_list:
            self.Bind(wx.EVT_BUTTON, self.OnShow, btn)

        # add two panels in to sizer
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer.Add(self.text_panel)
        self.sizer.Add(self.display_panel)

        # Layout the sizer
        self.SetSizerAndFit(self.sizer)
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

    def OnShow(self, e):
        btn = e.GetEventObject()
        print ("downloading... " + btn.url)
        c = urllib2.urlopen(btn.url).read()
        print ("rendering...")
        self.display_panel.updateContent(c)
        print ("done.")


app = wx.App(False)
frame = MainWindow(None, "xatier's RSS feed reader")
app.MainLoop()


