import os
import re
import requests
import json

# PAN card validation method
def isPanValid(pan):
    if len(pan) == 10:
        Result = re.compile(r"[A-Za-z]{5}\d{4}[A-Za-z]{1}")
        return Result.match(pan)
    else:
        return False


# Aadhaar Card Validation
def isAadhaarValid(aadhaar):
    if len(aadhaar) == 12:
        regex = r"^[0-9]{12}$"
        return re.search(regex, aadhaar)
    else:
        return False


def aadhaar_send_otp(aadhaar_no):
    try:
        if not aadhaar_no:
            error = {
                "name": "AADHAAR_MISSING",
                "message": "Aadhaar information missing",
            }
            return error
        request_data = {
            "consent": "Y",
            "aadhaarNo": aadhaar_no
        }
        payload = json.dumps(request_data)
        if not isAadhaarValid(aadhaar_no):
            error = {
                "name": "INVALID_AADHAAR",
                "message": "Aadhaar number length incorrect"
            }
            return error

        url = "https://testapi.karza.in/v3/aadhaar/otp"
        headers = {
            'x-karza-key': 'sDEtNu339YDuKi5J',
        }
        result = requests.post(url=url, data=payload, headers=headers)
        return result
    except Exception as error:
        error = {"name": "SERVER_ERROR", "message": str(error)}
        return error


# Aadhaar OTP Verify Api based on Digilocker
def aadhaar_verify_otp(otp, aadhaar_no, request_id):
    try:
        if not request_id or not aadhaar_no or not otp:
            error = {
                "name": "Details Missing",
                "message": "Information Missing"
            }
            return error

        request_data = {
            "otp": otp,
            "aadhaarNo": aadhaar_no,
            "requestId": request_id,
            "consent": "Y"
        }
        payload = json.dumps(request_data)
        url = "https://testapi.karza.in/v3/aadhaar/verify-otp"
        headers = {
            'x-karza-key': 'sDEtNu339YDuKi5J',
        }
        result = requests.post(url=url, data=payload, headers=headers)
        return result
    except Exception as error:
        error = {"name": "SERVER_ERROR", "message": str(error)}
        return error

# Aadhaar data download Api based on Digilocker
def aadhaar_download(event, context):
    request_id = event["requestContext"]["requestId"]
    try:
        event_body = json.loads(event["body"])
        if not event_body:
            error = {
                "name": "Details Missing",
                "message": "Information Missing"
            }
            return response.response(request_id, 400, None, error)

        aadhaar_request_id = event_body.get('request_id', None)

        if aadhaar_request_id is None:
            error = {
                "name": "Fields Missing",
                "message": "Field requestId is missing!"
            }
            return response.response(request_id, 400, None, error=error)

        request_data = {
            "requestId": aadhaar_request_id,
            "consent": "Y"
        }

        url = os.environ["KARZA_AADHAAR_OTP_API_URL"] + "/v3/aadhaar/download"
        result = utils.post(request_id, url, request_data)
        return response.response(request_id, 200, res_data=result, error=None)
    except Exception as error:
        error = {"name": "SERVER_ERROR", "message": str(error)}
        return response.response(request_id, 500, None, str(error))