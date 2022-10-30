# Copyright (C) 2008-2022 Luis Falcon <falcon@gnuhealth.org>
# Copyright (C) 2011-2022 GNU Solidario <health@gnusolidario.org>
# SPDX-FileCopyrightText: 2008-2022 Luis Falcón <falcon@gnuhealth.org>
# SPDX-FileCopyrightText: 2011-2022 GNU Solidario <health@gnusolidario.org>
#
# SPDX-License-Identifier: GPL-3.0-or-later

# GNU Health HMIS sequences for this package

from trytond.model import (ModelView, ModelSingleton, ModelSQL,
                           ValueMixin, MultiValueMixin, fields)
from trytond import backend
from trytond.pyson import Id
from trytond.pool import Pool
from trytond.tools.multivalue import migrate_property

# Sequences
ambulatory_care_sequence = fields.Many2One(
    'ir.sequence', 'Ambulatory Sequence', required=True,
    domain=[('sequence_type', '=', Id(
        'health', 'seq_type_gnuhealth_ambulatory_care'))])

patient_rounding_sequence = fields.Many2One(
    'ir.sequence', 'Patient Rounding Sequence', required=True,
    domain=[('sequence_type', '=', Id(
        'health', 'seq_type_gnuhealth_patient_rounding'))])



# GNU HEALTH SEQUENCES
class GnuHealthSequences(ModelSingleton, ModelSQL, ModelView, MultiValueMixin):
    'Standard Sequences for GNU Health'
    __name__ = 'gnuhealth.sequences'

    ambulatory_care_sequence = fields.MultiValue(
        ambulatory_care_sequence)

    patient_rounding_sequence = fields.MultiValue(
        patient_rounding_sequence)


    @classmethod
    def default_ambulatory_care_sequence(cls, **pattern):
        pool = Pool()
        ModelData = pool.get('ir.model.data')
        try:
            return ModelData.get_id('health',
                                    'seq_gnuhealth_ambulatory_care')
        except KeyError:
            return None

    @classmethod
    def default_patient_rounding_sequence(cls, **pattern):
        pool = Pool()
        ModelData = pool.get('ir.model.data')
        try:
            return ModelData.get_id('health',
                                    'seq_gnuhealth_patient_rounding')
        except KeyError:
            return None

class _ConfigurationValue(ModelSQL):

    _configuration_value_field = None

    @classmethod
    def __register__(cls, module_name):
        exist = backend.TableHandler.table_exist(cls._table)

        super(_ConfigurationValue, cls).__register__(module_name)

        if not exist:
            cls._migrate_property([], [], [])

    @classmethod
    def _migrate_property(cls, field_names, value_names, fields):
        field_names.append(cls._configuration_value_field)
        value_names.append(cls._configuration_value_field)
        migrate_property(
            'gnuhealth.sequences', field_names, cls, value_names,
            fields=fields)


class AmbulatoryCareSequence(_ConfigurationValue, ModelSQL, ValueMixin):
    'Ambulatory Care Sequences setup'
    __name__ = 'gnuhealth.sequences.ambulatory_care_sequence'
    ambulatory_care_sequence = ambulatory_care_sequence
    _configuration_value_field = 'ambulatory_care_sequence'

    @classmethod
    def check_xml_record(cls, records, values):
        return True


class PatientRoundingSequence(_ConfigurationValue, ModelSQL, ValueMixin):
    'Patient Evaluation Sequence setup'
    __name__ = 'gnuhealth.sequences.patient_rounding_sequence'
    patient_rounding_sequence = patient_rounding_sequence
    _configuration_value_field = 'patient_rounding_sequence'

    @classmethod
    def check_xml_record(cls, records, values):
        return True
