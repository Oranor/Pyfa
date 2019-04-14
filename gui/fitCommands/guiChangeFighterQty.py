import wx
import gui.mainFrame
from gui import globalEvents as GE
from .calc.fighter.localChangeAmount import FitChangeFighterAmountCommand
from service.fit import Fit
from logbook import Logger
pyfalog = Logger(__name__)


class GuiChangeFighterQty(wx.Command):
    def __init__(self, fitID, position, amount=1):
        wx.Command.__init__(self, True, "")
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()
        self.sFit = Fit.getInstance()
        self.fitID = fitID
        self.position = position
        self.amount = amount
        self.internal_history = wx.CommandProcessor()

    def Do(self):
        cmd = FitChangeFighterAmountCommand(self.fitID, self.position, self.amount)
        if self.internal_history.Submit(cmd):
            self.sFit.recalc(self.fitID)
            wx.PostEvent(self.mainFrame, GE.FitChanged(fitID=self.fitID))
            return True
        return False

    def Undo(self):
        pyfalog.debug("{} Undo()".format(self))
        for _ in self.internal_history.Commands:
            self.internal_history.Undo()
        self.sFit.recalc(self.fitID)
        wx.PostEvent(self.mainFrame, GE.FitChanged(fitID=self.fitID))
        return True
