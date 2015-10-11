#!/usr/bin/python3
# Copyright (c) 2015 Davide Gessa
# Distributed under the MIT software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.

# Helloworld example
import sys
import config
from libcontractvm import Wallet, WalletChainSo, WalletNode, ConsensusManager
from cotst import ContractManager, ContractException


if __name__ == "__main__" and len (sys.argv) == 2:
    player = sys.argv[1].lower ()
    consensusManager = ConsensusManager.ConsensusManager ('XLT')
    consensusManager.addNode ('http://localhost:8181')

    cm = ContractManager.ContractManager (consensusManager,
            wallet=WalletNode.WalletNode (chain='XLT', url=config.WALLET_NODE_URL, wallet_file='data/test_xltnode_'+player[0]+'.wallet'))
    
    print (player, 'Chain:', cm.getChainCode ())
    print (player, 'Address:', cm.getWallet ().getAddress ())
    print (player, 'Network time:', cm.getTime ())
    print (player, 'Balance:', cm.getWallet ().getBalance (), cm.getChainCode ())
    print (player, 'Time:', cm.getTime ())


    if player == 'alice':
        cm.tell (cm.translate ('!greet{;t}.?planet{t<7}'))
    else:
        cm.tell (cm.translate ('?greet{;t}.!planet{t<7}'))

    cm.waitUntilTelled ()
    print ('Told:', cm.getHash ())

    cm.waitUntilSessionStart ()

    if player == 'alice':
        cm.send ('greet', 'hello')
        cm.waitUntilReceive ()
        print ('hello', cm.receive ()['planet'])
    else:
        cm.waitUntilReceive ()
        cm.receive ()
        cm.send ('planet', 'world')

elif __name__ == "__main__":
    print ('usage: python3',sys.argv[0],'[alice|bob]')
