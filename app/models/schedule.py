from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
import pytz
import uuid
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
from sqlalchemy.orm import relationship

Base = declarative_base()

class Schedule(Base):
    __tablename__ = "schedules"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    day = Column(String, nullable=False)
    time = Column(DateTime(timezone=True), nullable=False)  # Timezone-aware DateTime
    frequency = Column(String, nullable=False)

    recycles = relationship("Recycle", back_populates="schedule")  # Relationship to Recycle model

    def __repr__(self):
        return f"<Schedule(id={self.id}, day={self.day}, frequency={self.frequency})>"

    def set_time(self, time_str: str):
        """Helper function to set a datetime with timezone."""
        local_tz = pytz.timezone('UTC')  # Use appropriate timezone
        naive_datetime = datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")
        aware_datetime = local_tz.localize(naive_datetime)
        self.time = aware_datetime
