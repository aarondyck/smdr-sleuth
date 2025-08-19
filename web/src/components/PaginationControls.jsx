import React from 'react';

const PaginationControls = ({ page, pageSize, total, onPageChange, onPageSizeChange }) => {
  const totalPages = Math.ceil(total / pageSize);
  return (
    <div className="pagination-controls">
      <button disabled={page === 1} onClick={() => onPageChange(page - 1)}>Previous</button>
      <span>Page {page} of {totalPages}</span>
      <button disabled={page === totalPages} onClick={() => onPageChange(page + 1)}>Next</button>
      <select value={pageSize} onChange={e => onPageSizeChange(Number(e.target.value))}>
        {[10, 25, 50, 100].map(size => (
          <option key={size} value={size}>{size} per page</option>
        ))}
      </select>
    </div>
  );
};

export default PaginationControls;
