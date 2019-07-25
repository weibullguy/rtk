# -*- coding: utf-8 -*-
#
#       ramstk.controllers.revision.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Revision Package Data Model."""

# Third Party Imports
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.controllers import RAMSTKDataManager
from ramstk.exceptions import DataAccessError
from ramstk.models.programdb import (
    RAMSTKEnvironment, RAMSTKFailureDefinition,
    RAMSTKMission, RAMSTKMissionPhase, RAMSTKRevision
)


class DataManager(RAMSTKDataManager):
    """
    Contain the attributes and methods of the Revision data manager.

    This class manages the revision data from the RAMSTKRevision,
    RAMSTKFailureDefinition, RAMSTKMission, RAMSTKMissionPhase, and
    RAMSKTEnvironment data models.
    """

    _tag = 'revision'
    _root = 0

    def __init__(self, dao, **kwargs):  # pylint: disable=unused-argument
        """
        Initialize a Revision data manager instance.

        :param dao: the data access object for communicating with the RAMSTK
            Program database.
        :type dao: :class:`ramstk.dao.DAO.DAO`
        """
        RAMSTKDataManager.__init__(self, dao, **kwargs)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        # Subscribe to PyPubSub messages.
        pub.subscribe(self.do_select_all, 'request_retrieve_revisions')
        pub.subscribe(self._do_delete, 'request_delete_revision')
        pub.subscribe(self._do_delete_failure_definition,
                      'request_delete_failure_definition')
        pub.subscribe(self._do_delete_mission, 'request_delete_mission')
        pub.subscribe(self._do_delete_mission_phase,
                      'request_delete_mission_phase')
        pub.subscribe(self._do_delete_environment,
                      'request_delete_environment')
        pub.subscribe(self.do_insert, 'request_insert_revision')
        pub.subscribe(self.do_update, 'request_update_revision')
        pub.subscribe(self.do_update_all, 'request_update_all_revisions')
        pub.subscribe(self.do_get_attributes,
                      'request_get_revision_attributes')
        pub.subscribe(self.do_get_all_attributes,
                      'request_get_all_revision_attributes')
        pub.subscribe(self.do_get_tree, 'request_get_revision_tree')
        pub.subscribe(self.do_set_attributes,
                      'request_set_revision_attributes')
        pub.subscribe(self.do_set_all_attributes,
                      'request_set_all_revision_attributes')

    def _do_delete(self, node_id):
        """
        Remove a revision.

        :param int node_id: the node (revision) ID to be removed from the
            RAMSTK Program database.
        :return: None
        :rtype: None
        """
        (_error_code,
         _error_msg) = RAMSTKDataManager.do_delete(self, node_id, 'revision')

        # pylint: disable=attribute-defined-outside-init
        # self.last_id is defined in RAMSTKDataManager.__init__
        if _error_code == 0:
            self.tree.remove_node(node_id)
            self.last_id = max(self.tree.nodes.keys())

            pub.sendMessage('succeed_delete_revision', node_id=node_id)
        else:
            _error_msg = ("Attempted to delete non-existent revision ID "
                          "{0:s}.").format(str(node_id))
            pub.sendMessage('fail_delete_revision', error_msg=_error_msg)

    def _do_delete_failure_definition(self, revision_id, node_id):
        """
        Remove a failure definition.

        :param int revision_id: the revision ID to remove the failure
            definition from.
        :param int node_id: the failure definition ID to remove.
        :return: None
        :rtype: None
        """
        _definitions = RAMSTKDataManager.do_select(self, revision_id,
                                                   'failure_definitions')
        try:
            _error_code, _error_msg = self.dao.db_delete(_definitions[node_id])

            if _error_code == 0:
                _definitions.pop(node_id)
                self.tree.get_node(
                    revision_id).data['failure_definitions'] = _definitions

                pub.sendMessage('succeed_delete_failure_definition',
                                node_id=node_id)
        except KeyError:
            pub.sendMessage('fail_delete_failure_definition',
                            error_msg=("Attempted to delete non-existent "
                                       "failure definition ID {0:s} from "
                                       "revision ID {1:s}.").format(
                                           str(node_id), str(revision_id)))

    def _do_delete_mission(self, revision_id, node_id):
        """
        Remove a mission from revision ID.

        :param int revision_id: the revision ID to remove the mission from.
        :param int node_id: the mission ID to remove.
        :return: None
        :rtype: None
        """
        try:
            self._do_delete_profile(revision_id, node_id)
            pub.sendMessage('succeed_delete_mission', node_id=node_id)
        except AttributeError:
            pub.sendMessage('fail_delete_mission',
                            error_msg=("Attempted to delete non-existent "
                                       "mission ID {0:s} from revision ID "
                                       "{1:s}.").format(
                                           str(node_id), str(revision_id)))

    def _do_delete_mission_phase(self, revision_id, mission_id, node_id):
        """
        Remove a mission phase from mission ID.

        :param int revision_id: the revision ID to remove the mission from.
        :param int mission_id: the mission ID to remove the mission phase from.
        :param int node_id: the mission phase ID to remove.
        :return: None
        :rtype: None
        """
        try:
            self._do_delete_profile(revision_id, node_id)
            pub.sendMessage('succeed_delete_mission_phase',
                            node_id=str(node_id))
        except AttributeError:
            pub.sendMessage('fail_delete_mission_phase',
                            error_msg=("Attempted to delete non-existent "
                                       "mission phase ID {0:s} from mission "
                                       "ID {1:s}.").format(
                                           str(node_id), str(mission_id)))

    def _do_delete_environment(self, revision_id, phase_id, node_id):
        """
        Remove a environment.

        :param int revision_id: the revision ID to remove the environment from.
        :param int mission_id: the mission phase ID to remove the environment
            from.
        :param int node_id: the environment ID to remove.
        :return: None
        :rtype: None
        """
        try:
            self._do_delete_profile(revision_id, node_id)
            pub.sendMessage('succeed_delete_environment', node_id=str(node_id))
        except AttributeError:
            pub.sendMessage('fail_delete_environment',
                            error_msg=("Attempted to delete non-existent "
                                       "environment ID {0:s} from mission "
                                       "phase ID {1:s}.").format(
                                           str(node_id), str(phase_id)))

    def _do_delete_profile(self, revision_id, node_id):
        """
        Remove a usage profile element.

        :param int revision_id: the revision ID to remove the udage profile
            element from.
        :param int node_id: the usage profile element ID to remove.
        :return: None
        :rtype: None
        """
        _profile = RAMSTKDataManager.do_select(self, revision_id,
                                               'usage_profile')

        (_error_code, _error_msg) = self.dao.db_delete(
            _profile.get_node(str(node_id)).data)

        if _error_code == 0:
            _profile.remove_node(str(node_id))
            self.tree.get_node(revision_id).data['usage_profile'] = _profile

    def _do_select_usage_profile(self, revision_id):
        """
        Retrieve the usage profile data from the RAMSTK Program database.

        :param int revision_id: the Revision ID to select the Usage Profile
            for.
        :return: _tree; the usage profile treelib Tree().
        :rtype: :class:`treelib.Tree()`
        """
        _tree = Tree()
        _tree.create_node(tag='usage_profile',
                          identifier=revision_id,
                          parent=None)

        for _mission in self.dao.session.query(RAMSTKMission).filter(
                RAMSTKMission.revision_id == revision_id).all():
            _tree.create_node(tag=_mission.description,
                              identifier='{0:d}'.format(_mission.mission_id),
                              parent=revision_id,
                              data=_mission)

            for _phase in self.dao.session.query(RAMSTKMissionPhase).filter(
                    RAMSTKMissionPhase.mission_id ==
                    _mission.mission_id).all():
                _tree.create_node(tag=_phase.description,
                                  identifier='{0:d}.{1:d}'.format(
                                      _mission.mission_id, _phase.phase_id),
                                  parent=str(_mission.mission_id),
                                  data=_phase)

                for _environment in self.dao.session.query(
                        RAMSTKEnvironment).filter(RAMSTKEnvironment.phase_id ==
                                                  _phase.phase_id).all():
                    _tree.create_node(tag=_environment.name,
                                      identifier='{0:d}.{1:d}.{2:d}'.format(
                                          _mission.mission_id, _phase.phase_id,
                                          _environment.environment_id),
                                      parent='{0:d}.{1:d}'.format(
                                          _mission.mission_id,
                                          _phase.phase_id),
                                      data=_environment)

        return _tree

    def _do_set_failure_definition(self, node_id, key, value, definition_id):
        """
        Set the attributes of the record associated with definition ID.

        This is a helper method to set the desired failure definition attribute
        since the failure definitions are carried in a dict and we need to
        select the correct record to update.

        :param int node_id: the ID of the record in the RAMSTK Program
            database table whose attributes are to be set.
        :param str key: the key in the attributes dict.
        :param value: the new value of the attribute to set.
        :param int definition_id: the failure definition ID if the attribute
            being set is a failure definition attribute.
        :return: None
        :rtype: None
        """
        try:
            _attributes = self.do_select(
                node_id,
                table='failure_definitions')[definition_id].get_attributes()
            _attributes.pop('revision_id')
            _attributes.pop('definition_id')
        except KeyError:
            _attributes = {}

        if key in _attributes:
            _attributes[key] = value
            self.do_select(
                node_id,
                table='failure_definitions')[definition_id].set_attributes(
                    _attributes)

    def _do_set_usage_profile(self, node_id, key, value, usage_id):
        """
        Set the attributes of the record associated with usage ID.

        This is a helper method to set the desired usage profile attribute
        since the usage profile is carried as a treelib Tree() and we need to
        select the correct node (record) to update.

        :param int node_id: the ID of the revision in the RAMSTK Program
            database table whose attributes are to be set.
        :param str key: the key in the attributes dict.
        :param value: the new value of the attribute to set.
        :param int usage_id: the usage profile ID of the element (mission,
            mission phase, or environment) whose attribute is being set.
        :return: None
        :rtype: None
        """
        try:
            _attributes = self.do_select(node_id,
                                         table='usage_profile').get_node(
                                             usage_id).data.get_attributes()

            if len(usage_id.split('.')) == 1:
                _attributes.pop('revision_id')
                _attributes.pop('mission_id')
            elif len(usage_id.split('.')) == 2:
                _attributes.pop('mission_id')
                _attributes.pop('phase_id')
            elif len(usage_id.split('.')) == 3:
                _attributes.pop('phase_id')
                _attributes.pop('environment_id')

        except (AttributeError, KeyError):
            _attributes = {}

        if key in _attributes:
            _attributes[key] = value
            self.do_select(node_id, table='usage_profile').get_node(
                usage_id).data.set_attributes(_attributes)

    def do_get_all_attributes(self, node_id):
        """
        Retrieve all RAMSTK data tables' attributes for the revision.

        This is a helper method to be able to retrieve all the revision's
        attributes in a single call.  It's used primarily by the
        AnalysisManager.

        :param int node_id: the node (revision) ID of the revision item to
            get the attributes for.
        :return: None
        :rtype: None
        """
        _attributes = {'failure_definitions': {}, 'usage_profile': None}
        for _table in ['revision', 'failure_definitions', 'usage_profile']:
            if _table == 'failure_definitions':
                _attributes['failure_definitions'].update(
                    self.do_select(node_id, table=_table))
            elif _table == 'usage_profile':
                _attributes['usage_profile'] = self.do_select(node_id,
                                                              table=_table)
            else:
                _attributes.update(
                    self.do_select(node_id, table=_table).get_attributes())

        pub.sendMessage('succeed_get_all_revision_attributes',
                        attributes=_attributes)

    def do_get_attributes(self, node_id, table):
        """
        Retrieve the RAMSTK data table attributes for the revision.

        .. important:: the failure definition will return a dict of all the
            failure definitions associated with the node (revision) ID.  This
            dict uses the definition ID as the key and the instance of the
            RAMSTKFailureDefinition as the value.  The subscibing methods and
            functions will need to unpack this dict.

        .. important:: the usage profile will return a treelib Tree() of all
            the usage profiles associated with the node (revision) ID.  The
            subscribing methods and functions will need to parse this Tree().

        :param int node_id: the node (revision) ID of the revision to get the
            attributes for.
        :param str table: the RAMSTK data table to retrieve the attributes
            from.
        :return: None
        :rtype: None
        """
        if table in ['failure_definitions', 'usage_profile']:
            _attributes = self.do_select(node_id, table=table)
        else:
            _attributes = self.do_select(node_id, table=table).get_attributes()

        pub.sendMessage('succeed_get_{0:s}_attributes'.format(table),
                        attributes=_attributes)

    def do_get_tree(self):
        """
        Retrieve the revision treelib Tree.

        :return: None
        :rtype: None
        """
        pub.sendMessage('succeed_get_revision_tree', dmtree=self.tree)

    def do_insert(self):  # pylint: disable=arguments-differ
        """
        Add a new revision.

        :return: None
        :rtype: None
        """
        _tree = Tree()

        try:
            _revision = RAMSTKRevision(name='New Revision')
            _error_code, _msg = self.dao.db_add([_revision])
            if _error_code == 0:
                self.last_id = _revision.revision_id
                _tree.create_node(tag='usage_profile',
                                  identifier=self.last_id,
                                  parent=None)
                self.tree.create_node(tag=_revision.name,
                                      identifier=self.last_id,
                                      parent=self._root,
                                      data={
                                          'revision': _revision,
                                          'failure_definitions': {},
                                          'usage_profile': _tree
                                      })
                self.do_insert_failure_definition(self.last_id)
                self.do_insert_mission(self.last_id)
                pub.sendMessage('succeed_insert_revision',
                                node_id=self.last_id)
            else:
                raise DataAccessError(_msg)
        except DataAccessError as _error:
            print(_error)
            pub.sendMessage("fail_insert_revision",
                            error_msg=("Failed to insert revision into "
                                       "program dabase."))

    def do_insert_environment(self, revision_id, mission_id, phase_id):
        """
        Add a new environment for phase ID.

        :param int revision_id: the revision ID to add the new environment.
        :param int mission_id: the mission ID to add the new environment.
        :param int phase_id: the mission phase ID to add the new environment.
        :return: None
        :rtype: None
        """
        try:
            _environment = RAMSTKEnvironment(phase_id=phase_id)
            _error_code, _msg = self.dao.db_add([_environment])
            if _error_code == 0:
                _phase_id = '{0:d}.{1:d}'.format(mission_id, phase_id)
                _environment_id = '{0:d}.{1:d}.{2:d}'.format(
                    mission_id, phase_id, _environment.environment_id)
                self.tree.get_node(
                    revision_id).data['usage_profile'].create_node(
                        tag=_environment.name,
                        identifier=_environment_id,
                        parent=str(_phase_id),
                        data=_environment)
                pub.sendMessage("succeed_insert_environment",
                                node_id=_environment_id)
            else:
                raise DataAccessError(_msg)
        except DataAccessError as _error:
            print(_error)
            pub.sendMessage("fail_insert_environment", error_message=_error)

    def do_insert_failure_definition(self, revision_id):
        """
        Add a new failure definition for revision ID.

        :param int revision_id: the revision ID to add the new failure
            definition to.
        :return: None
        :rtype: None
        """
        try:
            _failure_definition = RAMSTKFailureDefinition(
                revision_id=revision_id)
            _error_code, _msg = self.dao.db_add([_failure_definition])
            if _error_code == 0:
                self.tree.get_node(revision_id).data['failure_definitions'][
                    _failure_definition.definition_id] = _failure_definition
                pub.sendMessage("succeed_insert_failure_definition",
                                node_id=_failure_definition.definition_id)
            else:
                raise DataAccessError(_msg)
        except DataAccessError as _error:
            print(_error)
            pub.sendMessage("fail_insert_failure_definition", error_msg=_error)

    def do_insert_mission(self, revision_id):
        """
        Add a new mission for revision ID.

        :param int revision_id: the revision ID to add the new mission.
        :return: None
        :rtype: None
        """
        try:
            _mission = RAMSTKMission(revision_id=revision_id)
            _error_code, _msg = self.dao.db_add([_mission])
            if _error_code == 0:
                self.tree.get_node(
                    revision_id).data['usage_profile'].create_node(
                        tag=_mission.description,
                        identifier='{0:d}'.format(_mission.mission_id),
                        parent=revision_id,
                        data=_mission)
                pub.sendMessage("succeed_insert_mission",
                                node_id=_mission.mission_id)
            else:
                raise DataAccessError(_msg)
        except DataAccessError as _error:
            print(_error)
            pub.sendMessage("fail_insert_mission", error_message=_error)

    def do_insert_mission_phase(self, revision_id, mission_id):
        """
        Add a new mission phase for mission ID.

        :param int revision_id: the revision ID to add the new mission phase.
        :param int mission_id: the mission ID to add the new mission phase.
        :return: None
        :rtype: None
        """
        try:
            _phase = RAMSTKMissionPhase(mission_id=mission_id)
            _error_code, _msg = self.dao.db_add([_phase])
            if _error_code == 0:
                _phase_id = '{0:d}.{1:d}'.format(mission_id, _phase.phase_id)
                self.tree.get_node(
                    revision_id).data['usage_profile'].create_node(
                        tag=_phase.description,
                        identifier=_phase_id,
                        parent=str(mission_id),
                        data=_phase)
                pub.sendMessage("succeed_insert_mission_phase",
                                node_id=_phase_id)
            else:
                raise DataAccessError(_msg)
        except DataAccessError as _error:
            print(_error)
            pub.sendMessage("fail_insert_mission_phase", error_message=_error)

    def do_select_all(self):  # pylint: disable=arguments-differ
        """
        Retrieve all the Revision data from the RAMSTK Program database.

        :return: None
        :rtype: None
        """
        for _node in self.tree.children(self.tree.root):
            self.tree.remove_node(_node.identifier)

        for _revision in self.dao.session.query(RAMSTKRevision).all():

            _failure_definitions = self.dao.session.query(
                RAMSTKFailureDefinition).filter(
                    RAMSTKFailureDefinition.revision_id ==
                    _revision.revision_id).all()
            _failure_definitions = self.do_build_dict(_failure_definitions,
                                                      'definition_id')
            _usage_profile = self._do_select_usage_profile(
                _revision.revision_id)

            _data_package = {
                'revision': _revision,
                'failure_definitions': _failure_definitions,
                'usage_profile': _usage_profile
            }

            self.tree.create_node(tag=_revision.name,
                                  identifier=_revision.revision_id,
                                  parent=self._root,
                                  data=_data_package)

        self.last_id = max(self.tree.nodes.keys())

        pub.sendMessage('succeed_retrieve_revisions', tree=self.tree)

    def do_set_all_attributes(self,
                              attributes,
                              definition_id=None,
                              usage_id=None):
        """
        Set all the attributes of the record associated with the Module ID.

        This is a helper function to set a group of attributes in a single
        call.  Used mainly by the AnalysisManager.

        :param dict attributes: the aggregate attributes dict for the revision.
        :keyword int definition_id: the failure definition ID if the attribute
            being set is a failure definition attribute.
        :keyword str usage_id: the usage profile ID if the attribute being set
            is a usage profile (mission, mission phase, or environment)
            attribute.
        :return: None
        :rtype: None
        """
        for _key in attributes:
            self.do_set_attributes(attributes['revision_id'], _key,
                                   attributes[_key], definition_id, usage_id)

    def do_set_attributes(self,
                          node_id,
                          key,
                          value,
                          definition_id=None,
                          usage_id=None):
        """
        Set the attributes of the record associated with the Module ID.

        :param int node_id: the ID of the record in the RAMSTK Program
            database table whose attributes are to be set.
        :param str key: the key in the attributes dict.
        :param value: the new value of the attribute to set.
        :keyword int definition_id: the failure definition ID if the attribute
            being set is a failure definition attribute.
        :keyword str usage_id: the usage profile ID if the attribute being set
            is a usage profile (mission, mission phase, or environment)
            attribute.
        :return: None
        :rtype: None
        """
        for _table in ['revision', 'failure_definitions', 'usage_profile']:
            if _table == 'failure_definitions':
                self._do_set_failure_definition(node_id, key, value,
                                                definition_id)
            elif _table == 'usage_profile':
                self._do_set_usage_profile(node_id, key, value, usage_id)
            else:
                _attributes = self.do_select(node_id,
                                             table=_table).get_attributes()
                if key in _attributes:
                    _attributes[key] = value

                    try:
                        _attributes.pop('revision_id')
                    except KeyError:
                        pass

                    self.do_select(node_id,
                                   table=_table).set_attributes(_attributes)

    def do_update(self, node_id):
        """
        Update the record associated with node ID in RAMSTK Program database.

        :param int node_id: the node (revision) ID of the revision to save.
        :return: None
        :rtype: None
        """
        try:
            self.dao.session.add(self.tree.get_node(node_id).data['revision'])
            _error_code, _error_msg = self.dao.db_update()

            if _error_code == 0:
                pub.sendMessage('succeed_update_revision', node_id=node_id)
            else:
                pub.sendMessage('fail_update_revision', error_msg=_error_msg)
        except AttributeError:
            pub.sendMessage('fail_update_revision',
                            error_msg=('Attempted to save non-existent '
                                       'revision with revision ID '
                                       '{0:s}.').format(str(node_id)))
        except TypeError:
            if node_id != 0:
                pub.sendMessage('fail_update_revision',
                                error_msg=('No data package found for '
                                           'revision ID {0:s}.').format(
                                               str(node_id)))