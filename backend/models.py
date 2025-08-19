from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class SMDRRecord(Base):
    __tablename__ = 'smdr_records'

    id = Column(Integer, primary_key=True, autoincrement=True)
    call_start_time = Column(String, nullable=False)  # YYYY/MM/DD HH:MM:SS
    connected_time = Column(String, nullable=False)   # HH:MM:SS
    ring_time = Column(Integer, nullable=False)       # seconds
    caller = Column(String)
    direction = Column(String(1))
    called_number = Column(String)
    dialed_number = Column(String)
    account_code = Column(String)
    is_internal = Column(Boolean)
    call_id = Column(Integer, nullable=False)
    continuation = Column(Boolean)
    party1_device = Column(String)
    party1_name = Column(String)
    party2_device = Column(String)
    party2_name = Column(String)
    hold_time = Column(Integer)
    park_time = Column(Integer)
    authorization_valid = Column(Boolean)
    authorization_code = Column(String)
    user_charged = Column(String)
    call_charge = Column(Float)
    currency = Column(String)
    amount_at_last_user_change = Column(Float)
    call_units = Column(Integer)
    units_at_last_user_change = Column(Integer)
    cost_per_unit = Column(Float)
    mark_up = Column(Float)
    external_targeting_cause = Column(String)
    external_targeter_id = Column(String)
    external_targeted_number = Column(String)
    calling_party_server_ip = Column(String)
    unique_call_id_caller = Column(Integer)
    called_party_server_ip = Column(String)
    unique_call_id_called = Column(Integer)
    smdr_record_time = Column(String)
    caller_consent_directive = Column(Integer)
    calling_number_verification = Column(String)
