from odoo import models, fields

class MoveDateLog(models.Model):
    _name = 'movedate.log'
    _description = 'Move Date Log'
    _order = 'change_date desc'
    
    user_id = fields.Many2one('res.users', string='changed by', required=True)
    model_name = fields.Char(string='Model', required=True)
    record_name = fields.Char(string='Record', required=True)
    old_date = fields.Date(string='Old Date')
    new_date = fields.Date(string='New Date')
    reason = fields.Text(string='Reason')
    change_date = fields.Datetime(string='Change Date', default=fields.Datetime.now)