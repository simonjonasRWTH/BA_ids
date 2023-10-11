import json 
import ipal_iids.settings as settings
from ids.ids import MetaIDS

class tcp_ids(MetaIDs):
    __name = "tcp IDS"
    __description = "tcp based ids"
    __requires = ["train.ipal","live.ipal"]
    __tcp_default_settings = {
        "allow-zero-winsize" : False,
        "allow-port-scan" : False,
        }
    __supports_preprocessor=False

    def __init__(self, name=None):
        super().__init__(name=name)
        self._add_default_settings(self.__tcp_default_settings)

        self.flows = {}
        self.ratios = {
            "SYN" : None,
            "ACK" : None,
            "FIN" : None,
            "RST" : None,
            "PSH" : None,
            "URG" : None,
        }    # keep track of rations of Flags, if deviates too much -> flooding

    def _get_flow(self, msg):
        # compute flow identifier by concatenating source, source port, destination, port and message type
        
    def train(self, ipal=None, state=None):
        with self._open_file(ipal) as f:
            for line in f.readlines():
                ipal_msg = json.loads(line)
                timestamp = ipal_msg["timestamp"]


