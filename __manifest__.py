{ 
    'name': "Library Books", 
    'summary': "Manage your books", 
    'depends': ['base','product','decimal_precision'], 
    'data': [
        # 'views/menu.xml',
        # 'views/book.xml',
        'security/groups.xml',
        'views/library_book.xml',
        'views/product_view.xml',
        'security/ir.model.access.csv',
        ], 
} 
