all:
	python setup.py bdist_wheel
	python setup.py sdist
	twine upload dist/*
	mkdir -p log
	mv dist/* log
