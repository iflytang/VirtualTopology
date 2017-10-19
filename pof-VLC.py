#!/usr/bin/python

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.cli import CLI
from mininet.clean import cleanup
from mininet.node import RemoteController
from mininet.pof import POFSwitch
from mininet.topolib import TreeTopo

CONTROLLER_LISTEN_PORT = 6643

class Test(Topo):
    '''

    The network has 3 swithes, 2 hosts and 1 controller.
    This topology is used for testing pof-VLC.
          cn
          |
         sw3
         /  \
      sw2   sw1(AP)
   (wire)\   /(wireless)
          mn
    '''

    def __init__(self, n = 3, **opts):
        super(Test, self).__init__(**opts)

        # add switches
        sw1 = self.addSwitch('s1', listenPort = CONTROLLER_LISTEN_PORT + 1)
        sw2 = self.addSwitch('s2', listenPort = CONTROLLER_LISTEN_PORT + 2)
        sw3 = self.addSwitch('s3', listenPort = CONTROLLER_LISTEN_PORT + 3)

        # add hosts
        cn = self.addHost('cn')
        mn = self.addHost('mn')

        # add links
        self.addLink(sw3, sw2) # sw3-port1 == sw2-port1
        self.addLink(sw3, sw1) # sw3-port2 == sw1-port1
        self.addLink(sw3, cn)  # sw3-port3 == cn
        self.addLink(sw2, mn)  # sw2-port2 == mn
        self.addLink(sw1, mn)  # sw1-port2 == mn

if __name__ == '__main__':
    cleanup()
    topo6 = Test(3)
    net = Mininet(topo=topo6, switch=POFSwitch)
    net.addController('c0', controller = RemoteController, ip='192.168.109.111', port=CONTROLLER_LISTEN_PORT)
    setLogLevel('info')

    net.start()
    net.staticArp()
    print "Dumping host connections ..."

    dumpNodeConnections(net.hosts)
    dumpNodeConnections(net.switches)
    CLI(net)
    net.stop()
