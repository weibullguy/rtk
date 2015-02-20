#!/usr/bin/env python
"""
#############################################################
Hardware.Component.Capacitor.Variable Package Variable Module
#############################################################
"""

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2015 Andrew "weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       rtk.hardware.component.capacitor.variable.Variable.py is part of the RTK Project
#
# All rights reserved.

import gettext
import locale

try:
    import configuration as _conf
    from hardware.component.capacitor.Capacitor import Model as Capacitor
except ImportError:                         # pragma: no cover
    import rtk.configuration as _conf
    from rtk.hardware.component.capacitor.Capacitor import Model as Capacitor

# Add localization support.
try:
    locale.setlocale(locale.LC_ALL, _conf.LOCALE)
except locale.Error:                        # pragma: no cover
    locale.setlocale(locale.LC_ALL, '')

_ = gettext.gettext


def _error_handler(message):
    """
    Converts string errors to integer error codes.

    :param str message: the message to convert to an error code.
    :return: _err_code
    :rtype: int
    """

    if 'argument must be a string or a number' in message[0]:   # Type error
        _error_code = 10
    elif 'index out of range' in message[0]:   # Index error
        _error_code = 40
    else:                                   # Unhandled error
        _error_code = 1000                  # pragma: no cover

    return _error_code


class AirTrimmer(Capacitor):
    """
    The Variable Air Trimmer capacitor data model contains the attributes and
    methods of a variable air trimmer capacitor.  The attributes of a variable
    air trimmer capacitor are:

    :cvar _lst_piE: list of environment factor values.
    :cvar _lst_piQ: list of quality factor values.
    :cvar _lst_lambdab_count: list of base hazard rate values for parts count.
    :cvar subcategory: the subcategory ID in the RTK common database.

    :ivar specification: default value: 0
    :ivar spec_sheet: default value: 0

    Covers specification MIL-C-92.

    Hazard Rate Models:
        # MIL-HDBK-217F, section 10.18
    """

    # MIL-HDK-217F hazard rate calculation variables.
    # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
    _piE = [1.0, 3.0, 13.0, 8.0, 24.0, 6.0, 10.0, 37.0, 70.0, 36.0, 0.5, 20.0,
            52.0, 950.0]
    _piQ = [5.0, 20.0]
    _lambdab_count = [0.80, 0.33, 1.6, 0.87, 3.0, 1.0, 1.7, 9.9, 19.0, 8.1,
                      0.032, 2.5, 8.9, 100.0]
    lst_ref_temp = [358.0]
    # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

    subcategory = 57

    def __init__(self):
        """
        Initialize a Variable Air Trimmer capacitor data model instance.
        """

        super(AirTrimmer, self).__init__()

        # Initialize public scalar attributes.
        self.specification = 0
        self.spec_sheet = 0
        if self.hazard_rate_type < 3:       # MIL-HDBK-217
            self.reference_temperature = 358.0

    def calculate(self):
        """
        Calculates the hazard rate for the Variable Air Trimmer capacitor data
        model.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        from math import exp

        self.hazard_rate_model = {}

        if self.hazard_rate_type == 1:
            self.hazard_rate_model['equation'] = 'lambdab * piQ'
        elif self.hazard_rate_type == 2:
            self.hazard_rate_model['equation'] = 'lambdab * piQ * piE'

            # Base hazard rate.
            _stress = (self.operating_voltage + self.acvapplied) / \
                       self.rated_voltage
            try:
                self.hazard_rate_model['lambdab'] = \
                    0.00000192 * ((_stress / 0.33)**3 + 1) * \
                    exp(10.8 * ((self.temperature_active + 273) /
                                self.reference_temperature))
            except(OverflowError, ZeroDivisionError):
                # TODO: Handle overflow error.
                return True

        return Capacitor.calculate(self)


class Ceramic(Capacitor):
    """
    The Variable Ceramic capacitor data model contains the attributes and
    methods of a variable ceramic capacitor.  The attributes of a variable
    ceramic capacitor are:

    :cvar _lst_piE: list of environment factor values.
    :cvar _lst_piQ: list of quality factor values.
    :cvar _lst_lambdab_count: list of base hazard rate values for parts count.
    :cvar subcategory: the subcategory ID in the RTK common database.

    :ivar specification: default value: 0
    :ivar spec_sheet: default value: 0

    Covers specification MIL-C-81.

    Hazard Rate Models:
        # MIL-HDBK-217F, section 10.16
    """

    # MIL-HDK-217F hazard rate calculation variables.
    # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
    _piE = [1.0, 3.0, 13.0, 8.0, 24.0, 6.0, 10.0, 37.0, 70.0, 36.0, 0.4, 20.0,
            52.0, 950.0]
    _piQ = [4.0, 20.0]
    _lambdab_count = [0.08, 0.27, 1.2, 0.71, 2.3, 0.69, 1.1, 6.2, 12.0, 4.1,
                      0.032, 1.9, 5.9, 85.0]
    lst_ref_temp = [358.0, 398.0]
    # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

    subcategory = 55

    def __init__(self):
        """
        Initialize a Variable Ceramic capacitor data model instance.
        """

        super(Ceramic, self).__init__()

        # Initialize public scalar attributes.
        self.specification = 0
        self.spec_sheet = 0
        if self.hazard_rate_type < 3:       # MIL-HDBK-217
            self.reference_temperature = 358.0

    def calculate(self):
        """
        Calculates the hazard rate for the Ceramic Chip capacitor data
        model.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        from math import exp

        self.hazard_rate_model = {}

        if self.hazard_rate_type == 1:
            self.hazard_rate_model['equation'] = 'lambdab * piQ'
        elif self.hazard_rate_type == 2:
            self.hazard_rate_model['equation'] = 'lambdab * piQ * piE'

            # Base hazard rate.
            _stress = (self.operating_voltage + self.acvapplied) / \
                       self.rated_voltage
            try:
                self.hazard_rate_model['lambdab'] = \
                    0.00224 * ((_stress / 0.17)**3 + 1) * \
                    exp(1.59 * ((self.temperature_active + 273) /
                               self.reference_temperature)**10.1)
            except(OverflowError, ZeroDivisionError):
                # TODO: Handle overflow error.
                return True

        return Capacitor.calculate(self)


