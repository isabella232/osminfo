# -*- coding: utf-8 -*-
#******************************************************************************
#
# OSMInfo
# ---------------------------------------------------------
# This plugin takes coordinates of a mouse click and gets information about all 
# objects from this point from OSM using Overpass API.
#
# Author:   Maxim Dubinin, sim@gis-lab.info
# Author:   Alexander Lisovenko, alexander.lisovenko@nextgis.ru
# *****************************************************************************
# Copyright (c) 2012-2015. NextGIS, info@nextgis.com
#
# This source is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 2 of the License, or (at your option)
# any later version.
#
# This code is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details.
#
# A copy of the GNU General Public License is available on the World Wide Web
# at <http://www.gnu.org/licenses/>. You can also obtain it by writing
# to the Free Software Foundation, 51 Franklin Street, Suite 500 Boston,
# MA 02110-1335 USA.
#
#******************************************************************************

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from qgis.core import *
from qgis.gui import *

import resources
import os
import tempfile
import platform
import requests
from osminforesults import ResultsDialog
from rb_result_renderer import RubberBandResultRenderer

class OSMInfotool(QgsMapTool):
  def __init__(self, iface):
    QgsMapTool.__init__(self, iface.mapCanvas())
    self.result_renderer = RubberBandResultRenderer(iface)
    
    self.canvas = iface.mapCanvas()
    #self.emitPoint = QgsMapToolEmitPoint(self.canvas)
    self.iface = iface

    self.cursor = QCursor(QPixmap(":/icons/cursor.png"), 1, 1)
    #self.visibilityChanged.connect(self.result_renderer.clear)
  
  def __del__(self):
    self.result_renderer.clear()

  def clearCanvas(self):
    self.result_renderer.clear()
        
  def activate(self):
    self.canvas.setCursor(self.cursor)

  def canvasReleaseEvent(self, event):

    crsSrc = self.canvas.mapRenderer().destinationCrs()
    crsWGS = QgsCoordinateReferenceSystem(4326)

    QApplication.setOverrideCursor(Qt.WaitCursor)
    x = event.pos().x()
    y = event.pos().y()
    point = self.canvas.getCoordinateTransform().toMapCoordinates(x, y)

    xform = QgsCoordinateTransform(crsSrc, crsWGS)
    point = xform.transform(QgsPoint(point.x(), point.y()))
    QApplication.restoreOverrideCursor()

    xx = str(point.x())
    yy = str(point.y())

    self.result_renderer.clear()
    self.result_renderer.show_point(point, False)

    dlg = ResultsDialog('Query results', xx, yy, self.iface.mainWindow())
    dlg.finished.connect(self.clearCanvas)
    dlg.exec_()
