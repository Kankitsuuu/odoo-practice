from datetime import datetime
from odoo import models, fields, _, api
from odoo.exceptions import UserError
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DATE_FORMAT


class DoctorScheduleWizard(models.TransientModel):
    _name = 'doctor.schedule.wizard'
    _description = 'Wizard to schedule doctor work time'

    doctor_id = fields.Many2one(
        comodel_name='hospital.doctor',
        required=True,
    )
    work_date = fields.Date(
        string='Date',
        requeired=True,
        default=fields.Date.today,
    )
    from_time = fields.Float(
        string='From',
        requeired=True,
        default=9,
    )
    to_time = fields.Float(
        string='To',
        required=True,
        default=17,
    )

    # Action methods
    def action_open_wizard(self, reopen: bool = False):
        data = {
            'name': _('Doctor Schedule Wizard'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'doctor.schedule.wizard',
            'target': 'new',
            'context': {'default_doctor_id': self.env.context['active_ids'][0]}
        }
        if reopen:
            data['context'].update(default_work_date=None)
        return data

    def action_set_time(self):
        self.ensure_one()
        self.env['hospital.doctor.schedule'].create({
            'doctor_id': self.doctor_id.id,
            'work_date': self.work_date.strftime(DATE_FORMAT),
            'start_time': self.from_time,
            'end_time': self.to_time
        })
        if self.env.context.get('reopen'):
            return self.action_open_wizard(reopen=True)
        else:
            return {
                    'name': _('Change Supervising Doctor Wizard'),
                    'type': 'ir.actions.act_window',
                    'view_mode': 'tree,form',
                    'res_model': 'hospital.doctor.schedule',
                    'target': 'current',
            }

    # Custom methods
    @api.model
    def strtime_to_float(self, t: str) -> float:
        hours, minutes = t.split(':')
        return int(hours) + int(minutes) / 60

    @api.model
    def validate_date_format(self, date: str) -> bool:
        try:
            datetime.strptime(date, DATE_FORMAT)
            return True
        except:
            return False
