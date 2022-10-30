# SPDX-FileCopyrightText: 2020 Luis Falcón <falcon@gnuhealth.org>
# SPDX-FileCopyrightText: 2011-2022 GNU Solidario <health@gnusolidario.org>
#
# SPDX-License-Identifier: GPL-3.0-or-later
#########################################################################
#   Hospital Management Information System (HMIS) component of the      #
#                       GNU Health project                              #
#                   https://www.gnuhealth.org                           #
#########################################################################
#                       HEALTH IMAGING package                          #
#              sequences.py: Sequences for this package                 #
#########################################################################

from trytond.model import (ModelView, ModelSingleton, ModelSQL,
                           ValueMixin, MultiValueMixin, fields)
from trytond import backend
from trytond.pyson import Id
from trytond.pool import Pool
from trytond.tools.multivalue import migrate_property

# Sequences
imaging_req_seq = fields.MultiValue(
    fields.Many2One(
        'ir.sequence', 'Imaging Request Sequence', required=True,
        domain=[('sequence_type', '=', Id(
            'health_imaging', 'seq_type_gnuhealth_imaging_test_request'))]))

imaging_test_sequence = fields.MultiValue(
    fields.Many2One(
        'ir.sequence', 'Imaging Sequence', required=True,
        domain=[('sequence_type', '=', Id(
            'health_imaging', 'seq_type_gnuhealth_imaging_test'))]))


# GNU HEALTH SEQUENCES
class GnuHealthSequences(ModelSingleton, ModelSQL, ModelView, MultiValueMixin):
    'Standard Sequences for GNU Health'
    __name__ = 'gnuhealth.sequences'

    imaging_req_seq = fields.MultiValue(
        imaging_req_seq)

    imaging_test_sequence = fields.MultiValue(
        imaging_test_sequence)

    @classmethod
    def default_imaging_req_seq(cls, **pattern):
        pool = Pool()
        ModelData = pool.get('ir.model.data')
        try:
            return ModelData.get_id('health_imaging',
                                    'seq_gnuhealth_imaging_test_request')
        except KeyError:
            return None

    @classmethod
    def default_imaging_test_sequence(cls, **pattern):
        pool = Pool()
        ModelData = pool.get('ir.model.data')
        try:
            return ModelData.get_id('health_imaging',
                                    'seq_gnuhealth_imaging_test')
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


class ImagingRequestSequence(_ConfigurationValue, ModelSQL, ValueMixin):
    'Imaging Request Sequence setup'
    __name__ = 'gnuhealth.sequences.imaging_req_seq'
    imaging_req_seq = imaging_req_seq
    _configuration_value_field = 'imaging_req_seq'

    @classmethod
    def check_xml_record(cls, records, values):
        return True


class ImagingTestSequence(_ConfigurationValue, ModelSQL, ValueMixin):
    'Imaging Test Sequence setup'
    __name__ = 'gnuhealth.sequences.imaging_test_sequence'
    imaging_test_sequence = imaging_test_sequence
    _configuration_value_field = 'imaging_test_sequence'

    @classmethod
    def check_xml_record(cls, records, values):
        return True
