from fastapi import FastAPI
import socket

import os
import psycopg
from psycopg.rows import dict_row 
from pydantic import BaseModel 
import platform

app = FastAPI()


DATABASE_URL = os.getenv("DATABASE_URL")

class Note(BaseModel):
    text:str


def get_connection():
    return psycopg.connect(
            DATABASE_URL,
            row_factory=dict_row
            )


@app.get("/")
def root():
    return {
            "Hello from my home lab"
            }

@app.get("/health")
def health():
    return {
            "status: ok"
            }

@app.get("/server-info")
def server_info():
    return {
            "hostname": socket .gethostname(),
            "os": platform.system(),
            "kernel": platform.release()
            }

@app.post("/notes")
def create_note(note:Note):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                    """
                    CREATE TABLE IF NOT EXISTS notes (
                    id SERIAL PRIMARY KEY,
                    text TEXT NOT NULL
                    )
                    """
                    )
            cur.execute(
                    "INSERT INTO notes (text) VALUES (%s) RETURNING id, text",
                    (note.text,)
                    )
            return cur.fetchone()

@app.get("/notes")
def get_notes():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                    """
                    CREATE TABLE IF NOT EXISTS notes (
                    id SERIAL PRIMARY KEY,
                    text TEXT NOT NULL
                    )
                    """
                    )
            cur.execute(
                    "SELECT id, text FROM notes ORDER BY id")

            return cur.fetchall()





