from fastapi import FastAPI, HTTPException, Header, Request
from typing import Optional
from models import VideoGame, User
from database import video_games, users
import sqlite3
import os
import requests
from fastapi.responses import RedirectResponse
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):

    if not os.path.exists('videogames.db'):
        conn = sqlite3.connect('videogames.db')
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE video_games (
                id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                developer TEXT NOT NULL,
                publisher TEXT NOT NULL,
                year_published INTEGER NOT NULL,
                sales INTEGER NOT NULL
            )
        ''')

        for game in video_games:
            cursor.execute('''
                INSERT INTO video_games (id, title, developer, publisher, year_published, sales)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (game.id, game.title, game.developer, game.publisher, game.year_published, game.sales))
        conn.commit()
        conn.close()
    yield

app = FastAPI(
    title="Game Catalog API",
    description="Catalog, account, and sales reporting endpoints.",
    version="1.0.0",
    contact={
        "name": "Your Name",
        "email": "your.email@example.com",
    },
    root_path="/api",
    docs_url="/",
    redoc_url="/redoc",
    lifespan=lifespan
)


@app.get("/games")
def get_games():
    return video_games


@app.get("/games/{game_id}/sales")
def get_game_sales(game_id: int):
    for game in video_games:
        if game.id == game_id:
            return {"title": game.title, "sales": game.sales}
    raise HTTPException(status_code=404, detail="Game not found")


@app.post("/games")
def add_game(game: VideoGame, Authorization: Optional[str] = Header(None)):

    if not Authorization:
        raise HTTPException(status_code=401, detail="Authorization header required")


    if not Authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid Authorization header format")
    token = Authorization.split(" ")[1]


    for user in users:
        if user.token == token:
            if user.is_admin:
                video_games.append(game)
                return {"message": "Game added"}
            else:
                raise HTTPException(status_code=403, detail="Not authorized")
    raise HTTPException(status_code=401, detail="Invalid token")


@app.get("/users")
def get_users():

    return users


@app.post("/login")
def login(username: str):

    for user in users:
        if user.username == username:
            return {"token": user.token}
    raise HTTPException(status_code=404, detail="User not found")


@app.put("/games/{game_id}")
def update_game(game_id: int, updated_game: VideoGame):

    for i, game in enumerate(video_games):
        if game.id == game_id:
            video_games[i] = updated_game
            return {"message": "Game updated"}
    raise HTTPException(status_code=404, detail="Game not found")


@app.get("/search")
def search_games(query: str):

    conn = sqlite3.connect('videogames.db')
    cursor = conn.cursor()
    try:
        sql_query = f"SELECT * FROM video_games WHERE title = '{query}'"
        cursor.execute(sql_query)
        rows = cursor.fetchall()
    except Exception as e:
        return {"error": str(e)}
    finally:
        conn.close()

    results = []
    for row in rows:
        results.append({
            "id": row[0],
            "title": row[1],
            "developer": row[2],
            "publisher": row[3],
            "year_published": row[4],
            "sales": row[5],
        })
    return results


@app.get("/env")
def get_env():

    return {"SECRET_KEY": "supersecretkey"}


@app.post("/admin/delete_game")
def delete_game(game_id: int, Authorization: Optional[str] = Header(None)):

    if not Authorization:
        raise HTTPException(status_code=401, detail="Authorization header required")


    if not Authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid Authorization header format")
    token = Authorization.split(" ")[1]

    for user in users:
        if user.token == token and user.is_admin:
            for i, game in enumerate(video_games):
                if game.id == game_id:
                    deleted_game = video_games.pop(i)

                    return {"message": f"Game '{deleted_game.title}' deleted"}
            raise HTTPException(status_code=404, detail="Game not found")
    raise HTTPException(status_code=403, detail="Not authorized")

@app.post("/feedback")
def submit_feedback(feedback: str):
    response = HTMLResponse(content=f"<html><body><h1>Feedback Received</h1><p>{feedback}</p></body></html>")
    return response


@app.get("/user_profile")
def get_user_profile(user_id: int):

    for user in users:
        if user.username == f"user{user_id}":
            return user
    raise HTTPException(status_code=404, detail="User not found")


@app.post("/update_profile")
def update_profile(username: str, email: str, Authorization: Optional[str] = Header(None)):

    if not Authorization:
        raise HTTPException(status_code=401, detail="Authorization header required")

    if not Authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid Authorization header format")
    token = Authorization.split(" ")[1]

    for user in users:
        if user.token == token:
            user.username = username
            user.email = email
            return {"message": "Profile updated"}
    raise HTTPException(status_code=401, detail="Invalid token")


@app.get("/fetch_url")
def fetch_url_content(url: str):

    try:
        response = requests.get(url)
        return {"content": response.text}
    except Exception as e:
        return {"error": str(e)}


@app.get("/redirect")
def redirect_client(next: str):
    return RedirectResponse(url=next)
