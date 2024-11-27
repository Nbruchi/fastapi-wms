from sqlalchemy import Column, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .schedule import Base
import uuid
from sqlalchemy.dialects.postgresql import UUID

class Recycle(Base):
    __tablename__ = "recycle"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    type = Column(String, nullable=False)
    quantity = Column(Float, nullable=False)
    date = Column(DateTime(timezone=True), nullable=False)  # Timezone-aware DateTime
    schedule_id = Column(UUID(as_uuid=True), ForeignKey('schedules.id'), nullable=False)  # Foreign Key

    schedule = relationship("Schedule", back_populates="recycles")  # This creates a relationship back to Schedule

    def __repr__(self):
        return f"<RecyclingLog(id={self.id}, type={self.type}, quantity={self.quantity})>"
