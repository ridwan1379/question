# basic CSV import wizard placeholder
from odoo import fields, models, api
from odoo.exceptions import UserError
import base64, csv, io

class WizardImportShifts(models.TransientModel):
    _name = 'wizard.import.shifts'
    _description = 'Import Shifts from CSV'

    file = fields.Binary('CSV File', required=True)
    filename = fields.Char()

    def action_import(self):
        if not self.file:
            raise UserError('Please pick a file')
        data = base64.b64decode(self.file)
        file_input = io.StringIO(data.decode('utf-8'))
        reader = csv.DictReader(file_input)
        for row in reader:
            vals = {'name': row.get('name') or row.get('Name'), 'shift_type': row.get('shift_type') or 'morning'}
            try:
                vals['start_time'] = float(row.get('start_time', 0))
                vals['end_time'] = float(row.get('end_time', 0))
            except Exception:
                continue
            self.env['hr.shift'].create(vals)
        return {'type': 'ir.actions.act_window_close'}
