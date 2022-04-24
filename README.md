# FirstApp-DB2

First application with Frontend (React Native) and Backend (Flask) using DB2 (IBM) as DBMS.

## Installation

### Run DB

```BASH
docker pull ibmcom/db2
docker run -itd --name mydb2 --privileged=true -p 50000:50000 -e LICENSE=accept -e DB2INST1_PASSWORD=<choose an instance password> -e DBNAME=testdb -v <db storage dir>:/database ibmcom/db2
```

### Run Flask

```BASH
python3 -m venv ./venv
source ./venv/bin/activate
pip install -r requirements.txt
```
