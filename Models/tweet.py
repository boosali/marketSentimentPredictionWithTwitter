from db import db


class Tweet(db.Model):
    __tablename__ = 'tweets'

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(300))
    timestamp = db.Column(db.DateTime)
    source = db.Column(db.String(80))
    symbols = db.Column(db.String(80))
    company_names = db.Column(db.String(80))
    url = db.Column(db.String(80))
    verified = db.Column(db.Boolean)
    followers = db.Column(db.BigInteger)

    def __init__(self, text, timestamp, source, symbols, company_names, url, verified, followers):
        self.text = text
        self.timestamp = timestamp
        self.source = source
        self.symbols = symbols
        self.company_names = company_names
        self.url = url
        self.verified = verified
        self.followers = followers

    def json(self):
        return {'text': self.text, 'timestamp': self.timestamp, 'source': self.source, 'symbols': self.symbols,
                'company_names': self.company_names, 'url': self.url, 'verified': self.verified}

    @classmethod
    def find_by_symbols(cls, symbols, verified):
        return cls.query.filter_by(symbols=symbols).filter_by(cls.verified == verified)

    @classmethod
    def find_by_company_names(cls, company_names, verified):
        return cls.query.filter_by(company_names=company_names).filter_by(cls.verified == verified)

    @classmethod
    def find_by_dates(cls, start_datetime, end_datetime, verified):
        return cls.query.filter_by(cls.timestamp > start_datetime).filter_by(cls.timestamp < end_datetime).filter_by(cls.verified == verified)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
