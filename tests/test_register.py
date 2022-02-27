from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pytest
import logging
import os

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
                           json={"system_nm": "anothpricing1", 
                                 "system_desc": "The pricing system is responsible for accurately pricing vehicles in a responsive manner"})
    assert response.status_code == 200