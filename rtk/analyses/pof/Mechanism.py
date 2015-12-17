#!/usr/bin/env python
"""
####################
PoF Mechanism Module
####################
"""

# -*- coding: utf-8 -*-
#
#       rtk.analyses.pof.Mechanism.py is part of The RTK Project
#
# All rights reserved.

# Import modules for localization support.
import gettext
import locale

# Import other RTK modules.
try:
    import Configuration as _conf
    import Utilities as _util
except ImportError:                         # pragma: no cover
    import rtk.Configuration as _conf
    import rtk.Utilities as _util

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2015 Andrew "weibullguy" Rowland'

try:
    locale.setlocale(locale.LC_ALL, _conf.LOCALE)
except locale.Error:                        # pragma: no cover
    locale.setlocale(locale.LC_ALL, '')

_ = gettext.gettext


class Model(object):
    """
    The Mechanism data model contains the attributes and methods of a Physics
    of Failure failure mechanism.  A PoF will consist of one or more failure
    mechanism.  The attributes of a Mechanism are:

    :ivar dicLoads: Dictionary of the operating loads associated with the
                    failure mechanism.  Key is the Load ID; value is a
                    pointer to the instance of the operating Load data model.

    :ivar assembly_id: default value: None
    :ivar mechanism_id: default value: None
    :ivar description: default value: ''
    """

    def __init__(self):
        """
        Method to initialize a Mechanism data model instance.
        """

        # Set public dict attribute default values.
        self.dicLoads = {}

        # Set public scalar attribute default values.
        self.assembly_id = None
        self.mechanism_id = None
        self.description = ''

    def set_attributes(self, values):
        """
        Method to set the Mechanism data model attributes.

        :param tuple values: values to assign to instance attributes.
        :return: (_code, _msg); the error code and error message.
        :rtype: tuple
        """

        _code = 0
        _msg = ''

        try:
            self.assembly_id = int(values[0])
            self.mechanism_id = int(values[1])
            self.description = str(values[2])
        except IndexError as _err:
            _code = _util.error_handler(_err.args)
            _msg = "ERROR: Insufficient input values."
        except TypeError as _err:
            _code = _util.error_handler(_err.args)
            _msg = "ERROR: Converting one or more inputs to correct data type."
        except ValueError as _err:
            _code = _util.error_handler(_err.args)
            _msg = "ERROR: Wrong input data type."

        return(_code, _msg)

    def get_attributes(self):
        """
        Method to retrieve the current values of the Mechanism data model
        attributes.

        :return: (assembly_id, mechanism_id, description)
        :rtype: tuple
        """

        return(self.assembly_id, self.mechanism_id, self.description)


class Mechanism(object):
    """
    The Mechanism data controller provides an interface between the Mechanism
    data model and an RTK view model.  A single Mechanism data controller can
    control one or more Mechanism data models.  Currently the Mechanism data
    controller is unused.
    """

    def __init__(self):
        """
        Method to initialize a Mechanism data controller instance.
        """

        pass
