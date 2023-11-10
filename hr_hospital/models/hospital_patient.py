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
    visit_total = fields.Integer(
        string='Visit count',
        compute='_compute_visit_total',
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
    diagnosis_total = fields.Integer(
        string='Diagnosis count',
        compute='_compute_diagnosis_total',
    )
    analysis_ids = fields.One2many(
        string='Analyses',
        comodel_name='hospital.patient.analysis',
        inverse_name='patient_id',
    )
    analysis_total = fields.Integer(
        string='Analysis count',
        compute='_compute_analysis_total',
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

    @api.depends('visit_ids')
    def _compute_visit_total(self):
        for patient in self:
            patient.visit_total = len(patient.visit_ids)

    @api.depends('diagnosis_ids')
    def _compute_diagnosis_total(self):
        for patient in self:
            patient.diagnosis_total = len(patient.diagnosis_ids)

    @api.depends('analysis_ids')
    def _compute_analysis_total(self):
        for patient in self:
            patient.analysis_total = len(patient.analysis_ids)

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
        self.ensure_one()
        return {
            'name': _('Visits'),
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'res_model': 'hospital.visit',
            'domain': [('id', 'in', self.visit_ids.ids)],
            'target': 'current',
        }

    def action_open_analyses(self):
        self.ensure_one()
        return {
            'name': _('Analyses'),
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'res_model': 'hospital.patient.analysis',
            'domain': [('id', 'in', self.analysis_ids.ids)],
            'target': 'current',
        }

    def action_open_diagnoses(self):
        self.ensure_one()
        print(self.diagnosis_ids.ids)
        return {
            'name': _('Diagnoses'),
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'res_model': 'hospital.diagnosis',
            'domain': [('id', 'in', self.diagnosis_ids.ids)],
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
