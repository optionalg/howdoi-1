freeradius
===

how to get start connecting into freeradius python modules (Arch Linux)

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

