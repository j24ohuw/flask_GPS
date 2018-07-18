class UniqueMixin(object):
    @classmethod
    def unique_hash(cls, *arg, **kw):
        raise NotImplementedError()

    @classmethod
    def unique_filter(cls, query, *arg, **kw):
        raise NotImplementedError()

    @classmethod
    def as_unique(cls, session, *arg, **kw):
        return _unique(
                    session,
                    cls,
                    cls.unique_hash,
                    cls.unique_filter,
                    cls,
                    arg, kw
               )


from marshmallow import fields

class SmartNested(fields.Nested):

    def serialize(self, attr, obj, accessor=None):
        if attr not in obj.__dict__:
            return {'id': int(getattr(obj, attr + '_id'))}
        return super(SmartNested, self).serialize(attr, obj, accessor)
