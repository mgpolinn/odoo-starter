from odoo import models, fields, api 
class BookCategory(models.Model): 
    _name = 'my_module.book.category' 
    name = fields.Char('Category')
    _parent_store = True 
    parent_left = fields.Integer(index=True) 
    parent_right = fields.Integer(index=True) 
     
    parent_id = fields.Many2one( 
        'my_module.book.category', 
        string='Parent Category', 
        ondelete='restrict', 
        index=True) 
    child_ids = fields.One2many( 
        'my_module.book.category', 'parent_id', 
        string='Child Categories') 
    

    @api.constrains('parent_id')
    def _check_hierarchy(self):
        if not self._check_recursion():
            raise models.ValidationError(
                'Error! You cannot create recursive categories.') 