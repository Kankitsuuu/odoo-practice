from odoo import models, fields


class HospitalPerson(models.AbstractModel):
    _name = 'hospital.person'
    _description = 'Hospital Person'

    name = fields.Char(
        required=True,
    )
    surname = fields.Char(
        required=True,
    )
    phone = fields.Char()
    address = fields.Char()
    email = fields.Char()
    gender = fields.Selection(
        selection=[('male', 'Male'),
                   ('female', 'Female'),
                   ('other', 'Other')],
        required=True,
    )
    photo = fields.Image(
        max_width=300,
        max_height=400,
    )

    # Default methods
    def name_get(self) -> list:
        return [(rec.id, f'{rec.name} {rec.surname}') for rec in self]
