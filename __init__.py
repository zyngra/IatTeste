# -*- coding: utf-8 -*-



# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load IatTeste class from file IatTeste.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .iat_teste import IatTeste

    return IatTeste(iface)
