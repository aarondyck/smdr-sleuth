import { useState, useEffect } from 'react';
import './App.css';
import CallTable from './components/CallTable';
import PaginationControls from './components/PaginationControls';
import { fetchCalls } from './api';
import CallFilters from './components/CallFilters';

function Logo() {
  // Simple placeholder SVG logo
  return (
    <svg width="120" height="60" viewBox="0 0 120 60" xmlns="http://www.w3.org/2000/svg">
      <rect width="120" height="60" rx="12" fill="#1976d2" />
      <text x="60" y="35" textAnchor="middle" fontSize="22" fill="#fff" fontFamily="Arial">SMDR Sleuth</text>
    </svg>
  );
}

function Footer() {
  return (
    <footer style={{marginTop: '2rem', padding: '1rem', textAlign: 'center', background: '#f5f5f5'}}>
      <span>© {new Date().getFullYear()} Bovaird Telecom. All rights reserved. </span>
      <a href="https://bovaird.ca/" target="_blank" rel="noopener noreferrer">bovaird.ca</a>
    </footer>
  );
}

function App() {
  const [calls, setCalls] = useState([]);
  const [filters, setFilters] = useState({
    start_time: '',
    end_time: '',
    caller: '',
    called_number: '',
    direction: ''
  });
  const [page, setPage] = useState(1);
  const [pageSize, setPageSize] = useState(25);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    document.title = "SMDR Sleuth by Bovaird Telecom";
    const fetchData = async () => {
      setLoading(true);
      try {
        const data = await fetchCalls({
          ...filters,
          limit: pageSize,
          offset: (page - 1) * pageSize,
          sort_by: 'call_start_time',
          sort_order: 'desc'
        });
        setCalls(data);
        setTotal(data.length < pageSize ? (page - 1) * pageSize + data.length : page * pageSize + 1); // Approximate
      } catch (err) {
        setCalls([]);
      }
      setLoading(false);
    };
    fetchData();
  }, [filters, page, pageSize]);

  const handleFilterChange = (e) => {
    const { name, value } = e.target;
    setFilters(f => ({ ...f, [name]: value }));
  };

  const handleFilterSubmit = (e) => {
    e.preventDefault();
    setPage(1);
  };

  const handlePageChange = (newPage) => {
    setPage(newPage);
  };

  const handlePageSizeChange = (newSize) => {
    setPageSize(newSize);
    setPage(1);
  };

  return (
    <div className="container" style={{minHeight: '100vh', display: 'flex', flexDirection: 'column'}}>
      <div id="topbar">
        SMDR Sleuth by Bovaird Telecom
      </div>
      <main style={{flex: 1}}>
        <CallFilters filters={filters} onChange={handleFilterChange} onSubmit={handleFilterSubmit} />
        {loading ? <p>Loading...</p> : <CallTable calls={calls} />}
        <PaginationControls
          page={page}
          pageSize={pageSize}
          total={total}
          onPageChange={handlePageChange}
          onPageSizeChange={handlePageSizeChange}
        />
      </main>
      <Footer />
    </div>
  );
}

export default App;
