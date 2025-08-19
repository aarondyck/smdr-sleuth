import React from 'react';

const CallFilters = ({ filters, onChange }) => {
  return (
    <form>
      <label>
        Start Time:
        <input type="datetime-local" name="start_time" value={filters.start_time} onChange={onChange} />
      </label>
      <label>
        End Time:
        <input type="datetime-local" name="end_time" value={filters.end_time} onChange={onChange} />
      </label>
      <label>
        Caller:
        <input type="text" name="caller" value={filters.caller} onChange={onChange} />
      </label>
      <label>
        Called Number:
        <input type="text" name="called_number" value={filters.called_number} onChange={onChange} />
      </label>
      <label>
        Direction:
        <select name="direction" value={filters.direction} onChange={onChange}>
          <option value="">Any</option>
          <option value="I">Inbound</option>
          <option value="O">Outbound</option>
        </select>
      </label>
      <button type="submit">Apply Filters</button>
    </form>
  );
};

export default CallFilters;
