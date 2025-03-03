rm -rf dist
mkdir dist
python3 -m build
python3 -m twine upload --repository pypi dist/*
