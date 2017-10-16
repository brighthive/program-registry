from flask import Blueprint, make_response, request, jsonify
from flask.views import MethodView

from app.models import Organization


org_blueprint = Blueprint('organization', __name__)


class OrganizationView(MethodView):
    """This class-based handles api requests for the organization resource."""

    def post(self):
        """
        Create an organization and return the json response containing it
        """
        try:
            # Create the organization
            payload = request.data.to_dict()
            organization = Organization(**payload)
            organization.save()
            response = {
                'id': organization.id,
                'name': organization.name,
                'description': organization.description
            }
            if organization.email:
                response['email'] = organization.email
            if organization.url:
                response['url'] = organization.url
            if organization.year_incorporated:
                response['year_incorporated'] = organization.year_incorporated

            return make_response(jsonify(response)), 201
        except Exception as e:
            response = {
                "message": str(e)
            }
            return make_response(jsonify(response)), 500

    def get(self, organization_id):
        """
        Return an organization given it's id or all organizations given no
        query params
        """
        if organization_id is None:
            # Expose a list of organizations
            organizations = Organization.get_all()
            response = []

            for org in organizations:
                single_org = {
                    'id': org.id,
                    'name': org.name,
                    'description': org.description,
                }
                response.append(single_org)

            return make_response(jsonify(response)), 200

        else:
            # Expose a single organization
            try:
                organization = Organization.query.filter_by(id=organization_id).first()
                response = {
                    'id': organization.id,
                    'name': organization.name,
                    'description': organization.description,
                }

            except Exception as e:
                response = {
                    "message": str(e)
                }
                return make_response(jsonify(response)), 400

            return make_response(jsonify(response)), 200

    def put(self, organization_id):
        """Update an organization given its id."""
        if organization_id is not None:
            try:
                response = {}
                org = Organization.query.filter_by(id=organization_id).first()
                response['id'] = org.id

                if  'name' in request.form:
                    org.name = request.form.get('name')
                    response['name'] = org.name
                if 'email' in request.form:
                    org.name = request.form.get('email')
                    response['email'] = org.email
                if 'description' in request.form:
                    org.description = request.form.get('description')
                    response['description'] = org.description
                if 'url' in request.form:
                    org.url = request.form.get('url')
                    response['url'] = org.url
                if 'year_incorporated' in request.form:
                    org.year_incorporated = request.form.get('year_incorporated')
                    response['year_incorporated'] = org.year_incorporated
                org.save()

            except Exception as e:
                response = {
                    "message": str(e)
                }
                return make_response(jsonify(response)), 400

    def delete(self, organization_id):
        """Delete an organization given its id."""
        if organization_id is not None:
            # fetch org to delete
            try:
                org = Organization.query.filter_by(id=organization_id).first()
                org.delete()
                response = {
                    "message": "Organization successfully deleted."""
                }
                return make_response(jsonify(response)), 200

            except Exception as e:
                # the org does not exist?
                response = {
                    "message": str(e)
                }
                return make_response(jsonify(response)), 400


organization_view = OrganizationView.as_view('organization_view')
org_blueprint.add_url_rule(
    '/api/organizations/', defaults={'organization_id': None},
    view_func=organization_view, methods=['GET'])

org_blueprint.add_url_rule(
    '/api/organizations/<int:organization_id>',
    view_func=organization_view,
    methods=['GET', 'PUT', 'DELETE'])

org_blueprint.add_url_rule(
    '/api/organizations/', view_func=organization_view,
    methods=['POST',])



