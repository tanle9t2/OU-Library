import math

from app import db
from app.model.Request import Request, Status


def find_all_waiting_request(page=0, limit=5):
    query = Request.query.filter(Request.status == Status.WAIT)

    start = page * limit
    end = start + limit
    query_count = query
    total = query_count.count()
    total_page = math.ceil(total / limit)
    query = query.slice(start, end)
    requests = query.all()

    return {
        'total_request': total,
        'current_page': page,
        'pages': total_page,
        'request': requests,
    }


def accept_request(id):
    request = Request.query.get(id)
    request.status = Status.ACCEPT

    db.session.commit()


def cancel_request(id, note):
    request = Request.query.get(id)
    request.status = Status.CANCEL
    request.note = note
    db.session.commit()
