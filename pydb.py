import os
import json
from cryptography.fernet import Fernet

class PyDB:
    def __init__(self, location):
        self.location = location;
        self.dbdata = {};
        self.Connected = True;
        if(os.path.exists(self.location)):
            dbfile = open(self.location, "r");
            self.dbdata = json.loads(dbfile.read());
    def add(self, name, value):
        if(self.Connected):
          self.dbdata[name] = value;
          return True;
        else:
            return False;
    def get(self, name):
        if(self.Connected):
         if(name in self.dbdata):
             return self.dbdata[name];
         else:
             return False;
        else:
            return False;
    def delete(self, name):
        if(self.Connected):
         if(name in self.dbdata):
             del self.dbdata[name];
             return True;
         else:
             return False;
        else:
            return False;
    def deletebyvalue(self, value):
        if(self.Connected):
            for data in list(self.dbdata):
                if(self.dbdata[data] == value):
                    del self.dbdata[data];
            return True;
        else:
            return False;
    def commit(self):
        if(self.Connected):
         if(os.path.exists(self.location)):
             dbread = open(self.location, "r");
             dbfiledata = dbread.read();
             if(json.loads(dbfiledata) == self.dbdata):
                 return "No changes";
             else:
                  dbfile = open(self.location, "w");
                  dbtext = json.dumps(self.dbdata);
                  dbfile.write(dbtext);
                  dbfile.close();
                  return True;
         else:
              dbfile = open(self.location, "w");
              dbtext = json.dumps(self.dbdata);
              dbfile.write(dbtext);
              dbfile.close();
              return True;
        else:
            return False;
    def searchvalue(self, value):
        found = 0;
        for data in list(self.dbdata):
            if(self.dbdata[data] == value):
                found += 1;
        return found;
    def searchname(self, name):
        found = 0;
        for data in list(self.dbdata):
            if(data in self.dbdata):
                found += 1;
        return found;
    def close(self):
        self.Connected = False;
        return True;
    def connect(location):
        return PyDB(location);
    def status(self):
        if(self.Connected):
            return "Connected To DB";
        else:
            return "Not Connected To DB";
    def reload(self):
        if(os.path.exists(self.location)):
            dbfile = open(self.location, "r");
            self.dbdata = json.loads(dbfile.read());
        return True;
    def updatebyvalue(self, value, newvalue):
        for data in list(self.dbdata):
            if(self.dbdata[data] == value):
                self.add(data, newvalue);
        return True;
    def reset(self):
        self.dbdata = {};
        return True;
    def __repr__(self):
     try:
         dbread = open(self.location, "r");
         dbfiledata = dbread.read();
     except:
         return "PyDB.DatabaseFile.Unsaved: " + self.location;
     if(json.loads(dbfiledata) == self.dbdata):
            return "PyDB.DatabaseFile: " + self.location;
     else:
         return "PyDB.DatabaseFile.Unsaved: " + self.location;
    def resetdbfile(self):
        dbfile = open(self.location, "w");
        dbfile.write(json.dumps({}));
        dbfile.close();
        return True;
    def resetall(self):
        self.reset();
        self.resetdbfile();
    class Encryption:
        def __init__(self, PyDBObject):
            self.PyDBObj = PyDBObject;
        def generateKey(self):
            key = Fernet.generate_key().decode("utf-8");
            self.key = key;
            return key;
        def encrypt(self, outputfilename):
            key = self.key;
            f = Fernet(bytes(key, "utf-8"));
            self.PyDBObj.reload();
            dbdata = json.dumps(self.PyDBObj.dbdata);
            encrypted = f.encrypt(bytes(dbdata, "utf-8"));
            file = open(outputfilename, "wb");
            file.write(encrypted);
            file.close();
            return True;
        def decrypt(key, encfilename, PyDBObj):
            encfile = open(encfilename, "r");
            encdata = bytes(encfile.read(), "utf-8");
            f = Fernet(bytes(key, "utf-8"));
            decrypted2 = f.decrypt(encdata);
            PyDBObj.dbdata = json.loads(decrypted2);
