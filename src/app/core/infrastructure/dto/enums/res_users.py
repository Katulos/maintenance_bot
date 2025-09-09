from enum import Enum


class ResUsersCredentialsProtocol(Enum):
    jsonrpc = "jsonrpc"
    jsonrpc_ssl = "jsonrpc+ssl"


class EmployeeType(Enum):
    EMPLOYEE = "employee"
    STUDENT = "student"
    TRAINEE = "trainee"
    CONTRACTOR = "contractor"
    FREELANCE = "freelance"
