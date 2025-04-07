from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///notes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# MODELE
class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    done = db.Column(db.Boolean, default=False)

# ROUTES API
@app.route('/api/notes', methods=['GET', 'POST'])
def notes_api():
    if request.method == 'GET':
        notes = Note.query.all()
        return jsonify([{
            'id': n.id,
            'title': n.title,
            'content': n.content,
            'done': n.done
        } for n in notes])
    
    if request.method == 'POST':
        data = request.get_json()
        note = Note(title=data['title'], content=data['content'])
        db.session.add(note)
        db.session.commit()
        return jsonify({'ok': True}), 201

@app.route('/api/notes/<int:note_id>/done', methods=['POST'])
def toggle_done(note_id):
    note = Note.query.get_or_404(note_id)
    note.done = not note.done
    db.session.commit()
    return jsonify({'ok': True, 'done': note.done})

# ROUTE FRONTEND
@app.route('/front/notes')
def front_notes():
    notes = Note.query.all()
    return render_template("notes.html", notes=notes)

# INIT DB si besoin
@app.before_first_request
def create_tables():
    os.makedirs("instance", exist_ok=True)
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True, port=5001)