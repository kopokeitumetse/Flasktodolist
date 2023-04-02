from flask import Blueprint, jsonify, redirect, render_template, request, url_for
from flask_login import  login_required,logout_user,current_user
from . import db
from .model import Note
from datetime import datetime, timezone
import json
views = Blueprint('views', __name__)

@views.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form['note']
        new_note = Note(data=note, date= datetime.now(timezone.utc),user_id=current_user.id)
        db.session.add(new_note)
        db.session.commit()     
        
    return render_template("home.html", user= current_user)

@views.route('/delete-note', methods=[ 'GET','POST'])
@login_required
def delete_note():
    if request.method == 'POST':
        note = json.loads(request.data)
        note_id = note['noteId']
        note = Note.query.get(note_id)
        if note:
            if note.user_id == current_user.id:
                db.session.delete(note)
                db.session.commit()
        return jsonify({})
    else:
        return redirect(url_for('views.home'))
    
@views.route('/note-done', methods=[ 'GET','POST'])
@login_required
def doneWithNote():
    if request.method == 'POST':
        note = json.loads(request.data)
        note_id = note['noteId']
        print(note_id)
        note = Note.query.filter_by(id= note_id).first()
      
     
        if note:
            if note.user_id == current_user.id:
                note.done = "Done"
                db.session.commit()
        return jsonify({})
    else:
        return redirect(url_for('views.home'))