from sqlalchemy.orm import relationship
from blog.models.database import db
from blog.models.tags import article_tag_association_table
from datetime import datetime
from sqlalchemy import Column, Integer, ForeignKey, String, Text, DateTime, func


class Article(db.Model):
    id = Column(Integer, primary_key=True)
    author_id = Column(Integer, ForeignKey("author.id"))
    title = Column(String(200), nullable=False, default="", server_default="")
    body = Column(Text, nullable=False, default="", server_default="")
    dt_created = Column(DateTime, default=datetime.utcnow, server_default=func.now())
    dt_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    author = relationship("Author", back_populates="articles")
    tags = relationship(
        "Tag",
        secondary=article_tag_association_table,
        back_populates="articles",
    )

    def __str__(self):
        return self.title


