pip install --upgrade pip

pip uninstall -y -r services/text_to_text/requirements.txt
pip uninstall -y -r gateway/requirements.txt

pip install -e .
pip install -r services/text_to_text/requirements.txt
pip install -r gateway/requirements.txt