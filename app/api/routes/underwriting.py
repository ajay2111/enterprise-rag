import app
from fastapi import APIRouter, Depends, UploadFile, File, Form, Body
from app.rag.ingestion import (extract_text, chunk_text, create_embeddings, database)
from app.schemas.underwriting import underwriting_schema
from app.services.underwriting_services import underwrite_applicant, get_applicant
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.rag.rag_pipeline import run_rag
from app.agents import underwriting_agents
from langgraph.types import Command 
from app.graph.workflow import underwriting_graph

router = APIRouter(
    prefix="/api/v1/underwriting",
    tags = ["underwriting"]
)


@router.post("/check")
async def check_underwriting(data: underwriting_schema, db: Session = Depends(get_db)):
    result = underwrite_applicant(
    data.age,
    data.income,
    data.credit_score
    )

    return result 

@router.get("/{applicant_id}")
async def fetch_applicant(
    applicant_id: int,
    db: Session = Depends(get_db)
):
    applicant = get_applicant(db, applicant_id)

    return applicant


@router.post("/rag")
async def rag_query(
    query: str = Form(...),
    file: UploadFile = File(...)
):
    file_path = f"/tmp/{file.filename}"

    with open(file_path, "wb") as f:
        f.write(await file.read())

    answer = run_rag(
        query,
        file_path
    )

    return {
        "answer": answer
    }

@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...)
):
    file_path = f"/tmp/{file.filename}"

    with open(file_path, "wb") as f:
        f.write(await file.read())

    text = extract_text(file_path)

    chunks = chunk_text(text)

    embeddings = create_embeddings(chunks)

    database(
        chunks,
        embeddings
    )

    return {
        "message": "Document uploaded successfully",
        "chunks": len(chunks)
    }


@router.post("/underwrite")
async def underwrite(
    application: dict = Body(...),
    query: str = Body(...)
):

    result = underwriting_agents(
        application,
        query
    )

    return result


@router.post("/human-review")
async def human_review(
    decision: str = Body(...)
):

    result = underwriting_graph.invoke(
        Command(resume=decision)
    )

    return result