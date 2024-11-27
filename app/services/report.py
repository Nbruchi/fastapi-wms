from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.report import Report
from uuid import UUID
from app.schemas.report import ReportCreate, ReportUpdate

async def create_report(db: AsyncSession, report: ReportCreate):
    db_report = Report(**report.model_dump())
    db.add(db_report)
    await db.commit()
    await db.refresh(db_report)
    return db_report

async def get_reports(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(Report).offset(skip).limit(limit))
    return result.scalars().all()

async def get_report(db: AsyncSession, report_id: UUID):
    result = await db.execute(select(Report).filter(Report.id == report_id))
    return result.scalar_one_or_none()

async def update_report(db: AsyncSession, report_id: UUID, report_update: ReportUpdate):
    db_report = await get_report(db, report_id)
    if db_report:
        for key, value in report_update.model_dump(exclude_unset=True).items():
            setattr(db_report, key, value)
        await db.commit()
        await db.refresh(db_report)
        return db_report
    return None

async def delete_report(db: AsyncSession, report_id: UUID):
    db_report = await get_report(db, report_id)
    if db_report:
        await db.delete(db_report)
        await db.commit()
        return db_report
    return None
