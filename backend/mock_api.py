class MockAPI:
    RESPONSES = {
        "block_card": "Your card has been blocked.",
        "check_balance": "Your balance is ₹7,520.",
        "convert_emi": "Your purchase was converted into EMI.",
        "track_delivery": "Your card arrives tomorrow.",
        "download_statement": "Statement emailed.",
        "dispute_transaction": "Dispute registered.",
        "raise_complaint": "Complaint raised. Ticket: CC-10452."
    }

    def call(self, intent):
        return self.RESPONSES.get(intent, "Action completed.")
