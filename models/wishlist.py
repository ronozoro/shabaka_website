from odoo import models, fields


class Wishlist(models.Model):
    _name = 'product.wishlist'
    _rec_name = 'name'
    name = fields.Char(string='My Wishlist')
    product_wishlist_ids = fields.Many2many(comodel_name='product.template', relation='product_partner_wish',
                                            column1='partner_id', column2='product_id')


Wishlist()


class ResPartner(models.Model):
    _inherit = 'res.partner'

    wishlist_id = fields.Many2one(comodel_name='product.wishlist', string='Wishlist')


ResPartner()
