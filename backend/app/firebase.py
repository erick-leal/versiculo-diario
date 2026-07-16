import base64
import json

import firebase_admin
from firebase_admin import credentials

from app.core.config import settings

_service_account_info = json.loads(base64.b64decode(settings.firebase_service_account_base64))
_cred = credentials.Certificate(_service_account_info)
firebase_app = firebase_admin.initialize_app(_cred)
