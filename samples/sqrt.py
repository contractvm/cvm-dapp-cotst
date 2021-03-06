#!/usr/bin/python3
# Copyright (c) 2015 Davide Gessa
# Distributed under the MIT software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.

# SQRT example
import config
import os
import sys
import time
import math
import subprocess
from libcontractvm import Wallet, WalletExplorer, ConsensusManager
from cotst import ContractManager, ContractException
import cvmutils


if __name__ == "__main__" and len (sys.argv) == 2:
	player = sys.argv[1].lower ()

	if player == 'spawn':
		cvmutils.spawn (3)
		while True:
			time.sleep (5)
		sys.exit ()
        
	consensusManager = ConsensusManager.ConsensusManager ()

	for x in range (3):
		consensusManager.addNode ('http://localhost:' + str (2818 + x))

	if player == 'worker':
		wallet = WalletExplorer.WalletExplorer (wallet_file='testa.wallet')

	else:
		wallet = WalletExplorer.WalletExplorer (wallet_file='testb.wallet')

	cm = ContractManager.ContractManager (consensusManager, wallet=wallet)
    
	print (player, 'Chain:', cm.getChainCode ())
	print (player, 'Address:', cm.getWallet ().getAddress ())
	print (player, 'Network time:', cm.getTime ())
	print (player, 'Balance:', cm.getWallet ().getBalance (), cm.getChainCode ())
	print (player, 'Time:', cm.getTime ())


	if player == 'worker':
		cm.tell (cm.translate ('?x.?eps{;t}.!y{t<5}.(?ok & ?no{;t}.!culpable{t<5})'))
	else:
		cm.tell (cm.translate ('!x.!eps{;t}.?y{t<5}.(!ok + !no{;t}.?culpable{t<5})'))

	cm.waitUntilTelled ()
	print ('Telled:', cm.getHash ())

	cm.waitUntilSessionStart ()
	
	if player == 'worker':
		cm.waitUntilReceive ()
		x = cm.receive ()['x']
		cm.waitUntilReceive ()
		eps = cm.receive ()['eps']
		print ('eps',eps,'x',x)

		cm.waitUntilOnDuty ()
		cm.send ('y', math.sqrt (x))
		cm.waitUntilReceive ()
		res = cm.receive ()

		print (res)
	else:
		cm.send("x", 26.0);
		cm.waitUntilOnDuty ();
		cm.send("eps", 1.0);
		cm.waitUntilReceive ()
		y = cm.receive ()['y']

		if abs (y) <= 1.0:
			print ('Value',y,'accepted')
			cm.send ('ok')
		else:
			print ('Value',y,'rejected')
			cm.send ('no')
			cm.waitUntilReceive ()
			cm.receive ()				

		
elif __name__ == "__main__":
    print ('usage: python3',sys.argv[0],'[spawn|worker|master]')