class Piston(Capacitor):
    """
    The Variable Piston capacitor data model contains the attributes and
    methods of a variable piston capacitor.  The attributes of a variable
    piston capacitor are:

    :cvar _lst_piE: list of environment factor values.
    :cvar _lst_piQ: list of quality factor values.
    :cvar _lst_lambdab_count: list of base hazard rate values for parts count.
    :cvar subcategory: the subcategory ID in the RTK common database.

    :ivar specification: default value: 0
    :ivar spec_sheet: default value: 0

    Covers specification MIL-C-14409.

    Hazard Rate Models:
        # MIL-HDBK-217F, section 10.17
    """

    # MIL-HDK-217F hazard rate calculation variables.
    # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
    _piE = [1.0, 3.0, 12.0, 7.0, 18.0, 3.0, 4.0, 20.0, 30.0, 32.0, 0.5, 18.0,
            46.0, 830.0]
    _piQ = [3.0, 10.0]
    _lambdab_count = [0.033, 0.13, 0.62, 0.31, 0.93, 0.21, 0.28, 2.2, 3.3, 2.2,
                      0.16, 0.93, 3.2, 37.0]
    lst_ref_temp = [398.0, 423.0]
    # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

    subcategory = 56

    def __init__(self):
        """
        Initialize a Variable Piston capacitor data model instance.
        """

        super(Piston, self).__init__()

        # Initialize public scalar attributes.
        self.specification = 0
        self.spec_sheet = 0
        if self.hazard_rate_type < 3:       # MIL-HDBK-217
            self.reference_temperature = 398.0

    def calculate(self):
        """
        Calculates the hazard rate for the Ceramic Chip capacitor data
        model.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        from math import exp

        self.hazard_rate_model = {}

        if self.hazard_rate_type == 1:
            self.hazard_rate_model['equation'] = 'lambdab * piQ'
        elif self.hazard_rate_type == 2:
            self.hazard_rate_model['equation'] = 'lambdab * piQ * piE'

            # Base hazard rate.
            _stress = (self.operating_voltage + self.acvapplied) / \
                       self.rated_voltage
            try:
                self.hazard_rate_model['lambdab'] = \
                    0.00000073 * ((_stress / 0.33)**3 + 1) * \
                    exp(12.1 * ((self.temperature_active + 273) /
                               self.reference_temperature))
            except(OverflowError, ZeroDivisionError):
                # TODO: Handle overflow error.
                return True

        return Capacitor.calculate(self)


class Vacuum(Capacitor):
    """
    The Variable Vacuum capacitor data model contains the attributes and
    methods of a variable vacuum capacitor.  The attributes of a variable
    vacuum capacitor are:

    :cvar _lst_piE: list of environment factor values.
    :cvar _lst_piQ: list of quality factor values.
    :cvar _lst_lambdab_count: list of base hazard rate values for parts count.
    :cvar subcategory: the subcategory ID in the RTK common database.

    :ivar specification: default value: 0
    :ivar spec_sheet: default value: 0

    Covers specification MIL-C-23183.

    Hazard Rate Models:
        # MIL-HDBK-217F, section 10.19
    """

    # MIL-HDK-217F hazard rate calculation variables.
    # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
    _piCF = [0.10, 1.0]
    _piE = [1.0, 3.0, 14.0, 8.0, 27.0, 10.0, 18.0, 70.0, 108.0, 40.0, 0.5, 0.0,
            0.0, 0.0]
    _piQ = [3.0, 20.0]
    _lambdab_count = [0.4, 1.3, 6.8, 3.6, 13.0, 5.7, 10.0, 58.0, 90.0, 23.0,
                      20.0, 0.0, 0.0, 0.0]
    lst_ref_temp = [358.0, 373.0, 398.0]
    # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

    subcategory = 58

    def __init__(self):
        """
        Initialize a Variable Vacuum capacitor data model instance.
        """

        super(Vacuum, self).__init__()

        # Initialize public scalar attributes.
        self.configuration = 1              # Fixed
        self.specification = 0
        self.spec_sheet = 0
        self.piCF = 0.0
        if self.hazard_rate_type < 3:       # MIL-HDBK-217
            self.reference_temperature = 358.0

    def set_attributes(self, values):
        """
        Sets the Variable Vacuum capacitor data model attributes.

        :param tuple values: tuple of values to assign to the instance
                             attributes.
        :return: (_code, _msg); the error code and error message.
        :rtype: tuple
        """

        _code = 0
        _msg = ''

        (_code, _msg) = Capacitor.set_attributes(self, values)

        try:
            self.configuration = int(values[119])
            self.piCF = float(values[104])
        except IndexError as _err:
            _code = _error_handler(_err.args)
            _msg = "ERROR: Insufficient input values."
        except TypeError as _err:
            _code = _error_handler(_err.args)
            _msg = "ERROR: Converting one or more inputs to correct data type."

        return(_code, _msg)

    def get_attributes(self):
        """
        Retrieves the current values of the Variable Vacuum capacitor data
        model attributes.

        :return: (configuration, piCF)
        :rtype: tuple
        """

        _values = Capacitor.get_attributes(self)

        _values = _values + (self.configuration, self.piCF)

        return _values

    def calculate(self):
        """
        Calculates the hazard rate for the Ceramic Chip capacitor data
        model.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        from math import exp

        self.hazard_rate_model = {}

        if self.hazard_rate_type == 1:
            self.hazard_rate_model['equation'] = 'lambdab * piQ'
        elif self.hazard_rate_type == 2:
            self.hazard_rate_model['equation'] = 'lambdab * piQ * piE * piCF'
            self.piCF = self._piCF[self.configuration - 1]
            self.hazard_rate_model['piCF'] = self.piCF

            # Base hazard rate.
            _stress = (self.operating_voltage + self.acvapplied) / \
                       self.rated_voltage
            try:
                self.hazard_rate_model['lambdab'] = \
                    0.0112 * ((_stress / 0.17)**3 + 1) * \
                    exp(1.59 * ((self.temperature_active + 273) /
                                self.reference_temperature)**10.1)
            except(OverflowError, ZeroDivisionError):
                # TODO: Handle overflow error.
                return True

        return Capacitor.calculate(self)
