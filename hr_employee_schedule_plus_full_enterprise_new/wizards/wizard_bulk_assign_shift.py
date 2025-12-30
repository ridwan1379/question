# -*- coding: utf-8 -*-
from odoo import api, fields, models

class WizardBulkAssignShift(models.TransientModel):
    _name = 'wizard.bulk.assign.shift'
    _description = 'Bulk Assign Shift Wizard'

    shift_id = fields.Many2one('hr.shift', required=True)
    employee_ids = fields.Many2many('hr.employee')
    date_from = fields.Date()
    date_to = fields.Date()
    notify = fields.Boolean('Send Notification', default=True)
    force = fields.Boolean('Force assign (ignore conflicts)', default=False)

    def apply_shift(self):
        for emp in self.employee_ids:
            emp.action_assign_shift(self.shift_id.id, date_from=self.date_from, date_to=self.date_to, notify=self.notify, force=self.force)
        return {'type': 'ir.actions.act_window_close'}
