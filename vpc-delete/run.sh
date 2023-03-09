python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt > /dev/null 2>&1
python remove_vpc.py $1 $2 $3