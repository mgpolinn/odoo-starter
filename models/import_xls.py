# -*- coding: utf-8 -*-
from tempfile import TemporaryFile
from odoo import models, fields, api
import openpyxl
import base64


class import_xls(models.Model):
    _name = 'import.xls'

    xls_file = fields.Binary(string='xls file')

    @api.multi
    def import_xls(self):
        file = base64.decodestring(self.xls_file)
        excel_fileobj = TemporaryFile('wb+')
        excel_fileobj.write(file)
        excel_fileobj.seek(0)
        workbook = openpyxl.load_workbook(excel_fileobj)
        sheet = workbook[workbook.get_sheet_names()[0]]
        for row in sheet.rows:
            while row[0].row > 1:
                v1 = row[0].value
                v2 = row[1].value
                v3 = row[2].value
                print(v1)
                self.env['librarian.book'].create({'booktitle': v1, 'author': v2, 'publishingcompany': v3})
                break
        return {
            'view_mode': 'tree',
            'res_model': 'librarian.book',
            'type': 'ir.actions.act_window',
        }