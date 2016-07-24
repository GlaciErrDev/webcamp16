DHOST	    ?= 192.168.99.100
VIRTUAL_ENV ?= .env

.PHONY: reqs
reqs:
	@$(VIRTUAL_ENV)/bin/pip install -r $(CURDIR)/frameworks/aiohttp/requirements.txt
	@$(VIRTUAL_ENV)/bin/pip install -r $(CURDIR)/frameworks/tornado/requirements.txt
	@$(VIRTUAL_ENV)/bin/pip install -r $(CURDIR)/frameworks/twisted/requirements.txt
	@touch $(CURDIR)/frameworks
	@touch $(VIRTUAL_ENV)

.PHONY: lab
lab:
	@echo Start docker container
	@docker run -p 80:80 -p 5432:5432 --name frameworksbench -d bench:0.1 && sleep 3
	@make -C $(CURDIR) db

.PHONY: db
db:
	@echo Fill DATABASE
	@DHOST=$(DHOST) $(VIRTUAL_ENV)/bin/python db.py

WRK = wrk -d20s -c200 -t10 --timeout 10s -s scripts/cvs-report.lua
bench: $(VIRTUAL_ENV)
	@rm -f $(CURDIR)/results.csv
	# aiohttp
	@make aiohttp OPTS="-p pid -D -w 2"
	@sleep 2
	@make wrk TESTEE=aiohttp
	@kill `cat $(CURDIR)/pid`
	@sleep 3
	# bottle
	@make bottle OPTS="-p pid -D -w 2"
	@sleep 2
	@make wrk TESTEE=bottle
	@kill `cat $(CURDIR)/pid`
	@sleep 3
	# django
	@make django OPTS="-p pid -D -w 2"
	@sleep 2
	@make wrk TESTEE=django
	@kill `cat $(CURDIR)/pid`
	@sleep 4
	# falcon
	@make falcon OPTS="-p pid -D -w 2"
	@sleep 2
	@make wrk TESTEE=falcon
	@kill `cat $(CURDIR)/pid`
	@sleep 3
	# flask
	@make flask OPTS="-p pid -D -w 2"
	@sleep 2
	@TESTEE=flask $(WRK) http://127.0.0.1:5000/json
	@TESTEE=flask $(WRK) http://127.0.0.1:5000/remote
	@TESTEE=flask $(WRK) http://127.0.0.1:5000/complete
	@kill `cat $(CURDIR)/pid`
	@sleep 3
	# muffin
	@make muffin OPTS="--daemon --pid $(CURDIR)/pid --workers 2"
	@sleep 2
	@make wrk TESTEE=muffin
	@kill `cat $(CURDIR)/pid`
	@sleep 3
	# pyramid
	@make pyramid OPTS="-p pid -D -w 2"
	@sleep 2
	@make wrk TESTEE=pyramid
	@kill `cat $(CURDIR)/pid`
	@sleep 3
	# wheezy
	@make wheezy OPTS="-p pid -D -w 2"
	@sleep 2
	@make wrk TESTEE=wheezy
	@kill `cat $(CURDIR)/pid`
	@sleep 3
	# tornado
	@make tornado OPTS="-p pid -D -w 2"
	@sleep 2
	@make wrk TESTEE=tornado
	@kill `cat $(CURDIR)/pid`
	@sleep 3
	# weppy
	@make weppy OPTS="-p pid -D -w 2"
	@sleep 2
	@make wrk TESTEE=weppy
	@kill `cat $(CURDIR)/pid`
	@sleep 3
	# wsgi
	@make wsgi OPTS="-p pid -D -w 2"
	@sleep 2
	@make wrk TESTEE=wsgi
	@kill `cat $(CURDIR)/pid`
	@sleep 3
	# twisted
	# @make twisted OPTS="-pid &"
	# @sleep 1
	# @TESTEE=twisted $(WRK) http://127.0.0.1:5000/json
	# @TESTEE=twisted $(WRK) http://127.0.0.1:5000/remote
	# @TESTEE=twisted $(WRK) http://127.0.0.1:5000/complete
	# @kill `cat $(CURDIR)/pid`
	# @sleep 2

TESTEE = ""
wrk:
	TESTEE=$(TESTEE) $(WRK) http://127.0.0.1:5000/json
	TESTEE=$(TESTEE) $(WRK) http://127.0.0.1:5000/remote
	TESTEE=$(TESTEE) $(WRK) http://127.0.0.1:5000/complete

OPTS = 
aiohttp: $(VIRTUAL_ENV)
	@DHOST=$(DHOST) $(VIRTUAL_ENV)/bin/gunicorn app:app $(OPTS) \
	    -k aiohttp.worker.GunicornWebWorker --bind=127.0.0.1:5000 \
	    --chdir=$(CURDIR)/frameworks/aiohttp

tornado:
	@DHOST=$(DHOST) $(VIRTUAL_ENV)/bin/gunicorn app:app $(OPTS) \
	    --worker-class=gunicorn.workers.gtornado.TornadoWorker --bind=127.0.0.1:5000 \
	    --chdir=$(CURDIR)/frameworks/tornado

twisted:
	@DHOST=$(DHOST) $(VIRTUAL_ENV)/bin/python $(CURDIR)/frameworks/twisted/app.py
