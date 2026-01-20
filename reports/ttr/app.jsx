import React, { useState, useMemo } from 'react';

// Dickens STTR data from analysis
const dickensData = {
  author: "Charles Dickens",
  works: 45,
  totalWords: 4826057,
  sttrValues: [
    0.4123, 0.4153, 0.4056, 0.4665, 0.4173, 0.4397, 0.4130, 0.4190, 0.4271, 0.4205,
    0.4324, 0.4106, 0.4666, 0.4015, 0.3950, 0.3976, 0.4062, 0.4434, 0.4467, 0.4307,
    0.4375, 0.4026, 0.4287, 0.4119, 0.4116, 0.4718, 0.4166, 0.4694, 0.4560, 0.4315,
    0.4318, 0.4166, 0.4390, 0.4026, 0.4511, 0.4210, 0.4535, 0.4563, 0.4271, 0.4448,
    0.4533, 0.4268, 0.4125, 0.4251, 0.4202
  ],
  deltaStdValues: [
    0.0050, 0.0119, 0.0083, 0.0246, 0.0231, 0.0330, 0.0447, 0.0254, 0.0290, 0.0348,
    0.0393, 0.0229, 0.0268, 0.0239, 0.0274, 0.0329, 0.0225, 0.0327, 0.0294, 0.0324,
    0.0314, 0.0135, 0.0350, 0.0325, 0.0329, 0.0268, 0.0341, 0.0288, 0.0363, 0.0430,
    0.0364, 0.0333, 0.0353, 0.0298, 0.0306, 0.0210, 0.0310, 0.0326, 0.0333, 0.0311,
    0.0336, 0.0344, 0.0350, 0.0377, 0.0284
  ],
  workDetails: [
    { title: "The Trial of William Tinkling", words: 3075, sttr: 0.4123, deltaStd: 0.0050 },
    { title: "To Be Read at Dusk", words: 4507, sttr: 0.4153, deltaStd: 0.0119 },
    { title: "Going Into Society", words: 5120, sttr: 0.4056, deltaStd: 0.0083 },
    { title: "Sunday Under Three Heads", words: 11040, sttr: 0.4665, deltaStd: 0.0246 },
    { title: "The Lamplighter", words: 6956, sttr: 0.4173, deltaStd: 0.0231 },
    { title: "The Seven Poor Travellers", words: 10068, sttr: 0.4397, deltaStd: 0.0330 },
    { title: "Tom Tiddler's Ground", words: 9760, sttr: 0.4130, deltaStd: 0.0447 },
    { title: "George Silverman's Explanation", words: 11029, sttr: 0.4190, deltaStd: 0.0254 },
    { title: "The Holly-Tree", words: 13692, sttr: 0.4271, deltaStd: 0.0290 },
    { title: "Holiday Romance", words: 13152, sttr: 0.4205, deltaStd: 0.0348 },
    { title: "Somebody's Luggage", words: 19439, sttr: 0.4324, deltaStd: 0.0393 },
    { title: "A Message from the Sea", words: 12296, sttr: 0.4106, deltaStd: 0.0229 },
    { title: "Mudfog and Other Sketches", words: 30717, sttr: 0.4666, deltaStd: 0.0268 },
    { title: "Mrs. Lirriper's Legacy", words: 12331, sttr: 0.4015, deltaStd: 0.0239 },
    { title: "Doctor Marigold", words: 11646, sttr: 0.3950, deltaStd: 0.0274 },
    { title: "Mrs. Lirriper's Lodgings", words: 14302, sttr: 0.3976, deltaStd: 0.0329 },
    { title: "The Wreck of the Golden Mary", words: 12813, sttr: 0.4062, deltaStd: 0.0225 },
    { title: "A Christmas Carol", words: 28587, sttr: 0.4434, deltaStd: 0.0327 },
    { title: "The Battle of Life", words: 29774, sttr: 0.4467, deltaStd: 0.0294 },
    { title: "The Lazy Tour of Two Idle Apprentices", words: 40239, sttr: 0.4307, deltaStd: 0.0324 },
    { title: "The Chimes", words: 30805, sttr: 0.4375, deltaStd: 0.0314 },
    { title: "The Perils of Certain English Prisoners", words: 19446, sttr: 0.4026, deltaStd: 0.0135 },
    { title: "The Cricket on the Hearth", words: 32351, sttr: 0.4287, deltaStd: 0.0350 },
    { title: "A House to Let", words: 34082, sttr: 0.4119, deltaStd: 0.0325 },
    { title: "The Haunted Man", words: 33946, sttr: 0.4116, deltaStd: 0.0329 },
    { title: "Pictures from Italy", words: 72638, sttr: 0.4718, deltaStd: 0.0268 },
    { title: "No Thoroughfare", words: 47882, sttr: 0.4166, deltaStd: 0.0341 },
    { title: "American Notes", words: 102620, sttr: 0.4694, deltaStd: 0.0288 },
    { title: "The Uncommercial Traveller", words: 142905, sttr: 0.4560, deltaStd: 0.0363 },
    { title: "The Mystery of Edwin Drood", words: 95975, sttr: 0.4315, deltaStd: 0.0430 },
    { title: "Hard Times", words: 103569, sttr: 0.4318, deltaStd: 0.0364 },
    { title: "A Tale of Two Cities", words: 136336, sttr: 0.4166, deltaStd: 0.0333 },
    { title: "Oliver Twist", words: 157801, sttr: 0.4390, deltaStd: 0.0353 },
    { title: "Great Expectations", words: 185362, sttr: 0.4026, deltaStd: 0.0298 },
    { title: "The Old Curiosity Shop", words: 218000, sttr: 0.4511, deltaStd: 0.0306 },
    { title: "A Child's History of England", words: 163201, sttr: 0.4210, deltaStd: 0.0210 },
    { title: "The Pickwick Papers", words: 301253, sttr: 0.4535, deltaStd: 0.0310 },
    { title: "Barnaby Rudge", words: 254582, sttr: 0.4563, deltaStd: 0.0326 },
    { title: "Our Mutual Friend", words: 326115, sttr: 0.4271, deltaStd: 0.0333 },
    { title: "Martin Chuzzlewit", words: 337275, sttr: 0.4448, deltaStd: 0.0311 },
    { title: "Nicholas Nickleby", words: 323048, sttr: 0.4533, deltaStd: 0.0336 },
    { title: "Little Dorrit", words: 338919, sttr: 0.4268, deltaStd: 0.0344 },
    { title: "Bleak House", words: 354418, sttr: 0.4125, deltaStd: 0.0350 },
    { title: "Dombey and Son", words: 356291, sttr: 0.4251, deltaStd: 0.0377 },
    { title: "David Copperfield", words: 356694, sttr: 0.4202, deltaStd: 0.0284 },
  ]
};

