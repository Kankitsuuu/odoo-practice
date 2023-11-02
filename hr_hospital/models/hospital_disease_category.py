from odoo import models, fields


class HospitalDiseaseCategory(models.Model):
    _name = 'hospital.disease.category'
    _description = 'Hospital Disease Categories'

    name = fields.Char(
        required=True,
    )
