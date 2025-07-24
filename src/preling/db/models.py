from __future__ import annotations
from datetime import datetime

from sqlalchemy import ForeignKey, Index, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base

__all__ = [
    'Sentence',
    'Word',
]


class Sentence(Base):
    __tablename__ = 'sentences'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    sentence: Mapped[str]
    correct_attempts: Mapped[int]
    incorrect_attempts: Mapped[int]

    words: Mapped[list[Word]] = relationship(
        'Word',
        secondary='sentence_word_index',
        order_by=lambda: SentenceWord.word_id,
        back_populates='sentences',
        passive_deletes=True,
    )


class Word(Base):
    __tablename__ = 'words'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    word: Mapped[str]
    occurrences: Mapped[int]
    streak_start: Mapped[datetime | None]
    due: Mapped[datetime | None]

    sentences: Mapped[list[Sentence]] = relationship(
        'Sentence',
        secondary='sentence_word_index',
        order_by=lambda: SentenceWord.random_key,
        back_populates='words',
        passive_deletes=True,
    )

    __table_args__ = (
        Index('ix_words_id_due_null', 'id', sqlite_where=lambda: lambda: Word.due.is_(None)),
        Index('ix_words_due_id_due_not_null', 'due', 'id', sqlite_where=lambda: Word.due.is_not(None)),
    )


class SentenceWord(Base):
    __tablename__ = 'sentence_word_index'

    sentence_id: Mapped[int] = mapped_column(
        ForeignKey(
            Sentence.id,
            ondelete='CASCADE',
            onupdate='CASCADE',
        ),
        primary_key=True,
    )
    word_id: Mapped[int] = mapped_column(
        ForeignKey(
            Word.id,
            ondelete='CASCADE',
            onupdate='CASCADE',
        ),
        primary_key=True,
    )
    random_key: Mapped[int] = mapped_column(server_default=text("(abs(random()))"))

    __table_args__ = (
        Index('ix_sentence_word_index_word_id_random_key', 'word_id', 'random_key'),
    )
