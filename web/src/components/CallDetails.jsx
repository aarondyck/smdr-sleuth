import React from 'react';

const CallDetails = ({ call, onClose }) => {
  if (!call) return null;
  return (
    <div className="call-details-modal">
      <button onClick={onClose}>Close</button>
      <h2>Call Details (Call ID: {call.call_id})</h2>
      <ul>
        {call.legs && call.legs.map((leg, idx) => (
          <li key={idx}>
            <strong>Leg {idx + 1}:</strong> {JSON.stringify(leg)}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default CallDetails;
