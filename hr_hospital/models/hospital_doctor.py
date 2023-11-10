from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


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
    patient_total = fields.Integer(
        string='Patient count',
        compute='_compute_patient_total',
    )
    visit_ids = fields.One2many(
        comodel_name='hospital.visit',
        inverse_name='doctor_id',
        string='Visits',
    )
    visit_total = fields.Integer(
        string='Visit count',
        compute='_compute_visit_total'
    )

    # Compute methods
    @api.depends('patient_ids')
    def _compute_patient_total(self):
        for doctor in self:
            doctor.patient_total = len(doctor.patient_ids)

    @api.depends('visit_ids')
    def _compute_visit_total(self):
        for doctor in self:
            doctor.visit_total = len(doctor.visit_ids)

    # Constraints
    @api.constrains('mentor_id')
    def check_mentor_id(self):
        for doctor in self:
            mentor = doctor.mentor_id
            if mentor.id == doctor.id:
                raise ValidationError(_('You cannot choose yourself as mentor.'))
            elif mentor.mentor_id:
                raise ValidationError(_('You cannot choose intern as mentor.'))

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

    # Action methods
    def action_open_patients(self):
        self.ensure_one()
        return {
            'name': _('Patients'),
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'res_model': 'hospital.patient',
            'domain': [('id', 'in', self.patient_ids.ids)],
            'target': 'current',
        }

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
