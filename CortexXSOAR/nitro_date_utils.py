from abc import ABC
from datetime import datetime, timezone
from enum import Enum
import dateutil


class NitroDate(ABC):
    def __init__(self, date: datetime = None):
        self.date = date

    def __repr__(self):
        return str(self.date)

    def is_ready(self):
        if self.date is None:
            return False
        elif isinstance(self.date, datetime):
            return True
        else:
            raise NitroDateInconsistentError

    def to_iso8601(self):
        raise NotImplementedError()

    def to_getincidentsbyquery_arg(self):
        return self.to_iso8601()


class NitroDateInconsistentError(Exception):
    pass


class NitroDateParsingError(Exception):
    pass


class NitroUnlimitedPastDate(NitroDate):
    def __repr__(self):
        return "NitroUnlimitedPastDate"

    def to_iso8601(self):
        return NitroDateFactory.datetime_to_iso8601(date=self.date)


class NitroUnlimitedFutureDate(NitroDate):
    def __repr__(self):
        return "NitroUnlimitedFutureDate"

    def to_iso8601(self):
        return NitroDateFactory.datetime_to_iso8601(date=self.date)


class NitroUndefinedDate(NitroDate):
    def __repr__(self):
        return "NitroUndefinedDate"

    def to_iso8601(self):
        raise NotImplementedError


class NitroRegularDate(NitroDate):
    def __init__(self, date: datetime = None):
        super(NitroRegularDate, self).__init__(date=date)

    def to_iso8601(self):
        return NitroDateFactory.datetime_to_iso8601(date=self.date)


class NitroDateHint(Enum):
    Future = 1
    Past = 2


class NitroDateFactory(ABC):
    @classmethod
    def from_iso_8601_string(cls, arg: str = ""):
        try:
            date = dateutil.parser.isoparse(arg)
        except Exception as e:
            raise NitroDateParsingError from e
        return NitroRegularDate(date=date)

    @classmethod
    def from_regular_xsoar_date_range_arg(cls, arg: str = "", hint: NitroDateHint = None):
        if arg == "0001-01-01T00:00:00Z":
            if hint is None:
                return NitroUndefinedDate()
            elif hint == NitroDateHint.Future:
                return NitroUnlimitedFutureDate()
            elif hint == NitroDateHint.Past:
                return NitroUnlimitedPastDate()
        else:
            return cls.from_iso_8601_string(arg=arg)

    @classmethod
    def from_regular_xsoar_date_range_args(cls, the_args: dict) -> (NitroDate, NitroDate):
        ret = [NitroUndefinedDate(), NitroUndefinedDate()]
        if isinstance(the_args, dict):
            for word, i, hint in [("from", 0, NitroDateHint.Past), ("to", 1, NitroDateHint.Future)]:
                if isinstance(tmp := the_args.get(word, None), str):
                    nitro_date = cls.from_regular_xsoar_date_range_arg(arg=tmp, hint=hint)
                    # print(f"arg={tmp}, hint={hint}, date={nitro_date}")
                    if isinstance(nitro_date, NitroDate):
                        ret[i] = nitro_date
        return ret

    @classmethod
    def datetime_to_iso8601(cls, date: datetime = None):
        if isinstance(date, datetime):
            return date.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")

    @classmethod
    def datetime_to_utc_datetime(cls, date: datetime = None):
        if isinstance(date, datetime):
            return date.astimezone(timezone.utc)
