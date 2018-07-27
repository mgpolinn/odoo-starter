
from odoo import models, fields, api
from odoo.exceptions import UserError, AccessError, ValidationError


class Book(models.Model):
    _name = 'librarian.book'
    _rec_name = 'booktitle'
    booktitle = fields.Char("Book Title")
    description = fields.Char("Description")
    author = fields.Char("Author")
    publishingcompany = fields.Char("Publishing Company")
    amount = fields.Float(string="Amount")
    price = fields.Float(string="Price")
    state = fields.Selection([
        ('new', 'New'),
        ('open', 'Open')
    ])

    @api.model
    @api.multi
    def show_import(self):
        return {
            'name': ("Import test"),
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'import.xls',
            'type': 'ir.actions.act_window',
            'target': 'new',
        }

    @api.one
    def new_progressbar(self):
        self.write({
            'state': 'new',
        })

    @api.one
    def open_progressbar(self):
        self.write({
            'state': 'open'
        })

    @api.multi
    @api.onchange('state')
    def update_status(self):
        self.ensure_one()
        if self.state == 'new':
            self.status = '1'
        elif self.state == 'open':
            self.status = '2'
    @api.depends('price', 'amount')
    def _totalprice(self):
        self.totalprice = self.price * self.amount
    totalprice = fields.Float(string="Tong gia", store=True, compute="_totalprice")