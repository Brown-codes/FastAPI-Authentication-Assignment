from typing import Annotated

from fastapi import APIRouter, Depends, Query, Response, status
from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from auth import get_current_user, get_readable_note, get_writable_note
from database import get_db
from models import Note, User
from schemas import NoteCreate, NoteOut, NoteUpdate

router = APIRouter(prefix="/notes", tags=["notes"])


@router.post("/", response_model=NoteOut, status_code=status.HTTP_201_CREATED)
def create_note(
    note_in: NoteCreate,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
):
    note = Note(**note_in.model_dump(), owner=current_user.username)
    db.add(note)
    db.commit()
    db.refresh(note)
    return note


@router.get("/", response_model=list[NoteOut])
def list_notes(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
    tag: str | None = Query(default=None),
    search_term: str | None = Query(default=None),
):
    stmt = select(Note)

    if current_user.role != "admin":
        stmt = stmt.where(
            or_(Note.owner == current_user.username, Note.is_public.is_(True))
        )

    if search_term:
        like = f"%{search_term}%"
        stmt = stmt.where(or_(Note.title.ilike(like), Note.content.ilike(like)))

    stmt = stmt.order_by(Note.created_at.desc())
    notes = db.scalars(stmt).all()

    if tag:
        notes = [n for n in notes if tag in (n.tags or [])]
    return notes


@router.get("/{note_id}", response_model=NoteOut)
def get_note(note: Annotated[Note, Depends(get_readable_note)]):
    return note


@router.put("/{note_id}", response_model=NoteOut)
def update_note(
    note_in: NoteUpdate,
    note: Annotated[Note, Depends(get_writable_note)],
    db: Annotated[Session, Depends(get_db)],
):
    for field, value in note_in.model_dump(exclude_unset=True).items():
        setattr(note, field, value)
    db.commit()
    db.refresh(note)
    return note


@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_note(
    note: Annotated[Note, Depends(get_writable_note)],
    db: Annotated[Session, Depends(get_db)],
):
    db.delete(note)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)