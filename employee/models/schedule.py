from odoo import models,fields,api,_
from pytz import timezone

class CompanySchedule(models.Model):
    _name = 'company.schedule'
    _description = 'Schedule'

    def convert_to_local_time(self, start_time):
        tz_utc = timezone('UTC')
        tz_destination = timezone('Asia/Ho_Chi_Minh')
        localized_dt = start_time.replace(tzinfo=tz_utc).astimezone(tz_destination)
        return localized_dt


    @api.depends('start_time','end_time')
    def set_ot_category(self):
        for r in self:
            if r.start_time and r.end_time:
                start = float((self.convert_to_local_time(r.start_time)).hour)
                end = float((self.convert_to_local_time(r.end_time)).hour)
                if start <= 7:
                    r.ot_category = 'Tăng ca - ban ngày'
                elif end >= 20:
                    r.ot_category = 'Tăng ca - buổi tối'
                elif start >=7 and end <= 20:
                    r.ot_category = 'Làm việc bình thường'
                else:
                    r.ot_category = 'Không xác định'
            else:
                return False

    def set_ot_category_inverse(self):
        for r in self:
            r.start_time = r.start_time
            r.end_time = r.end_time

    @api.depends('start_time', 'end_time')
    def set_time_ot(self):
        for r in self:
            if r.start_time and r.end_time:
                start = float((self.convert_to_local_time(r.start_time)).hour) + float((self.convert_to_local_time(r.start_time)).minute/60.0)
                end = float((self.convert_to_local_time(r.end_time)).hour) + float((self.convert_to_local_time(r.end_time)).minute/60.0)
                print(start,end)
                if start <= 7 and end >= 7:
                    r.time_ot = float(7-start)
                elif start <=7 and end<=7:
                    r.time_ot = float(end-start)
                elif end >= 20 and start <= 20:
                    r.time_ot = float(end-20)
                elif end >= 20 and start >= 20:
                    r.time_ot = float(end-start)
                else:
                    r.time_ot = float(0)
            else:
                return False

    start_time = fields.Datetime(string = 'From')
    end_time = fields.Datetime(string='To')
    ot_category = fields.Char(string='OT Category',compute='set_ot_category',inverse='set_ot_category_inverse')
    time_ot = fields.Float(string='Time OT', compute='set_time_ot')
    employee_id = fields.Many2one('company.employee')

class CompanyEmployee(models.Model):
    _inherit = 'company.employee'

    schedule_ids = fields.One2many('company.schedule','employee_id')