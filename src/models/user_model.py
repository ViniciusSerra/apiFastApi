from src.config.database import Base
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


class Users(Base):
    __tablename__ = "tb_users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    client_id = Column(Integer, ForeignKey('tb_clients.id'))
    role_id = Column(Integer, ForeignKey('tb_roles.id'))
    name = Column(String(50))
    login = Column(String(20))
    password = Column(String(50))
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    status = Column(String(20))
    last_access = Column(DateTime)
    n_tentativas = Column(Integer)
    email = Column(String(50))

    client = relationship("Client", back_populates="users")
    role = relationship("Role", back_populates="users")


class Client(Base):
    __tablename__ = "tb_clients"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))

    users = relationship("Users", back_populates="client")


class Role(Base):
    __tablename__ = "tb_roles"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    users = relationship("Users", back_populates="role")
