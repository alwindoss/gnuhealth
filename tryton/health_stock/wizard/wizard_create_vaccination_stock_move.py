# Copyright (C) 2008-2022 Luis Falcon <falcon@gnuhealth.org>
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
from ..exceptions import (StockMoveExists)

__all__ = ['CreateVaccinationStockMoveInit', 'CreateVaccinationStockMove']


class CreateVaccinationStockMoveInit(ModelView):
    'Create Vaccination Stock Move Init'
    __name__ = 'gnuhealth.vaccination.stock.move.init'


class CreateVaccinationStockMove(Wizard):
    'Create Vaccination Stock Move'
    __name__ = 'gnuhealth.vaccination.stock.move.create'

    start = StateView(
        'gnuhealth.vaccination.stock.move.init',
        'health_stock.view_create_vaccination_stock_move', [
            Button('Cancel', 'end', 'tryton-cancel'),
            Button('Create Stock Move', 'create_stock_move', 'tryton-ok', True)
        ])
    create_stock_move = StateTransition()

    def transition_create_stock_move(self):
        pool = Pool()
        StockMove = pool.get('stock.move')
        Vaccination = pool.get('gnuhealth.vaccination')

        vaccinations = Vaccination.browse(Transaction().context.get(
            'active_ids'))
        for vaccination in vaccinations:

            if vaccination.moves:
                raise StockMoveExists(
                    gettext('health_stock.msg_stock_move_exists')
                    )

            lines = []

            line_data = {}
            line_data['origin'] = str(vaccination)
            line_data['from_location'] = \
                vaccination.location.id
            line_data['to_location'] = \
                vaccination.name.name.customer_location.id
            line_data['product'] = \
                vaccination.vaccine.name.id
            line_data['unit_price'] = \
                vaccination.vaccine.name.list_price
            line_data['quantity'] = 1
            line_data['uom'] = \
                vaccination.vaccine.name.default_uom.id
            line_data['state'] = 'draft'
            lines.append(line_data)

            moves = StockMove.create(lines)

            StockMove.assign(moves)
            StockMove.do(moves)

        return 'end'
