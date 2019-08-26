cd docker
sudo docker-compose up -d

docker exec -it my_postgres psql -U postgres -c "create database citizen_analyzer"

sudo apt-get install -y python3-setuptools

pip3 install aiohttp
pip3 install psycopg2

pip3 freeze > requirements.txt
pip3 install -r requirements.txt

create database citizen_analyzer;

sudo service postgresql restart

sudo nano /etc/postgresql/10/main/pg_hba.conf

peer to md5 for postgres (trust)

create database citizen_analyzer;

ALTER USER postgres WITH PASSWORD 'ghsgdh12';

ssh entrant@84.201.129.208

b341588d9a1d548e7af6809aa29a0b8e7b5716e4d81691c9914aca3ff33982ef