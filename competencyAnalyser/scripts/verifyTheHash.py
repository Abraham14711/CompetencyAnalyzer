import hashlib
import hmac
import time
from competencyAnalyser.config import BOT_TOKEN


def verify_telegram_authentication(request_data: dict):
    try:
        request_data = request_data.copy()
        received_hash = request_data['hash']
        auth_date = request_data['auth_date']

        request_data.pop('hash', None)
        request_data_alphabetical_order = sorted(request_data.items(),
                                                 key=lambda x: x[0])

        data_check_string = []

        for data_pair in request_data_alphabetical_order:
            key, value = data_pair[0], data_pair[1]
            data_check_string.append(key + '=' + value)

        data_check_string = '\n'.join(data_check_string)

        secret_key = hashlib.sha256(BOT_TOKEN.encode()).digest()
        _hash = hmac.new(secret_key, msg=data_check_string.encode(),
                         digestmod=hashlib.sha256).hexdigest()

        unix_time_now = float(time.time())
        unix_time_auth_date = float(auth_date)

        if unix_time_now - unix_time_auth_date > 86400:
            return False

        if _hash != received_hash:
            return False

        return True
    except:
        return False
