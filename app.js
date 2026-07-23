document.addEventListener('DOMContentLoaded', () => {
  // Sample analytical data matching synthetic distributions
  const categoryData = {
    labels: ['Electronics', 'Luxury Goods', 'Online Retail', 'Travel & Hotels', 'Entertainment', 'Gas Station', 'Dining', 'Grocery'],
    fraudLoss: [142500, 118400, 98200, 41200, 15300, 8400, 3100, 1850],
    fraudRate: [8.4, 7.8, 6.2, 4.5, 3.1, 2.1, 1.4, 0.9]
  };

  const hourlyData = {
    labels: ['00:00', '01:00', '02:00', '03:00', '04:00', '05:00', '06:00', '07:00', '08:00', '09:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00', '20:00', '21:00', '22:00', '23:00'],
    rates: [4.2, 9.8, 12.4, 14.1, 11.2, 5.8, 2.1, 1.4, 1.2, 1.5, 1.8, 2.1, 2.4, 2.2, 2.0, 2.3, 2.5, 2.8, 3.1, 3.4, 4.0, 4.5, 5.6, 6.8]
  };

  const sampleHighRiskTransactions = [
    { id: 'TXN_004821', time: '2026-07-23 02:41:15', cust: 'CUST_0412', amount: 1450.00, cat: 'Electronics', ratio: 8.5, dist: 340.2, score: 92.5, status: 1 },
    { id: 'TXN_008912', time: '2026-07-23 03:12:09', cust: 'CUST_1189', amount: 2890.50, cat: 'Luxury Goods', ratio: 11.2, dist: 512.0, score: 98.0, status: 1 },
    { id: 'TXN_012410', time: '2026-07-23 01:18:44', cust: 'CUST_0094', amount: 620.00, cat: 'Online Retail', ratio: 4.8, dist: 180.5, score: 78.5, status: 1 },
    { id: 'TXN_015904', time: '2026-07-23 04:05:30', cust: 'CUST_0762', amount: 980.25, cat: 'Travel & Hotels', ratio: 5.4, dist: 720.0, score: 85.0, status: 1 },
    { id: 'TXN_020119', time: '2026-07-23 02:55:01', cust: 'CUST_1520', amount: 1200.00, cat: 'Electronics', ratio: 6.9, dist: 290.8, score: 88.0, status: 1 },
    { id: 'TXN_024881', time: '2026-07-23 14:22:10', cust: 'CUST_0311', amount: 310.00, cat: 'Grocery', ratio: 1.2, dist: 4.5, score: 15.0, status: 0 },
    { id: 'TXN_029104', time: '2026-07-23 03:40:12', cust: 'CUST_0843', amount: 1750.00, cat: 'Luxury Goods', ratio: 7.8, dist: 410.0, score: 91.0, status: 1 }
  ];

  // 1. Merchant Category Chart
  const catCtx = document.getElementById('categoryChart').getContext('2d');
  const categoryChart = new Chart(catCtx, {
    type: 'bar',
    data: {
      labels: categoryData.labels,
      datasets: [
        {
          label: 'Total Fraud Loss ($)',
          data: categoryData.fraudLoss,
          backgroundColor: 'rgba(255, 71, 87, 0.75)',
          borderColor: '#ff4757',
          borderWidth: 1,
          borderRadius: 6,
          yAxisID: 'y'
        },
        {
          label: 'Fraud Rate (%)',
          data: categoryData.fraudRate,
          type: 'line',
          borderColor: '#ffa502',
          backgroundColor: '#ffa502',
          pointRadius: 4,
          borderWidth: 2,
          yAxisID: 'y1'
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        x: { ticks: { color: '#94a3b8' }, grid: { display: false } },
        y: { 
          position: 'left',
          ticks: { color: '#94a3b8', callback: (val) => '$' + (val / 1000) + 'k' },
          grid: { color: 'rgba(255, 255, 255, 0.05)' }
        },
        y1: {
          position: 'right',
          ticks: { color: '#ffa502', callback: (val) => val + '%' },
          grid: { display: false }
        }
      },
      plugins: {
        legend: { labels: { color: '#f1f5f9' } }
      }
    }
  });

  // 2. Hourly Fraud Spike Chart
  const hourlyCtx = document.getElementById('hourlyChart').getContext('2d');
  const hourlyChart = new Chart(hourlyCtx, {
    type: 'line',
    data: {
      labels: hourlyData.labels,
      datasets: [{
        label: 'Fraud Rate %',
        data: hourlyData.rates,
        borderColor: '#ff4757',
        backgroundColor: 'rgba(255, 71, 87, 0.15)',
        fill: true,
        tension: 0.4,
        pointRadius: 3,
        pointHoverRadius: 6
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        x: { ticks: { color: '#94a3b8' }, grid: { color: 'rgba(255, 255, 255, 0.04)' } },
        y: { 
          ticks: { color: '#ff4757', callback: (val) => val + '%' },
          grid: { color: 'rgba(255, 255, 255, 0.05)' }
        }
      },
      plugins: {
        legend: { display: false }
      }
    }
  });

  // 3. Scatter Plot for Anomalies
  const scatterCtx = document.getElementById('scatterChart').getContext('2d');
  
  const legitScatter = [];
  const fraudScatter = [];
  
  for (let i = 0; i < 60; i++) {
    legitScatter.push({ x: Math.random() * 50, y: (Math.random() * 2.5 + 0.2).toFixed(2) });
  }
  for (let i = 0; i < 30; i++) {
    fraudScatter.push({ x: (Math.random() * 800 + 80).toFixed(1), y: (Math.random() * 10 + 3.2).toFixed(2) });
  }

  const scatterChart = new Chart(scatterCtx, {
    type: 'scatter',
    data: {
      datasets: [
        {
          label: 'Legitimate Transactions',
          data: legitScatter,
          backgroundColor: 'rgba(46, 213, 115, 0.6)',
          pointRadius: 5
        },
        {
          label: 'Fraudulent Anomalies',
          data: fraudScatter,
          backgroundColor: 'rgba(255, 71, 87, 0.85)',
          pointRadius: 7,
          pointStyle: 'triangle'
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        x: { 
          title: { display: true, text: 'Distance from Home (Miles)', color: '#94a3b8' },
          ticks: { color: '#94a3b8' },
          grid: { color: 'rgba(255, 255, 255, 0.05)' }
        },
        y: { 
          title: { display: true, text: 'Ratio to Customer Median Price', color: '#94a3b8' },
          ticks: { color: '#94a3b8' },
          grid: { color: 'rgba(255, 255, 255, 0.05)' }
        }
      },
      plugins: {
        legend: { labels: { color: '#f1f5f9' } }
      }
    }
  });

  // 4. Render Table
  const tbody = document.getElementById('transactions-tbody');
  
  function renderTable(data) {
    tbody.innerHTML = '';
    data.forEach(txn => {
      const tr = document.createElement('tr');
      const statusBadge = txn.status === 1 
        ? `<span class="badge badge-fraud">Confirmed Fraud</span>` 
        : `<span class="badge badge-legit">Legitimate</span>`;

      tr.innerHTML = `
        <td style="font-family: monospace; font-weight: 600;">${txn.id}</td>
        <td style="color: var(--text-muted);">${txn.time}</td>
        <td>${txn.cust}</td>
        <td style="font-weight: 600;">$${txn.amount.toFixed(2)}</td>
        <td>${txn.cat}</td>
        <td class="risk-pill">${txn.ratio}x</td>
        <td>${txn.dist} mi</td>
        <td><strong style="color: ${txn.score >= 80 ? 'var(--accent-red)' : 'var(--accent-amber)'}">${txn.score}</strong></td>
        <td>${statusBadge}</td>
      `;
      tbody.appendChild(tr);
    });
  }

  renderTable(sampleHighRiskTransactions);

  // Dynamic filter handling
  document.getElementById('filter-category').addEventListener('change', (e) => {
    const val = e.target.value;
    if (val === 'ALL') {
      renderTable(sampleHighRiskTransactions);
    } else {
      const filtered = sampleHighRiskTransactions.filter(t => t.cat === val);
      renderTable(filtered);
    }
  });
});
