import os
from flask import render_template, request, redirect, url_for, session, current_app
from ..models import Flashcard_packs, Flashcards

# Ensure the secret key is set for the session
from app import db
import datetime
from . import create
from app.core.utils.utils import validate_image_and_upload
import csv
import pandas as pd
import numpy as np

# Main Create route. Think of it as the create homepage
@create.route('/', methods=["GET"])
def create_index():
    if session.get('metadata'):
        session.pop('metadata', None)
    return render_template('create/create.html')

# After choosing the FLashcard Pack type, You go here to input metadata for the pack
@create.route('/meta_create/<pack_type>', methods=['GET','POST'])
def meta_create(pack_type):
    if request.method == 'POST':
        try:
            if db.session.query(Flashcard_packs).filter(Flashcard_packs.name == request.form["name"]).first():
                return render_template('create/core/pack_meta.html', packtype=pack_type, error="A pack with this name already exists.")
            
            # Create a dictionary for holding the metadata of pack
            metadata = {
                'name': request.form['name'],
                'flashcard_desc': request.form['description'],
                'created_at': datetime.datetime.now().isoformat()
            }
            
            session['metadata'] = metadata  # Save the metadata temporarily in a session

            # Redirect us to the page for creating the chosen flashcard types flashcards.
            url = f"create.{pack_type}"
            return redirect(url_for(url))
        except Exception as e:
            print(f"Error: {e}")
            return redirect(url_for('create.create_index'))    
    elif request.method == 'GET':
        if session.get('metadata'):
            session.pop('metadata', None)
        return render_template('create/core/pack_meta.html', packtype=pack_type)

# Renders the page for creating basic type flashcards after metadata has been written
@create.route('/basic_card', methods=["GET"])
def basic_create():
    return render_template('create/basic_pack/basic_create.html')

# Route to render the page for the client to upload the file they want to import
@create.route('/import', methods=["GET"])
def import_table():
    return render_template('create/import_pack/import_create.html')

# Route for creating flashcards through importing a file instead
@create.route('/import_create', methods=['POST'])
def import_create():
    if request.method == 'POST':
        try:
            # Flashcard Pack meta to meta database
            has_headers = "has-header" in request.form
            qheaders = request.form['qheaders'].split(";")
            aheaders = request.form['aheaders'].split(";")
            date = datetime.datetime.now()
            metadata = session.get('metadata')
            new_pack = Flashcard_packs(name=metadata['name'], 
                                       description=metadata['flashcard_desc'],
                                       created_at=metadata['created_at'])
            if has_headers:
                new_pack.key_headers = qheaders
                new_pack.value_headers = aheaders
            db.session.add(new_pack)
            db.session.flush()  # Ensure the new_pack is assigned an ID before committing
            new_pack_id = new_pack.id  # Get the assigned ID
            

            # Flashcards to flashcards databasE
            created_at = date
            file = request.files['table']
            if file.filename.endswith('.csv'):
                content = file.read().decode('utf-8-sig')
                csv_reader = csv.reader(content.splitlines(), delimiter=";")
                q_indexes = []
                a_indexes = []
                for i, row in enumerate(csv_reader):
                    if has_headers and i == 0: # Get the column indexes of headers if named
                        for q in qheaders:
                            q_indexes.append(row.index(q))
                        for a in aheaders:
                            a_indexes.append(row.index(a))
                        continue                       
                    elif not has_headers and i == 0: # Get the column indexes of headers if not named
                        q_indexes = [(int(item) - 1) for item in qheaders]
                        a_indexes = [(int(item) - 1) for item in aheaders]

                    key_data = {}
                    key_data["key"] = [row[i] for i in q_indexes]
                    
                    value_data = {}                    
                    value_data["value"] = [row[i] for i in a_indexes]
                    
                    flashcard = Flashcards(pack_id=new_pack_id, key=key_data, value=value_data, created_at=created_at)
                    db.session.add(flashcard)
            elif file.filename.endswith('.xlsx') or file.filename.endswith('.xls'):
                
                df = pd.read_excel(file) if has_headers else pd.read_excel(file, header=None)
                json_data = df.replace({np.nan: None}).to_dict(orient="records")

                # Getting the headers
                q_indexes = []
                a_indexes = []
                if has_headers:
                    q_indexes = [q for q in qheaders]
                    a_indexes = [a for a in aheaders]
                elif not has_headers:
                    q_indexes = [(int(item) - 1) for item in qheaders]
                    a_indexes = [(int(item) - 1) for item in aheaders]    
                
                for index, row in enumerate(json_data):
                    if index < 5:
                        print(row, "\n")
                        
                    key_data = {}
                    key_data["key"] = [row[i] for i in q_indexes]
                    
                    value_data = {}
                    value_data["value"] = [row[i] for i in a_indexes]

                    flashcard = Flashcards(pack_id=new_pack_id, key=key_data, value=value_data, created_at=created_at)
                    db.session.add(flashcard)
            else:
                print("Unsupported file format")
            db.session.commit()
            session.pop('metadata', None)
            
            
        except Exception as e:
            print(f"Error: {e}")
            return redirect(url_for('create.create_index'))

    return redirect(url_for('create.create_index'))

# Creates and posts the flashcards and the metadata to database
@create.route('/create', methods=['POST'])
def create_flashcard():
    if request.method == 'POST':
        try:
            # Flashcard Pack meta to meta database
            date = datetime.datetime.now()
            metadata = session.get('metadata')
            new_pack = Flashcard_packs(name=metadata['name'], 
                                       description=metadata['flashcard_desc'],
                                       created_at=metadata['created_at'])
            db.session.add(new_pack)
            db.session.flush()  # Ensure the new_pack is assigned an ID before committing
            new_pack_id = new_pack.id  # Get the assigned ID
            
            # Flashcards to flashcards database
            num_flashcards = len([key for key in request.form.keys() if key.startswith('key-')])
            for i in range(1, num_flashcards + 1):
                key_file = request.files[f"key-file-{i}"]
                key_filename = validate_image_and_upload(key_file, f"pack-{new_pack_id}")
                key = request.form.get(f'key-{i}')
                
                value_file = request.files[f"value-file-{i}"]
                value_filename = validate_image_and_upload(value_file, f"pack-{new_pack_id}")
                value = request.form.get(f'value-{i}')
                
                created_at = date
                
                
                # Combine key and key_file into a JSON object if both are present
                key_data = {}
                if key:
                    key_data['key'] = key
                if key_file:
                    key_data['key_file'] = key_filename
                
                # Combine value and value_file into a JSON object if both are present
                value_data = {}
                if value:
                    value_data['value'] = value
                if value_file:
                    value_data['value_file'] = value_filename
                
                flashcard = Flashcards(pack_id=new_pack_id, key=key_data, value=value_data, created_at=created_at)
                db.session.add(flashcard)
            
            db.session.commit()
            
            session.pop('metadata', None)
            
        except Exception as e:
            print(f"Error: {e}")
            return redirect(url_for('create.create_index'))

    return redirect(url_for('create.create_index'))

