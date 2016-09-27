import abc
from sponge.objects.document import Document
from sponge.utils import make_uuid

class Contract(Document):
    __metaclass__ = abc.ABCMeta

    def __init__(self, **kwargs):
        self.item = kwargs["item"]
        self.borrower = kwargs["borrower"]
        self.lender = kwargs["lender"]
        self.start_date = kwargs["start_date"]
        self.end_date = kwargs["end_date"]
        self.cost = kwargs["cost"]
        self.confirmed = kwargs.get("confirmed", False)
        self.cancelled = kwargs.get("cancelled", False)
        self.payment_received = kwargs.get("payment_received", False)
        self.payment_sent = kwargs.get("payment_sent", False)
        self.messages = kwargs.get("messages", [])
        self.borrower_feedback = kwargs.get("borrower_feedback", {})
        self.lender_feedback = kwargs.get("lender_feedback", {})
        super(Contract, self).__init__(**kwargs)

    def _json(self):
        return {
            "item": self.item,
            "borrower": self.borrower,
            "lender": self.lender,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "cost": self.cost,
            "confirmed": self.confirmed,
            "cancelled": self.cancelled,
            "payment_received": self.payment_received,
            "payment_sent": self.payment_sent,
            "messages": self.messages,
            "borrower_feedback": self.borrower_feedback,
            "lender_feedback": self.lender_feedback
        }

    def _uuid(self):
        return make_uuid(self.item + self.borrower + self.lender)

    def _valid(self):
        return True