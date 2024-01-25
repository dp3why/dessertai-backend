from mongoengine import Document, StringField, EmailField


class User(Document):
    username = StringField(required=True, unique=True, max_length=100)
    email = EmailField(required=True, unique=True)
    _id = StringField(required=True, max_length=100)
    photo_url = StringField(required=True, max_length=100)
    # Add more fields as needed

    def __str__(self):
        return self.username
