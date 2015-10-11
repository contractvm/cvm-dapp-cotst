#!/usr/bin/python2
import web, requests, json, collections, sys

RPCPORT = 2820

def do_request (command, args = []):
	payload = {
		"method": command,
		"params": args,
		"jsonrpc": "2.0",
		"id": 0,
	}
	return requests.post('http://localhost:'+str (RPCPORT)+'/', data=json.dumps(payload), headers={'content-type': 'application/json'}).json()


urls = (
	'/', 'Index',
	'/session/(.*)', 'Session',
	'/contract/(.*)', 'Contract',
	'/static/(.*)', 'Static',
	'/search', 'Search'
)


template_globals = {
	'datestr': web.datestr,
	'str': str,
}


render = web.template.render('templates', base='base', globals=template_globals)



class Static:
	def GET (self, fpath):
		f = open ('static/'+fpath, 'r')
		data = f.read ()
		f.close ()
		return data


class Index:
	def GET (self):
		tstinfo = do_request ('tst.info')['result']
		info = do_request ('info')['result']
		return render.index (tstinfo, info)

class Session:
	def GET (self, sessionhash):
		if sessionhash == 'list':
			sessions = do_request ('tst.listsessions', ['all'])['result']
			return render.list ('session', 'List of sessions', 'all', sessions)
		elif sessionhash == 'list/running':
			sessions = do_request ('tst.listsessions', ['running'])['result']
			return render.list ('session', 'List of running sessions', 'running', sessions)
		elif sessionhash == 'list/ended':
			sessions = do_request ('tst.listsessions', ['ended'])['result']
			return render.list ('session', 'List of ended sessions', 'ended', sessions)
		else:
			actions = []
			session = do_request ('tst.getsession', [sessionhash])['result']

			if 'error' in session:
				return render.notfound (sessionhash)
			else:
				for act in sorted (map (int, sorted (session['state']['history']))):
					#print (act)
					a = do_request ('tst.getaction', [session['state']['history'][str (act)]])['result']
					actions.append (a)
				return render.session (session, actions)

class Contract:
	def GET (self, contracthash):
		if contracthash == 'list':
			contracts = do_request ('tst.listcontracts', ['all'])['result']
			return render.list ('contract', 'List of contracts', 'all', contracts)
		elif contracthash == 'list/pending':
			contracts = do_request ('tst.listcontracts', ['pending'])['result']
			return render.list ('contract', 'List of pending contracts', 'pending', contracts)
		elif contracthash == 'list/fused':
			contracts = do_request ('tst.listcontracts', ['fused'])['result']
			return render.list ('contract', 'List of fused contracts', 'fused', contracts)
		elif contracthash == 'list/ended':
			contracts = do_request ('tst.listcontracts', ['ended'])['result']
			return render.list ('contract', 'List of ended contracts', 'ended', contracts)
		elif contracthash == 'list/expired':
			contracts = do_request ('tst.listcontracts', ['expired'])['result']
			return render.list ('contract', 'List of expired contracts', 'expired', contracts)
		else:
			contract = do_request ('tst.getcontract', [contracthash])['result']
			
			if 'error' in contract:
				return render.notfound (contracthash)
			else:
				return render.contract (contract)


class Search:
	def GET (self):
		data = web.input(hash=None)
		ob = do_request ('tst.getobject', [data['hash']])['result']

		if 'error' in ob:
			return render.notfound (data['hash'])
		else:
			if ob['type'] == 'contract':
				return Contract ().GET (data['hash'])
			elif ob['type'] == 'session':
				return Session ().GET (data['hash'])
			else:
				return render.notfound (data['hash'])


if __name__ == "__main__":
		app = web.application(urls, globals())
		app.run()
