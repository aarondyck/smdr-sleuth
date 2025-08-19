from fastapi import FastAPI, Query
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from models import SMDRRecord, Base
from typing import List, Optional
from datetime import datetime

DB_FILENAME = 'smdr.db'
DB_URL = f'sqlite:///{DB_FILENAME}'
engine = create_engine(DB_URL)
Session = sessionmaker(bind=engine)


app = FastAPI()

@app.get("/records", response_model=List[dict])
def get_records(
    call_id: Optional[int] = Query(None),
    direction: Optional[str] = Query(None),
    caller: Optional[str] = Query(None),
    called_number: Optional[str] = Query(None),
    start_time: Optional[str] = Query(None, description="Start date/time in YYYY/MM/DD HH:MM:SS format"),
    end_time: Optional[str] = Query(None, description="End date/time in YYYY/MM/DD HH:MM:SS format"),
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    sort_by: Optional[str] = Query('call_start_time'),
    sort_order: Optional[str] = Query('desc')
):
    session = Session()
    query = session.query(SMDRRecord)
    if call_id is not None:
        query = query.filter(SMDRRecord.call_id == call_id)
    if direction is not None:
        query = query.filter(SMDRRecord.direction == direction)
    if caller is not None:
        query = query.filter(SMDRRecord.caller.like(f"%{caller}%"))
    if called_number is not None:
        query = query.filter(SMDRRecord.called_number.like(f"%{called_number}%"))
    if start_time is not None:
        try:
            start_dt = datetime.strptime(start_time, "%Y/%m/%d %H:%M:%S")
            query = query.filter(SMDRRecord.call_start_time >= start_time)
        except Exception:
            pass
    if end_time is not None:
        try:
            end_dt = datetime.strptime(end_time, "%Y/%m/%d %H:%M:%S")
            query = query.filter(SMDRRecord.call_start_time <= end_time)
        except Exception:
            pass
    # Sorting
    if sort_by:
        sort_column = getattr(SMDRRecord, sort_by, None)
        if sort_column is not None:
            if sort_order == 'desc':
                query = query.order_by(sort_column.desc())
            else:
                query = query.order_by(sort_column.asc())
    records = query.offset(offset).limit(limit).all()
    result = [r.__dict__ for r in records]
    for r in result:
        r.pop('_sa_instance_state', None)
    session.close()
    return result


# Consolidated calls endpoint
@app.get("/calls", response_model=List[dict])
def get_consolidated_calls(
    start_time: Optional[str] = Query(None),
    end_time: Optional[str] = Query(None),
    direction: Optional[str] = Query(None),
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    sort_by: Optional[str] = Query('call_start_time'),
    sort_order: Optional[str] = Query('desc')
):
    session = Session()
    query = session.query(SMDRRecord.call_id).distinct()
    if direction is not None:
        query = query.filter(SMDRRecord.direction == direction)
    if start_time is not None:
        try:
            start_dt = datetime.strptime(start_time, "%Y/%m/%d %H:%M:%S")
            query = query.filter(SMDRRecord.call_start_time >= start_time)
        except Exception:
            pass
    if end_time is not None:
        try:
            end_dt = datetime.strptime(end_time, "%Y/%m/%d %H:%M:%S")
            query = query.filter(SMDRRecord.call_start_time <= end_time)
        except Exception:
            pass
    # Sorting
    if sort_by:
        sort_column = getattr(SMDRRecord, sort_by, None)
        if sort_column is not None:
            if sort_order == 'desc':
                query = query.order_by(sort_column.desc())
            else:
                query = query.order_by(sort_column.asc())
    call_ids = [row.call_id for row in query.offset(offset).limit(limit).all()]
    consolidated = []
    for cid in call_ids:
        legs = session.query(SMDRRecord).filter(SMDRRecord.call_id == cid).all()
        # Use the first leg as summary, add all legs for expansion
        summary = legs[0].__dict__.copy()
        summary['legs'] = [leg.__dict__ for leg in legs]
        for leg in summary['legs']:
            leg.pop('_sa_instance_state', None)
        summary.pop('_sa_instance_state', None)
        consolidated.append(summary)
    session.close()
    return consolidated
