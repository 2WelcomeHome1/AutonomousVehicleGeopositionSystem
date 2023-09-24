from pubnub.pnconfiguration import PNConfiguration

class PubNub_Connection(PNConfiguration):
    def __init__(self):
        super().__init__()
        self.subscribe_key = "sub-c-f7df9fe1-d873-4c52-b6d1-d09161021e5d"
        self.publish_key = "pub-c-8488393d-d966-4f8a-bbe9-3ec83cbb4a2f"
        self.user_id = "111"
        self.ssl = False

    def _pnconfig(self):
        return self