from datetime import datetime
from odoo import models, fields, _, api
from odoo.exceptions import UserError
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DATE_FORMAT


class DoctorScheduleWizard(models.TransientModel):
    _name = 'doctor.schedule.wizard'
    _description = 'Wizard to schedule doctor work time'

    doctor_id = fields.Many2one(
        comodel_name='hospital.doctor',
    )
    schedules = fields.Text(
        string='Schedules data',
    )

    # Action methods
    def action_open_wizard(self):
        return {
            'name': _('Doctor Schedule Wizard'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'doctor.schedule.wizard',
            'target': 'new',
            'context': {'default_doctor_id': self.env.context['active_ids'][0]}
        }

    def action_set_time(self) -> None:
        try:
            schedules = self.schedules.split('\n')
        except Exception:
            raise UserError(_('Wrong data.\n'
                              'Use this template for each line:\n'
                              'yyyy-mm-dd hh:mm-hh:mm'))
        error_msg = ''
        i = 1
        for schedule in schedules:
            if schedule:
                try:
                    work_date, work_times = schedule.split(' ')
                    if not self.validate_date_format(work_date):
                        raise ValueError
                    from_time, to_time = work_times.split('-')
                    from_time = self.strtime_to_float(from_time)
                    to_time = self.strtime_to_float(to_time)
                    self.env['hospital.doctor.schedule'].create({
                        'doctor_id': self.doctor_id.id,
                        'work_date': work_date,
                        'start_time': from_time,
                        'end_time': to_time

                    })

                except UserError as e:
                    error_msg += f'Line {i}: {e}\n'

                except ValueError:
                    error_msg += (f'Line {i}: Line starts with invalid date format.\n'
                                  f'Please use format: yyyy-mm-dd\n')

                except Exception:
                    error_msg += (f'Line {i}: Invalid time format.\n'
                                  f'Please use format: hh:mm')
            i += 1
        if error_msg:
            raise UserError(_(error_msg))

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
