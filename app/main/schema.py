from marshmallow import validate, fields, ValidationError
from app import marshmallow
from app.models import Project, Ticket, Comment



class TicketSchema(marshmallow.Schema):
    class Meta:
        model = Ticket
        fields = ('id', 'project_id', 'subject', 'description', 'priority', 'status', 
                    'created_by', 'created_at', 'updated_at' 'user_id' )



class ProjectSchema(marshmallow.Schema):
    class Meta:
        model = Project
        fields = ('id', 'name', 'manager', 'description', 'tickets')
    tickets = marshmallow.Nested(TicketSchema, many=True)


class CreateProjectSchema(marshmallow.Schema):
    name = fields.Str(required=True, validate=[validate.Length(min=1, max=100)])
    description = fields.Str(required=True, validate=[validate.Length(min=1, max=10000)])


class CommentSchema(marshmallow.Schema):
    class Meta:
        model = Comment
        fields = ('id', 'text', 'user_id', 'ticket_id', 'author', 'created_at', 'updated_at', 'depth')

comment_schema = CommentSchema()
comments_schema = CommentSchema(many=True)
ticket_schema = TicketSchema()
tickets_schema = TicketSchema(many=True)
projects_schema = ProjectSchema(many=True)
project_schema = ProjectSchema()
create_project_schema = CreateProjectSchema()
