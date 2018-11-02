# -*- coding: utf-8 -*-
from flask import Flask
from flask_cors import *
from flask import request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

app = Flask(__name__)
CORS(app, supports_credentials=True)
CONSTR = 'mysql+mysqlconnector://root:123456@193.112.82.110:3306/trust?charset=utf8'
engine = create_engine(CONSTR, echo=True)
db_session = sessionmaker(bind=engine)
session = db_session()
from processor import *

@app.route("/process", methods=["POST"])
def precess():
    username = request.form.get("username", type=str, default=None)
    card_path = school_card_process(request.form.get("card", type=str, default=None), username)
    alipay_path = alipay_process(request.form.get("alipay", type=str, default=None), username)
    path = process_csv_data(alipay_path, card_path, username)
    score = calculate_score(path)
    row = session.execute('select campus_score from user where username=\''+ username + '\';').first()
    score = row[0] + score
    session.execute('update user set credit_score=\''+str(score) +'\' where username=\'' + username + '\';')
    return "success"


@app.route("/", methods=["POST","GET"])
def connect():
    return "success connect!!!"



if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8001)