const authorsData = [dickensData];

// Calculate quartiles for box plot
function calculateQuartiles(values) {
  const sorted = [...values].sort((a, b) => a - b);
  const n = sorted.length;

  const q1Index = Math.floor(n * 0.25);
  const q2Index = Math.floor(n * 0.5);
  const q3Index = Math.floor(n * 0.75);

  return {
    min: sorted[0],
    q1: sorted[q1Index],
    median: sorted[q2Index],
    q3: sorted[q3Index],
    max: sorted[n - 1],
    mean: values.reduce((a, b) => a + b, 0) / n,
    std: Math.sqrt(values.reduce((sum, v) => sum + Math.pow(v - (values.reduce((a, b) => a + b, 0) / n), 2), 0) / n)
  };
}

// Box Plot Component
function BoxPlot({ data, width = 600, height = 300 }) {
  const padding = { top: 40, right: 40, bottom: 60, left: 80 };
  const plotWidth = width - padding.left - padding.right;
  const plotHeight = height - padding.top - padding.bottom;

  const allValues = data.flatMap(d => d.sttrValues);
  const minVal = Math.min(...allValues) - 0.02;
  const maxVal = Math.max(...allValues) + 0.02;

  const scaleY = (val) => padding.top + plotHeight - ((val - minVal) / (maxVal - minVal)) * plotHeight;
  const boxWidth = Math.min(80, plotWidth / (data.length * 2));

  return (
    <svg width={width} height={height} style={{ display: 'block', margin: '0 auto' }}>
      {/* Y-axis */}
      <line x1={padding.left} y1={padding.top} x2={padding.left} y2={height - padding.bottom} stroke="#64748b" strokeWidth={1} />

      {/* Y-axis ticks and labels */}
      {[0.38, 0.40, 0.42, 0.44, 0.46, 0.48].map(tick => (
        <g key={tick}>
          <line x1={padding.left - 5} y1={scaleY(tick)} x2={padding.left} y2={scaleY(tick)} stroke="#64748b" />
          <text x={padding.left - 10} y={scaleY(tick)} textAnchor="end" alignmentBaseline="middle" fontSize={12} fill="#64748b">
            {tick.toFixed(2)}
          </text>
          <line x1={padding.left} y1={scaleY(tick)} x2={width - padding.right} y2={scaleY(tick)} stroke="#e2e8f0" strokeDasharray="4,4" />
        </g>
      ))}

      {/* Y-axis label */}
      <text x={20} y={height / 2} textAnchor="middle" fontSize={14} fill="#1e293b" transform={`rotate(-90, 20, ${height / 2})`}>
        STTR
      </text>

      {/* Box plots */}
      {data.map((author, i) => {
        const stats = calculateQuartiles(author.sttrValues);
        const x = padding.left + (i + 0.5) * (plotWidth / data.length);
        const boxColor = '#3b82f6';

        return (
          <g key={author.author}>
            {/* Whisker line (min to max) */}
            <line x1={x} y1={scaleY(stats.min)} x2={x} y2={scaleY(stats.max)} stroke={boxColor} strokeWidth={1} />

            {/* Min whisker cap */}
            <line x1={x - boxWidth/4} y1={scaleY(stats.min)} x2={x + boxWidth/4} y2={scaleY(stats.min)} stroke={boxColor} strokeWidth={2} />

            {/* Max whisker cap */}
            <line x1={x - boxWidth/4} y1={scaleY(stats.max)} x2={x + boxWidth/4} y2={scaleY(stats.max)} stroke={boxColor} strokeWidth={2} />

            {/* Box (Q1 to Q3) */}
            <rect
              x={x - boxWidth/2}
              y={scaleY(stats.q3)}
              width={boxWidth}
              height={scaleY(stats.q1) - scaleY(stats.q3)}
              fill={boxColor}
              fillOpacity={0.3}
              stroke={boxColor}
              strokeWidth={2}
            />

            {/* Median line */}
            <line x1={x - boxWidth/2} y1={scaleY(stats.median)} x2={x + boxWidth/2} y2={scaleY(stats.median)} stroke={boxColor} strokeWidth={3} />

            {/* Mean dot */}
            <circle cx={x} cy={scaleY(stats.mean)} r={4} fill="#ef4444" />

            {/* Author label */}
            <text x={x} y={height - padding.bottom + 20} textAnchor="middle" fontSize={14} fill="#1e293b" fontWeight="600">
              {author.author}
            </text>
            <text x={x} y={height - padding.bottom + 36} textAnchor="middle" fontSize={11} fill="#64748b">
              ({author.works} works)
            </text>
          </g>
        );
      })}

      {/* Legend */}
      <g transform={`translate(${width - padding.right - 120}, ${padding.top})`}>
        <rect x={0} y={0} width={15} height={15} fill="#3b82f6" fillOpacity={0.3} stroke="#3b82f6" strokeWidth={2} />
        <text x={20} y={12} fontSize={11} fill="#64748b">IQR (Q1-Q3)</text>
        <line x1={0} y1={28} x2={15} y2={28} stroke="#3b82f6" strokeWidth={3} />
        <text x={20} y={32} fontSize={11} fill="#64748b">Median</text>
        <circle cx={7} cy={48} r={4} fill="#ef4444" />
        <text x={20} y={52} fontSize={11} fill="#64748b">Mean</text>
      </g>
    </svg>
  );
}

