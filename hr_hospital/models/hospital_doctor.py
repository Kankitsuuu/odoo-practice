import time

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class HospitalDoctor(models.Model):
    _name = 'hospital.doctor'
    _description = 'Hospital Doctors'
    _inherit = 'hospital.person'

    specialty_id = fields.Many2one(
        comodel_name='hospital.doctor.specialty',
    )
    mentor_id = fields.Many2one(
        comodel_name='hospital.doctor',
    )
    intern_ids = fields.One2many(
        string='Interns',
        comodel_name='hospital.doctor',
        inverse_name='mentor_id',
        readonly=True,
    )
    patient_ids = fields.One2many(
        comodel_name='hospital.patient',
        inverse_name='doctor_id',
        string='Patients',
    )
    visit_ids = fields.One2many(
        comodel_name='hospital.visit',
        inverse_name='doctor_id',
        string='Visits',
    )

    # CRUD methods
    @api.model
    def create(self, vals):
        if vals.get('mentor_id') and self.doctor_is_intern(vals['mentor_id']):
            raise UserError(_('You cannot choose intern as mentor.'))
        return super(HospitalDoctor, self).create(vals)

    def write(self, vals):
        if vals.get('mentor_id'):
            if self.doctor_is_intern(vals['mentor_id']):
                raise UserError(_('You cannot choose intern as mentor.'))
            elif self._origin.id == vals['mentor_id']:
                raise UserError(_('You cannot choose yourself as mentor.'))
        return super(HospitalDoctor, self).write(vals)

    # Action methods
    def action_create_visit(self):
        doctor_id = self.env.context.get('doctor_id')
        return {
            'name': _('New Visit'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'visit.create.wizard',
            'target': 'new',
            'context': {'default_doctor_id': doctor_id}
        }

    def action_get_report(self):
        doctor_id = self.env.context['active_ids'][0]
        doctor = self.env['hospital.doctor'].browse(doctor_id)
        data = {
            'doctor_name': f'{doctor.name} {doctor.surname}',
            'doctor_specialty': doctor.specialty_id.name
        }
        # use `module_name.report_id` as reference
        return self.env.ref('hr_hospital.doctor_report_id').report_action(self, data=data)

    # Custom methods
    def doctor_is_intern(self, rec_id: int) -> bool:
        record = self.browse(rec_id)
        if record.mentor_id:
            return True
        return False
