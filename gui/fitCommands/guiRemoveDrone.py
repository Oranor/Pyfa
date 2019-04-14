import wx
from service.fit import Fit

import gui.mainFrame
from gui import globalEvents as GE
from .calc.drone.localRemove import FitRemoveDroneCommand


class GuiRemoveDroneCommand(wx.Command):
    def __init__(self, fitID, position, amount=1):
        wx.Command.__init__(self, True, "Drone Remove")
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()
        self.sFit = Fit.getInstance()
        self.internal_history = wx.CommandProcessor()
        self.fitID = fitID
        self.position = position
        self.amount = amount

    def Do(self):
        cmd = FitRemoveDroneCommand(self.fitID, self.position, self.amount)
        if self.internal_history.Submit(cmd):
            self.sFit.recalc(self.fitID)
            wx.PostEvent(self.mainFrame, GE.FitChanged(fitID=self.fitID))
            return True
        return False

    def Undo(self):
        for _ in self.internal_history.Commands:
            self.internal_history.Undo()
        self.sFit.recalc(self.fitID)
        wx.PostEvent(self.mainFrame, GE.FitChanged(fitID=self.fitID))
        return True
