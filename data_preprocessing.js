const fs = require('fs');
const path = require('path');

function preprocessData(rawCsvPath, cleanedCsvPath, powerBiCsvPath) {
  console.log(`Reading raw transactions from '${rawCsvPath}'...`);
  const content = fs.readFileSync(rawCsvPath, 'utf-8');
  const lines = content.trim().split('\n');
  const headers = lines[0].split(',');

  const newHeaders = [
    ...headers,
    "hour_of_day", "day_of_week", "is_night_transaction",
    "high_risk_amount_flag", "distance_anomaly_flag", "risk_severity_score"
  ];

  const cleanedRows = [newHeaders.join(',')];
  let totalAmount = 0;
  let fraudAmount = 0;
  let fraudCount = 0;

  const days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];

  for (let i = 1; i < lines.length; i++) {
    const cols = lines[i].split(',');
    if (cols.length < 12) continue;

    const [txnId, ts, custId, amtStr, cat, distStr, ratioStr, repeat, chip, pin, online, fraudStr] = cols;
    const amount = parseFloat(amtStr);
    const distance = parseFloat(distStr);
    const ratio = parseFloat(ratioStr);
    const isFraud = parseInt(fraudStr, 10);
    const isOnline = parseInt(online, 10);
    const usedPin = parseInt(pin, 10);

    const dt = new Date(ts);
    const hour = dt.getHours();
    const dayOfWeek = days[dt.getDay()] || "Monday";

    const isNight = [22, 23, 0, 1, 2, 3, 4, 5].includes(hour) ? 1 : 0;
    const highRiskAmount = ratio >= 3.0 ? 1 : 0;
    const distanceAnomaly = distance >= 100.0 ? 1 : 0;

    let riskScore = 0.0;
    if (ratio >= 3.0) riskScore += 35.0;
    if (distanceAnomaly) riskScore += 25.0;
    if (isNight) riskScore += 15.0;
    if (isOnline && !usedPin) riskScore += 15.0;
    if (["Electronics", "Luxury Goods", "Online Retail"].includes(cat)) riskScore += 10.0;
    riskScore = Math.min(100.0, riskScore);

    const row = [
      txnId, ts, custId, amount.toFixed(2), cat, distance.toFixed(2),
      ratio.toFixed(2), repeat, chip, pin, online, isFraud,
      hour, dayOfWeek, isNight, highRiskAmount, distanceAnomaly, riskScore.toFixed(1)
    ];

    cleanedRows.push(row.join(','));
    totalAmount += amount;
    if (isFraud === 1) {
      fraudCount++;
      fraudAmount += amount;
    }
  }

  fs.mkdirSync(path.dirname(cleanedCsvPath), { recursive: true });
  fs.writeFileSync(cleanedCsvPath, cleanedRows.join('\n'), 'utf-8');

  fs.mkdirSync(path.dirname(powerBiCsvPath), { recursive: true });
  fs.writeFileSync(powerBiCsvPath, cleanedRows.join('\n'), 'utf-8');

  console.log("Data Preprocessing Completed!");
  console.log(` - Processed Records: ${cleanedRows.length - 1}`);
  console.log(` - Total Volume: $${totalAmount.toLocaleString('en-US', {minimumFractionDigits: 2})}`);
  console.log(` - Total Fraud Loss: $${fraudAmount.toLocaleString('en-US', {minimumFractionDigits: 2})} (${fraudCount} txns)`);
  console.log(` - Saved cleaned data to '${cleanedCsvPath}'`);
  console.log(` - Saved Power BI dataset to '${powerBiCsvPath}'`);
}

if (require.main === module) {
  const baseDir = path.join(__dirname, '..');
  const rawPath = path.join(baseDir, 'data', 'raw_transactions.csv');
  const cleanedPath = path.join(baseDir, 'data', 'cleaned_transactions.csv');
  const pbiPath = path.join(baseDir, 'data', 'power_bi_export.csv');
  preprocessData(rawPath, cleanedPath, pbiPath);
}

module.exports = { preprocessData };
