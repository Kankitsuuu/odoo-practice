from typing import Optional, NoReturn
from odoo import models, fields, api, _
from odoo.exceptions import UserError
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT as DATETIME_FORMAT
from datetime import datetime


class PatientChangeVisitWizard(models.TransientModel):
    _name = 'patient.change.visit.wizard'
    _description = 'Wizard to change patient visit'

    date = fields.Datetime()
    doctor_id = fields.Many2one(
        comodel_name='hospital.doctor',
    )
    visit_id = fields.Many2one(
        comodel_name='hospital.visit',
        domain=[
            ('is_canceled', '=', False),
            ('is_succeed', '!=', True),
            ('date', '>', fields.Datetime.now()),
        ],
        required=True,
    )

    @api.onchange('visit_id')
    def _onchange_visit_id(self) -> Optional[NoReturn]:
        if self.visit_id:
            if self.visit_id.is_canceled:
                raise UserError(_('You cannot change data for canceled visits'))
            elif self.visit_id.date < datetime.now():
                raise UserError(_('You cannot change past visits.'))
            self.write({
                'doctor_id': self.visit_id.doctor_id.id,
                'date': self.visit_id.date
            })

    # Action methods
    def action_open_wizard(self) -> dict:
        context = {}
        if self.env.context.get('active_ids'):
            active_visit_id = self.env.context['active_ids'][0]
            visit_id = self.env['hospital.visit'].browse(active_visit_id)
            context = {
                'default_visit_id': visit_id.id,
                'default_doctor_id': visit_id.doctor_id.id,
                'default_date': visit_id.date
            }
        data = {
            'name': _('Patient Change Visit Wizard'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'patient.change.visit.wizard',
            'target': 'new',
            'context': context
        }
        return data

    def action_change_visit(self) -> None:
        vals = dict()
        if self.date != self.visit_id.date:
            print('Date changed')
            print(self.date, self.visit_id.date)
            vals['date'] = datetime.strftime(self.date, DATETIME_FORMAT)
        if self.doctor_id != self.visit_id.doctor_id:
            print('Doctor changed')
            print(self.doctor_id, self.visit_id.doctor_id)
            vals['doctor_id'] = self.doctor_id.id
        if vals:
            self.visit_id.write(vals)
