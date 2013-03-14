#!/usr/bin/python2

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
        hwin = HtmlWindow(self, -1, size=(400,200))

        hwin.SetPage(content)
        btn = hwin.FindWindowById(wx.ID_OK)
        irep = hwin.GetInternalRepresentation()
        hwin.SetSize((irep.GetWidth()+25, irep.GetHeight()+10))
        self.SetClientSize(hwin.GetSize())
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


class TextPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        Sizer = wx.BoxSizer(wx.VERTICAL)
        grid = wx.GridBagSizer(hgap=5, vgap=3)

        self.titles = []
        self.links = []
        cnt = 0
        for feed in parent.feeds:
            for e in feed.entry:
                self.titles.append(wx.StaticText(self, label=e[0]))
                self.links.append(wx.TextCtrl(self, style=wx.TE_MULTILINE))
                self.links[-1].SetValue(e[1])
                grid.Add(self.titles[-1], pos=(cnt, 0))
                grid.Add(self.links[-1], pos=(cnt, 1))
                cnt += 1

        Sizer.Add(grid, wx.EXPAND)
        self.SetSizerAndFit(Sizer)



class MainWindow(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=wx.Size(500,500))
        self.CreateStatusBar()
        self.Centre()


        # read feed data
        self.feedsdir = os.listdir('feeds')
        os.chdir('feeds')
        self.feeds = []
        for feedname in self.feedsdir:
            self.feeds.append(Feed(feedname))

        # Setting up the menu
        filemenu= wx.Menu()

        menuAbout = filemenu.Append(wx.ID_ABOUT, '&About', 'about this program')
        menuExit  = filemenu.Append(wx.ID_EXIT, 'E&xit', 'ByeBye')

        # Creating the menubar
        menuBar = wx.MenuBar()
        menuBar.Append(filemenu,"&File")
        self.SetMenuBar(menuBar)

        self.mypanel = TextPanel(self)

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

        # add sizer2 to sizer
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.sizer2, 0, wx.EXPAND)
        self.sizer.Add(self.mypanel, 1, wx.EXPAND)

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




app = wx.App(False)
frame = MainWindow(None, "RSS")
app.MainLoop()


