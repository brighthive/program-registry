# -*- coding: utf-8 -*-

from flask import Blueprint
from flask_restful import Api

from .endpoints.provider import *
from .endpoints.program import *
from .endpoints.service import *
from .endpoints.location import *
from .endpoints.physical_address import *


api_blueprint = Blueprint('reg_api', __name__)
reg_api = Api(api_blueprint)

reg_api.add_resource(ProviderResource, '/providers',
                                        '/providers?name=<string:name>',
                                        '/providers/<int:organization_id>')

reg_api.add_resource(ProviderProgramResource, '/providers/<int:organization_id>/programs',
                                                '/providers/<int:organization_id>/programs?cip=<int:cip>',
                                                '/providers/<int:organization_id>/programs?name=<string:name>',
                                                '/providers/<int:organization_id>/programs/<int:program_id>')

reg_api.add_resource(ProviderServiceResource, '/providers/<int:organization_id>/services',
                                                '/providers/<int:organization_id>/services?status=<string:status>',
                                                '/providers/<int:organization_id>/services?name=<string:name>',
                                                '/providers/<int:organization_id>/services/<int:service_id>')

reg_api.add_resource(ProviderLocationResource, '/providers/<int:organization_id>/locations',
                                                '/providers/<int:organization_id>/locations?name=<string:name>',
                                                '/providers/<int:organization_id>/locations/<int:location_id>')

reg_api.add_resource(ProgramResource, '/programs',
                                        '/programs?cip=<int:cip>',
                                        '/programs?name=<string:name>',
                                        '/programs/<int:program_id>')

reg_api.add_resource(ProgramServiceResource, '/programs/<int:program_id>/services',
                                                '/programs/<int:program_id>/services?status=<string:status>',
                                                '/programs/<int:program_id>/services?name=<string:name>',
                                                '/programs/<int:program_id>/services/<int:service_id>')

reg_api.add_resource(ServiceResource, '/services', 
                                        '/services?status=<string:status>',
                                        '/services?name=<string:name>',
                                        '/services/<int:service_id>')
reg_api.add_resource(ServiceLocationResource, '/services/<int:service_id>/locations',
                                                '/services/<int:service_id>/locations?name=<string:name>',
                                                '/services/<int:service_id>/locations/<int:location_id>')
reg_api.add_resource(LocationResource, '/locations',
                                        '/locations?name=<string:name>',
                                        '/locations/<int:location_id>')
reg_api.add_resource(LocationPhysicalAddressResource, '/locations/<int:location_id>/address') # TODO: filter by city, state, postal_code
reg_api.add_resource(LocationServiceResource, '/locations/<int:location_id>/services',
                                        '/locations/<int:location_id>/services?status=<string:status>',
                                        '/locations/<int:location_id>/services?name=<string:name>',
                                        '/locations/<int:location_id>/services/<int:service_id>')


