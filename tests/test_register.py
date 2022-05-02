from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pytest
import logging
import os
import json

from main import app
from alert_db import get_db
from orm_models import *  # importing all here so that ORM models added to Base
    

DATABASE_PATH = "./test.db"
SQLALCHEMY_DATABASE_URL = f"sqlite:///{DATABASE_PATH}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


@pytest.fixture(scope='module', autouse=True)
def setup_teardown_db():
    print("Cleaning up database")
    try:
        os.remove(DATABASE_PATH)
    except FileNotFoundError:
        print("Did not remove")
        logging.info("Database not present pre-test")
    init_db(engine, override_get_db)
    yield
    logging.info("Removing database")
    os.remove(DATABASE_PATH)


def test_register_system():
    
    response = client.post("/register/system", 
                           json={"system_nm": "anothpricing2", 
                                 "system_desc": "The pricing system is responsible for accurately pricing vehicles in a responsive manner"})
    assert response.status_code == 200
    res = json.loads(response.text)
    assert res["system_nm"] == "anothpricing2"
    assert res["system_desc"] == "The pricing system is responsible for accurately pricing vehicles in a responsive manner"
    assert res["system_id"] == 2
    
    response = client.post("/register/system", 
                           json={"system_nm": "anothpricing0", 
                                 "system_desc": "The pricing system is responsible for accurately pricing vehicles in a responsive manner"})
    assert response.status_code == 200
    res = json.loads(response.text)
    assert res["system_nm"] == "anothpricing0"
    assert res["system_desc"] == "The pricing system is responsible for accurately pricing vehicles in a responsive manner"
    assert res["system_id"] == 3
    

def test_register_diag():
    response = client.post("/register/alert", 
                           json={"alert_nm": "firstalert", 
                                 "alert_desc": "Ensure the world is working"})
    assert response.status_code == 200
    alert_res = json.loads(response.text)
    assert alert_res["alert_nm"] == "firstalert"
    assert alert_res["alert_desc"] == "Ensure the world is working"
    assert alert_res["alert_id"] == 2
    
    response = client.post("/register/alert", 
                           json={"alert_nm": "firstalert", 
                                 "alert_desc": "Ensure the world is working"})
    assert response.status_code == 400
    
    response = client.post("/register/alert", 
                           json={"alert_nm": "2ndalert", 
                                 "system_nm": "anothpricing2",
                                 "alert_desc": "Ensure the world is working still"})
    assert response.status_code == 200
    alert_res = json.loads(response.text)
    assert alert_res["alert_nm"] == "2ndalert"
    assert alert_res["alert_desc"] == "Ensure the world is working still"
    assert alert_res["alert_id"] == 3
    
    response = client.post("/register/alert", 
                           json={"alert_nm": "3rdalert", 
                                 "system_nm": "anothpricing15",
                                 "alert_desc": "Ensure the world is working still"})
    assert response.status_code == 400
    
    