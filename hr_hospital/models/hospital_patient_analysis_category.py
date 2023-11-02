from odoo import models, fields


class HospitalPatientAnalysisCategory(models.Model):
    _name = 'hospital.patient.analysis.category'
    _description = 'Hospital Patient Analysis Categories'

    name = fields.Char(
        required=True,
    )
