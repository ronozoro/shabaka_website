from odoo import models, fields


class BlogPost(models.Model):
    _inherit = 'blog.post'

    image = fields.Binary(string='Image')


BlogPost()
