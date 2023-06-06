from odoo import models,fields,api,_

class CompanyManager(models.Model):
    _name = 'company.manager'
    _description = 'Manager'
    _rec_name = 'name_manager'

    @api.depends('manager_id')
    def set_name_manager(self):
        for r in self:
            if r.manager_id:
                r.name_manager = r.manager_id.name
            else:
                return False

    name_manager = fields.Char(string = 'Name Manager',compute='set_name_manager')
    manager_id = fields.Many2one('hr.employee', 'Employee')
    contact = fields.Char(string= 'Email')

