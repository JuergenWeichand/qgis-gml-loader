# -*- coding: utf-8 -*-
"""
/***************************************************************************
 GmlLoader
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
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load GmlLoader class from file GmlLoader.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from gml_loader import GmlLoader
    return GmlLoader(iface)
