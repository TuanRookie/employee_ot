from odoo import models,fields,api,_

class CompanyEmployee(models.Model):
    _name = 'company.employee'
    _description = 'Employee'
    _rec_name = 'name_employee'

    @api.depends('employee_id')
    def set_name_employee(self):
        for r in self:
            if r.employee_id:
                r.name_employee = r.employee_id.name
            else:
                return False

    def action_confirm(self):
        for r in self:
            r.state = 'confirm'

    def action_done(self):
        for r in self:
            r.state = 'done'

    @api.depends('schedule_ids.time_ot')
    def compute_ot_hour(self):
        for r in self:
            r.ot_hour = sum(r.schedule_ids.mapped('time_ot'))

    def action_send_card(self):
        template_id = self.env.ref('employee.employee_card_email_template').id
        template = self.env['mail.template'].browse(template_id)
        template.send_mail(self.id, force_send=True)

    name_employee = fields.Char(string='Name' , compute='set_name_employee')
    employee_id = fields.Many2one('hr.employee', 'Employee')
    manager_id = fields.Many2one('company.manager',string= 'Manager')
    total_ot = fields.Float(string='Total OT')
    ot_hour = fields.Float(string = 'OT hours',compute='compute_ot_hour')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirm', 'Confirm'),
        ('done', 'Done'),
        ('cancel', 'Cancelled'),
    ], string='Status', readonly=True, default='draft')


