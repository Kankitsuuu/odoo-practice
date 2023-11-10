from odoo import models, fields, api, _


class DoctorReportWizard(models.TransientModel):
    _name = 'doctor.report.wizard'
    _description = 'Wizard to print doctor report'

    doctor_id = fields.Many2one(
        comodel_name='hospital.doctor',
    )

    def action_open_wizard(self):
        print(self.env.context.get('active_ids'))
        doctor_id = None
        if self.env.context.get('active_ids'):
            doctor_id = self.env.context['active_ids'][0]
        return {
            'name': _('Doctor Report Wizard'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'doctor.report.wizard',
            'target': 'new',
            'context': {'default_doctor_id': doctor_id}
        }

    def action_get_report(self):
        patients = []
        for patient in self.doctor_id.patient_ids:
            patient_data = {
                'name': f'{patient.name} {patient.surname}',
                'phone': patient.phone,
                'email': patient.email,
                'age': patient.age,
            }
            diagnoses = []
            for diagnosis in patient.diagnosis_ids:
                diagnosis_data = {
                    'disease_name': diagnosis.disease_id.name,
                    'level': diagnosis.level,
                }
                diagnoses.append(diagnosis_data)
            patient_data['diagnoses'] = diagnoses
            patients.append(patient_data)

        doctor_activity = {}
        diagnoses = self.env['hospital.diagnosis'].search([
            ('doctor_id', '=', self.doctor_id.id)
        ])
        for diagnosis in diagnoses:
            year = diagnosis.set_date.year
            month = self.integer_as_month_name(diagnosis.set_date.month)
            if doctor_activity.get(year):
                if doctor_activity[year].get(month):
                    doctor_activity[year][month] += 1
                else:
                    doctor_activity[year][month] = 1
            else:
                doctor_activity[year] = {
                    month: 1,
                }
        data = {
            'doctor_name': f'{self.doctor_id.name} {self.doctor_id.surname}',
            'doctor_specialty': self.doctor_id.specialty_id.name,
            'doctor_patients': patients,
            'doctor_activity': doctor_activity,
        }
        # use `module_name.report_id` as reference
        return self.env.ref('hr_hospital.doctor_report_id').report_action(self, data=data)

    # Custom methods
    @api.model
    def integer_as_month_name(self, value: int) -> str:
        months = {
            1: 'January',
            2: 'February',
            3: 'March',
            4: 'April',
            5: 'May',
            6: 'June',
            7: 'July',
            8: 'August',
            9: 'September',
            10: 'October',
            11: 'November',
            12: 'December'
        }
        return months[value] if months.get(value) else 'Wrong month value'
