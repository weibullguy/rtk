# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.models.programdb.ramstkmilhdbkf_unit_test.py is part of The
#       RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2021 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Class for testing the RAMSTKMilHdbkF module algorithms and models."""

# Third Party Imports
# noinspection PyPackageRequirements
import pytest
# noinspection PyUnresolvedReferences
from mocks import MockDAO

# RAMSTK Package Imports
from ramstk.models.programdb import RAMSTKMilHdbkF


@pytest.fixture
def mock_program_dao(monkeypatch):
    _mil_hdbk_f_1 = RAMSTKMilHdbkF()
    _mil_hdbk_f_1.revision_id = 1
    _mil_hdbk_f_1.hardware_id = 1
    _mil_hdbk_f_1.A1 = 0.0
    _mil_hdbk_f_1.A2 = 0.0
    _mil_hdbk_f_1.B1 = 0.0
    _mil_hdbk_f_1.B2 = 0.0
    _mil_hdbk_f_1.C1 = 0.0
    _mil_hdbk_f_1.C2 = 0.0
    _mil_hdbk_f_1.lambdaBD = 0.0
    _mil_hdbk_f_1.lambdaBP = 0.0
    _mil_hdbk_f_1.lambdaCYC = 0.0
    _mil_hdbk_f_1.lambdaEOS = 0.0
    _mil_hdbk_f_1.piA = 0.0
    _mil_hdbk_f_1.piC = 0.0
    _mil_hdbk_f_1.piCD = 0.0
    _mil_hdbk_f_1.piCF = 0.0
    _mil_hdbk_f_1.piCR = 0.0
    _mil_hdbk_f_1.piCV = 0.0
    _mil_hdbk_f_1.piCYC = 0.0
    _mil_hdbk_f_1.piE = 0.0
    _mil_hdbk_f_1.piF = 0.0
    _mil_hdbk_f_1.piI = 0.0
    _mil_hdbk_f_1.piK = 0.0
    _mil_hdbk_f_1.piL = 0.0
    _mil_hdbk_f_1.piM = 0.0
    _mil_hdbk_f_1.piMFG = 0.0
    _mil_hdbk_f_1.piN = 0.0
    _mil_hdbk_f_1.piNR = 0.0
    _mil_hdbk_f_1.piP = 0.0
    _mil_hdbk_f_1.piPT = 0.0
    _mil_hdbk_f_1.piQ = 0.0
    _mil_hdbk_f_1.piR = 0.0
    _mil_hdbk_f_1.piS = 0.0
    _mil_hdbk_f_1.piT = 0.0
    _mil_hdbk_f_1.piTAPS = 0.0
    _mil_hdbk_f_1.piU = 0.0
    _mil_hdbk_f_1.piV = 0.0

    DAO = MockDAO()
    DAO.table = [
        _mil_hdbk_f_1,
    ]

    yield DAO


ATTRIBUTES = {
    'A1': 0.0,
    'A2': 0.0,
    'B1': 0.0,
    'B2': 0.0,
    'C1': 0.0,
    'C2': 0.0,
    'lambdaBD': 0.0,
    'lambdaBP': 0.0,
    'lambdaCYC': 0.0,
    'lambdaEOS': 0.0,
    'piA': 0.0,
    'piC': 0.0,
    'piCD': 0.0,
    'piCF': 0.0,
    'piCR': 0.0,
    'piCV': 0.0,
    'piCYC': 0.0,
    'piE': 0.0,
    'piF': 0.0,
    'piI': 0.0,
    'piK': 0.0,
    'piL': 0.0,
    'piM': 0.0,
    'piMFG': 0.0,
    'piN': 0.0,
    'piNR': 0.0,
    'piP': 0.0,
    'piPT': 0.0,
    'piQ': 0.0,
    'piR': 0.0,
    'piS': 0.0,
    'piT': 0.0,
    'piTAPS': 0.0,
    'piU': 0.0,
    'piV': 0.0
}


