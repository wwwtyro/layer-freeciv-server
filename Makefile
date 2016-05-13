NAME=`grep "name: " metadata.yaml | cut -d " " -f 2`
SERIES=xenial
REPO=$(JUJU_REPOSITORY)/$(SERIES)/$(NAME)

t:
	make build
	bundletester -F -v -l debug -e `juju switch` -t $(REPO)

proof:
	make build
	charm proof $(REPO)

build:
	charm build -s $(SERIES) --force

remove-service:
	juju remove-service $(NAME)

deploy:
	juju deploy $(REPO) --series $(SERIES)

expose:
	juju expose $(NAME)

boot:
	make build
	make deploy
	make expose

reboot:
	make remove-service
	make boot
