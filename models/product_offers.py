from odoo import models, fields, api
from odoo.exceptions import Warning
from odoo.tools.translate import _


class ProductOffer(models.Model):
    _name = 'product.offer'

    name = fields.Char(string='Name', readonly=True)
    valid_from = fields.Date(string='Valid From', required=True)
    valid_to = fields.Date(string='Valid To', required=True)
    product_id = fields.Many2one(comodel_name='product.template', required=True)
    discount_value = fields.Float(string='Discount Value', required=True)

    @api.constrains('discount_value', 'valid_from', 'valid_to')
    def _constrains_valid_record(self):
        if self.discount_value <= 0:
            raise Warning(_('Discount Value Must be more than 0'))
        if self.valid_to < self.valid_from:
            raise Warning(_('Valid to must be greater than valid from '))

    @api.model
    def create(self, vals):
        res = super(ProductOffer, self).create(vals)
        res.write({'name': self.env['ir.sequence'].next_by_code('product.offer.code') or '/'})
        return res


ProductOffer()
