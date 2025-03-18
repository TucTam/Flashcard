from flask import render_template, request, redirect, url_for
from ..models import Flashcard_packs, Flashcards
from . import study
from ....database import db

@study.route('/', methods=["GET"])
def study_index():
    flashcard_packs = db.session.query(Flashcard_packs).all()
    return render_template('study/study.html', database_packs = flashcard_packs)
    
@study.route('/<pack_name>')
def study_pack(pack_name):
    pack = db.session.query(Flashcard_packs).filter(Flashcard_packs.name == pack_name).first()
    pack_id = pack.id if pack else None
    flashcards = db.session.query(Flashcards).filter(Flashcards.pack_id == pack_id).all()
    pack_dict = [card.to_dict() for card in flashcards]
    return render_template('study/study_pack.html', packname=pack.name, pack = pack_dict, keyheaders = pack.key_headers, valueheaders = pack.value_headers)

