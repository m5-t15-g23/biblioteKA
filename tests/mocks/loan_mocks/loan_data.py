from datetime import datetime as dt, timedelta as td

from loans.serializers import return_date

loan_data = {
    "new_loan": {
        "loan_date": str(dt.now().date()),
        "loan_return": str(return_date()),
        "is_active": True,
        "returned_at": None
    }
}
