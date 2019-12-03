from django.utils.translation import ugettext_lazy as _
from boogie.fields import IntEnum


class ClusterStatus(IntEnum):
    """ Status of Clusters
    Attributes:
        peding_data:
        active: if active status
        disabled: if disabled status
    """

    PENDING_DATA = 0, _("Waiting for more data")
    ACTIVE = 1, _("Active")
    DISABLED = 2, _("Disabled")

    # FIXME: deprecated, a future boogie version will implement this!
    # Normalized clusters status
    @classmethod
    def normalize(cls, obj):
        """
        Normalize enumeration that can be passed as value or a string argument.
        """
        if isinstance(obj, cls):
            return obj
        elif isinstance(obj, str):
            value = getattr(cls, obj.upper(), None)
            if value is None:
                raise ValueError(f"invalid {cls.__name__}: {obj}")
            elif isinstance(obj, int):
                return cls(obj)
            else:
                raise TypeError(type(obj))
