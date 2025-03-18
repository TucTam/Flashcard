from flask import render_template, request, redirect, url_for, send_file
from ..models import Flashcard_packs, Flashcards
from . import manage
from ....database import db
from .core.utils.utils import delete_cards
import json
import csv
import zipfile
from io import StringIO, BytesIO

@manage.route('/', methods=['GET'])
def manage_index():
    flashcard_packs = Flashcard_packs.query.all()
    return render_template('manage/manage.html', flashcard_packs=flashcard_packs)

@manage.route('/manage', methods=['POST'])
def manage_action():
    if request.method == 'POST':
        if request.form["actions"] == "action": # Do nothing
            return redirect(url_for('manage.manage_index'))
        elif request.form["actions"] == "edit": # Edit selected
            
            exclude_keys = ['actions', 'check-all']
            filtered_form = {key: value for key, value in request.form.items() if key not in exclude_keys}

            form_data = json.dumps(filtered_form)
            return redirect(url_for('manage.list_edit_items', items = form_data))
            
        elif request.form["actions"] == "delete": # Delete selected    
            delete_cards(request.form)
            return redirect(url_for('manage.manage_index'))
            
        elif request.form["actions"] == "download": # Download selected
            exclude_keys = ['actions', 'check-all']
            filtered_form = {key: value for key, value in request.form.items() if key not in exclude_keys}            
            form_data = list(json.loads(json.dumps(filtered_form)))

            # Create a zip archive in memory
            zip_buffer = BytesIO()
            with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                for item in form_data:
                    pack_id = item[5:]
                    pack_meta = db.session.query(Flashcard_packs).filter(Flashcard_packs.id == pack_id).first()
                    pack_cards = db.session.query(Flashcards).filter(Flashcards.pack_id == pack_id).all()
                    
                    # Prepare CSV content
                    si = StringIO()
                    writer = csv.writer(si, delimiter=';')
                    
                    # Write headers if available
                    if pack_meta.key_headers or pack_meta.value_headers:
                        headers = (pack_meta.key_headers or []) + (pack_meta.value_headers or [])
                        writer.writerow(headers)
                    
                    # Write card values
                    for card in pack_cards:
                        values = (card.key.get("key", [])) + (card.value.get("value", []))
                        writer.writerow(values)

                    # Add CSV content to ZIP archive
                    csv_filename = f"{pack_meta.name}.csv"
                    zip_file.writestr(csv_filename, si.getvalue())

            # Prepare ZIP file for download
            zip_buffer.seek(0)
            return send_file(
                zip_buffer,
                mimetype='application/zip',
                as_attachment=True,
                download_name="flashcard_packs.zip"
            )
        else:
            return "Method Not Allowed", 405

@manage.route('/manage/edit/<items>', methods=["GET"])
def list_edit_items(items):
    packs = []
    items = json.loads(items)
    print(len(items))
    for item in items:
        id = int(item[5:])
        pack = db.session.query(Flashcard_packs).filter(Flashcard_packs.id == id).first()
        packs.append(pack)
    return render_template("manage/edit.html", items = packs)

@manage.route('/manage/edit', methods=["POST"])
def commit_meta_edit():
    print(request.form)
    if request.method == "POST":
        data = json.loads(json.dumps(request.form))
        # Convert dictionary items to a list of tuples
        items = list(data.items())

        # Group every two items into their own list
        grouped = [items[i:i+2] for i in range(0, len(items), 2)]
        for item in grouped:
            item_id = item[0][0].split("-")[-1]
            pack = db.session.query(Flashcard_packs).filter(Flashcard_packs.id == item_id).first()
            
            print(item[0][1])
            print(item[1][1])

            if item[0][1] != "":
                pack.name = item[0][1]
            if item[1][1] != "":
                pack.description = item[1][1]
        db.session.commit()  # Save changes
    return redirect(url_for('manage.manage_index'))
