all:
	mkdir sslsplit
	mkdir sslsplit/logdir
	mv mitm_attack.py mitm_attack
	mv pharm_attack.py pharm_attack
	chmod +x mitm_attack pharm_attack
	openssl genrsa -out ca.key 4096
	openssl req -new -x509 -days 1826 -key ca.key -out ca.crt -subj '/C=TW/ST=Taiwan/L=HC/CN=tatree.com/emailAddress=sa0963278610@gmail.com'
clear:
	rm -rf sslsplit
	rm ca.key ca.crt