from typing import Optional, Dict

from odoo import models, fields, _


class DoctorChangeMultiWizard(models.TransientModel):
    _name = 'doctor.change.multi.wizard'
    _description = 'Wizard to change supervising doctor for patients'

    patient_id = fields.Many2one(
        comodel_name='hospital.patient',
    )

    doctor_id = fields.Many2one(
        comodel_name='hospital.doctor',
        string='Supervising doctor',
    )

    # Action methods
    def action_open_wizard(self, reopen: bool = False) -> Dict:
        active_patient = None
        if self.env.context['active_ids'] and not reopen:
            active_patient = self.env.context['active_ids'][0]
        return {
            'name': _('Change Supervising Doctor Wizard'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'doctor.change.multi.wizard',
            'target': 'new',
            'context': {'default_patient_id': active_patient}
        }

    def action_change_doctor(self) -> Optional[Dict]:
        self.ensure_one()
        patient = self.env['hospital.patient'].browse(self.patient_id.id)
        patient.write({'doctor_id': self.doctor_id.id})
        if self.env.context.get('reopen'):
            return self.action_open_wizard(reopen=True)
