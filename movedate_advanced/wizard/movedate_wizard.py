from odoo import models, fields, api
from odoo.exceptions import UserError

class MoveDateWizard(models.TransientModel):
    _name = 'movedate.wizard'
    _description = 'Move Date Wizard'

    new_date = fields.Date(string='New Date', required=True)
    reason = fields.Text(string='Reason', required=True)

    def action_apply(self):
        if not self.new_date:
            raise UserError('New date must be filled.')

        active_model = self.env.context.get('active_model')
        active_ids = self.env.context.get('active_ids')

        records = self.env[active_model].browse(active_ids)

        for rec in records:
            if active_model == 'sale.order':
                old_date = rec.date_order
                rec.date_order = self.new_date
            elif active_model == 'account.move':
                old_date = rec.invoice_date
                rec.invoice_date = self.new_date
            else:
                continue

            self.env['movedate.log'].create({
                'user_id': self.env.user.id,
                'model_name': active_model,
                'record_name': rec.display_name,
                'old_date': old_date,
                'new_date': self.new_date,
                'reason': self.reason,
            })
