import socket
import csv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import SMDRRecord, Base

DB_FILENAME = 'smdr.db'
DB_URL = f'sqlite:///{DB_FILENAME}'
engine = create_engine(DB_URL)
Session = sessionmaker(bind=engine)

LISTEN_IP = '0.0.0.0'  # Listen on all interfaces
LISTEN_PORT = 5000      # Change to your configured SMDR port
BUFFER_SIZE = 4096


# Field names and expected types for conversion
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

FIELD_TYPES = {
    'call_start_time': str,
    'connected_time': str,
    'ring_time': int,
    'caller': str,
    'direction': str,
    'called_number': str,
    'dialed_number': str,
    'account_code': str,
    'is_internal': lambda v: v == '1',
    'call_id': int,
    'continuation': lambda v: v == '1',
    'party1_device': str,
    'party1_name': str,
    'party2_device': str,
    'party2_name': str,
    'hold_time': int,
    'park_time': int,
    'authorization_valid': lambda v: v == '1',
    'authorization_code': str,
    'user_charged': str,
    'call_charge': lambda v: float(v) if v else None,
    'currency': str,
    'amount_at_last_user_change': lambda v: float(v) if v else None,
    'call_units': lambda v: int(v) if v else None,
    'units_at_last_user_change': lambda v: int(v) if v else None,
    'cost_per_unit': lambda v: float(v) if v else None,
    'mark_up': lambda v: float(v) if v else None,
    'external_targeting_cause': str,
    'external_targeter_id': str,
    'external_targeted_number': str,
    'calling_party_server_ip': str,
    'unique_call_id_caller': lambda v: int(v) if v else None,
    'called_party_server_ip': str,
    'unique_call_id_called': lambda v: int(v) if v else None,
    'smdr_record_time': str,
    'caller_consent_directive': lambda v: int(v) if v else None,
    'calling_number_verification': str
}

def convert_row_types(row):
    converted = {}
    for k, v in row.items():
        if k is None:
            continue  # Skip extra columns
        key = str(k).strip()
        value = v.strip() if isinstance(v, str) else v
        converter = FIELD_TYPES.get(key, str)
        try:
            converted[key] = converter(value) if value != '' else None
        except Exception:
            converted[key] = None
    return converted

def handle_connection(conn, addr):
    print(f"Connection from {addr}")
    session = Session()
    buffer = ''
    record_count = 0
    error_count = 0
    try:
        while True:
            data = conn.recv(BUFFER_SIZE)
            if not data:
                break
            buffer += data.decode('utf-8', errors='replace')
            while '\n' in buffer:
                line, buffer = buffer.split('\n', 1)
                if line.strip():
                    try:
                        reader = csv.DictReader([line], fieldnames=FIELD_NAMES)
                        for row in reader:
                            converted_row = convert_row_types(row)
                            record = SMDRRecord(**converted_row)
                            session.add(record)
                            try:
                                session.commit()
                                print(f"Record committed for {addr}.")
                            except Exception as commit_err:
                                session.rollback()
                                error_count += 1
                                print(f"Database error for {addr}: {commit_err}. Rolled back transaction.")
                            record_count += 1
                    except Exception as parse_err:
                        error_count += 1
                        print(f"Malformed record from {addr}: {line}\nError: {parse_err}")
    except Exception as e:
        print(f"Error handling connection from {addr}: {e}")
    finally:
        conn.close()


def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((LISTEN_IP, LISTEN_PORT))
        s.listen()
        print(f"SMDR server listening on {LISTEN_IP}:{LISTEN_PORT}")
        while True:
            conn, addr = s.accept()
            handle_connection(conn, addr)

if __name__ == "__main__":
    start_server()
