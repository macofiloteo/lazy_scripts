import twitter
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

#Twitter Api
CONSUMER_KEY = "JcebnYst5gQRAR6X1pUJshOOZ"
CONSUMER_SECRET = "VygAVLJgpZMA4AiiIX6XgjvQxwP8WwvR7oSal5MxhIN4EGRwyI"
ACCESS_TOKEN = "69463291-n0p6A0j26XujzDZzKLtRYIzlqbwvgzgJtWg71G7qg"
ACCESS_SECRET = "m39TAWgCyx4WdwkqnIYxiKizhhgOPpsPGTiFfwcW0B9Hq"

#Firestore Admin
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

twitterApi = twitter.Api(
    consumer_key = CONSUMER_KEY,
    consumer_secret = CONSUMER_SECRET,
    access_token_key = ACCESS_TOKEN,
    access_token_secret = ACCESS_SECRET
)

db = firestore.client()






