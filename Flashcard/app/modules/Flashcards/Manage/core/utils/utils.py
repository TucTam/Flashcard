from ....models import Flashcard_packs, Flashcards
from ......database import db

def delete_cards(items):
    """Manage page specific function for deleting flashcard packs from the database

    Args:
        items (list): a request.form formatted specific to the manage page
    Returns:
        string: a string whether action was successful or not
    """
    try:
        for index, item in enumerate(items):
            if index < 2: continue
            id = item[5:]
            # Delete the metadata pack from Flashcard_packs table
            meta = db.session.query(Flashcard_packs).filter(Flashcard_packs.id == id).first()
            db.session.delete(meta)

            # Delete the flashcards pack from Flashcards table
            db.session.query(Flashcards).filter(Flashcards.pack_id == id).delete(synchronize_session=False)
        db.session.commit()
        return "Items deleted successfully"
    except:
        print("Fail")

        return "Failed to delete"
