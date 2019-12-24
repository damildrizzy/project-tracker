from flask import request, jsonify, make_response
from app.main.schema import (project_schema, projects_schema, 
                            create_project_schema, tickets_schema,
                            ticket_schema, comment_schema,
                            comments_schema)
from flask_restful import Resource
from app.models import User, Project, Ticket, Comment
from app.decorators import admin_required
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    set_access_cookies,
    unset_jwt_cookies,
    get_jwt_identity
)
from app import db



class ProjectsView(Resource):
    @admin_required
    def get(self):
        projects = Project.query.all()
        response = {
            'data':projects_schema.dump(projects)
        }
        return response, 200
    
    @admin_required
    def post(self):
        json_data = request.get_json()

        if not json_data:
            response = jsonify({
                'error': 'Invalid Input'
            })
            response.status_code = 400
            return response
        
        data = create_project_schema.load(json_data)

        project = Project()
        project.name = data['name']
        current_user = get_jwt_identity()
        #manager = User.query.filter_by(email = current_user).first()
        project.manager = current_user
        project.description = data['description']

        db.session.add(project)
        db.session.commit()

        return make_response(jsonify(data), 200)


class ProjectView(Resource):
    def get(self, id):
        project = Project.query.get_or_404(id)
        response = {
            'data': project_schema.dump(project)
        }
        return response
    



    @admin_required
    def put(self, id):
        json_data = request.get_json(data)
        if not json:
            response = jsonify({
                'error': 'Invalid Input'
            })
            response.status_code = 400
            return response

        project = Project.query.get_or_404(id)
        project.name = request.data('name')
        project.description = request.data('description')
        db.session.commit()

        response = jsonify({
            'data': project_schema.dump(project).data
        })
        response.status_code = 200
        return response
    

    @admin_required
    def delete(self, id):
        project = Project.query.get_or_404(id)

        if not project:
            response = {
                'error': 'No such project was found'
            }
            return jsonify(response), 404
        
        db.session.delete(projet)
        db.session.commit()

        response = {
            'data': project_schema.dump(project).data
        }
        return jsonify(response), 200

#All tickets (admin only)
class TicketsView(Resource):
    @admin_required
    def get(self):
        tickets = Ticket.query.all()
        response = {
            'data': tickets_schema.dump(tickets)
        }
        return response, 200

    
#tickets by project
class TicketView(Resource):
    #All tickets that belong to a project

    def get(self, id):
        tickets = Ticket.query.filter_by(project_id = id)
        response = {
            'data': tickets_schema.dump(tickets)
        }
        return response, 200
        
    #retriving a ticket
    def get(self, id, tid):
        ticket = Ticket.query.get_or_404(tid)
        response = {
            'data': ticket_schema.dump(ticket)
        }
        return response, 200
        
    @jwt_required
    def post(self, id):
        json_data = request.get_json()
        if not json_data:
            response = jsonify({
                'error': 'Invalid Input'
            })
            response.status_code = 400
            return response
        
        #deserialising json_data
        data = ticket_schema.load(json_data)

        project = Project.query.get_or_404(id)
        if not project:
            response = {
                'error': 'Project not found'
            }
            return resoponse, 400
        
        ticket = Ticket()
        ticket.project_id = project.id
        ticket.subject = data['subject']
        ticket.description = data['description']
        ticket.priority = data['priority']

        db.session.add(ticket)
        db.session.commit()

        return make_response(jsonify(data), 200)


class CommentView(Resource):
    #All comments under a ticket
    def get(self, id, tid):
        comments = Comment.query.filter_by(ticket_id = tid)
        response = {
            'data': comments_schema.dump(comments)
        }
        return response, 200

    @jwt_required
    def post(self, id, tid):
        json_data = request.get_json()

        if not json_data:
            return {
                'error': 'Invalid Input'
            }, 400
        
        #deserialising
        data = comment_schema.load(json_data)

        ticket = Ticket.query.get_or_404(tid)

        if not ticket:
            return {
                'error': 'Ticket not found'
            }, 400
        
        comment = Comment()
        comment.text = data['text']
        comment.ticket_id = ticket.id
        
        db.session.add(comment)
        db.session.commit()

        return make_response(jsonify(data), 200)








