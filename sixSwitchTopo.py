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
class sixNodeTopo(Topo):
    '''
    The network has 6 switches.
    
         h2   h3     
         |     |
         s2---s3
        /|     |\
    h1-s1|     | s4-h4  
        \|     |/
         s6---s5
         |     |
         h6   h5
    '''
    def __init__(self, n = 6, **opts):
        super(sixNodeTopo, self).__init__(**opts)
        
        switchList = [self.addSwitch('s%d' % i, listenPort = (CONTROLLER_LISTEN_PORT + i)) for i in range(1,n+1)]
        lastSwitch = None
        for switch in switchList:
            if lastSwitch:
                self.addLink(lastSwitch, switch)
            lastSwitch = switch
        self.addLink(switchList[0], switchList[5])
        self.addLink(switchList[1], switchList[5])
        self.addLink(switchList[2], switchList[4])
        
        for j in range(n):
            host = self.addHost('h%d' % (j+1))
            self.addLink(host, switchList[j])
if __name__ == '__main__':
    
    cleanup()
    
    topo6 = sixNodeTopo(6)          
    net = Mininet(topo=topo6, switch=POFSwitch)
    net.addController('c0', controller = RemoteController, ip='192.168.109.115', port=CONTROLLER_LISTEN_PORT)
    
    setLogLevel('info')
    net.start()
    net.staticArp()
    print "Dumping host connections ..."
    dumpNodeConnections(net.hosts)
    dumpNodeConnections(net.switches)
    CLI(net)
    net.stop()





