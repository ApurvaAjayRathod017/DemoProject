from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from MovieCollectionDatabase import SessionLocal, engine
from MovieCollectionModels import Base, Movie, MovieCreate, MovieOut
from fastapi import FastAPI
import json

Base.metadata.create_all(bind=engine)

app = FastAPI(title="🎬 Movie Collection API")

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Add Movie
@app.post("/movies/", response_model=MovieOut)
def add_movie(movie: MovieCreate, db: Session = Depends(get_db)):
    db_movie = Movie(**movie.dict())
    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)
    return db_movie

# View All Movies
@app.get("/movies/", response_model=list[MovieOut])
def view_movies(db: Session = Depends(get_db)):
    return db.query(Movie).all()

# Search Movies
@app.get("/movies/search/", response_model=list[MovieOut])
def search_movies(query: str, db: Session = Depends(get_db)):
    results = db.query(Movie).filter(
        Movie.title.ilike(f"%{query}%") |
        Movie.year.ilike(f"%{query}%") |
        Movie.director.ilike(f"%{query}%")
    ).all()
    if not results:
        raise HTTPException(status_code=404, detail="No movies found")
    return results

# Endpoint to generate files from DB data
@app.get("/generate-files")
def generate_files(db: Session = Depends(get_db)):
    movies = db.query(Movie).all()

    # Convert SQLAlchemy objects to dictionaries
    movie_dicts = [
        {
            "id": movie.id,
            "title": movie.title,
            "year": movie.year,
            "director": movie.director,
        }
        for movie in movies
    ]


    # Save as JSON
    with open("movies_output.json", "w") as json_file:
        json.dump(movie_dicts, json_file, indent=4)

    return {"message": "Files generated successfully in local directory."}