@pytest.mark.usefixtures('mock_program_dao')
class TestRAMSTKMilHdbk217F():
    """Class for testing the RAMSTKMilHdbk217F model."""
    @pytest.mark.unit
    def test_ramstkmilhdbkf_create(self, mock_program_dao):
        """__init__() should create an RAMSTKMilHdbkF model."""
        DUT = mock_program_dao.do_select_all(RAMSTKMilHdbkF)[0]

        assert isinstance(DUT, RAMSTKMilHdbkF)
        assert DUT.__tablename__ == 'ramstk_mil_hdbk_f'
        assert DUT.hardware_id == 1
        assert DUT.A1 == 0.0
        assert DUT.A2 == 0.0
        assert DUT.B1 == 0.0
        assert DUT.B2 == 0.0
        assert DUT.C1 == 0.0
        assert DUT.C2 == 0.0
        assert DUT.lambdaBD == 0.0
        assert DUT.lambdaBP == 0.0
        assert DUT.lambdaCYC == 0.0
        assert DUT.lambdaEOS == 0.0
        assert DUT.piA == 0.0
        assert DUT.piC == 0.0
        assert DUT.piCD == 0.0
        assert DUT.piCF == 0.0
        assert DUT.piCR == 0.0
        assert DUT.piCV == 0.0
        assert DUT.piCYC == 0.0
        assert DUT.piE == 0.0
        assert DUT.piF == 0.0
        assert DUT.piI == 0.0
        assert DUT.piK == 0.0
        assert DUT.piL == 0.0
        assert DUT.piM == 0.0
        assert DUT.piMFG == 0.0
        assert DUT.piN == 0.0
        assert DUT.piNR == 0.0
        assert DUT.piP == 0.0
        assert DUT.piPT == 0.0
        assert DUT.piQ == 0.0
        assert DUT.piR == 0.0
        assert DUT.piS == 0.0
        assert DUT.piT == 0.0
        assert DUT.piTAPS == 0.0
        assert DUT.piU == 0.0
        assert DUT.piV == 0.0

    @pytest.mark.unit
    def test_get_attributes(self, mock_program_dao):
        """get_attributes() should return a tuple of attribute values."""
        DUT = mock_program_dao.do_select_all(RAMSTKMilHdbkF)[0]

        _attributes = DUT.get_attributes()

        assert isinstance(_attributes, dict)
        assert _attributes['hardware_id'] == 1
        assert _attributes['A1'] == 0.0
        assert _attributes['A2'] == 0.0
        assert _attributes['B1'] == 0.0
        assert _attributes['B2'] == 0.0
        assert _attributes['C1'] == 0.0
        assert _attributes['C2'] == 0.0
        assert _attributes['lambdaBD'] == 0.0
        assert _attributes['lambdaBP'] == 0.0
        assert _attributes['lambdaCYC'] == 0.0
        assert _attributes['lambdaEOS'] == 0.0
        assert _attributes['piA'] == 0.0
        assert _attributes['piC'] == 0.0
        assert _attributes['piCD'] == 0.0
        assert _attributes['piCF'] == 0.0
        assert _attributes['piCR'] == 0.0
        assert _attributes['piCV'] == 0.0
        assert _attributes['piCYC'] == 0.0
        assert _attributes['piE'] == 0.0
        assert _attributes['piF'] == 0.0
        assert _attributes['piI'] == 0.0
        assert _attributes['piK'] == 0.0
        assert _attributes['piL'] == 0.0
        assert _attributes['piM'] == 0.0
        assert _attributes['piMFG'] == 0.0
        assert _attributes['piN'] == 0.0
        assert _attributes['piNR'] == 0.0
        assert _attributes['piP'] == 0.0
        assert _attributes['piPT'] == 0.0
        assert _attributes['piQ'] == 0.0
        assert _attributes['piR'] == 0.0
        assert _attributes['piS'] == 0.0
        assert _attributes['piT'] == 0.0
        assert _attributes['piTAPS'] == 0.0
        assert _attributes['piU'] == 0.0
        assert _attributes['piV'] == 0.0

    @pytest.mark.unit
    def test_set_attributes(self, mock_program_dao):
        """set_attributes() should return a zero error code on success."""
        DUT = mock_program_dao.do_select_all(RAMSTKMilHdbkF)[0]

        assert DUT.set_attributes(ATTRIBUTES) is None

    @pytest.mark.unit
    def test_set_attributes_none_value(self, mock_program_dao):
        """set_attributes() should set an attribute to it's default value when
        the attribute is passed with a None value."""
        DUT = mock_program_dao.do_select_all(RAMSTKMilHdbkF)[0]

        ATTRIBUTES['piA'] = None

        assert DUT.set_attributes(ATTRIBUTES) is None
        assert DUT.get_attributes()['piA'] == 0.0

    @pytest.mark.unit
    def test_set_attributes_unknown_attributes(self, mock_program_dao):
        """set_attributes() should raise an AttributeError when passed an
        unknown attribute."""
        DUT = mock_program_dao.do_select_all(RAMSTKMilHdbkF)[0]

        with pytest.raises(AttributeError):
            DUT.set_attributes({'shibboly-bibbly-boo': 0.9998})
