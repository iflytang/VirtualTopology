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
    The network has 6 switches.
    
          s6-cn
           |
          s5
         /   \
        s3---s4
        |     |
    mn1-s2    s1-mn2		
    '''
    def __init__(self, n = 6, **opts):
        super(Test, self).__init__(**opts)
        
        switchList = [self.addSwitch('s%d' % i, listenPort = (CONTROLLER_LISTEN_PORT + i)) for i in range(1,n+1)]
        lastSwitch = None
       # for switch in switchList:
        #    if lastSwitch:
         #       self.addLink(lastSwitch, switch)
          #  lastSwitch = switch
	cn=self.addHost('cn');
	mn1=self.addHost('mn1');
	mn2=self.addHost('mn2');
	    #self.addLink(cn,switchList[5]);
	    #self.addLink(mn1,switchList[1]);
	    #self.addLink(mn2,switchList[0]);
        #self.addLink(switchList[0], switchList[3])
        #self.addLink(switchList[1], switchList[2])
        #self.addLink(switchList[2], switchList[3])
        #self.addLink(switchList[2], switchList[4])
	    #self.addLink(switchList[4], switchList[3])
	    #self.addLink(switchList[4], switchList[5])
		
	self.addLink(mn1, switchList[1])
	self.addLink(switchList[1], switchList[2])
	self.addLink(switchList[4], switchList[3])
	self.addLink(switchList[2], switchList[4])
	self.addLink(switchList[2], switchList[3])
	self.addLink(mn2, switchList[0])
	self.addLink(switchList[0], switchList[3])
	self.addLink(switchList[4], switchList[5])
	self.addLink(cn, switchList[5])
		
        


        #for j in range(n):
         #   host = self.addHost('h%d' % (j+1))
          #  self.addLink(host, switchList[j])
if __name__ == '__main__':
    
    cleanup()
    
    topo6 = Test(6)          
    net = Mininet(topo=topo6, switch=POFSwitch)
    net.addController('c0', controller = RemoteController, ip='192.168.109.123', port=CONTROLLER_LISTEN_PORT)
    
    setLogLevel('info')
    net.start()
    net.staticArp()
    print "Dumping host connections ..."
    #dumpNodeConnections(net.hosts)
    dumpNodeConnections(net.switches)
    CLI(net)
    net.stop()





