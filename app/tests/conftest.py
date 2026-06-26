from typing import Iterator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from ..core.database import Base, get_db
from ..main import app

SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app_test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture()
def session() -> Iterator[TestingSessionLocal]:
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()


# Test client
@pytest.fixture()
def client(session: TestingSessionLocal) -> Iterator[TestClient]:
    # Dependency override

    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db

    yield TestClient(app)

""" l'instruction de la ligne 46 , vient signifier à FastAPI qu'il doit remplacer 
la fonction get_db dans toutes les dépendances par 
la fonction override_get_db. Cette dernière renvoyant 
la base de données de test, cela va avoir pour effet de faire 
tourner notre application FastAPI sur la base de données de test, 
au lieu de la base de données par défaut.

"""



"""Le fait d'entourer notre fonction par ce décorateur
 va nous permettre d'obtenir le résultat de la fonction
  client() directement dans notre fonction de test test_home.
  
  
  
  En effet, dans notre fichier de test, le seul fait d'ajouter 
  un paramètre nommé client à notre fonction va suffire à pytest 
  pour aller chercher, dans le fichier conftest.py une fonction 
  décorée avec @pytest.fixture() correspondant au même nom. Ici,
   puisque nous déclarons un paramètre nommé client, pytest va aller 
   automatiquement chercher une fonction nommée client() dans le fichier 
   conftest."""
