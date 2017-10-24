from flask import Blueprint, make_response, request, jsonify, abort
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
            response = organization.serialize()
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
                response.append(org.serialize())

            return make_response(jsonify(response)), 200

        else:
            # Expose a single organization
            organization = Organization.query.filter_by(id=organization_id).first()
            if not organization:
                abort(404)
            else:
                try:
                    response = organization.serialize()
                    return make_response(jsonify(response)), 200
                except Exception as e:
                    response = {
                        "message": str(e)
                    }
                    return make_response(jsonify(response)), 400


    def put(self, organization_id):
        """Update an organization given its id."""
        if organization_id is not None:
            try:
                response = {}
                org = Organization.query.filter_by(id=organization_id).first()
                # return a 404 if org does not exist
                abort(404) if org is None else org

                for key in request.data.to_dict().keys():
                    setattr(org, key, request.data.get(key))
                org.save()
                response = org.serialize()

                return make_response(jsonify(response)), 200

            except Exception as e:
                response = {
                    "message": str(e)
                }
                print(str(e))
                return make_response(jsonify(response)), 400

    def delete(self, organization_id):
        """Delete an organization given its id."""
        if organization_id is not None:
            # fetch org to delete
            try:
                org = Organization.query.filter_by(id=organization_id).first()
                # return 404 if org does not exist
                abort(404) if org is None else org

                org.delete()
                response = {
                    "message": "Organization successfully deleted."""
                }
                return make_response(jsonify(response)), 202

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



