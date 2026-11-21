// Render task intervals in one coordinate system; never assign fixed widths per hour.
function currentTimeRange() {
  const first = data.hours[0];
  const limit = data.hours.at(-1) + 1;
  const size = timeWindow === 'all' ? limit - first : Math.min(Number(timeWindow), limit - first);
  windowStart = Math.max(first, Math.min(windowStart, limit - size));
  return {start: timeWindow === 'all' ? first : windowStart, end: timeWindow === 'all' ? limit : windowStart + size};
}

function escapeChartText(value) {
  return String(value).replace(/[&<>"']/g, char => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[char]));
}

function renderAxis(start, end) {
  return Array.from({length: 5}, (_, i) => `<i style="left:${i * 25}%">${Math.round(start + (end - start) * i / 4)}h</i>`).join('');
}

function renderVisual() {
  const controls = document.querySelector('#timelineControls');
  for (const selector of ['#vehicleView', '#coverageView', '#expandChart', '[data-window]', '#previousWindow', '#nextWindow']) {
    document.querySelectorAll(selector).forEach(button => { button.disabled = !data; });
  }
  if (!data) { controls.hidden = true; return; }
  const {start, end} = currentTimeRange();
  const first = data.hours[0], limit = data.hours.at(-1) + 1, duration = end - start;
  controls.hidden = false;
  document.querySelector('#rangeLabel').textContent = `${start}–${end}h`;
  const slider = document.querySelector('#timelineRange');
  slider.min = first; slider.max = limit - duration; slider.value = start;
  slider.disabled = timeWindow === 'all' || duration === limit - first;
  document.querySelector('#previousWindow').disabled = start === first;
  document.querySelector('#nextWindow').disabled = end === limit;
  document.querySelectorAll('[data-window]').forEach(button => {
    const active = button.dataset.window === String(timeWindow);
    button.classList.toggle('active', active); button.setAttribute('aria-pressed', String(active));
  });
  for (const [id, mode] of [['vehicleView', 'vehicle'], ['coverageView', 'coverage']]) {
    const button = document.getElementById(id);
    button.classList.toggle('active', view === mode); button.setAttribute('aria-pressed', String(view === mode));
  }
  const records = data.hours.map((hour, i) => ({hour, coverage: data.coverage[i]})).filter(x => x.hour >= start && x.hour < end);
  const shortage = records.reduce((sum, x) => sum + Math.max(0, solvedDemand - x.coverage), 0);
  const boundaryNote = `输入 ${first}–${data.hours.at(-1)}h，含首尾共 ${data.hours.length} 条小时记录；末条记录的结束边界为 ${limit}h。`;
  document.querySelector('#chartHint').textContent = boundaryNote;
  const chartSummary = view === 'vehicle'
    ? `当前显示 ${start}–${end}h · ${data.vehicles.length} 辆车 · ${timeWindow === 'all' ? '全部任务已按比例完整呈现' : '局部放大，可用滑块或上一段 / 下一段浏览'}。`
    : `当前 ${start}–${end}h · 需求 ${solvedDemand} 辆 · 实际 ${Math.min(...records.map(x => x.coverage))}–${Math.max(...records.map(x => x.coverage))} 辆 · 缺口 ${shortage} 车·小时。`;
  document.querySelector('#chartSummary').textContent = chartSummary;
  if (view === 'coverage') { renderCoverage(records, start, end); return; }
  const rows = data.vehicles.map(vehicle => {
    const segments = data.segments.map((segment, index) => ({segment, index})).filter(({segment}) => segment.vehicle === vehicle.id && segment.end > start && segment.start < end);
    const bars = segments.map(({segment, index}) => {
      const left = 100 * (Math.max(start, segment.start) - start) / duration;
      const width = 100 * (Math.min(end, segment.end) - Math.max(start, segment.start)) / duration;
      const title = `${vehicle.type}-${vehicle.id} · ${segment.activity} · ${segment.start}–${segment.end}h · ${segment.end - segment.start} 小时`;
      return `<button type="button" class="timeline-segment s${segment.state}" data-segment="${index}" style="left:${left}%;width:${width}%" aria-label="${escapeChartText(title)}" title="${escapeChartText(title)}"></button>`;
    }).join('');
    return `<div class="timeline-row"><b>${escapeChartText(vehicle.type)}-${vehicle.id}</b><section class="timeline-track">${bars}</section></div>`;
  }).join('');
  document.querySelector('#visual').innerHTML = `<div class="timeline"><div class="timeline-axis"><span>车辆</span><section class="axis-track">${renderAxis(start, end)}</section></div>${rows}</div>`;
}

function renderCoverage(records, start, end) {
  const w = 800, h = 250, left = 48, right = 20, top = 20, bottom = 35;
  const plotW = w - left - right, plotH = h - top - bottom;
  const max = Math.max(solvedDemand + 1, ...records.map(x => x.coverage), 1);
  const x = hour => left + (hour - start) / (end - start) * plotW;
  const y = value => top + plotH * (1 - value / max);
  const grid = Array.from({length: max + 1}, (_, n) => `<line x1="${left}" x2="${w - right}" y1="${y(n)}" y2="${y(n)}" stroke="#e5edf2"/><text x="${left - 8}" y="${y(n) + 4}" text-anchor="end">${n}</text>`).join('');
  const ticks = Array.from({length: 5}, (_, i) => {const hour = start + (end - start) * i / 4;return `<text x="${x(hour)}" y="${h - 10}" text-anchor="${i === 0 ? 'start' : i === 4 ? 'end' : 'middle'}">${Math.round(hour)}h</text>`;}).join('');
  const line = records.map((r, i) => `${i ? 'L' : 'M'}${x(r.hour)},${y(r.coverage)}H${x(r.hour + 1)}`).join('');
  const gaps = records.filter(r => r.coverage < solvedDemand).map(r => `<rect x="${x(r.hour)}" y="${y(solvedDemand)}" width="${Math.max(.8, plotW / (end - start))}" height="${y(r.coverage) - y(solvedDemand)}" fill="#fee4e2"/>`).join('');
  document.querySelector('#visual').innerHTML = `<div class="coverage-plot"><svg viewBox="0 0 ${w} ${h}" role="img" aria-label="${start}到${end}小时服务覆盖，需求为${solvedDemand}辆">${grid}${gaps}<path d="${line}" fill="none" stroke="#0891b2" stroke-width="2"/><line x1="${left}" x2="${w - right}" y1="${y(solvedDemand)}" y2="${y(solvedDemand)}" stroke="#d92d20" stroke-dasharray="6 5"/>${ticks}<text x="8" y="14">辆</text></svg><p>蓝线：实际服务车辆 · 红色虚线：需求 ${solvedDemand} 辆 · 浅红区域：未满足需求。点击曲线查询该时刻。</p></div>`;
  document.querySelector('.coverage-plot svg').onclick = event => {
    const svg = event.currentTarget;
    const point = svg.createSVGPoint(); point.x = event.clientX; point.y = event.clientY;
    const position = point.matrixTransform(svg.getScreenCTM().inverse());
    const hour = Math.max(start, Math.min(end - 1, Math.floor(start + (position.x - left) / plotW * (end - start))));
    const record = records.find(r => r.hour === hour);
    if (record) document.querySelector('#chartDetail').textContent = `${hour}–${hour + 1}h：实际服务 ${record.coverage} 辆，需求 ${solvedDemand} 辆，缺口 ${Math.max(0, solvedDemand - record.coverage)} 辆。`;
  };
}

function setupRosterControls() {
  const switchView = mode => {
    view = mode;
    document.querySelector('#chartDetail').textContent = mode === 'coverage'
      ? '点击覆盖曲线，查询该小时实际服务车辆数、需求和缺口。'
      : '点击甘特图中的色块，查看车辆、任务和起止时间；窄色块可先切换 24 小时放大。';
    renderVisual();
  };
  document.querySelector('#vehicleView').onclick = () => switchView('vehicle');
  document.querySelector('#coverageView').onclick = () => switchView('coverage');
  document.querySelectorAll('[data-window]').forEach(button => {button.onclick = () => {
    if (!data) return;
    timeWindow = button.dataset.window; renderVisual();
  };});
  document.querySelector('#timelineRange').oninput = event => {windowStart = Number(event.target.value); renderVisual();};
  for (const [id, direction] of [['previousWindow', -1], ['nextWindow', 1]]) {
    document.getElementById(id).onclick = () => {const {start, end} = currentTimeRange();windowStart = start + direction * (end - start);renderVisual();};
  }
  document.querySelector('#visual').onclick = event => {
    const button = event.target.closest('[data-segment]');
    if (!button) return;
    const segment = data.segments[Number(button.dataset.segment)];
    document.querySelector('#chartDetail').textContent = `${segment.type}-${segment.vehicle}（原始编号 ${segment.label}）：${segment.activity} · ${segment.start}–${segment.end}h · 持续 ${segment.end - segment.start} 小时。`;
  };
  const panel = document.querySelector('.roster-panel'), expand = document.querySelector('#expandChart');
  const close = () => {panel.classList.remove('chart-expanded');document.body.classList.remove('chart-open');expand.textContent = '展开大图';expand.setAttribute('aria-expanded', 'false');};
  expand.onclick = () => {
    if (panel.classList.contains('chart-expanded')) {close();return;}
    panel.classList.add('chart-expanded');document.body.classList.add('chart-open');expand.textContent = '收起大图';expand.setAttribute('aria-expanded', 'true');expand.focus();
  };
  document.addEventListener('keydown', event => {if (event.key === 'Escape') close();});
  renderVisual();
}
