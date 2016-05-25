#coding=utf-8
import hashlib, hmac , string , base64, urllib, json
api_url = "http://cloudstack:8080/client/api"
api_key = "AK"
secret = "SK"

class CloudStackAPI(object):
	""" """
	def __init__(self, api_url,api_key,secret):
		self.api_url = api_url
		self.api_key = api_key
		self.secret = secret
	def __getattr__(self,name):
		def handlerfun(*args,**kwargs):
			if kwargs:
				return self._make_request(name,kwargs)
			return self._make_request(name,args[0])
		return handlerfun
	def _make_request(self,name,args):
		args['response'] = 'json'
		args['command'] = name
		args['apiKey'] = api_key
		self._request(args)
		key = name.lower() + 'response'
		return json.loads(self.response.read())[key]
	def _request(self,args):
		''' create value'''
		self.params = []
		self._sort_reques(args)
		self._create_signature()
		self._build_post_request()
		self._http_get()
	def _sort_reques(self,args):
		keys = sorted(args.keys())
		for key in keys:
			self.params.append(key+'='+urllib.quote_plus(args[key]))
	def _create_signature(self):
		self.query = '&'.join(self.params)
		digest = hmac.new(self.secret,msg=self.query.lower(),digestmod=hashlib.sha1).digest()
		self.signature = base64.b64encode(digest)
	def _build_post_request(self):
		self.query = self.query +'&signature='+urllib.quote_plus(self.signature)
		self.value = self.api_url+'?'+self.query
	def _http_get(self):
		self.response = urllib.urlopen(self.value)
		
api = CloudStackAPI(api_url,api_key,secret)
request = {'install':'True'}
print api.listVirtualMachines(request)
