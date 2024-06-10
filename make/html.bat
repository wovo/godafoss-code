python make/sphinx/prepare_documentation.py
sphinx-build -E -a -b html make/sphinx ../godafoss
python make/sphinx/html_postprocess.py
cp make/sphinx/website/*.* ../godafoss
