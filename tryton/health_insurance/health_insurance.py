# SPDX-FileCopyrightText: 2008-2022 Luis Falcón <falcon@gnuhealth.org>
# SPDX-FileCopyrightText: 2011-2022 GNU Solidario <health@gnusolidario.org>
#
# SPDX-License-Identifier: GPL-3.0-or-later
#########################################################################
#   Hospital Management Information System (HMIS) component of the      #
#                       GNU Health project                              #
#                   https://www.gnuhealth.org                           #
#########################################################################
#                      HEALTH INSURANCE package                         #
#              health_insurance.py: main module                         #
#########################################################################

from trytond.model import ModelView, ModelSQL, fields
from trytond.pyson import Eval
from trytond.i18n import gettext

from .exceptions import (DiscountPctOutOfRange, NeedAPolicy,
                         DiscountWithoutElement)


__all__ = ['InsurancePlanProductPolicy', 'InsurancePlan', 'HealthService']


class InsurancePlanProductPolicy(ModelSQL, ModelView):
    'Policy associated to the product on the insurance plan'
    __name__ = "gnuhealth.insurance.plan.product.policy"

    plan = fields.Many2One(
        'gnuhealth.insurance.plan',
        'Plan', required=True)

    product = fields.Many2One('product.product', 'Product')

    product_category = fields.Many2One('product.category', 'Category')

    discount = fields.Float(
        'Discount', digits=(3, 2),
        help="Discount in Percentage. It has higher precedence than "
             "the fixed price when both values coexist")

    price = fields.Float(
        'Price', help="Apply a fixed price for this product or category")

    @classmethod
    def validate(cls, policies):
        super(InsurancePlanProductPolicy, cls).validate(policies)
        for policy in policies:
            policy.validate_discount()
            policy.validate_policy_elements()

    def validate_discount(self):
        if (self.discount):
            if (self.discount < 0 or self.discount > 100):
                raise DiscountPctOutOfRange(
                    gettext('health_insurance.msg_pct_out_of_range')
                    )
        if (not self.discount and not self.price):
            raise NeedAPolicy(
                gettext('health_insurance.msg_need_a_policy')
                )

    def validate_policy_elements(self):
        if (not self.product and not self.product_category):
            raise DiscountWithoutElement(
                gettext('health_insurance.msg_discount_without_element')
                )


class InsurancePlan(ModelSQL, ModelView):
    __name__ = "gnuhealth.insurance.plan"
    _rec_name = 'name'

    product_policy = fields.One2Many(
        'gnuhealth.insurance.plan.product.policy',
        'plan', 'Policy')


class HealthService(ModelSQL, ModelView):
    __name__ = 'gnuhealth.health_service'

    insurance_holder = fields.Many2One(
        'party.party', 'Insurance Holder',
        help="Insurance Policy Holder")

    insurance_plan = fields.Many2One(
        'gnuhealth.insurance',
        'Plan',
        domain=[('name', '=', Eval('insurance_holder'))],
        depends=['insurance_holder'])

    # Set the insurance holder upon entering the patient
    @fields.depends('patient')
    def on_change_patient(self):
        if self.patient:
            self.insurance_holder = self.patient.name
