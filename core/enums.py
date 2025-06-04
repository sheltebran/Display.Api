created_status = ["new", "update", "delete"]
created_status_dict = {status: index for index, status in enumerate(created_status)}
class CreatedStatus:
    """Enum for created status."""
    
    NEW = 0
    UPDATE = 1
    DELETE = 2

    @classmethod
    def to_dict(cls):
        """Return a dictionary representation of the enum."""
        return {status: index for index, status in enumerate(cls.__dict__.keys()) if not status.startswith('_')}