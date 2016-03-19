# -*- coding: utf-8 -*-
"""
/***************************************************************************
 ZoomToLatLon
                                 A QGIS plugin
 Zoom to a point given in WGS84 Lat/lon
                              -------------------
        begin                : 2014-05-09
        copyright            : (C) 2014 by GV
        email                : guilhem.vellut@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
# Import the PyQt and QGIS libraries
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
# Initialize Qt resources from file resources.py
import resources_rc
# Import the code for the dialog
from zoomtolatlondialog import ZoomToLatLonDialog
import os.path
import math


class ZoomToLatLon:

    def __init__(self, iface):
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.pluginDir = os.path.dirname(__file__)
        # Create the dialog (after translation) and keep reference
        self.dlg = ZoomToLatLonDialog()

    def initGui(self):
        # Create action that will start plugin configuration
        self.action = QAction(
            QIcon(":/plugins/zoomtolatlon/icon.png"),
            u"Zoom to Lat/Lon", self.iface.mainWindow())
        # connect the action to the run method
        self.action.triggered.connect(self.run)

        # Add toolbar button and menu item
        self.iface.addToolBarIcon(self.action)
        self.iface.addPluginToMenu(u"&Zoom to Lat/Lon", self.action)

    def unload(self):
        # Remove the plugin menu item and icon
        self.iface.removePluginMenu(u"&Zoom to Lat/Lon", self.action)
        self.iface.removeToolBarIcon(self.action)

    # run method that performs all the real work
    def run(self):
        self.dlg.clear()
        self.dlg.show()
        result = self.dlg.exec_()
        # See if OK was pressed
        if result == 1:
            self.zoomToLatLon()

    def zoomToLatLon(self):
        latitude = self.dlg.latitude
        longitude = self.dlg.longitude

        qDebug("%s %s" % (latitude,longitude))
            
        # EPSG:4326 == WGS 84
        crsSrc = QgsCoordinateReferenceSystem(4326)
        canvas = self.iface.mapCanvas()
        mapRenderer = canvas.mapSettings()
        crsDest = mapRenderer.destinationCrs()
        crsTransform = QgsCoordinateTransform(crsSrc, crsDest)

        newCenter = crsTransform.transform(QgsPoint(longitude,latitude))

        canvas = self.iface.mapCanvas()
        extent = canvas.extent()
        currentCenter = extent.center()
        dx = newCenter.x() - currentCenter.x()
        dy = newCenter.y() - currentCenter.y()
        extent.set(extent.xMinimum() + dx, extent.yMinimum() + dy, extent.xMaximum() + dx, extent.yMaximum() + dy)

        canvas.setExtent(extent)
        canvas.refresh()






