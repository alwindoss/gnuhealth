-- SPDX-FileCopyrightText: 2021 Tryton Foundation <info@tryton.org>
--
-- SPDX-License-Identifier: GPL-3.0-or-later

-- 5.8 -> 6.0
-- [SQL] after update, remove code column
ALTER table ir_sequence_type DROP COLUMN code
