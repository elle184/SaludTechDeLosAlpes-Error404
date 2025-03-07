import uuid

from pulsar.schema import *

class Message(Record) :
    username : String()
    password : String()