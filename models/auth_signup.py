# -*- coding: utf-8 -*-
from odoo import models, api


class AuthSignUpUser(models.Model):
    _inherit = 'res.users'

    @api.model
    def _signup_create_user(self, values):
        res = super(AuthSignUpUser, self)._signup_create_user(values)
        if res.partner_id:
            res.partner_id.sudo().write({'city': values.get('city'), 'phone': values.get('phone')})
        return res


AuthSignUpUser()
