const state = { projects: [], customers: [], tasks: [], risks: [], invoices: [], milestones: [], logs: [], summary: {} };
const schemas = {
  projects: [
    ['name','Project name','text'], ['customer_id','Customer','select:customers'], ['owner','Owner','text'], ['status','Status','select:Active|Planning|At Risk|Completed'], ['priority','Priority','select:Low|Medium|High|Critical'], ['budget','Budget','number'], ['spent','Spent','number'], ['progress','Progress %','number'], ['start_date','Start date','date'], ['due_date','Due date','date'], ['risk_level','Risk level','select:Low|Medium|High'], ['description','Description','textarea']
  ],
  customers: [
    ['name','Customer name','text'], ['industry','Industry','text'], ['region','Region','text'], ['owner','Owner','text'], ['contract_value','Contract value','number'], ['health_score','Health score','number'], ['renewal_date','Renewal date','date'], ['status','Status','select:Active|Watch|Renewal'], ['notes','Notes','textarea']
  ],
  tasks: [
    ['project_id','Project','select:projects'], ['title','Task title','text'], ['assignee','Assignee','text'], ['stage','Stage','select:To Do|In Progress|Review|Blocked|Done'], ['effort','Effort points','number'], ['due_date','Due date','date']
  ],
  risks: [
    ['project_id','Project','select:projects'], ['title','Risk title','text'], ['severity','Severity','select:Low|Medium|High'], ['probability','Probability','number'], ['impact','Impact','number'], ['mitigation','Mitigation plan','textarea'], ['owner','Owner','text'], ['status','Status','select:Open|Monitoring|Closed']
  ],
  invoices: [
    ['customer_id','Customer','select:customers'], ['invoice_no','Invoice number','text'], ['amount','Amount','number'], ['status','Status','select:Paid|Pending|Overdue'], ['due_date','Due date','date']
  ],
  milestones: [
    ['project_id','Project','select:projects'], ['title','Milestone title','text'], ['target_date','Target date','date'], ['status','Status','select:On Track|Watch|At Risk|Done'], ['confidence','Confidence %','number']
  ]
};
const titles = { dashboard:'Operational Intelligence Dashboard', projects:'Project Management', customers:'Customer Relationship Center', tasks:'Delivery Board', risks:'Enterprise Risk Register', finance:'Finance & Billing Control', milestones:'Milestone Roadmap', analytics:'Analytics Canvas', audit:'Audit Timeline' };
const $ = id => document.getElementById(id);
const money = value => `$${Number(value || 0).toLocaleString()}`;
const badgeClass = value => String(value || '').replaceAll(' ', '');

async function loadData() {
  const response = await fetch('/api/dashboard');
  const data = await response.json();
  Object.assign(state, data);
  renderAll();
}

function renderAll() {
  renderMetrics(); renderProjects(); renderCustomers(); renderRisks(); renderTasks(); renderInvoices(); renderMilestones(); renderAudit(); renderCharts();
}

function renderMetrics() {
  $('forecastConfidence').textContent = `${state.summary.forecast}%`;
  const metrics = [
    ['Total Projects', state.summary.projects], ['Portfolio Budget', money(state.summary.budget)], ['Budget Spent', money(state.summary.spent)], ['Average Progress', `${state.summary.avg_progress}%`],
    ['Customers', state.summary.customers], ['Average Health', `${state.summary.avg_health}%`], ['Open Risks', state.summary.open_risks], ['Pending Revenue', money(state.summary.pending_revenue)]
  ];
  $('metricGrid').innerHTML = metrics.map(([label, value]) => `<div class="metric"><small>${label}</small><strong>${value}</strong></div>`).join('');
}

function actionButtons(table, item) {
  return `<div class="row-actions"><button class="ghost" onclick='openEditor("${table}", ${JSON.stringify(item)})'>Edit</button><button class="danger" onclick="removeRecord('${table}', ${item.id})">Delete</button></div>`;
}

function renderProjects() {
  const rows = state.projects.map(p => `<tr><td><strong>${p.name}</strong><br><small>${p.customer_name || ''}</small></td><td>${p.owner}</td><td><span class="pill ${badgeClass(p.status)}">${p.status}</span></td><td>${money(p.budget)}</td><td>${money(p.spent)}</td><td><div class="progress"><span style="width:${p.progress}%"></span></div><small>${p.progress}%</small></td><td><span class="pill ${badgeClass(p.risk_level)}">${p.risk_level}</span></td><td>${p.due_date}</td><td>${actionButtons('projects', p)}</td></tr>`).join('');
  const table = `<thead><tr><th>Name</th><th>Owner</th><th>Status</th><th>Budget</th><th>Spent</th><th>Progress</th><th>Risk</th><th>Due</th><th>Actions</th></tr></thead><tbody>${rows}</tbody>`;
  $('projectTable').innerHTML = table;
  $('projectsFullTable').innerHTML = table;
}

