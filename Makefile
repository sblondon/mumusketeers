install: clean
	sh ./scripts/local/install-virtualenv.sh
	
run:
	sh ./scripts/local/run.sh

run-wsgi:
	sh ./scripts/local/run-wsgi.sh

run-zeo:
	sh ./scripts/local/run-zeo.sh

check:
	find web -name '*.py' -exec ./local.virtualenv/bin/pyflakes {} +

test: check
	./local.virtualenv/bin/py.test --ignore local.virtualenv --ignore node_modules --ignore media -n auto $* --cov web/ --cov models/ --color=yes

clean:
	find . -name "*.pyc" -delete
	find . -name "*.swp" -delete
	find . -name "__pycache__" -delete
	rm -f npm-debug.log

clean-data:
	rm -rf local.persistent/files
	rm -f local.persistent/Data.*

mrproper: clean
	rm -rf local.persistent local.virtualenv node_modules

shell:
	./local.virtualenv/bin/ptipython --vi --interactive=scripts/local/shell.py

