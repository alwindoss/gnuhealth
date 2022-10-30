# Copyright (C) 2008-2022 Luis Falcon <lfalcon@gnusolidario.org>
# Copyright (C) 2011-2022 GNU Solidario <health@gnusolidario.org>
# Copyright (C) 2013  Sebastian Marro <smarro@gnusolidario.org>
# SPDX-FileCopyrightText: 2008-2022 Luis Falcón <falcon@gnuhealth.org>
# SPDX-FileCopyrightText: 2011-2022 GNU Solidario <health@gnusolidario.org>
# SPDX-FileCopyrightText: 2013 Sebastian Marro <smarro@thymbra.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later

from trytond.wizard import Wizard, StateView, Button, StateTransition
from trytond.model import ModelView
from trytond.transaction import Transaction
from trytond.pool import Pool
from trytond.i18n import gettext
from ..exceptions import (StockMoveExists, NoPharmacy)

__all__ = ['CreatePrescriptionStockMoveInit', 'CreatePrescriptionStockMove']


class CreatePrescriptionStockMoveInit(ModelView):
    'Create Prescription Stock Move Init'
    __name__ = 'gnuhealth.prescription.stock.move.init'


class CreatePrescriptionStockMove(Wizard):
    'Create Prescription Stock Move'
    __name__ = 'gnuhealth.prescription.stock.move.create'

    start = StateView(
        'gnuhealth.prescription.stock.move.init',
        'health_stock.view_create_prescription_stock_move', [
            Button('Cancel', 'end', 'tryton-cancel'),
            Button(
                'Create Stock Move', 'create_stock_move',
                'tryton-ok', True),
        ])
    create_stock_move = StateTransition()

    def transition_create_stock_move(self):
        pool = Pool()
        StockMove = pool.get('stock.move')
        Prescription = pool.get('gnuhealth.prescription.order')

        moves = []
        prescriptions = Prescription.browse(Transaction().context.get(
            'active_ids'))
        for prescription in prescriptions:

            if prescription.moves:
                raise StockMoveExists(
                    gettext('health_stock.msg_stock_move_exists')
                    )

            if not prescription.pharmacy:
                raise NoPharmacy(
                    gettext('health_stock.msg_no_pharmacy')
                    )

            from_location = prescription.pharmacy.warehouse
            if from_location.type == 'warehouse':
                from_location = from_location.storage_location
            to_location = prescription.patient.name.customer_location

            for line in prescription.prescription_line:
                move = StockMove()
                move.origin = prescription
                move.from_location = from_location
                move.to_location = to_location
                move.product = line.medicament.name
                move.unit_price = line.medicament.name.list_price
                move.quantity = line.quantity
                move.uom = line.medicament.name.default_uom
                moves.append(move)
        StockMove.save(moves)
        StockMove.do(moves)
        return 'end'
