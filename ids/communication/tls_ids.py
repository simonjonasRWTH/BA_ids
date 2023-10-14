import json
import ipal_iids.settings as settings
from ids.ids import MetaIDS

class TLS_IDS(MetaIDS):
    _name = "TLS_IDS"
    _description = "IDS based on TCP"
    _requires = ["train.ipal", "live.ipal"]
    _supports_preprocessor = False #? maybe yes

    def __init__(self, name=None):
        super().__init__(name=name)
        # Was kann ne ids mit TLS machen außer alerts?
        