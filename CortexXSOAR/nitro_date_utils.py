from abc import ABC
from datetime import datetime, timezone
from enum import Enum
import dateutil


class NitroDate(ABC):
    """ Base line Nitro wrapper around datetime.datetime"""
    def __init__(self, date: datetime = None):
        """
        :type date: ``datetime``
        :param date: the underlying datetime
        """
        self.date = date

    def __repr__(self):
        """a NitroDate is usually represented by the date it wraps"""
        return str(self.date)

    def is_ready(self):
        """
        :return: whether the NitroDate is ready
        :rtype: ``bool``
        """
        if self.date is None:
            return False
        elif isinstance(self.date, datetime):
            return True
        else:
            raise NitroDateInconsistentError

    def to_iso8601(self):
        """ returns the NitraDate in the iso8601 format"""
        raise NotImplementedError()

    def to_getincidentsbyquery_arg(self):
        """ returns the NitraDate in a format that is suitable to use in xsoar incident queries"""
        return self.to_iso8601()


class NitroDateInconsistentError(Exception):
    pass
# custom exception raised when a NitroDate does not have a valid datetime.datetime in it


class NitroDateParsingError(Exception):
    pass
# custom exception raised when an Error is Caught while parsing a datetime.datetime in a NitroDate


class NitroUnlimitedPastDate(NitroDate):
    def __repr__(self):
        """the representation of a NitroUnlimitedPastDate is meant to be explicit"""
        return "NitroUnlimitedPastDate"

    def to_iso8601(self):
        return NitroDateFactory.datetime_to_iso8601(date=self.date)


class NitroUnlimitedFutureDate(NitroDate):
    def __repr__(self):
        """the representation of a NitroUnlimitedFutureDate is meant to be explicit"""
        return "NitroUnlimitedFutureDate"

    def to_iso8601(self):
        return NitroDateFactory.datetime_to_iso8601(date=self.date)


class NitroUndefinedDate(NitroDate):
    def __repr__(self):
        """the representation of a NitroUndefinedDate is meant to be explicit"""
        return "NitroUndefinedDate"

    def to_iso8601(self):
        raise NotImplementedError


class NitroRegularDate(NitroDate):
    def __init__(self, date: datetime = None):
        """
        :type date: ``datetime``
        :param date: the underlying datetime
        """
        super(NitroRegularDate, self).__init__(date=date)

    def to_iso8601(self):
        """ returns the NitraDate in the iso8601 format"""
        return NitroDateFactory.datetime_to_iso8601(date=self.date)


class NitroDateHint(Enum):
    Future = 1
    Past = 2
# a NitroEnum used as a flag for functions that build NitroDates and let's them know whether or not we have
# an indication as to whether an undefined date we're parsing should be future or past


class NitroDateFactory(ABC):
    """this class is a factory, as in it's able to generate NitroDates from a variety of initial arguments"""
    @classmethod
    def from_iso_8601_string(cls, arg: str = ""):
        """
        this function is able to create a NitroDate from an iso 8601 datestring
        :param arg: the iso 8601 string
        :type arg: str
        """
        try:
            date = dateutil.parser.isoparse(arg)
        except Exception as e:
            raise NitroDateParsingError from e
        return NitroRegularDate(date=date)

    @classmethod
    def from_regular_xsoar_date_range_arg(cls, arg: str = "", hint: NitroDateHint = None):
        """
        this function is able to create a NitroDate from a single argument passed by
        a xsoar GUI element and a Hint
        :param arg: the iso 8601 string or cheatlike string
        :type arg: str
        :param hint: a hint to know whether the date, if a predetermined value, should be interpreted as future or past
        :type hint: NitroDateHint
        """
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
        """
        this function is able to create NitroDates from the two arguments passed by
        a xsoar GUI element
        :param the_args: the args passed to the xsoar automation by the timepicker GUI element
        :type the_args: dict
        """
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
        """
        :type date: ``datetime.datetime``
        :param date: the datetime to convert

        :return: an ISO 8601 string returned in the UTC timezone, this maximizes encoding compatibility
        :rtype: ``str``
        """
        if isinstance(date, datetime):
            return date.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")

    @classmethod
    def datetime_to_utc_datetime(cls, date: datetime = None):
        """
        :type date: ``datetime.datetime``
        :param date: the datetime to convert

        :return: a datetime set in the UTC timezone
        :rtype: ``datetime.datetime``
        """
        if isinstance(date, datetime):
            return date.astimezone(timezone.utc)
