pre-receive-pass
===

a pre-receive hook for pass repositories that will check for gpg keys being used to sign and being all present.

to install, navigate to the hooks folder of the served git repo, replay "key|val|ues" with the keys to replace/use
```
curl https://raw.githubusercontent.com/enckse/howdoi/master/software/git/pre-receive.pass | sed "s/MY_KEYS/key|val|ues/g" > pre-receive
```
