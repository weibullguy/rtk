# -*- coding: utf-8 -*-
#
#       ramstk.controllers.function.analysismanager.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright 2019 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Function Controller Package analysis manager."""

# Third Party Imports
from pubsub import pub

# RAMSTK Package Imports
from ramstk.analyses import improvementfactor
from ramstk.controllers import RAMSTKAnalysisManager


class AnalysisManager(RAMSTKAnalysisManager):
    """
    Contain the attributes and methods of the Function analysis manager.

    This class manages the functional analysis for functional hazards analysis
    (FHA).  Attributes of the function Analysis Manager are:
    """
    def __init__(self, configuration, **kwargs):  # pylint: disable=unused-argument
        """
        Initialize an instance of the function analysis manager.

        :param configuration: the Configuration instance associated with the
            current instance of the RAMSTK application.
        :type configuration: :class:`ramstk.Configuration.Configuration`
        """
        super(AnalysisManager, self).__init__(configuration, **kwargs)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        # Subscribe to PyPubSub messages.
        pub.subscribe(self.on_get_all_attributes,
                      'succeed_get_all_stakeholder_attributes')
        pub.subscribe(self.on_get_tree, 'succeed_get_stakeholder_tree')
        pub.subscribe(self.do_calculate_stakeholder,
                      'request_calculate_stakeholder')

    def _do_calculate_improvement(self):
        """
        Calculate improvement factor and weight for currently selected item.

        :return: None
        :rtype: None
        """
        (self._attributes['improvement'], self._attributes['overall_weight']
         ) = improvementfactor.calculate_improvement(
             self._attributes['planned_rank'],
             self._attributes['customer_rank'],
             self._attributes['priority'],
             user_float_1=self._attributes['user_float_1'],
             user_float_2=self._attributes['user_float_2'],
             user_float_3=self._attributes['user_float_3'],
             user_float_4=self._attributes['user_float_4'],
             user_float_5=self._attributes['user_float_5'])

    def do_calculate_stakeholder(self, node_id):
        """
        Calculate improvement factor and weight for currently selected item.

        :param int node_id: the node (stakeholder) ID to calculate.
        :return: None
        :rtype: None
        """
        # Retrieve all the attributes from all the RAMSTK data tables for the
        # requested stakeholder.  We need to build a comprehensive dict of
        # attributes to pass to the various analysis methods/functions.
        pub.sendMessage('request_get_all_stakeholder_attributes',
                        node_id=node_id)

        self._do_calculate_improvement()

        pub.sendMessage('succeed_calculate_stakeholder',
                        attributes=self._attributes)
