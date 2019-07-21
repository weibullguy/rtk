# -*- coding: utf-8 -*-
#
#       ramstk.analyses.fha.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright 2019 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Functional Hazards Analysis (FHA) Module."""

# Third Party imports
from sympy import symbols, sympify

# RAMSTK Package Imports
from ramstk.exceptions import OutOfRangeError

PROBABILITY = {
    'Level E - Extremely Unlikely': 1,
    'Level D - Remote': 2,
    'Level C - Occasional': 3,
    'Level B - Reasonably Probable': 4,
    'Level A - Frequent': 5
}
SEVERITY = {
    'Insignificant': 1,
    'Slight': 2,
    'Low': 3,
    'Medium': 4,
    'High': 5,
    'Major': 6
}


def calculate_hri(probability, severity):
    """
    Calculate the hazard risk index (HRI).

    .. note:: See MIL-STD-882.

    :param str probability: the hazard probability expressed in text.
    :param str severity: the hazard severity expressed in text.
    :return: _hri; the calculated hazard risk index.
    :rtype: int
    :raise: OutOfRangeError if passed an unknown probability or severity
        description.
    """
    try:
        return PROBABILITY[probability] * SEVERITY[severity]
    except KeyError:
        raise OutOfRangeError(("calculate_hri() was passed an unknown hazard "
                               "probability ({0:s}) or severity ({1:s}) "
                               "description.").format(probability, severity))


def calculate_user_defined(fha):
    """
    Calculate the user-defined hazards analysis.

    :param dict fha: the user-defined functional hazards assessment dict.  The
        calling method/function should create the fha dict as follows:

        fha = OrderedDict({
            _key: None
            for _key in [
                'uf1', 'uf2', 'uf3', 'ui1', 'ui2', 'ui3', 'equation1',
                'equation2', 'equation3', 'equation4', 'equation5', 'res1',
                'res2', 'res3', 'res4', 'res5'
                ]
            })

    :return: fha; the functional hazards assessment dict with updated results.
    :rtype: dict
    """
    (uf1, uf2, uf3, ui1, ui2, ui3, res1, res2, res3, res4,
     res5) = symbols('uf1 uf2 uf3 ui1 ui2 ui3 res1 res2 res3 res4 res5')

    # pylint: disable=eval-used
    fha['res1'] = sympify(fha['equation1']).evalf(
        subs={
            uf1: fha['uf1'],
            uf2: fha['uf2'],
            uf3: fha['uf3'],
            ui1: fha['ui1'],
            ui2: fha['ui2'],
            ui3: fha['ui3'],
            res1: fha['res1'],
            res2: fha['res2'],
            res3: fha['res3'],
            res4: fha['res4'],
            res5: fha['res5']
        })
    fha['res2'] = sympify(fha['equation2']).evalf(
        subs={
            uf1: fha['uf1'],
            uf2: fha['uf2'],
            uf3: fha['uf3'],
            ui1: fha['ui1'],
            ui2: fha['ui2'],
            ui3: fha['ui3'],
            res1: fha['res1'],
            res2: fha['res2'],
            res3: fha['res3'],
            res4: fha['res4'],
            res5: fha['res5']
        })
    fha['res3'] = sympify(fha['equation3']).evalf(
        subs={
            uf1: fha['uf1'],
            uf2: fha['uf2'],
            uf3: fha['uf3'],
            ui1: fha['ui1'],
            ui2: fha['ui2'],
            ui3: fha['ui3'],
            res1: fha['res1'],
            res2: fha['res2'],
            res3: fha['res3'],
            res4: fha['res4'],
            res5: fha['res5']
        })
    fha['res4'] = sympify(fha['equation4']).evalf(
        subs={
            uf1: fha['uf1'],
            uf2: fha['uf2'],
            uf3: fha['uf3'],
            ui1: fha['ui1'],
            ui2: fha['ui2'],
            ui3: fha['ui3'],
            res1: fha['res1'],
            res2: fha['res2'],
            res3: fha['res3'],
            res4: fha['res4'],
            res5: fha['res5']
        })
    fha['res5'] = sympify(fha['equation5']).evalf(
        subs={
            uf1: fha['uf1'],
            uf2: fha['uf2'],
            uf3: fha['uf3'],
            ui1: fha['ui1'],
            ui2: fha['ui2'],
            ui3: fha['ui3'],
            res1: fha['res1'],
            res2: fha['res2'],
            res3: fha['res3'],
            res4: fha['res4'],
            res5: fha['res5']
        })

    return fha


def set_user_defined_floats(fha, floats):
    """
    Set the user-defined float values for the user-defined calculations.

    :param dict fha: the functional hazard assessment dict.
    :param list floats: the list of float values.
    :return: fha; the functional hazard assessment dict with updated float
        values.
    :rtype: dict
    """
    for _idx in [0, 1, 2]:
        try:
            _key = list(fha.keys())[_idx]
            fha[_key] = float(floats[_idx])
        except IndexError:
            fha[_key] = 0.0
    print(fha)
    return fha


def set_user_defined_ints(fha, ints):
    """
    Set the user-defined integer values for the user-defined calculations.

    :param dict fha: the functional hazard assessment dict.
    :param list ints: the list of integer values.
    :return: fha; the functional hazard assessment dict with updated integer
        values.
    :rtype: dict
    """
    for _idx in [3, 4, 5]:
        try:
            _key = list(fha.keys())[_idx]
            fha[_key] = int(ints[_idx - 3])
        except IndexError:
            fha[_key] = 0

    return fha


def set_user_defined_functions(fha, functions):
    """
    Set the user-defined functions for the user-defined calculations.

    :param dict fha: the functional hazard assessment dict.
    :param list functions: the list of functions; list items are str.
    :return: fha; the functional hazard assessment dict with updated functions.
    :rtype: dict
    """
    for _idx in [6, 7, 8, 9, 10]:
        try:
            _key = list(fha.keys())[_idx]
            fha[_key] = str(functions[_idx - 6])
        except IndexError:
            fha[_key] = ''

    return fha


def set_user_defined_results(fha, results):
    """
    Set the user-defined results for the user-defined calculations.

    This allows the use of the results fields to be manually set to float
    values by the user essentially creating five more user-defined float
    values.

    :param dict fha: the functional hazard assessment dict.
    :param list results: the list of results.
    :return: fha; the functional hazard assessment dict with updated results.
    :rtype: dict
    """
    for _idx in [11, 12, 13, 14, 15]:
        try:
            _key = list(fha.keys())[_idx]
            fha[_key] = results[_idx - 11]
        except IndexError:
            fha[_key] = 0

    return fha
