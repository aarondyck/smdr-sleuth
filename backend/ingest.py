import csv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import SMDRRecord, Base

DB_FILENAME = 'smdr.db'
DB_URL = f'sqlite:///{DB_FILENAME}'

engine = create_engine(DB_URL)
Session = sessionmaker(bind=engine)

FIELD_NAMES = [
    'call_start_time', 'connected_time', 'ring_time', 'caller', 'direction', 'called_number',
    'dialed_number', 'account_code', 'is_internal', 'call_id', 'continuation', 'party1_device',
    'party1_name', 'party2_device', 'party2_name', 'hold_time', 'park_time', 'authorization_valid',
    'authorization_code', 'user_charged', 'call_charge', 'currency', 'amount_at_last_user_change',
    'call_units', 'units_at_last_user_change', 'cost_per_unit', 'mark_up', 'external_targeting_cause',
    'external_targeter_id', 'external_targeted_number', 'calling_party_server_ip', 'unique_call_id_caller',
    'called_party_server_ip', 'unique_call_id_called', 'smdr_record_time', 'caller_consent_directive',
    'calling_number_verification'
]

def ingest_csv(csv_file_path):
    session = Session()
    with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile, fieldnames=FIELD_NAMES)
        for row in reader:
            record = SMDRRecord(**row)
            session.add(record)
        session.commit()
    print(f"Ingested SMDR records from {csv_file_path}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python ingest.py <smdr_csv_file>")
    else:
        ingest_csv(sys.argv[1])
