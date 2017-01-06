freeradius
===

how to get start connecting into freeradius python modules (Arch Linux). From my investigating and understanding the actual authorize and authenticate steps can NOT be undertaken in python HOWEVER they can enhance/add to existing operations

need python to be able to find the module(s) you define
```
vim /etc/environment
---
PYTHONPATH=/etc/raddb/mods-config/python/
```

foreach interface you want availalbe, edit mods-enabled/python (symlink python)
```
python {
	module = example
	mod_instantiate = ${.module}
	func_instantiate = instantiate

	mod_detach = ${.module}
	func_detach = instantiate

	mod_authorize = ${.module}
	func_authorize = authorize

	mod_authenticate = ${.module}
	func_authenticate = authenticate

	mod_preacct = ${.module}
	func_preacct = preacct

	mod_accounting = ${.module}
	func_accounting = accounting

	mod_checksimul = ${.module}
	func_checksimul = checksimul

	mod_pre_proxy = ${.module}
	func_pre_proxy = pre_proxy

	mod_post_proxy = ${.module}
	func_post_proxy = post_proxy

	mod_post_auth = ${.module}
	func_post_auth = post_auth

	mod_recv_coa = ${.module}
	func_recv_coa = recv_coa

	mod_send_coa = ${.module}
	func_send_coa = send_coa
}
```

under your sites-enabled/default
```
...config text...
authorize {
	...other steps...
	python
	# if you want to auth with python
	update control {
		Auth-Type := python
	}
	...more other steps...
}
...other config...
authenticate {
	...other steps...
	python
	...more other steps
}
...rest of config
```

troubleshoot
```
radiusd -X
```

hitting things like missing methods (e.g. the example doesn't have authenticate as a method as of this writing) should be pretty clear

## module

sending reply/config in authorize/authenticate
```
reply = ( ('key', 'value'), ('key2', 'value'), )
config = ( ('ckey', 'value'), ('ckey2', 'value'), )
return (radiusd.RLM_MODULE_OK, reply, config)
```
