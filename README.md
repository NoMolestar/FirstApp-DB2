# FirstApp-DB2

First application with Frontend (React Native) and Backend (Flask) using DB2 (IBM) as DBMS.

## Installation

### Run DB

```BASH
docker pull ibmcom/db2
docker run -itd --name mydb2 --privileged=true -p 50000:50000 -e LICENSE=accept -e DB2INST1_PASSWORD=<choose an instance password> -e DBNAME=testdb -v <db storage dir>:/database ibmcom/db2

# Example
docker run -itd --name mydb2 --privileged=true -p 50000:50000 -e LICENSE=accept -e DB2INST1_PASSWORD=hola -e DBNAME=testdb -v /home/grivas/work/TC3005B/database:/database ibmcom/db2
```

### Run Backend

```BASH
cd backend
python3 -m venv ./venv
source ./venv/bin/activate
pip install -r requirements.txt
flask run
```

### Run Frontend

```BASH
cd frontend
yarn
yarn web
```
