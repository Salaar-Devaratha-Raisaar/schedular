from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from datetime import date, time, datetime

app = FastAPI(title="Scheduler API")

class Note(BaseModel):
    id: int | None = None
    title: str
    body: str
    created_at: datetime | None = None

# in-memory store for initial scaffold
_notes: List[Note] = []
_next_id = 1

@app.post('/notes', response_model=Note)
async def create_note(note: Note):
    global _next_id
    note.id = _next_id
    note.created_at = datetime.utcnow()
    _next_id += 1
    _notes.append(note)
    return note

@app.get('/notes', response_model=List[Note])
async def list_notes():
    return _notes

@app.get('/notes/{note_id}', response_model=Note)
async def get_note(note_id: int):
    for n in _notes:
        if n.id == note_id:
            return n
    raise HTTPException(status_code=404, detail='Not found')

@app.delete('/notes/{note_id}')
async def delete_note(note_id: int):
    global _notes
    before = len(_notes)
    _notes = [n for n in _notes if n.id != note_id]
    if len(_notes) == before:
        raise HTTPException(status_code=404, detail='Not found')
    return {'ok': True}
