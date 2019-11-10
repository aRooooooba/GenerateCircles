import wx
import random
from sympy import *

class MyFrame(wx.Frame):
    """
    The main frame.
    """

    def __init__(self, *args, **kw):
        super(MyFrame, self).__init__(*args, **kw)
        panel = wx.Panel(self, id=wx.WindowIDRef(-1))
        
        # 20 * 20 buttons
        self.buttonPool, self.onPoints = [], []
        self.isShowing = False
        for i in range(20):
            for j in range(20):
                button = wx.Button(
                        panel,
                        # reord the index of the button in its ID
                        id = wx.WindowIDRef(100 * i + j),
                        label = '',
                        pos = ((i + 1) * 20, (j + 1) * 20),
                        size = (10, 10)
                        )
                # original colour is grey
                button.SetBackgroundColour(wx.Colour(180, 180, 180))
                button.Bind(wx.EVT_LEFT_UP, self.onLeftUp)
                self.buttonPool.append(button)

        generateBtn = wx.Button(panel, label='Generate', pos=((180, 430)))
        generateBtn.Bind(wx.EVT_LEFT_UP, self.onGenerate)


    def onLeftUp(self, event):
        """
        Invoke when left is released on one button.
        If it's currently showing circles, refresh the window and reinitialize all the buttons.
        If it's not, turn on or off the clicked button.
        """

        # reinitialize the window
        if self.isShowing:
            self.Refresh()
            [pt.SetBackgroundColour(wx.Colour(180, 180, 180)) for pt in self.onPoints]
            self.onPoints = []
            self.isShowing = False

        button = wx.MouseEvent(event).GetEventObject()
        if button not in self.onPoints:
            # is currently off
            self.onPoints.append(button)
            button.SetBackgroundColour(wx.Colour(0, 0, 255))
        else:
            # is currently on
            self.onPoints.remove(button)
            button.SetBackgroundColour(wx.Colour(180, 180, 180))

    def onGenerate(self, event):
        """
        Invoke when left is release on generate button.
        Generate the circle.
        """

        # FOR THE CIRCLE
        if len(self.onPoints) == 0:
            # no points, no circles
            return
        elif len(self.onPoints) == 1:
            # one point, a small circle above it
            posId = self.onPoints[0].GetId()
            circle = [5 + (posId // 100 + 1) * 20, (posId % 100 + 1) * 20, 5]
        elif len(self.onPoints) == 2:
            # two points, the smallest circle between them
            posId1, posId2 = self.onPoints[0].GetId(), self.onPoints[1].GetId()
            x1, y1, x2, y2 = 5 + (posId1 // 100 + 1) * 20, 5 + (posId1 % 100 + 1) * 20, 5 + (posId2 // 100 + 1) * 20, 5 + (posId2 % 100 + 1) * 20
            circle = [(x1 + x2) / 2, (y1 + y2) / 2, sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2) / 2]
        else:
            # more points, get the circle with the least squares method
            a, b, c = symbols('a b c')
            s = 0
            for pt in self.onPoints:
                posId = pt.GetId()
                x, y = 5 + (posId // 100 + 1) * 20, 5 + (posId % 100 + 1) * 20
                s += (x ** 2 + y ** 2 + a * x + b * y + c) ** 2
            res = solve([diff(s, a), diff(s, b), diff(s, c)])
            # error may occur when the points are in a strange shape
            while a not in res or b not in res or c not in res:
                x, y = random.randrange(100, 400), random.randrange(100, 400)
                s += (x ** 2 + y ** 2 + a * x + b * y + c) ** 2
                res = solve([diff(s, a), diff(s, b), diff(s, c)])
            circle = [-res[a] / 2, -res[b] / 2, sqrt(res[a] ** 2 + res[b] ** 2 - 4 * res[c]) / 2]
        # draw
        dc = wx.ClientDC(self)
        dc.SetPen(wx.Pen(wx.Colour(0, 0, 255)))
        dc.SetBrush(wx.Brush(wx.Colour(0, 0, 0), style=wx.BRUSHSTYLE_TRANSPARENT))
        dc.DrawCircle(*circle)
        self.isShowing = True


app = wx.App()
frame = MyFrame(None, title='Draw Circles', size=(440,500))
frame.Show()
app.MainLoop()
