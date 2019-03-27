# -*- coding: utf-8 -*-

from flask import current_app
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)


db = SQLAlchemy()


class User(UserMixin, db.Model):
    __tablename__ = "users_tbl"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(32), nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

    def hash_password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_auth_token(self, expiration=600):  # expires in 10 min by default
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None  # valid token, but expired
        except BadSignature:
            return None  # invalid token
        user = User.query.get(data['id'])
        return user

    def get_id(self):
        """
        This method must return a unicode that uniquely identifies this user,
        and can be used to load the user from the user_loader callback.
        """
        # return self.username
        return str(self.id).encode("utf-8").decode("utf-8")


class Post(db.Model):
    __tablename__ = "posts_tbl"
    id        = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title     = db.Column(db.String(255), nullable=False)
    body      = db.Column(db.String(255), nullable=False)
    author_id = db.Column(db.Integer, nullable=False)
    username  = db.Column(db.String(32), nullable=False)
    created   = db.Column(db.DateTime, nullable=False,
                          default=db.func.current_timestamp())

    def __repr__(self):
        return '<Post %r title: %r body: %d username:%d>' % (self.id, self.title, self.body, self.username)


class SampleInfo(db.Model):
    __tablename__ = "sampleInfo"

    id       = db.Column(db.Integer, primary_key=True, autoincrement=True)
    famID    = db.Column(db.String(30), nullable=False)
    sampleID = db.Column(db.String(30), nullable=False)
    fatherID = db.Column(db.String(30), nullable=False, default=0)
    motherID = db.Column(db.String(30), nullable=False, default=0)
    sex      = db.Column(db.Integer,    nullable=False, default=0)
    pheno    = db.Column(db.Integer,    nullable=False, default=0)
    personName = db.Column(db.String(255), nullable=True)
    phenoDesc  = db.Column(db.String(255), nullable=True)
    birthDate  = db.Column(db.String(30), nullable=True)
    seqBatch   = db.Column(db.String(255), nullable=True)

    def __repr__(self):
        return '<SampleInfo %r>' % self.sampleID


class Gene(db.Model):
    __tablename__ = "genes_tbl"

    id        = db.Column(db.Integer, primary_key=True, autoincrement=True)
    gene_id   = db.Column(db.String(50), nullable=False)
    gene_name = db.Column(db.String(50), nullable=False)
    gene_name_upper = db.Column(db.String(50), nullable=False)
    chrom     = db.Column(db.String(30), nullable=False)
    start     = db.Column(db.Integer, nullable=False)
    stop      = db.Column(db.Integer, nullable=False)
    strand    = db.Column(db.String(5))

    def __repr__(self):
        return '<Gene %r %r:%d-%d>' % (self.gene_id, self.chrom, self.start, self.stop)


class Transcript(db.Model):
    __tablename__ = "transcripts_tbl"

    id        = db.Column(db.Integer, primary_key=True, autoincrement=True)
    transcript_id = db.Column(db.String(50), nullable=False)
    gene_id   = db.Column(db.String(50), nullable=False)
    chrom     = db.Column(db.String(30), nullable=False)
    start     = db.Column(db.Integer, nullable=False)
    stop      = db.Column(db.Integer, nullable=False)
    strand    = db.Column(db.String(5))

    def __repr__(self):
        return '<Transcript %r %r:%d-%d>' % (self.transcript_id, self.chrom, self.start, self.stop)


class Exon(db.Model):
    __tablename__ = "exons_tbl"

    id        = db.Column(db.Integer, primary_key=True, autoincrement=True)
    feature_type = db.Column(db.String(50), nullable=False)
    transcript_id = db.Column(db.String(50), nullable=False)
    gene_id   = db.Column(db.String(50), nullable=False)
    chrom     = db.Column(db.String(30), nullable=False)
    start     = db.Column(db.Integer, nullable=False)
    stop      = db.Column(db.Integer, nullable=False)
    strand    = db.Column(db.String(5))

    def __repr__(self):
        return '<Exon %r %r:%d-%d>' % (self.feature_type, self.chrom, self.start, self.stop)


