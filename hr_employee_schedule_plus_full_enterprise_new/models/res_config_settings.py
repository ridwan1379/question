# -*- coding: utf-8 -*-
from odoo import api, fields, models

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    auto_assign_shift = fields.Boolean('Auto Assign Weekly Shift', default=False, config_parameter='hr_employee_schedule_plus.auto_assign_shift')
    reminder_days = fields.Integer('Reminder Before (days)', default=1, config_parameter='hr_employee_schedule_plus.reminder_days')
