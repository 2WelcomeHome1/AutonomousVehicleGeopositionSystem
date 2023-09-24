from pubnub.pnconfiguration import PNConfiguration

class PubNub_Connection(PNConfiguration):
    def __init__(self):
        super().__init__()
        self.subscribe_key = "#"
        self.publish_key = "# "
        self.user_id = "111"
        self.ssl = False

    def _pnconfig(self):
        return self
