from odoo import models,fields
from odoo.addons import decimal_precision as dp 
from odoo import api  # if not already imported 
from odoo.fields import Date as fDate
from datetime import timedelta

class BaseArchive(models.AbstractModel): 
    _name = 'base.archive' 
    active = fields.Boolean(default=True) 
 
    def do_archive(self): 
        for record in self: 
            record.active = not record.active 

class LibraryBook(models.Model):
    _name = 'my_module.book'
    _inherit = ['base.archive'] 
    _description = 'Library Book'
    _order = 'date_release desc, name' 
    _rec_name = 'short_name' 
    name = fields.Char('Title',required=True)
    short_name = fields.Char( 
        string='Short Title', 
        size=100,  # For Char only 
        translate=False,  # also for Text fields 
        ) 
    notes = fields.Text('Internal Notes')
    state = fields.Selection( 
    [('draft', 'Not Available'), 
        ('available', 'Available'), 
        ('lost', 'Lost')], 
    'State')
    description = fields.Html( 
        string='Description', 
        # optional: 
        sanitize=True, 
        strip_style=False, 
        translate=False, 
    )
    retail_price = fields.Monetary( 
        'Retail Price', 
        # optional: currency_field='currency_id', 
        ) 
    cover = fields.Binary('Book Cover')
    out_of_print = fields.Boolean('Out of Print?')
    date_release = fields.Date('Release Date')
    author_ids = fields.Many2many('res.partner',string='Authors')
    date_updated = fields.Datetime('Last Updated')
    active = fields.Boolean('Active', default=True)
    cost_price = fields.Float( 
        'Book Cost', dp.get_precision('Book Price'))
    currency_id = fields.Many2one( 
        'res.currency', string='Currency')
    retail_price = fields.Monetary( 
        'Retail Price', 
        # optional: currency_field='currency_id', 
        )
    publisher_id = fields.Many2one('res.partner',string='Publisher',ondelete='set null',context={},domain=[],)
    pages = fields.Integer( 
        string='Number of Pages', 
        default=0, 
        help='Total book page count', 
        groups='base.group_user', 
        states={'lost': [('readonly', True)]}, 
        copy=True, 
        index=False, 
        readonly=False, 
        required=False, 
        company_dependent=False, 
        )
    publisher_city = fields.Char( 
        'Publisher City', 
        related='publisher_id.city',
        readonly=True) 
        
    reader_rating = fields.Float( 
        'Reader Average Rating', 
        digits=(14, 4),  # Optional precision (total, decimals), 
    )
    age_days = fields.Float( 
        string='Days Since Release', 
        compute='_compute_age', 
        inverse='_inverse_age', 
        search='_search_age', 
        store=False, 
        compute_sudo=False, 
    )
    @api.model
    def _referencable_models(self):
        models = self.env['res.request.link'].search([])
        return [(x.object,x.name) for x in models]
    
    ref_doc_id = fields.Reference( 
        selection='_referencable_models', 
        string='Reference Document')

    @api.depends('date_release')
    def _compute_age(self): 
        today = fDate.from_string(fDate.today()) 
        for book in self.filtered('date_release'): 
            delta = (today -
                     fDate.from_string(book.date_release)) 
            book.age_days = delta.days 
    
    def _inverse_age(self):
        today = fDate.from_string(fDate.context_today(self)) 
        for book in self.filtered('date_release'): 
            d = today - timedelta(days=book.age_days)
            book.date_release = fDate.to_string(d)
    def _search_age(self, operator, value): 
        today = fDate.from_string(fDate.context_today(self)) 
        value_days = timedelta(days=value) 
        value_date = fDate.to_string(today - value_days)
        # convert the operator:
        # book with age > value have a date < value_date
        operator_map = {
            '>': '<', '>=': '<=',
            '<': '>', '<=': '>=',
        }
        new_op = operator_map.get(operator, operator)
        return [('date_release', new_op, value_date)]

    _sql_constraints = [ 
    ('name_uniq', 
        'UNIQUE (name)', 
        'Book title must be unique.') 
    ]
    @api.constrains('date_release') 
    def _check_release_date(self):
        for record in self:
            if (record.date_release and
                    record.date_release > fields.Date.today()):
                raise models.ValidationError(
                    'Release date must be in the past')
    # publisher_id = fields.Many2one(
    #     'res.partner', string='Publisher',
    #     # optional:
    #     ondelete='set null',
    #     context={},
    #     domain=[],
    #     )

    
class ResPartner(models.Model):
    _inherit = 'res.partner'
    _order = 'name'
    published_book_ids = fields.One2many( 
        'my_module.book', 'publisher_id', 
        string='Published Books')

    authored_book_ids = fields.Many2many( 
        'my_module.book', 
        string='Authored Books', 
        # relation='library_book_res_partner_rel'  # optional 
        )
    
    count_books = fields.Integer( 
        'Number of Authored Books', 
        compute='_compute_count_books' 
        )

    @api.depends('authored_book_ids')
    def _compute_count_books(self):
        for r in self:
            r.count_books=len(r.authored_book_ids)

