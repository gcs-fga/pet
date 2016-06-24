all:
	mv dist/* log
	python setup.py bdist_wheel
	python setup.py sdist
	twine upload dist/*
	mkdir -p log
	mv dist/* log
	git add .
	git commit -m "Update packing setup.py"
