from enum import Enum
from typing import List
from flask import Request
import re
import flask_jwt_extended
from werkzeug.exceptions import abort

class SecurityPolicyEnum(Enum):
    ANNONYMOUS = 1
    JWT = 2

class MethodsEnum(Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"
    ALL = "ALL"    

class Path:
    def __init__(self, url: str, methods: List[MethodsEnum] = [MethodsEnum.ALL], policy: SecurityPolicyEnum = SecurityPolicyEnum.ANNONYMOUS):
        self.__url = url
        self.__policy = policy
        self.__methods = methods

    def getUrl(self) -> str:
        return self.__url

    def getPolicy(self) -> SecurityPolicyEnum:
        return self.__policy

    def getMethods(self) -> List[MethodsEnum]:
        return self.__methods

class ModuleSecurityChecker:
    def __init__(self):
        self.__paths = list()

    def addPath(self, path: Path):
        if path not in self.__paths:
            self.__paths.append(path)

    def checkPath(self, url: str, method: str):
        found = False
        policy = None

        for path in self.__paths:
            pattern = re.compile(path.getUrl())
            if pattern.match(url) != None:
                if method in path.getMethods() or path.getMethods() == [MethodsEnum.ALL]:
                    found = True
                    policy = path.getPolicy()
                    break

        if found and policy != SecurityPolicyEnum.ANNONYMOUS:
            if policy == SecurityPolicyEnum.JWT:
                flask_jwt_extended.verify_jwt_in_request()
        else:
            abort(404)
