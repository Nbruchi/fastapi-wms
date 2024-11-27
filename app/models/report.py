from sqlalchemy import Column, String, DateTime, Text
from .schedule import Base
import uuid
from sqlalchemy.dialects.postgresql import UUID

class Report(Base):
    __tablename__ = "reports"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    type = Column(String, nullable=False)
    time = Column(DateTime(timezone=True), nullable=False)  # Timezone-aware DateTime
    data = Column(Text, nullable=False)

    def __repr__(self):
        return f"<Report(id={self.id}, type={self.type}, time={self.time})>"
