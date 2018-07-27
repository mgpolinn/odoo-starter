from odoo import models, fields

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    myproductname = fields.Char("Product Name")