// Histogram Component
function Histogram({ values, bins = 12, width = 500, height = 200, color = '#3b82f6' }) {
  const padding = { top: 20, right: 20, bottom: 40, left: 50 };
  const plotWidth = width - padding.left - padding.right;
  const plotHeight = height - padding.top - padding.bottom;

  const minVal = Math.min(...values);
  const maxVal = Math.max(...values);
  const binWidth = (maxVal - minVal) / bins;

  const histogram = Array(bins).fill(0);
  values.forEach(v => {
    const binIndex = Math.min(Math.floor((v - minVal) / binWidth), bins - 1);
    histogram[binIndex]++;
  });

  const maxCount = Math.max(...histogram);
  const barWidth = plotWidth / bins;

  return (
    <svg width={width} height={height}>
      {/* Y-axis */}
      <line x1={padding.left} y1={padding.top} x2={padding.left} y2={height - padding.bottom} stroke="#64748b" />

      {/* X-axis */}
      <line x1={padding.left} y1={height - padding.bottom} x2={width - padding.right} y2={height - padding.bottom} stroke="#64748b" />

      {/* Bars */}
      {histogram.map((count, i) => (
        <rect
          key={i}
          x={padding.left + i * barWidth + 1}
          y={padding.top + plotHeight - (count / maxCount) * plotHeight}
          width={barWidth - 2}
          height={(count / maxCount) * plotHeight}
          fill={color}
          fillOpacity={0.7}
        />
      ))}

      {/* X-axis labels */}
      {[0, bins/2, bins].map(i => (
        <text key={i} x={padding.left + i * barWidth} y={height - padding.bottom + 15} textAnchor="middle" fontSize={10} fill="#64748b">
          {(minVal + i * binWidth).toFixed(2)}
        </text>
      ))}

      <text x={width / 2} y={height - 5} textAnchor="middle" fontSize={11} fill="#64748b">STTR</text>
      <text x={15} y={height / 2} textAnchor="middle" fontSize={11} fill="#64748b" transform={`rotate(-90, 15, ${height / 2})`}>Count</text>
    </svg>
  );
}

