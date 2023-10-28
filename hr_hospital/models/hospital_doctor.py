from odoo import models, fields, api, _
from odoo.exceptions import UserError


class HospitalDoctor(models.Model):
    _name = 'hospital.doctor'
    _description = 'Hospital Doctors'
    _inherit = 'hospital.person'

    specialty = fields.Char()
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

    # Custom methods
    def doctor_is_intern(self, rec_id: int) -> bool:
        record = self.browse(rec_id)
        if record.mentor_id:
            return True
        return False
