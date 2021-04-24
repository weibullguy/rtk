# pylint: disable=cyclic-import
# -*- coding: utf-8 -*-
#
#       ramstk.controllers.validation.analysismanager.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright 2007 - 2020 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Validation Controller Package analysis manager."""

# Standard Library Imports
from datetime import date
from typing import Any, Dict

# Third Party Imports
# noinspection PyPackageRequirements
import pandas as pd
import treelib
from pubsub import pub

# RAMSTK Package Imports
from ramstk.configuration import RAMSTKUserConfiguration
from ramstk.controllers import RAMSTKAnalysisManager


class AnalysisManager(RAMSTKAnalysisManager):
    """Contain the attributes and methods of the Validation analysis manager.

    This class manages the validation analysis for Allocation, MIL-HDBK-217F,
    NSWC, and Similar Item.  Attributes of the validation Analysis Manager are:

    :ivar _attributes: the dict used to hold the aggregate attributes for
        the validation item being analyzed.
    """

    def __init__(
        self, configuration: RAMSTKUserConfiguration, **kwargs: Dict[str, Any]
    ) -> None:
        """Initialize an instance of the validation analysis manager.

        :param configuration: the Configuration instance associated with the
            current instance of the RAMSTK application.
        :type configuration: :class:`ramstk.Configuration.Configuration`
        """
        super().__init__(configuration, **kwargs)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self._status_tree: treelib.Tree = treelib.Tree()

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        # Subscribe to PyPubSub messages.
        pub.subscribe(
            super().on_get_all_attributes, "succeed_get_all_validation_attributes"
        )
        pub.subscribe(super().on_get_tree, "succeed_get_validations_tree")

        pub.subscribe(self.do_calculate_plan, "request_calculate_plan")

        pub.subscribe(
            self._do_calculate_all_tasks, "request_calculate_validation_tasks"
        )
        pub.subscribe(self._do_calculate_task, "request_calculate_validation_task")
        pub.subscribe(self._do_request_status_tree, "succeed_retrieve_validations")
        pub.subscribe(self._on_get_status_tree, "succeed_retrieve_program_status")
        pub.subscribe(self._on_get_status_tree, "succeed_get_program_status_tree")

    def do_calculate_plan(self) -> None:
        """Calculate the planned burndown of the overall validation effort.

        This method will calculate three values for each scheduled end date
        in the validation plan, the lower bound, average, and upper bound
        for the tasks planned to still be open on each of the scheduled end
        dates in the plan.

        :return: _planned; the pandas DataFrame() containing the planned
            burndown hours for the entire validation effort.
        """
        _dic_plan = {}
        _dic_planned = {}  # type: ignore
        _time_ll = 0.0
        _time_mean = 0.0
        _time_ul = 0.0
        _start_date = date.today()

        for _node in self._tree.all_nodes()[1:]:
            # Calculate the three times if the mean task time is zero.
            if _node.data["validation"].time_mean <= 0.0:
                _node.data["validation"].calculate_task_time()

            # Keep a running total of the three times and the earliest task
            # start date.  The earliest start date will be assigned the
            # total number of hours in the validation program.
            _start_date = min(
                _start_date, pd.to_datetime(_node.data["validation"].date_start)
            )
            _time_ll += _node.data["validation"].time_ll
            _time_mean += _node.data["validation"].time_mean
            _time_ul += _node.data["validation"].time_ul

            # Calculate the sum of task hours for each, unique end date.
            _end_date = _node.data["validation"].date_end
            try:
                # Update the end date's times.
                _dic_planned[pd.to_datetime(_end_date)][0] += _node.data[
                    "validation"
                ].time_ll
                _dic_planned[pd.to_datetime(_end_date)][1] += _node.data[
                    "validation"
                ].time_mean
                _dic_planned[pd.to_datetime(_end_date)][2] += _node.data[
                    "validation"
                ].time_ul
            except KeyError:
                # Add the first time to the end date.
                _dic_planned[pd.to_datetime(_end_date)] = [
                    _node.data["validation"].time_ll,
                    _node.data["validation"].time_mean,
                    _node.data["validation"].time_ul,
                ]

        # Create a pandas DataFrame() of the task times sorted by date in
        # descending order.  The descending order is needed because the
        # ultimate DataFrame() will contain *remaining* total task hours for
        # the validation effort, not the total task hours planned to
        # complete on each day.
        # noinspection PyTypeChecker
        _planned = pd.DataFrame(
            _dic_planned.values(),
            index=_dic_planned.keys(),
            columns=["lower", "mean", "upper"],
        ).sort_index(ascending=False)

        # Calculate the total task time remaining on each planned end date
        # and then sort the DataFrame() by date in ascending order.
        _planned = _planned.cumsum() - _planned
        _planned.loc[_start_date] = [_time_ll, _time_mean, _time_ul]
        _planned = _planned.sort_index()

        _dic_plan["plan"] = _planned
        _dic_plan["assessed"] = self._do_select_assessment_targets()
        _dic_plan["actual"] = self._do_select_actual_status()

        pub.sendMessage(
            "succeed_calculate_verification_plan",
            attributes=_dic_plan,
        )

    def _do_calculate_all_tasks(self) -> None:
        """Calculate mean, standard error, and bounds on all task's time/cost.

        These values are calculated assuming a beta distribution (typical
        project management assumption).  This method also calculates the
        remaining average time and cost of the overall validation plan.

        :return: None
        :rtype: None
        """
        _program_cost_remaining = 0.0
        _program_time_remaining = 0.0

        _node: treelib.Node
        for _node in self._tree.all_nodes_itr():
            # noinspection PyDeepBugsBinOperand
            if _node.identifier != 0:
                self._do_calculate_task(_node.identifier)

                _program_cost_remaining += _node.data["validation"].cost_average * (
                    1.0 - _node.data["validation"].status / 100.0
                )
                _program_time_remaining += _node.data["validation"].time_average * (
                    1.0 - _node.data["validation"].status / 100.0
                )

        pub.sendMessage(
            "succeed_calculate_all_validation_tasks",
            cost_remaining=_program_cost_remaining,
            time_remaining=_program_time_remaining,
        )

    def _do_calculate_task(self, node_id: int) -> None:
        """Calculate mean, standard error, and bounds on task time and cost.

        These values are calculated assuming a beta distribution (typical
        project management assumption).

        :param node_id: the ID of the node (task) to calculate.
        :return: None
        :rtype: None
        """
        _node = self._tree.get_node(node_id)

        _node.data["validation"].calculate_task_time()
        _node.data["validation"].calculate_task_cost()

        pub.sendMessage(
            "request_set_validation_attributes",
            node_id=[node_id, -1],
            package={"time_ll": _node.data["validation"].time_ll},
        )
        pub.sendMessage(
            "request_set_validation_attributes",
            node_id=[node_id, -1],
            package={"time_mean": _node.data["validation"].time_mean},
        )
        pub.sendMessage(
            "request_set_validation_attributes",
            node_id=[node_id, -1],
            package={"time_ul": _node.data["validation"].time_ul},
        )
        pub.sendMessage(
            "request_set_validation_attributes",
            node_id=[node_id, -1],
            package={"cost_ll": _node.data["validation"].cost_ll},
        )
        pub.sendMessage(
            "request_set_validation_attributes",
            node_id=[node_id, -1],
            package={"cost_mean": _node.data["validation"].cost_mean},
        )
        pub.sendMessage(
            "request_set_validation_attributes",
            node_id=[node_id, -1],
            package={"cost_ul": _node.data["validation"].cost_ul},
        )
        pub.sendMessage(
            "succeed_calculate_validation_task",
            tree=self._tree,
        )

    def _do_request_status_tree(self, tree: treelib.Tree) -> None:
        """Send the request to retrieve the Program Status tree.

        :param tree: the Validation treelib Tree().
        :return: None
        :rtype: None
        """
        self._tree = tree

        pub.sendMessage(
            "request_get_program_status_tree",
        )

    def _do_select_actual_status(self) -> pd.DataFrame:
        """Select the actual program status remaining time and cost.

        :return: a pandas DataFrame() containing the actual status update
            dates and the remaining time/cost.
        :rtype: :class:`pandas.DataFrame`
        """
        _dic_actual = {}
        for _node in self._status_tree.all_nodes()[1:]:
            _dic_actual[pd.to_datetime(_node.data["program_status"].date_status)] = [
                _node.data["program_status"].cost_remaining,
                _node.data["program_status"].time_remaining,
            ]

        # noinspection PyTypeChecker
        return pd.DataFrame(
            _dic_actual.values(), index=_dic_actual.keys(), columns=["cost", "time"]
        ).sort_index()

    def _do_select_assessment_targets(self) -> pd.DataFrame:
        """Select the targets for all tasks of Reliability Assessment type.

        :return: _assessed; a pandas DataFrame() containing the assessment
            dates as the index and associated targets.
        """
        _dic_assessed = {}
        for _node in self._tree.all_nodes()[1:]:
            if _node.data["validation"].task_type == 5:
                _dic_assessed[pd.to_datetime(_node.data["validation"].date_end)] = [
                    _node.data["validation"].acceptable_minimum,
                    _node.data["validation"].acceptable_mean,
                    _node.data["validation"].acceptable_maximum,
                ]

        # noinspection PyTypeChecker
        return pd.DataFrame(
            _dic_assessed.values(),
            index=_dic_assessed.keys(),
            columns=["lower", "mean", "upper"],
        ).sort_index()

    def _on_get_status_tree(self, tree: treelib.Tree) -> None:
        """Set the analysis manager's status treelib Tree().

        :param tree: the program status data manager's treelib Tree().
        :return: None
        :rtype: None
        """
        self._status_tree = tree