// Stats Table Component
function StatsTable({ data }) {
  return (
    <table style={styles.table}>
      <thead>
        <tr>
          <th style={styles.th}>Author</th>
          <th style={styles.th}>Works</th>
          <th style={styles.th}>Total Words</th>
          <th style={styles.th}>STTR Mean</th>
          <th style={styles.th}>STTR Std</th>
          <th style={styles.th}>Min</th>
          <th style={styles.th}>Max</th>
        </tr>
      </thead>
      <tbody>
        {data.map(author => {
          const stats = calculateQuartiles(author.sttrValues);
          return (
            <tr key={author.author}>
              <td style={styles.td}>{author.author}</td>
              <td style={{...styles.td, textAlign: 'right'}}>{author.works}</td>
              <td style={{...styles.td, textAlign: 'right'}}>{author.totalWords.toLocaleString()}</td>
              <td style={{...styles.td, textAlign: 'right'}}>{stats.mean.toFixed(4)}</td>
              <td style={{...styles.td, textAlign: 'right'}}>{stats.std.toFixed(4)}</td>
              <td style={{...styles.td, textAlign: 'right'}}>{stats.min.toFixed(4)}</td>
              <td style={{...styles.td, textAlign: 'right'}}>{stats.max.toFixed(4)}</td>
            </tr>
          );
        })}
      </tbody>
    </table>
  );
}