function renderCustomers() {
  const cards = state.customers.map(c => `<div class="card"><h4>${c.name}</h4><p>${c.industry} • ${c.region}</p><p>Owner: <strong>${c.owner}</strong></p><p>Contract: <strong>${money(c.contract_value)}</strong></p><p>Health: <strong>${c.health_score}%</strong></p><span class="pill ${badgeClass(c.status)}">${c.status}</span>${actionButtons('customers', c)}</div>`).join('');
  $('customerCards').innerHTML = cards;
  $('customersFull').innerHTML = cards;
}

function renderRisks() {
  $('riskCards').innerHTML = state.risks.slice(0, 6).map(r => `<div class="card"><h4>${r.title}</h4><p>${r.project_name}</p><span class="pill ${badgeClass(r.severity)}">${r.severity}</span><p>Probability ${r.probability}% • Impact ${r.impact}%</p>${actionButtons('risks', r)}</div>`).join('');
  $('riskTable').innerHTML = `<thead><tr><th>Risk</th><th>Project</th><th>Severity</th><th>Probability</th><th>Impact</th><th>Owner</th><th>Status</th><th>Actions</th></tr></thead><tbody>${state.risks.map(r => `<tr><td><strong>${r.title}</strong><br><small>${r.mitigation}</small></td><td>${r.project_name}</td><td><span class="pill ${badgeClass(r.severity)}">${r.severity}</span></td><td>${r.probability}%</td><td>${r.impact}%</td><td>${r.owner}</td><td>${r.status}</td><td>${actionButtons('risks', r)}</td></tr>`).join('')}</tbody>`;
}

function renderTasks() {
  const stages = ['To Do','In Progress','Review','Blocked','Done'];
  const board = stages.map(stage => `<div class="lane"><h4>${stage}</h4>${state.tasks.filter(t => t.stage === stage).map(t => `<div class="task"><strong>${t.title}</strong><p>${t.project_name}</p><small>${t.assignee} • ${t.effort} pts</small>${actionButtons('tasks', t)}</div>`).join('') || '<p class="empty">No tasks</p>'}</div>`).join('');
  $('taskBoard').innerHTML = board;
  $('taskBoardFull').innerHTML = board;
}

function renderInvoices() {
  $('invoiceTable').innerHTML = `<thead><tr><th>Invoice</th><th>Customer</th><th>Amount</th><th>Status</th><th>Due Date</th><th>Actions</th></tr></thead><tbody>${state.invoices.map(i => `<tr><td><strong>${i.invoice_no}</strong></td><td>${i.customer_name}</td><td>${money(i.amount)}</td><td><span class="pill ${badgeClass(i.status)}">${i.status}</span></td><td>${i.due_date}</td><td>${actionButtons('invoices', i)}</td></tr>`).join('')}</tbody>`;
}

function renderMilestones() {
  $('milestoneTable').innerHTML = `<thead><tr><th>Milestone</th><th>Project</th><th>Target</th><th>Status</th><th>Confidence</th><th>Actions</th></tr></thead><tbody>${state.milestones.map(m => `<tr><td><strong>${m.title}</strong></td><td>${m.project_name}</td><td>${m.target_date}</td><td><span class="pill ${badgeClass(m.status)}">${m.status}</span></td><td>${m.confidence}%</td><td>${actionButtons('milestones', m)}</td></tr>`).join('')}</tbody>`;
}

function renderAudit() {
  $('auditList').innerHTML = state.logs.map(log => `<div class="event"><span class="dot"></span><div><strong>${log.event_type}</strong><p>${log.message}</p><small>${log.created_at}</small></div></div>`).join('');
}

