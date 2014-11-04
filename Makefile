all:
	python -c "import inspect; import versioned; print inspect.getdoc(versioned)" > README.md
	pandoc -o README.rst README.md

upload:
	python setup.py sdist upload