// Work Details Table Component
function WorksTable({ works }) {
  const [sortBy, setSortBy] = useState('sttr');
  const [sortDir, setSortDir] = useState('desc');

  const sorted = useMemo(() => {
    return [...works].sort((a, b) => {
      const mult = sortDir === 'desc' ? -1 : 1;
      return mult * (a[sortBy] - b[sortBy]);
    });
  }, [works, sortBy, sortDir]);

  const handleSort = (col) => {
    if (sortBy === col) {
      setSortDir(sortDir === 'desc' ? 'asc' : 'desc');
    } else {
      setSortBy(col);
      setSortDir('desc');
    }
  };

  return (
    <div style={{ maxHeight: 400, overflowY: 'auto' }}>
      <table style={styles.table}>
        <thead>
          <tr>
            <th style={styles.th}>Title</th>
            <th style={{...styles.th, cursor: 'pointer'}} onClick={() => handleSort('words')}>
              Words {sortBy === 'words' && (sortDir === 'desc' ? '↓' : '↑')}
            </th>
            <th style={{...styles.th, cursor: 'pointer'}} onClick={() => handleSort('sttr')}>
              STTR {sortBy === 'sttr' && (sortDir === 'desc' ? '↓' : '↑')}
            </th>
            <th style={{...styles.th, cursor: 'pointer'}} onClick={() => handleSort('deltaStd')}>
              Volatility {sortBy === 'deltaStd' && (sortDir === 'desc' ? '↓' : '↑')}
            </th>
          </tr>
        </thead>
        <tbody>
          {sorted.map(work => (
            <tr key={work.title}>
              <td style={styles.td}>{work.title}</td>
              <td style={{...styles.td, textAlign: 'right'}}>{work.words.toLocaleString()}</td>
              <td style={{...styles.td, textAlign: 'right'}}>{work.sttr.toFixed(4)}</td>
              <td style={{...styles.td, textAlign: 'right'}}>{work.deltaStd.toFixed(4)}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

// Scatter Plot Component for STTR vs Volatility
function ScatterPlot({ works, width = 600, height = 300 }) {
  const padding = { top: 30, right: 30, bottom: 50, left: 60 };
  const plotWidth = width - padding.left - padding.right;
  const plotHeight = height - padding.top - padding.bottom;

  const sttrMin = 0.38, sttrMax = 0.48;
  const volMin = 0, volMax = 0.05;

  const scaleX = (val) => padding.left + ((val - sttrMin) / (sttrMax - sttrMin)) * plotWidth;
  const scaleY = (val) => padding.top + plotHeight - ((val - volMin) / (volMax - volMin)) * plotHeight;

  return (
    <svg width={width} height={height} style={{ display: 'block', margin: '0 auto' }}>
      {/* Axes */}
      <line x1={padding.left} y1={height - padding.bottom} x2={width - padding.right} y2={height - padding.bottom} stroke="#64748b" />
      <line x1={padding.left} y1={padding.top} x2={padding.left} y2={height - padding.bottom} stroke="#64748b" />

      {/* X-axis ticks */}
      {[0.38, 0.40, 0.42, 0.44, 0.46, 0.48].map(tick => (
        <g key={tick}>
          <line x1={scaleX(tick)} y1={height - padding.bottom} x2={scaleX(tick)} y2={height - padding.bottom + 5} stroke="#64748b" />
          <text x={scaleX(tick)} y={height - padding.bottom + 18} textAnchor="middle" fontSize={10} fill="#64748b">{tick.toFixed(2)}</text>
        </g>
      ))}

      {/* Y-axis ticks */}
      {[0.01, 0.02, 0.03, 0.04, 0.05].map(tick => (
        <g key={tick}>
          <line x1={padding.left - 5} y1={scaleY(tick)} x2={padding.left} y2={scaleY(tick)} stroke="#64748b" />
          <text x={padding.left - 10} y={scaleY(tick)} textAnchor="end" alignmentBaseline="middle" fontSize={10} fill="#64748b">{tick.toFixed(2)}</text>
          <line x1={padding.left} y1={scaleY(tick)} x2={width - padding.right} y2={scaleY(tick)} stroke="#e2e8f0" strokeDasharray="4,4" />
        </g>
      ))}

      {/* Axis labels */}
      <text x={width / 2} y={height - 8} textAnchor="middle" fontSize={12} fill="#475569">STTR</text>
      <text x={15} y={height / 2} textAnchor="middle" fontSize={12} fill="#475569" transform={`rotate(-90, 15, ${height / 2})`}>Volatility</text>

      {/* Data points */}
      {works.map((work, i) => (
        <circle
          key={i}
          cx={scaleX(work.sttr)}
          cy={scaleY(work.deltaStd)}
          r={5}
          fill="#3b82f6"
          fillOpacity={0.6}
          stroke="#3b82f6"
          strokeWidth={1}
        >
          <title>{work.title}: STTR={work.sttr.toFixed(3)}, Vol={work.deltaStd.toFixed(3)}</title>
        </circle>
      ))}
    </svg>
  );
}

const styles = {
  container: {
    fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
    backgroundColor: "#f8fafc",
    color: "#1e293b",
    minHeight: "100vh",
    padding: 32,
    maxWidth: 1000,
    margin: "0 auto",
  },
  header: {
    marginBottom: 32,
  },
  title: {
    fontSize: 28,
    fontWeight: 700,
    marginBottom: 8,
    color: "#0f172a",
  },
  subtitle: {
    fontSize: 16,
    color: "#64748b",
  },
  card: {
    backgroundColor: "#ffffff",
    borderRadius: 12,
    padding: 24,
    border: "1px solid #e2e8f0",
    boxShadow: "0 1px 3px rgba(0,0,0,0.08)",
    marginBottom: 24,
  },
  cardTitle: {
    fontSize: 18,
    fontWeight: 600,
    marginBottom: 16,
    color: "#1e293b",
  },
  section: {
    marginBottom: 16,
  },
  sectionTitle: {
    fontSize: 14,
    fontWeight: 600,
    color: "#475569",
    marginBottom: 8,
  },
  text: {
    fontSize: 14,
    lineHeight: 1.7,
    color: "#475569",
  },
  formula: {
    fontFamily: 'Monaco, Consolas, monospace',
    backgroundColor: '#f1f5f9',
    padding: '2px 8px',
    borderRadius: 4,
    fontSize: 13,
  },
  table: {
    width: '100%',
    borderCollapse: 'collapse',
    fontSize: 13,
  },
  th: {
    textAlign: 'left',
    padding: '10px 12px',
    borderBottom: '2px solid #e2e8f0',
    fontWeight: 600,
    color: '#475569',
    backgroundColor: '#f8fafc',
  },
  td: {
    padding: '8px 12px',
    borderBottom: '1px solid #e2e8f0',
  },
  highlight: {
    backgroundColor: '#dbeafe',
    padding: '12px 16px',
    borderRadius: 8,
    marginTop: 12,
  },
  grid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
    gap: 16,
  },
  stat: {
    backgroundColor: '#f8fafc',
    padding: 16,
    borderRadius: 8,
    textAlign: 'center',
  },
  statValue: {
    fontSize: 24,
    fontWeight: 700,
    color: '#3b82f6',
  },
  statLabel: {
    fontSize: 12,
    color: '#64748b',
    marginTop: 4,
  },
};

export default function App() {
  const dickensStats = calculateQuartiles(dickensData.sttrValues);

  return (
    <div style={styles.container}>
      <header style={styles.header}>
        <h1 style={styles.title}>Type-Token Ratio Analysis</h1>
        <p style={styles.subtitle}>Vocabulary richness metrics for stylometric comparison</p>
      </header>

      {/* Summary Stats - big numbers first */}
      <div style={styles.card}>
        <div style={styles.grid}>
          <div style={styles.stat}>
            <div style={styles.statValue}>{dickensStats.mean.toFixed(3)}</div>
            <div style={styles.statLabel}>Mean STTR</div>
          </div>
          <div style={styles.stat}>
            <div style={styles.statValue}>{dickensStats.median.toFixed(3)}</div>
            <div style={styles.statLabel}>Median STTR</div>
          </div>
          <div style={styles.stat}>
            <div style={styles.statValue}>{dickensData.works}</div>
            <div style={styles.statLabel}>Works Analyzed</div>
          </div>
          <div style={styles.stat}>
            <div style={styles.statValue}>{(dickensData.totalWords / 1000000).toFixed(1)}M</div>
            <div style={styles.statLabel}>Total Words</div>
          </div>
        </div>
      </div>

      {/* Box Plot */}
      <div style={styles.card}>
        <h2 style={styles.cardTitle}>STTR Distribution</h2>
        <BoxPlot data={authorsData} width={600} height={320} />
      </div>

      {/* Histogram */}
      <div style={styles.card}>
        <h2 style={styles.cardTitle}>Frequency Distribution</h2>
        <Histogram values={dickensData.sttrValues} width={600} height={200} />
      </div>

      {/* Individual Works */}
      <div style={styles.card}>
        <h2 style={styles.cardTitle}>Individual Works</h2>
        <p style={{...styles.text, marginBottom: 16}}>
          Click column headers to sort.
        </p>
        <WorksTable works={dickensData.workDetails} />
      </div>

      {/* Key Findings */}
      <div style={styles.card}>
        <h2 style={styles.cardTitle}>Key Findings</h2>
        <div style={styles.text}>
          <ul style={{ paddingLeft: 20 }}>
            <li style={{ marginBottom: 8 }}>
              <strong>Genre affects STTR:</strong> Travel writing ("Pictures from Italy": 0.4718,
              "American Notes": 0.4694) shows higher vocabulary richness than fiction.
            </li>
            <li style={{ marginBottom: 8 }}>
              <strong>Essays score high:</strong> "Mudfog and Other Sketches" (0.4666) and
              "Sunday Under Three Heads" (0.4665) demonstrate expository writing's vocabulary diversity.
            </li>
            <li style={{ marginBottom: 8 }}>
              <strong>Dialogue-heavy works score lower:</strong> "Doctor Marigold" (0.3950) and
              "Mrs. Lirriper's Lodgings" (0.3976) feature heavy dialect and conversational repetition.
            </li>
            <li style={{ marginBottom: 8 }}>
              <strong>STTR is length-independent:</strong> "David Copperfield" (356k words, STTR 0.4202)
              and "George Silverman's Explanation" (11k words, STTR 0.4190) have nearly identical STTR
              despite 32x length difference.
            </li>
          </ul>
        </div>
      </div>

      {/* What is TTR? - explanatory content at bottom */}
      <div style={styles.card}>
        <h2 style={styles.cardTitle}>What is TTR?</h2>
        <div style={styles.text}>
          <p style={{ marginBottom: 12 }}>
            <strong>Type-Token Ratio (TTR)</strong> measures vocabulary richness by comparing the number of
            unique words (types) to the total number of words (tokens) in a text.
          </p>
          <p style={{ marginBottom: 12 }}>
            <span style={styles.formula}>TTR = unique_words / total_words</span>
          </p>
          <p style={{ marginBottom: 12 }}>
            A text with TTR = 0.50 means half the words are unique. Higher TTR indicates more diverse vocabulary.
          </p>
          <div style={styles.highlight}>
            <strong>Problem:</strong> Raw TTR is biased by text length. Longer texts naturally have lower TTR because
            common words (the, and, is) repeat more often. A 1,000-word essay might have TTR = 0.40, while
            a 300,000-word novel might have TTR = 0.05, even if both use equally rich vocabulary.
          </div>
        </div>
      </div>

      {/* What is STTR? */}
      <div style={styles.card}>
        <h2 style={styles.cardTitle}>What is STTR?</h2>
        <div style={styles.text}>
          <p style={{ marginBottom: 12 }}>
            <strong>Standardized Type-Token Ratio (STTR)</strong> solves the length bias problem by computing
            TTR on fixed-size chunks and averaging the results.
          </p>
          <p style={{ marginBottom: 12 }}>
            <span style={styles.formula}>STTR = mean(TTR of each 1000-word chunk)</span>
          </p>
          <p style={{ marginBottom: 12 }}>
            By using consistent chunk sizes (typically 1,000 words), STTR produces comparable scores
            regardless of total text length. This makes it suitable for comparing works of different sizes.
          </p>
          <div style={styles.highlight}>
            <strong>Interpretation:</strong> STTR typically ranges from 0.35 to 0.50 for English prose.
            Higher values indicate richer vocabulary within local passages. Technical writing and
            travel narratives often score higher than dialogue-heavy fiction.
          </div>
        </div>
      </div>

      <footer style={{ textAlign: 'center', color: '#94a3b8', fontSize: 12, marginTop: 32 }}>
        Generated from Project Gutenberg corpus analysis
      </footer>
    </div>
  );
}
