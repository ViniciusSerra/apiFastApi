from typing import Annotated
from fastapi import Depends

from src import test
from src.test.database_teste import  test_database_connection


teste = Annotated[database_teste.test_database_connection, Depends(test.database_teste)]