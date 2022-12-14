#!/usr/bin/python3
import boofuzz as bf

session = bf.Session(target=bf.Target(connection=bf.TCPSocketConnection("172.19.0.5", 44582)))
Flag = bf.Request("send",children=(bf.Static("header","\x31\x00\x00\x00\x2d\x00\x00\x00"),bf.String("value","Flag")))
session.connect(Flag)
session.fuzz()
