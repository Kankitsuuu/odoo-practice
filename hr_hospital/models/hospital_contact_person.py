from odoo import models, fields


class HospitalContactPerson(models.Model):
    _name = 'hospital.contact.person'
    _description = 'Hospital Contact Person'
    _inherit = 'hospital.person'

    patient_ids = fields.One2many(
        comodel_name='hospital.patient',
        inverse_name='contact_person_id',
        string='Patients',
        readonly=True,
    )
