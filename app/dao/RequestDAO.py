import math

from app import db
from app.model.Request import Request, Status
from sqlalchemy import extract, desc, asc


def find_all_waiting_request(page=1, limit=5, order=None, date=None):
    query = Request.query.filter(Request.status == Status.WAIT)

    if date:  # assuming date is a datetime.date or datetime.datetime object
        date_arr = date.split('-')
        query = query.filter(
            extract('month', Request.created_at) == date_arr[1],
            extract('year', Request.created_at) == date_arr[0]
        )
    if order:
        if order == 'latest':
            query = query.order_by(desc(getattr(Request, "created_at")))
        elif order == 'oldest':
            query = query.order_by(asc(getattr(Request, "created_at")))

    start = (page - 1) * limit
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
