# Copyright 2013-present Barefoot Networks, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import oftest.dataplane as dataplane
import oftest.pd_base_tests as pd_base_tests

from oftest.testutils import *

from utils import *

from p4_pd_rpc.ttypes import *
from res_pd_rpc.ttypes import *


class EchoTest(pd_base_tests.ThriftInterfaceDataPlane):
    def __init__(self):
        pd_base_tests.ThriftInterfaceDataPlane.__init__(self, "pass_through")

    def runTest(self):
        # Get connection handle for communicating with the target.
        sess_hdl = self.conn_mgr.client_init(16)
        # Get device handle for the target itself.
        dev_tgt = DevTarget_t(0, hex_to_i16(0xFFFF))

        # Clean all state in the target.
        self.client.clean_all(sess_hdl, dev_tgt)

        # Set a default action for the forward table.
        result = self.client.forward_set_default_action__drop(sess_hdl, dev_tgt)
        assert result == 0

        # Set a default action for the pass_through table.
        result = self.client.pass_through_set_default_action__no_op(sess_hdl, dev_tgt)
        assert result == 0

        # Add a new flow entry in the forward table i.e., send all packets with
        # destination MAC address '00:00:00:00:00:01' to port 1.
        mac1 = '00:00:00:00:00:01'
        self.client.forward_table_add_with_set_egr(sess_hdl, dev_tgt,
                                                   pass_through_forward_match_spec_t(macAddr_to_string(mac1)),
                                                   pass_through_set_egr_action_spec_t(1))
        # Create a simple packet to send through the target.
        pkt = simple_ip_packet(eth_dst='00:00:00:00:00:01')
        # Send the packet through the dataplane via its port 2.
        self.dataplane.send(2, str(pkt))
        # Verify if the packet is received from the dataplane on port 1.
        verify_packets(self, pkt, [1])

        # Add a new flow entry in the forward table i.e., send all packets with
        # destination MAC address '00:00:00:00:00:02' to port 2.
        mac2 = '00:00:00:00:00:02'
        self.client.forward_table_add_with_set_egr(sess_hdl, dev_tgt,
                                                   pass_through_forward_match_spec_t(macAddr_to_string(mac2)),
                                                   pass_through_set_egr_action_spec_t(2))

        # Create a simple packet to send through the target.
        pkt = simple_ip_packet(eth_dst='00:00:00:00:00:02')
        # Send the packet through the dataplane via its port 1.
        self.dataplane.send(1, str(pkt))
        # Verify if the packet is received from the dataplane on port 2.
        verify_packets(self, pkt, [2])
