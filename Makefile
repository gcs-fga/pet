all:
	-mv -f dist/* log
	python setup.py sdist bdist_wheel
	twine upload dist/*
	mkdir -p log
	mv dist/* log
	git add .
	git commit -m "Update packing setup.py"
