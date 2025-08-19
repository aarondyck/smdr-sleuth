// API utility for SMDR web interface

const API_BASE = '';

export async function fetchCalls({ start_time, end_time, direction, caller, called_number, limit = 25, offset = 0 }) {
  const params = new URLSearchParams();
  if (start_time) params.append('start_time', start_time);
  if (end_time) params.append('end_time', end_time);
  if (direction) params.append('direction', direction);
  if (caller) params.append('caller', caller);
  if (called_number) params.append('called_number', called_number);
  params.append('limit', limit);
  params.append('offset', offset);
  const url = `${API_BASE}/calls?${params.toString()}`;
  const res = await fetch(url);
  if (!res.ok) throw new Error('Failed to fetch calls');
  return await res.json();
}

export async function fetchCallDetails(call_id) {
  const url = `${API_BASE}/records/${call_id}`;
  const res = await fetch(url);
  if (!res.ok) throw new Error('Failed to fetch call details');
  return await res.json();
}
