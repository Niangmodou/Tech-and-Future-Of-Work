from app import db

class Student(db.Model):
    __tablename__ = 'student'

    netId = db.Column(db.String(), primary_key = True)

    first_name = db.Column(db.String())
    last_name = db.Column(db.String())

    topic = db.Column(db.String())

    def __init__(self, netId, first, last, topic):
        self.netId = netId
        self.first_name = first
        self.last_name =  last
        self.topic = topic

    def __repr__(self):
         return 'Student: {}, {}: \n \
                 NetId: {} \n \
                 Topic: {}'.format(self.first_name, self.last_name, self.netId, self.topic)

    def serialize(self):
        return {
            'netId': self.netId,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'topic': self.topic
        }

class Topic(db.Model):
    __tablename__ = 'topic'

    name = db.Column(db.String(), primary_key = True)
    status = db.Column(db.String())

    def __init__(self, name, status):
        self.name = name
        self.status = status

    def __repr__(self):
        return 'Topic: {}, {}'.format(self.name, self.status)

    def serialize(self):
        return {
            'name': self.name,
            'status': self.status
        }

class Admin(db.Model):
    __tablename__ = 'admin'

    username = db.Column(db.String(), primary_key = True)
    password = db.Column(db.String())

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return 'Username: {}'.format(self.username)
