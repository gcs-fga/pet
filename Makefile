all:
	-mv -f dist/* log
	python2.7 setup.py sdist
	python2.7 setup.py bdist_wheel
	twine upload dist/*
	mkdir -p log
	mv dist/* log
	git add .
	git commit -m "Update packing setup.py"
