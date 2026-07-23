const fs = require('fs');
const path = require('path');

function generateDataset(outputPath, numRecords = 50000) {
  console.log(`Generating ${numRecords} credit card transactions...`);
  
  const categories = [
    "Online Retail", "Electronics", "Grocery", "Dining",
    "Travel & Hotels", "Luxury Goods", "Gas Station", "Entertainment"
  ];

  const catWeights = {
    "Online Retail": 1.8, "Electronics": 2.2, "Luxury Goods": 2.5,
    "Travel & Hotels": 1.5, "Entertainment": 1.1, "Dining": 0.6,
    "Gas Station": 0.7, "Grocery": 0.4
  };

  const customers = Array.from({length: 2000}, (_, i) => `CUST_${String(i+1).padStart(4, '0')}`);
  const customerMedians = {};
  customers.forEach(c => {
    customerMedians[c] = parseFloat((Math.random() * 165 + 15).toFixed(2));
  });

  const headers = [
    "transaction_id", "timestamp", "customer_id", "amount",
    "merchant_category", "distance_from_home", "ratio_to_median_price",
    "repeat_retailer", "used_chip", "used_pin", "is_online_order", "is_fraud"
  ];

  const rows = [headers.join(',')];
  let fraudCount = 0;
  const startDate = new Date();
  startDate.setDate(startDate.getDate() - 90);

  for (let i = 1; i <= numRecords; i++) {
    const txnId = `TXN_${String(i).padStart(6, '0')}`;
    const custId = customers[Math.floor(Math.random() * customers.length)];
    const cMedian = customerMedians[custId];

    const randomMinutes = Math.floor(Math.random() * (90 * 24 * 60));
    const txnDate = new Date(startDate.getTime() + randomMinutes * 60000);
    const hour = txnDate.getHours();

    const isOnline = Math.random() < 0.45 ? 1 : 0;
    const merchantCat = categories[Math.floor(Math.random() * categories.length)];
    const repeatRetailer = Math.random() < 0.65 ? 1 : 0;

    let usedChip = 0, usedPin = 0;
    if (!isOnline) {
      usedChip = Math.random() < 0.85 ? 1 : 0;
      usedPin = Math.random() < 0.70 ? 1 : 0;
    }

    let distance = Math.random() < 0.90 ? parseFloat((Math.random() * 25 + 0.1).toFixed(2)) : parseFloat((Math.random() * 800 + 50).toFixed(2));
    
    let baseRisk = catWeights[merchantCat] * 0.015;
    if ([1, 2, 3, 4].includes(hour)) baseRisk *= 2.5;
    if (isOnline && !usedPin) baseRisk *= 1.8;
    if (distance > 100) baseRisk *= 2.2;

    const isFraud = Math.random() < Math.min(baseRisk, 0.45) ? 1 : 0;
    let ratioToMedian, amount;

    if (isFraud === 1) {
      fraudCount++;
      ratioToMedian = parseFloat((Math.random() * 11.3 + 3.2).toFixed(2));
      amount = parseFloat((cMedian * ratioToMedian).toFixed(2));
      if (Math.random() < 0.4) distance = parseFloat((Math.random() * 1380 + 120).toFixed(2));
    } else {
      ratioToMedian = parseFloat((Math.random() * 1.5 + 0.3).toFixed(2));
      amount = parseFloat((cMedian * ratioToMedian).toFixed(2));
    }

    amount = Math.max(0.99, amount);

    const tsStr = txnDate.toISOString().replace('T', ' ').substring(0, 19);
    rows.push([
      txnId, tsStr, custId, amount.toFixed(2), merchantCat,
      distance.toFixed(2), ratioToMedian.toFixed(2), repeatRetailer,
      usedChip, usedPin, isOnline, isFraud
    ].join(','));
  }

  fs.mkdirSync(path.dirname(outputPath), { recursive: true });
  fs.writeFileSync(outputPath, rows.join('\n'), 'utf-8');

  console.log(`Generated ${numRecords} records (${fraudCount} frauds / ${(fraudCount/numRecords*100).toFixed(2)}%) at '${outputPath}'`);
}

if (require.main === module) {
  const targetCsv = path.join(__dirname, '..', 'data', 'raw_transactions.csv');
  generateDataset(targetCsv, 50000);
}

module.exports = { generateDataset };
