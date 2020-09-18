# -*- coding: utf-8 -*-
#
#       views.gtk3.hardware.components.meter.py is part of the RAMSTK
#       Project
#
# All rights reserved.
# Copyright 2007 - 2020 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Meter Work View."""

# Standard Library Imports
from typing import Any, Dict, List

# Third Party Imports
from pubsub import pub

# RAMSTK Package Imports
# noinspection PyPackageRequirements
from ramstk.configuration import RAMSTKUserConfiguration
from ramstk.logger import RAMSTKLogManager
from ramstk.views.gtk3 import _
from ramstk.views.gtk3.widgets import RAMSTKComboBox, RAMSTKEntry

# RAMSTK Local Imports
from .workview import RAMSTKAssessmentInputs, RAMSTKAssessmentResults


class AssessmentInputs(RAMSTKAssessmentInputs):
    """
    Display Meter assessment input attribute data in the RAMSTK Work Book.

    The Meter assessment input view displays all the assessment inputs for
    the selected Meter item.  This includes, currently, inputs for
    MIL-HDBK-217FN2.  The attributes of a Meter assessment input view are:

    :cvar dict _dic_quality: dictionary of meter quality levels.  Key is
        meter subcategory ID; values are lists of quality levels.
    :cvar dict _dic_type: dictionary of meter types.  Key is meter
        subcategory ID; values are lists of types.
    :cvar dict _dic_specification: dictionary of meter MIL-SPECs.  Key is
        meter tye ID; values are lists of specifications.
    :cvar dict _dic_insert: dictionary of meter insert materials.  First
        key is meter type ID, second key is meter specification ID; values are
        lists of insert materials.

    :ivar cmbApplication: select and display the application of the meter.
    :ivar cmbType: select and display the type of meter.
    """

    # Define private dict class attributes.
    _dic_keys = {0: 'quality_id', 1: 'application_id', 2: 'type_id'}

    # Quality levels; key is the subcategory ID.
    _dic_quality = {
        2: [["MIL-SPEC"], [_("Lower")]],
        1: [["MIL-SPEC"], [_("Lower")]]
    }
    # Meter types; key is the subcategory ID.
    _dic_types = {
        1: [[_("AC")], [_("Inverter Driver")], [_("Commutator DC")]],
        2: [[_("Direct Current")], [_("Alternating Current")]]
    }

    # Define private list class attributes.
    _lst_labels = [_("Quality Level:"), _("Meter Type:"), _("Meter Function:")]
    _lst_title: List[str] = ["", ""]

    # Define private scalar class attributes.
    _module: str = 'meter'
    _tablabel: str = ""
    _tabtooltip: str = ""

    def __init__(self, configuration: RAMSTKUserConfiguration,
                 logger: RAMSTKLogManager) -> None:
        """
        Initialize an instance of the Meter assessment input view.

        :param configuration: the RAMSTKUserConfiguration class instance.
        :type configuration: :class:`ramstk.configuration.RAMSTKUserConfiguration`
        :param logger: the RAMSTKLogManager class instance.
        :type logger: :class:`ramstk.logger.RAMSTKLogManager`
        """
        super().__init__(configuration, logger)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.cmbApplication: RAMSTKComboBox = RAMSTKComboBox()
        self.cmbType: RAMSTKComboBox = RAMSTKComboBox()

        self._lst_widgets = [
            self.cmbQuality, self.cmbType, self.cmbApplication
        ]

        self.__set_properties()
        self.__set_callbacks()
        self.make_ui()

        # Subscribe to PyPubSub messages.
        pub.subscribe(self.do_load_comboboxes, 'changed_subcategory')

        pub.subscribe(self._do_load_page, 'loaded_hardware_inputs')

    def __set_callbacks(self) -> None:
        """
        Set callback methods for Meter assessment input widgets.

        :return: None
        :rtype: None
        """
        self.cmbQuality.dic_handler_id['changed'] = self.cmbQuality.connect(
            'changed', self._on_combo_changed, 0)
        self.cmbApplication.dic_handler_id[
            'changed'] = self.cmbApplication.connect('changed',
                                                     self._on_combo_changed, 1)
        self.cmbType.dic_handler_id['changed'] = self.cmbType.connect(
            'changed', self._on_combo_changed, 2)

    def __set_properties(self) -> None:
        """
        Set properties for Meter assessment input widgets.

        :return: None
        :rtype: None
        """
        self.cmbApplication.do_set_properties(
            tooltip=_("The application of the panel meter."))
        self.cmbType.do_set_properties(tooltip=_("The type of meter."))

    def _do_load_page(self, attributes: Dict[str, Any]) -> None:
        """
        Load the Meter assesment input widgets.

        :param dict attributes: the attributes dictionary for the selected
            Meter.
        :return: None
        :rtype: None
        """
        super().do_load_page(attributes)

        self.cmbApplication.do_update(attributes['application_id'],
                                      signal='changed')
        self.cmbType.do_update(attributes['type_id'], signal='changed')

        self._do_set_sensitive()

    def _do_set_sensitive(self) -> None:
        """
        Set widget sensitivity as needed for the selected meter.

        :return: None
        :rtype: None
        """
        self.cmbType.set_sensitive(True)
        self.cmbApplication.set_sensitive(False)

        if self._hazard_rate_method_id == 2 and self._subcategory_id == 2:
            self.cmbApplication.set_sensitive(True)

    def _on_combo_changed(self, combo: RAMSTKComboBox, index: int) -> None:
        """
        Retrieve RAMSTKCombo() changes and assign to Meter attribute.

        This method is called by:

            * Gtk.Combo() 'changed' signal

        :param combo: the RAMSTKCombo() that called this method.
        :type combo: :class:`ramstk.gui.gtk.ramstk.RAMSTKCombo`
        :param int index: the position in the signal handler list associated
            with the calling RAMSTKComboBox().  Indices are:

            +---------+------------------+---------+------------------+
            |  Index  | Widget           |  Index  | Widget           |
            +=========+==================+=========+==================+
            |    0    | cmbQuality       |    3    | cmbType          |
            +---------+------------------+---------+------------------+
            |    1    | cmbApplication   |         |                  |
            +---------+------------------+---------+------------------+

        :return: None
        :rtype: None
        """
        super().on_combo_changed(combo, index, 'wvw_editing_component')

    def do_load_comboboxes(self, subcategory_id: int) -> None:
        """
        Load the meter RAMSTKComboBox()s.

        This method is used to load the specification RAMSTKComboBox() whenever
        the meter subcategory is changed.

        :param int subcategory_id: the newly selected meter subcategory ID.
        :return: None
        :rtype: None
        """
        # Load the quality level RAMSTKComboBox().
        if self._hazard_rate_method_id == 1:
            _data = [["MIL-SPEC"], [_("Lower")]]
        else:
            try:
                _data = self._dic_quality[subcategory_id]
            except KeyError:
                _data = []
        self.cmbQuality.do_load_combo(_data, signal='changed')

        # Load the meter application RAMSTKComboBox().
        self.cmbApplication.do_load_combo(
            [[_("Ammeter")], [_("Voltmeter")], [_("Other")]], signal='changed')

        # Load the meter type RAMSTKComboBox().
        try:
            _data = self._dic_types[subcategory_id]
        except KeyError:
            _data = []
        self.cmbType.do_load_combo(_data, signal='changed')


