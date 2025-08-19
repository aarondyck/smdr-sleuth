import React from 'react';

const CallTable = ({ calls }) => {
  // Show only basic columns
    // Debugging output
    console.log('CallTable received calls:', calls);
    // Columns to display (customizable for future user selection)
    const columns = [
      { key: 'call_id', label: 'Call ID' },
      { key: 'call_start_time', label: 'Call Start Time' },
      { key: 'caller', label: 'Caller Number' },
      { key: 'party1_name', label: 'Party1 Name' },
      { key: 'call_type', label: 'Call Type' },
      { key: 'called_number', label: 'Called Number' },
      { key: 'dialed_number', label: 'Dialed Number' },
      { key: 'party2_name', label: 'Party2 Name' },
    ];

    // Helper to get call type from direction and is_internal
    function getCallType(call) {
      const dir = call.direction;
      const internal = call.is_internal;
      if (internal === true) return 'Internal Call';
      if (dir === 'I' && internal === false) return 'Incoming External Call';
      if (dir === 'O' && internal === false) return 'Outgoing External Call';
      return 'Unknown';
    }
    console.log('Rendering columns:', columns);
  return (
    <table style={{ width: '100%', borderCollapse: 'collapse', margin: '1rem 0' }}>
      <thead>
        <tr>
          {columns.map(col => (
            <th key={col.key} style={{ borderBottom: '2px solid #1976d2', padding: '0.5rem', background: '#f0f4fa', textAlign: 'left' }}>{col.label}</th>
          ))}
        </tr>
      </thead>
      <tbody>
        {calls.map((call, idx) => (
          <tr key={call.call_id ?? idx} style={{ background: idx % 2 === 0 ? '#fff' : '#f5f5f5' }}>
            {columns.map(col => (
              <td key={col.key} style={{ padding: '0.5rem', borderBottom: '1px solid #e0e0e0' }}>
                {col.key === 'call_type' ? getCallType(call) : call[col.key]}
              </td>
            ))}
          </tr>
        ))}
      </tbody>
    </table>
  );
};

export default CallTable;
