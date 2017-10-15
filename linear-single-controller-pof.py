#!/usr/bin/python
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.cli import CLI
from mininet.clean import cleanup
from mininet.node import RemoteController
from mininet.pof import POFSwitch

CONTROLLER_LISTEN_PORT = 6643
class linear(Topo):
    '''
    h1-s1-s2-s3-h2
    '''
    def __init__(self, n = 3, **opts):
        super(linear, self).__init__(**opts)

        # add switches
        switchList = [self.addSwitch('s%d' % i, listenPort = (CONTROLLER_LISTEN_PORT + i)) for i in range(1,n+1)]

        # add hosts
        h1 = self.addHost('h1')
        h2 = self.addHost('h2')

        # add links for switches and hosts
        self.addLink(h1, switchList[0])            # h1-s1
        self.addLink(switchList[0],switchList[1])  # s1-s2
        self.addLink(switchList[1],switchList[2])  # s2-s3
        self.addLink(switchList[2], h2)            # s3-h2
       
if __name__ == '__main__':

    cleanup()

    linear_topo = linear(3)
    net = Mininet(topo=linear_topo, switch=POFSwitch)
    net.addController('c0', controller = RemoteController, ip='192.168.109.123', port=CONTROLLER_LISTEN_PORT)

    setLogLevel('info')
    net.start()
    net.staticArp()
    print "Dumping host connections ..."
    dumpNodeConnections(net.hosts)
    dumpNodeConnections(net.switches)
    CLI(net)
    net.stop()

