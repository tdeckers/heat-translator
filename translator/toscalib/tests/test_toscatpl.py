# vim: tabstop=4 shiftwidth=4 softtabstop=4

#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import os
from translator.toscalib.tests.base import TestCase
from translator.toscalib.tosca_template import ToscaTemplate


class ToscaTemplateTest(TestCase):

    '''TOSCA template.'''
    tosca_tpl = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "data/tosca_single_instance_wordpress.yaml")
    tosca = ToscaTemplate(tosca_tpl)

    def test_version(self):
        self.assertEqual(self.tosca.version, "tosca_simple_1.0")

    def test_description(self):
        expected_description = "TOSCA simple profile with wordpress, " \
                               "web server and mysql on the same server."
        self.assertEqual(self.tosca.description, expected_description)

    def test_inputs(self):
        self.assertEqual(
            ['cpus', 'db_name', 'db_port',
             'db_pwd', 'db_root_pwd', 'db_user'],
            sorted([input.name for input in self.tosca.inputs]))

        input_name = "db_port"
        expected_description = "Port for the MySQL database."
        for input in self.tosca.inputs:
            if input.name == input_name:
                self.assertEqual(input.description, expected_description)

    def test_node_tpls(self):
        '''Test nodetemplate names.'''
        self.assertEqual(
            ['mysql_database', 'mysql_dbms', 'server',
             'webserver', 'wordpress'],
            sorted([tpl.name for tpl in self.tosca.nodetemplates]))

        tpl_name = "mysql_database"
        expected_type = "tosca.nodes.Database"
        expected_properties = ['db_name', 'db_password', 'db_user']
        expected_capabilities = ['database_endpoint']
        expected_requirements = [{'host': 'mysql_dbms'}]
        expected_relationshp = ['tosca.relationships.HostedOn']
        expected_host = ['mysql_dbms']
        expected_interface = ['tosca.interfaces.node.Lifecycle']

        for tpl in self.tosca.nodetemplates:
            if tpl_name == tpl.name:
                '''Test node type.'''
                self.assertEqual(tpl.type, expected_type)

                '''Test properties.'''
                self.assertEqual(
                    expected_properties,
                    sorted([p.name for p in tpl.properties]))

                '''Test capabilities.'''
                self.assertEqual(
                    expected_capabilities,
                    sorted([p.name for p in tpl.tpl_capabilities]))

                '''Test requirements.'''
                self.assertEqual(
                    expected_requirements, tpl.tpl_requirements)

                '''Test relationship.'''
                self.assertEqual(
                    expected_relationshp,
                    [x.type for x in tpl.tpl_relationship.keys()])
                self.assertEqual(
                    expected_host,
                    [y.name for y in tpl.tpl_relationship.values()])

                '''Test interfaces.'''
                self.assertEqual(
                    expected_interface,
                    [x.type for x in tpl.tpl_interfaces])

    def test_outputs(self):
        self.assertEqual(
            ['website_url'],
            sorted([output.name for output in self.tosca.outputs]))