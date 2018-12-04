.PHONY: start
start:
	: @$${CLIENT_SECRET?"CLIENT_SECRET must be set. Use 'export CLIENT_SECRET=secret-key-here' "}
	export KEYCLOAK_SERVER=http://localhost:8080/auth/realms &&\
	export CLIENT_ID=token-service &&\
	export KEYCLOAK_REALM=dataplattform &&\
	python3 main.py