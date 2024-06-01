from flask import Flask

app=Flask(__name__)

DB="theexam"
app.secret_key="Secret Key"