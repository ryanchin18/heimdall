"""
The base class for all analysers that used to identify attackers and legitimate HTTP Traffic
"""
from common import SeverityRecord


class BaseAnalyser(object):
    """
    Using various factors identified can calculated by the modeler,
    this will analyse and compute a severity value to reflect the
    possibility of a requester been an attacker.
    The severity factor should be represented by a numerical value.
    """

    def __init__(self, session):
        self._session = session
        self._ANALYSER_INDEX = -1        # since this is an abstract class this is not a actual index
        self._ANALYSER_KEY = "Analyser"  # since this is an abstract class this is not a actual key
        self._WEIGHT = 0
        pass

    def analyse(self):
        """
        Subclasses inherits from this class should override this method to
        perform the factor analyse. And the value of the computed severity factor
        should be used to update the existing severity record for that particular
        session using either update_severity()
        """
        pass

    def update_severity(self, value):
        """

        :param value: computed severity
        :return:
        """

        # TODO : how to update the severity, IT should be weighted

        # update severity after analysing
        severity = SeverityRecord(self._session, value)
        severity.save()
        pass