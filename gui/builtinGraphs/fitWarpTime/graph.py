# =============================================================================
# Copyright (C) 2010 Diego Duclos
#
# This file is part of pyfa.
#
# pyfa is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# pyfa is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with pyfa.  If not, see <http://www.gnu.org/licenses/>.
# =============================================================================


from service.const import GraphCacheCleanupReason
from gui.builtinGraphs.base import FitGraph, XDef, YDef, Input
from .getter import Distance2TimeGetter, AU_METERS
from .cache import SubwarpSpeedCache


class FitWarpTimeGraph(FitGraph):

    def __init__(self):
        super().__init__()
        self._subspeedCache = SubwarpSpeedCache()

    def _clearInternalCache(self, reason, extraData):
        if reason in (GraphCacheCleanupReason.fitChanged, GraphCacheCleanupReason.fitRemoved):
            self._subspeedCache.clearForFit(extraData)
        elif reason == GraphCacheCleanupReason.graphSwitched:
            self._subspeedCache.clearAll()

    # UI stuff
    internalName = 'warpTimeGraph'
    name = 'Warp Time'
    xDefs = [
        XDef(handle='distance', unit='AU', label='Distance', mainInput=('distance', 'AU')),
        XDef(handle='distance', unit='km', label='Distance', mainInput=('distance', 'km'))]
    yDefs = [
        YDef(handle='time', unit='s', label='Warp time')]
    inputs = [
        Input(handle='distance', unit='AU', label='Distance', iconID=1391, defaultValue=20, defaultRange=(0, 50)),
        Input(handle='distance', unit='km', label='Distance', iconID=1391, defaultValue=1000, defaultRange=(150, 5000))]
    srcExtraCols = ('WarpSpeed', 'WarpDistance')

    # Calculation stuff
    _normalizers = {
        ('distance', 'AU'): lambda v, fit, tgt: v * AU_METERS,
        ('distance', 'km'): lambda v, fit, tgt: v * 1000}
    _limiters = {
        'distance': lambda fit, tgt: (0, fit.maxWarpDistance * AU_METERS)}
    _denormalizers = {
        ('distance', 'AU'): lambda v, fit, tgt: v / AU_METERS,
        ('distance', 'km'): lambda v, fit, tgt: v / 1000}
    _getters = {
        ('distance', 'time'): Distance2TimeGetter}


FitWarpTimeGraph.register()