function drawBar(canvasId, labels, values) {
  const canvas = $(canvasId); if (!canvas) return;
  const ctx = canvas.getContext('2d'); ctx.clearRect(0,0,canvas.width,canvas.height);
  const max = Math.max(...values, 1); const barWidth = Math.max(26, (canvas.width - 80) / values.length - 16);
  ctx.font = '12px Segoe UI'; ctx.fillStyle = '#101828';
  values.forEach((value, index) => {
    const height = (value / max) * 180; const x = 45 + index * (barWidth + 18); const y = 220 - height;
    const gradient = ctx.createLinearGradient(0, y, 0, 220); gradient.addColorStop(0, '#2563eb'); gradient.addColorStop(1, '#7c3aed');
    ctx.fillStyle = gradient; ctx.roundRect(x, y, barWidth, height, 8); ctx.fill();
    ctx.fillStyle = '#475467'; ctx.fillText(String(labels[index]).slice(0, 10), x - 4, 246); ctx.fillText(value, x + 5, y - 8);
  });
}

function renderCharts() {
  const countBy = (items, key) => items.reduce((acc, item) => (acc[item[key]] = (acc[item[key]] || 0) + 1, acc), {});
  const status = countBy(state.projects, 'status'); drawBar('statusChart', Object.keys(status), Object.values(status));
  drawBar('healthChart', state.customers.map(c => c.name.split(' ')[0]), state.customers.map(c => Number(c.health_score)));
  const severity = countBy(state.risks, 'severity'); drawBar('riskChart', Object.keys(severity), Object.values(severity));
  const invoice = countBy(state.invoices, 'status'); drawBar('invoiceChart', Object.keys(invoice), Object.values(invoice));
}

CanvasRenderingContext2D.prototype.roundRect = function(x, y, w, h, r) {
  this.beginPath(); this.moveTo(x + r, y); this.arcTo(x + w, y, x + w, y + h, r); this.arcTo(x + w, y + h, x, y + h, r); this.arcTo(x, y + h, x, y, r); this.arcTo(x, y, x + w, y, r); this.closePath(); return this;
};

function inputFor(field, label, type, value = '') {
  if (type === 'textarea') return `<textarea name="${field}" placeholder="${label}">${value || ''}</textarea>`;
  if (type.startsWith('select:')) {
    const source = type.split(':')[1];
    let options = [];
    if (source === 'customers') options = state.customers.map(c => [c.id, c.name]);
    else if (source === 'projects') options = state.projects.map(p => [p.id, p.name]);
    else options = source.split('|').map(v => [v, v]);
    return `<select name="${field}">${options.map(([id, name]) => `<option value="${id}" ${String(id) === String(value) ? 'selected' : ''}>${name}</option>`).join('')}</select>`;
  }
  return `<input name="${field}" type="${type}" placeholder="${label}" value="${value ?? ''}" required />`;
}

function openEditor(table, item = null) {
  const isEdit = Boolean(item && item.id);
  const title = `${isEdit ? 'Edit' : 'Add'} ${table.slice(0, -1)}`;
  $('modalHost').innerHTML = `<div class="modal open"><form id="recordForm"><h3>${title}</h3>${schemas[table].map(([f,l,t]) => inputFor(f,l,t,item ? item[f] : '')).join('')}<div class="form-actions"><button type="button" onclick="closeModal()">Cancel</button><button class="primary">${isEdit ? 'Update' : 'Save'}</button></div></form></div>`;
  $('recordForm').addEventListener('submit', async event => {
    event.preventDefault();
    const payload = Object.fromEntries(new FormData(event.target).entries());
    await fetch(`/api/${table}${isEdit ? '/' + item.id : ''}`, { method: isEdit ? 'PATCH' : 'POST', headers: {'Content-Type':'application/json'}, body: JSON.stringify(payload) });
    closeModal(); await loadData();
  });
}

function closeModal() { $('modalHost').innerHTML = ''; }
async function removeRecord(table, id) {
  if (!confirm('Are you sure you want to delete this record?')) return;
  await fetch(`/api/${table}/${id}`, { method: 'DELETE' });
  await loadData();
}

document.querySelectorAll('.nav').forEach(button => button.addEventListener('click', () => {
  document.querySelectorAll('.nav').forEach(x => x.classList.remove('active'));
  document.querySelectorAll('.page').forEach(x => x.classList.remove('active-page'));
  button.classList.add('active'); $(button.dataset.page).classList.add('active-page'); $('pageTitle').textContent = titles[button.dataset.page];
}));
document.addEventListener('click', event => { const opener = event.target.closest('[data-open]'); if (opener) openEditor(opener.dataset.open.replace('Modal','') + 's'); });
$('refreshBtn').addEventListener('click', loadData);
$('globalSearch').addEventListener('input', event => {
  const query = event.target.value.toLowerCase();
  document.querySelectorAll('tbody tr,.card,.task,.event').forEach(node => { node.style.display = node.textContent.toLowerCase().includes(query) ? '' : 'none'; });
});
loadData();
