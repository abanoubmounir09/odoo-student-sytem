
from odoo import fields,models


class ItiTrack(models.Model):
    _name="iti.track"

    name=fields.Char()
    is_open=fields.Boolean()
    capacity=fields.Integer()

    student_ids=fields.One2many("iti.student","track_id")
