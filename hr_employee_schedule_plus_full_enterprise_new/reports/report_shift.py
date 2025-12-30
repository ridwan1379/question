from odoo import models

class ReportShift(models.AbstractModel):
    _name = 'report.hr_employee_schedule_plus.shift_report'

    def _get_report_values(self, docids, data=None):
        docs = self.env['hr.employee'].browse(docids)
        return {
            'doc_ids': docids,
            'doc_model': 'hr.employee',
            'docs': docs,
        }
