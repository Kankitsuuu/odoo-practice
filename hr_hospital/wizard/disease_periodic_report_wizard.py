from typing import Optional, NoReturn
from odoo import models, fields, _
from datetime import datetime
from odoo.exceptions import UserError


class DiseasePeriodicReportWizard(models.TransientModel):
    _name = 'disease.periodic.report.wizard'
    _description = 'Wizard to get monthly disease report'

    start_date = fields.Date(
        string='From',
        required=True,
        default=fields.Date.today,
    )
    end_date = fields.Date(
        string='To',
        required=True,
        default=fields.Date.today,
    )
    disease_ids = fields.Many2many(
        comodel_name='hospital.disease',
        string='Diseases',
        required=True,
    )

    # Action methods
    def action_open_wizard(self) -> dict:
        return {
            'name': _('Disease Periodic Report Wizard'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'disease.periodic.report.wizard',
            'target': 'new',
            'context': {'default_disease_ids': self.env.context.get('active_ids')}
        }

    def action_get_report(self) -> dict:
        """Call when button 'Get Report' clicked."""
        self.validate_data()
        data = {
            'form': {
                'start_date': self.start_date,
                'end_date': self.end_date,
                'diseases': dict()
            }
        }
        for disease in self.disease_ids:
            diagnoses_count = self.env['hospital.diagnosis'].search_count([
                            ('disease_id', '=', disease.id),
                            ('date', '>=', self.start_date),
                            ('date', '<=', self.end_date)
                        ])
            print(diagnoses_count)
            data['form']['diseases'][disease.name] = diagnoses_count

        # use `module_name.report_id` as reference
        return self.env.ref('hr_hospital.disease_report_id').report_action(self, data=data)

    # Custom methods
    def validate_data(self) -> Optional[NoReturn]:
        """Validate data from wizard"""
        if not self.disease_ids:
            raise UserError(_('You should choose at least one disease.'))
        elif not self.start_date < self.end_date <= datetime.today().date():
            raise UserError(_('Wrong date value.'))
