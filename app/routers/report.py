from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.report import create_report, get_reports, get_report, update_report, delete_report
from app.schemas.report import ReportCreate, ReportUpdate, ReportOut
from app.database import get_db
from uuid import UUID

router = APIRouter()

@router.post("/", response_model=ReportOut)
async def create_report_endpoint(report: ReportCreate, db: AsyncSession = Depends(get_db)):
    return await create_report(db, report)

@router.get("/", response_model=list[ReportOut])
async def read_reports(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    return await get_reports(db, skip, limit)

@router.get("/{report_id}", response_model=ReportOut)
async def read_report(report_id: UUID, db: AsyncSession = Depends(get_db)):
    db_report = await get_report(db, report_id)
    if db_report is None:
        raise HTTPException(status_code=404, detail="Report not found")
    return db_report

@router.put("/{report_id}", response_model=ReportOut)
async def update_report_endpoint(report_id: UUID, report_update: ReportUpdate, db: AsyncSession = Depends(get_db)):
    db_report = await update_report(db, report_id, report_update)
    if db_report is None:
        raise HTTPException(status_code=404, detail="Report not found")
    return db_report

@router.delete("/{report_id}", response_model=ReportOut)
async def delete_report_endpoint(report_id: UUID, db: AsyncSession = Depends(get_db)):
    db_report = await delete_report(db, report_id)
    if db_report is None:
        raise HTTPException(status_code=404, detail="Report not found")
    return db_report
