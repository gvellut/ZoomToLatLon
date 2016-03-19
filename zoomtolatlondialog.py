# -*- coding: utf-8 -*-
"""
/***************************************************************************
 ZoomToLatLonDialog
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

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from ui_zoomtolatlon import Ui_ZoomToLatLon
import re


class ZoomToLatLonDialog(QtGui.QDialog, Ui_ZoomToLatLon):
    def __init__(self):
        QtGui.QDialog.__init__(self)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)

    def clear(self):
        self.lineEditLatLonZoom.setText("")
        self.lineEditLatLonZoom.setFocus()


    def accept(self):
        result, message, details = self.validate()
        if result:
            self.done(QtGui.QDialog.Accepted)
        else:
            msgBox = QtGui.QMessageBox()
            msgBox.setWindowTitle(u"Error")
            msgBox.setText(message)
            msgBox.setInformativeText(details)
            msgBox.setStandardButtons(QMessageBox.Ok)
            msgBox.exec_()

    def validate(self):
        result = True
        message = ""
        details = ""

        latLonZoom = self.lineEditLatLonZoom.text()
        fields = re.split('\\s*,\\s*', latLonZoom)
        numFields = len(fields)
        if numFields != 2:
            result = False
            details = u"The expression must be '<lat>,<lon>'"
        else:
            if not isFloat(fields[0]) or not isFloat(fields[1]):
                result = False
                details = u"The types of the fields must be '<Float>,'<Float>'"
            else:
                self.latitude = float(fields[0])
                self.longitude = float(fields[1])

        if not result:
            message = "There were errors in the form:"

        return result, message, details



def isFloat(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def isInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

