from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy import create_engine, Column, String, Integer, ForeignKey, LargeBinary
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from typing import List
from pydantic import BaseModel
from fastapi.templating import Jinja2Templates

from Src.mailsender import send_notification_to_admin


# Database Setup
DATABASE_URL = "sqlite:///./Database/database.db"
Base = declarative_base()
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)
db = SessionLocal()

# FastAPI App Initialization
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount Static Files and Templates
app.mount("/cssFiles", StaticFiles(directory="templates/cssFiles"), name="css")
app.mount("/assets", StaticFiles(directory="templates/assets"), name="assets")

templates = Jinja2Templates(directory="templates/htmlFiles")

# Models
class User(Base):
    __tablename__ = "users"
    email = Column(String, primary_key=True, unique=True, index=True)
    username = Column(String, nullable=False)


class Query(Base):
    __tablename__ = "queries"
    id = Column(Integer, primary_key=True, autoincrement=True)
    query = Column(String, nullable=False)
    user_email = Column(String, ForeignKey("users.email"), nullable=False)
    files = relationship("FileModel", back_populates="query")


class FileModel(Base):  # Renamed to avoid conflict
    __tablename__ = "files"
    id = Column(Integer, primary_key=True, autoincrement=True)
    filename = Column(String, nullable=False)
    content = Column(LargeBinary, nullable=False)
    query_id = Column(Integer, ForeignKey("queries.id"), nullable=False)
    query = relationship("Query", back_populates="files")


# Create tables
Base.metadata.create_all(bind=engine)

# Schemas
class QueryResponse(BaseModel):
    query_id: int
    query: str
    files: List[str]


# Routes
@app.post("/submit/")
async def submit_form(
    username: str = Form(...),
    email: str = Form(...),
    query: str = Form(...),
    files: List[UploadFile] = File(...),
):
    try:
        # Check if user exists or create one
        user = db.query(User).filter(User.email == email).first()
        if not user:
            user = User(username=username, email=email)
            db.add(user)
            db.commit()

        # Create query entry
        query_entry = Query(query=query, user_email=email)
        db.add(query_entry)
        db.commit()

        # Save files
        for file in files:
            content = await file.read()
            file_entry = FileModel(
                filename=file.filename, content=content, query_id=query_entry.id
            )
            db.add(file_entry)
        db.commit()

        # Send notification to admin
        send_notification_to_admin(username, email, query)

        return {"message": "Form submitted successfully!", "query_id": query_entry.id}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/queries/{query_id}/", response_model=QueryResponse)
def get_query(query_id: int):
    query = db.query(Query).filter(Query.id == query_id).first()
    if not query:
        raise HTTPException(status_code=404, detail="Query not found")
    files = [file.filename for file in query.files]
    return QueryResponse(query_id=query.id, query=query.query, files=files)


# New Route for Serving the HTML Page
@app.get("/", response_class=HTMLResponse)
async def serve_homepage(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
