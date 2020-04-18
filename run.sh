# virtualenv .env --python=/usr/bin/python3
source .env/bin/activate

pip3 install requirements.txt

uvicorn main:app --reload