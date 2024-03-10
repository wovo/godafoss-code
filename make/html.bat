python make/sphinx/prepare_documentation.py
sphinx-build -E -a -b html make/sphinx docs
python make/sphinx/html_postprocess.py
