class BaseModel(object):
    @property
    def _column_names(self):
        return [c.name for c in self.__table__.columns]