class AssessmentResults(RAMSTKAssessmentResults):
    """
    Display Meter assessment results attribute data in the RAMSTK Work Book.

    The Meter assessment result view displays all the assessment results
    for the selected meter.  This includes, currently, results for
    MIL-HDBK-217FN2 parts count and MIL-HDBK-217FN2 part stress methods.  The
    attributes of a meter assessment result view are:

    :ivar txtPiA: displays the application factor for the panel meter.
    :ivar txtPiF: displays the function factor for the panel meter.
    :ivar txtPiT: displays the temperature stress factor for the elapsed time
        meter.
    """

    # Define private class dict class attributes.
    _dic_part_stress = {
        1:
        "<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>A</sub>\u03C0<sub>F</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>",
        2:
        "<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>T</sub>\u03C0<sub>E</sub></span>"
    }

    # Define private class list class attributes.
    _lst_title: List[str] = ["", ""]

    # Define private scalar class attributes.
    _module: str = 'meter'
    _tablabel: str = ""
    _tabtooltip: str = ""

    def __init__(self, configuration: RAMSTKUserConfiguration,
                 logger: RAMSTKLogManager) -> None:
        """
        Initialize an instance of the Meter assessment result view.

        :param configuration: the RAMSTKUserConfiguration class instance.
        :type configuration: :class:`ramstk.configuration.RAMSTKUserConfiguration`
        :param logger: the RAMSTKLogManager class instance.
        :type logger: :class:`ramstk.logger.RAMSTKLogManager`
        """
        super().__init__(configuration, logger)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.
        self._lst_tooltips = [
            _("The assessment model used to calculate the meter failure "
              "rate."),
            _("The base hazard rate of the meter."),
            _("The quality factor for the meter."),
            _("The environment factor for the meter."),
            _("The application factor for the meter."),
            _("The function factor for the meter."),
            _("The temperature stress factor for the meter.")
        ]
        self._lst_labels.append("\u03C0<sub>A</sub>:")
        self._lst_labels.append("\u03C0<sub>F</sub>:")
        self._lst_labels.append("\u03C0<sub>T</sub>:")

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.txtPiA: RAMSTKEntry = RAMSTKEntry()
        self.txtPiF: RAMSTKEntry = RAMSTKEntry()
        self.txtPiT: RAMSTKEntry = RAMSTKEntry()

        self._lst_widgets.append(self.txtPiA)
        self._lst_widgets.append(self.txtPiF)
        self._lst_widgets.append(self.txtPiT)

        #// TODO: update all component workviews to use the public set_properties() method.
        #//
        #// The capacitor, connection, and inductor assessment results
        #// workviws need to be updated to use the public set_properties()
        #// method in the parent RAMSTKAssessmentResults() class.
        self.set_properties()
        self.make_ui()

        # Subscribe to PyPubSub messages.
        pub.subscribe(self._do_load_page, 'loaded_hardware_results')
        pub.subscribe(self._do_load_page, 'succeed_calculate_hardware')

    def __do_set_part_stress_sensitive(self) -> None:
        """
        Set the widgets needed to display assessment results sensitive.

        :return: None
        :rtype: None
        """
        if self._hazard_rate_method_id == 2:
            self.txtPiE.set_sensitive(True)
            if self._subcategory_id == 1:
                self.txtPiT.set_sensitive(True)
                self.txtPiQ.set_sensitive(False)
            elif self._subcategory_id == 2:
                self.txtPiA.set_sensitive(True)
                self.txtPiF.set_sensitive(True)

    def _do_load_page(self, attributes: Dict[str, Any]) -> None:
        """
        Load the meter assessment results page.

        :param dict attributes: the attributes dictionary for the selected
            Meter.
        :return: None
        :rtype: None
        """
        super().do_load_page(attributes)

        self.txtPiA.do_update(str(self.fmt.format(attributes['piA'])))
        self.txtPiF.do_update(str(self.fmt.format(attributes['piF'])))
        self.txtPiT.do_update(str(self.fmt.format(attributes['piT'])))

        self._do_set_sensitive()

    def _do_set_sensitive(self) -> None:
        """
        Set widget sensitivity as needed for the selected meter.

        :return: None
        :rtype: None
        """
        super().do_set_sensitive()

        self.txtPiA.set_sensitive(False)
        self.txtPiF.set_sensitive(False)
        self.txtPiT.set_sensitive(False)

        self.__do_set_part_stress_sensitive()