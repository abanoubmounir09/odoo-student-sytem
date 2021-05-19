
from odoo import models,fields,api
from odoo.exceptions import UserError

class ItiStudent(models.Model):
    _name="iti.student"

    name=fields.Char(required=True)
    email =fields.Char()
    birth_date=fields.Date()
    salary=fields.Float()
    tax = fields.Float(compute="calc_tax",store=True)
    address=fields.Text()
    gender=fields.Selection(
        [('m','male'),('f','female')]
    )
    accepted=fields.Boolean()
    level=fields.Integer()
    image=fields.Binary()
    cv=fields.Html()
    login_time=fields.Datetime()
    state = fields.Selection(
        [
            ('applied','applied'),
            ('first', 'first interview'),
            ('second', 'second interview'),
            ('passed', 'passed'),
            ('rejected', 'rejected'),
        ],default='applied'
    )


    # relations
    track_id=fields.Many2one("iti.track")
    # related just on relation many-> 2 -> one
    track_capacity = fields.Integer(related="track_id.capacity")
    skills_ids=fields.Many2many("iti.skill")
    grads_ids=fields.One2many("student.course.line","student_id")

    @api.depends('salary')
    def calc_tax(self):
        for student in self:
            student.tax = student.salary * 0.20

    @api.constrains("salary")
    def check_salary(self):
        if self.salary > 13000:
            raise UserError("salary can't be more 13000")

    @api.model
    def create(self,vals):
        name_split = vals['name'].split()
        vals['email'] = f"{name_split[0][0]}{name_split[1]}@gmail.com"
        # print(new_student.email)

        track = self.env['iti.track'].browse(vals['track_id'])
        if track.is_open is False:
            raise UserError("this track is closed")
        return super().create(vals)

    # @api.multi remove from odoo 13(update function)
    def write(self,vals):
        print(vals)
        if "name" in vals:
            name_split=vals['name'].split()
            vals['email'] = f"{name_split[0][0]}{name_split[1]}@gmail.com"
        super().write(vals)

    def unlink(self):
        for record in self:
            if record.state  in ['passed','rejected']:
                raise UserError("you can't delete this student")
        super().unlink()



    def change_state(self):
        if  self.state == 'applied':
            self.state = 'first'
        elif self.state == 'first':
            self.state = 'second'
        elif self.state in ['passed','rejected']:
            self.state = 'applied'

    def set_pass(self):
        self.state='passed'

    def set_reject(self):
        self.state='rejected'



    @api.onchange('gender')
    def _onchabge_gender(self):
        domain={'track_id':[]}
        if self.gender == 'f':
            self.salary = 8000

        else:
            self.salary = 13000
            domain = {'track_id': [('is_open', '=', 'True')]}

        return{
            'warning':{
            'title':'Hello',
            'message':"you changed gender and salary changed also"
             },
            'domain':domain
        }


class ItiCourse(models.Model):
    _name="iti.course"
    name=fields.Char()

class StudentCourseGrades(models.Model):
    _name="student.course.line"

    student_id = fields.Many2one("iti.student")
    course_id = fields.Many2one("iti.course")
    grades = fields.Selection(
        [('g', 'Good'), ('vg', 'Very Good')]
    )


