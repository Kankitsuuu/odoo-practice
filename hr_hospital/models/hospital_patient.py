from odoo import models, fields, api, _
from datetime import datetime


class HospitalPatient(models.Model):
    _name = 'hospital.patient'
    _description = 'Hospital Patients'
    _inherit = 'hospital.person'

    birthday_date = fields.Date(
        required=True,
    )
    age = fields.Integer(
        compute='_compute_age',
        readonly=True,
    )
    passport = fields.Char(
        string='Passport(Details)',
        required=True,
    )
    contact_person_id = fields.Many2one(
        comodel_name='hospital.contact.person',
    )
    doctor_id = fields.Many2one(
        comodel_name='hospital.doctor',
        string='Supervising doctor',
    )
    visit_ids = fields.One2many(
        comodel_name='hospital.visit',
        inverse_name='patient_id',
        string='Visits',
    )
    disease_ids = fields.Many2many(
        comodel_name='hospital.disease',
        string='Diseases',
    )
    doctor_change_ids = fields.One2many(
        comodel_name='hospital.doctor.change',
        inverse_name='patient_id',
        readonly=True,
    )
    diagnosis_ids = fields.One2many(
        comodel_name='hospital.diagnosis',
        inverse_name='patient_id',
        readonly=True,
    )

    # Compute methods
    @api.depends('birthday_date')
    def _compute_age(self):
        today = datetime.today()
        for record in self:
            birthday = record.birthday_date
            if birthday:
                current = (today.month, today.day) < (birthday.month, birthday.day)
                record.age = today.year - birthday.year - current
            else:
                record.age = None

    # CRUD methods
    @api.model
    def create(self, vals):
        res = super(HospitalPatient, self).create(vals)
        if vals.get('doctor_id'):
            doctor_change = {
                'set_time': datetime.now(),
                'doctor_id': vals['doctor_id'],
                'patient_id': res.id,
            }
            self.env['hospital.doctor.change'].create(doctor_change)
        return res

    def write(self, vals):
        for patient in self:
            if vals.get('doctor_id') and patient.doctor_id.id != vals['doctor_id']:
                doctor_change = {
                    'set_time': datetime.now(),
                    'doctor_id': vals['doctor_id'],
                    'patient_id': patient.id,
                }
                self.env['hospital.doctor.change'].create(doctor_change)
        return super(HospitalPatient, self).write(vals)

    # Action methods
    def action_open_visits(self):
        return {
            'name': _('Visits'),
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'res_model': 'hospital.visit',
            'target': 'current',
        }

    def action_open_analyses(self):
        return {
            'name': _('Analyses'),
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'res_model': 'hospital.patient.analysis',
            'target': 'current',
        }

    def action_open_diagnoses(self):
        return {
            'name': _('Diagnoses'),
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'res_model': 'hospital.diagnosis',
            'target': 'current',
        }

    def action_create_visit(self):
        patient_id = self.env.context.get('patient_id')
        return {
            'name': _('New Visit'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'visit.create.wizard',
            'target': 'new',
            'context': {'default_patient_id': patient_id}
        }
