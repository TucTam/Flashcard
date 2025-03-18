from app import db
from sqlalchemy.dialects.postgresql import JSONB

# Stores flashcards
class Flashcards(db.Model):
    __tablename__ = 'Flashcard'
    
    id = db.Column(db.Integer, primary_key=True)
    pack_id = db.Column(db.Integer, index=True, unique=False)
    key = db.Column(JSONB, index=True, unique=False)
    value = db.Column(JSONB, index=True, unique=False)
    created_at = db.Column(db.DateTime, index=True, unique=False)
    
    def to_dict(self):
        return {
            "id": self.id,
            "pack_id": self.pack_id,
            "key": self.key,
            "value": self.value,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
    
    @staticmethod
    def get_flashcards_by_pack_id(pack_id):
        return db.session.query(Flashcards).filter(Flashcards.pack_id == pack_id).all()

    def __repr__(self):
        return f'<Flashcard {self.id}>'

# Stores metadata about flashcard packs
class Flashcard_packs(db.Model):
    __tablename__ = 'Flashcard_pack'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, index=True, unique=True)
    key_headers = db.Column(JSONB, unique=False, nullable=True)
    value_headers = db.Column(JSONB, unique=False, nullable=True)
    description = db.Column(db.String, index=True, unique=False)
    created_at = db.Column(db.DateTime, index=True, unique=False)
    
    def __repr__(self):
        return f'<Cardpack {self.name}>'