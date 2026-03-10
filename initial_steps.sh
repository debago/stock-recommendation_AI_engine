Python -m pip install --upgrade pip setuptools wheel
sleep 5    # This is to add Sleep of 5 seconds to ensure that pip, setuptools and wheel are upgraded before we run pip install pip-tools
pip install pip-tools 
sleep 5 # # This is to add Sleep of 5 seconds to ensure that pip-tools is installed before we run pip-compile
pip-compile requirements.in  #this generates requirements.txt, then install requirements.txt
pip install -r requirements.txt