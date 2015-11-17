# -*- coding: utf-8 -*-
"""
/***************************************************************************
 GmlLoaderDialog
                                 A QGIS plugin

 Load GML using OGR with customized config options
                             -------------------
        begin                : 2015-04-07
        copyright            : (C) 2015 by Juergen Weichand
        email                : juergen@weichand.de
        website              : http://www.weichand.de
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

from PyQt4 import QtGui, QtCore
from gml_loader_dialog_base import Ui_GmlLoaderDialogBase
import shutil
from osgeo import gdal
import os

class GmlLoaderDialog(QtGui.QDialog):
    def __init__(self, parent):
        QtGui.QDialog.__init__(self)
        self.parent = parent
        self.ui = Ui_GmlLoaderDialogBase()
        self.ui.setupUi(self)

        self.gfs_file = ''
        QtCore.QObject.connect(self.ui.cmdSelectGfs, QtCore.SIGNAL('clicked()'), self.select_gfs)
        QtCore.QObject.connect(self.ui.cmdSelectGml, QtCore.SIGNAL('clicked()'), self.select_gml)


    def select_gfs(self):
        self.gfs_file = QtGui.QFileDialog.getOpenFileName(self, 'Open File', '', 'OGR GFS (*.gfs)')
        self.ui.lblGfs.setText(self.gfs_file)

    def select_gml(self):
        gdaltimeout = 5
        gdal.SetConfigOption('GDAL_HTTP_TIMEOUT', str(gdaltimeout))

        if self.ui.chkAttributesToFields.isChecked():
            gdal.SetConfigOption('GML_ATTRIBUTES_TO_OGR_FIELDS', 'YES')
        else:
            gdal.SetConfigOption('GML_ATTRIBUTES_TO_OGR_FIELDS', 'NO')

        if self.ui.chkResolveXlinkHref.isChecked():
            gdal.SetConfigOption('GML_SKIP_RESOLVE_ELEMS', 'NONE')
        else:
            gdal.SetConfigOption('GML_SKIP_RESOLVE_ELEMS', 'ALL')


        gml_file = QtGui.QFileDialog.getOpenFileName(self, 'Open File', '', 'GML (*.gml)')

        target_gfs = str(gml_file).replace('.gml', '.gfs')
        if len(self.gfs_file) > 0:
            if len(gml_file):
                if self.gfs_file != target_gfs:
                    if os.path.isfile(target_gfs):
                        shutil.copyfile(target_gfs, target_gfs + '.bak')
                        os.remove(target_gfs)
                    shutil.copyfile(self.gfs_file, target_gfs)
        else:
            if os.path.isfile(target_gfs):
                shutil.copyfile(target_gfs, target_gfs + '.bak')
                os.remove(target_gfs)

        if len(gml_file) > 0:
            gml_resolved = gml_file.replace('.gml', '.resolved.gml')
            if os.path.isfile(gml_resolved):
                os.remove(gml_resolved)

            head, tail = os.path.split(gml_file)
            self.parent.iface.addVectorLayer(gml_file, tail, 'ogr')
            self.close()
