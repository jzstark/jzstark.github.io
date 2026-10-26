const DAY = 86400000;
const integer = new Intl.NumberFormat('en-US');
const compact = new Intl.NumberFormat('en-US', { notation: 'compact', maximumFractionDigits: 1 });
const dateLabel = new Intl.DateTimeFormat('en-US', { month: 'short', day: 'numeric', year: 'numeric', timeZone: 'UTC' });
const iso = (value) => new Date(value).toISOString().slice(0, 10);
const midnight = (value) => Date.parse(`${iso(value)}T00:00:00Z`);

export function validateDataset(data) {
  if (data?.schema_version !== 1 || data?.source?.id !== 'codex-account-usage' || !Array.isArray(data.days)) {
    throw new Error('Unsupported usage data');
  }
  if (data.updated_at !== null && (typeof data.updated_at !== 'string' || !Number.isFinite(Date.parse(data.updated_at)))) {
    throw new Error('Invalid update timestamp');
  }
  const seen = new Set();
  for (const day of data.days) {
    if (!/^\d{4}-\d{2}-\d{2}$/.test(day.date) || !Number.isFinite(Date.parse(day.date)) || iso(day.date) !== day.date ||
        !Number.isSafeInteger(day.tokens) || day.tokens < 0 || seen.has(day.date)) {
      throw new Error('Invalid daily usage');
    }
    seen.add(day.date);
  }
  if (data.days.length && data.updated_at === null) throw new Error('Missing update timestamp');
  return data;
}

export function recentStats(days, now = new Date()) {
  const today = midnight(now);
  const end = iso(today - DAY);
  const start = iso(today - 30 * DAY);
  const reported = days.filter((day) => day.date >= start && day.date <= end);
  const total = reported.reduce((sum, day) => sum + day.tokens, 0);
  return {
    start, end, reported: reported.length,
    total: reported.length ? total : null,
    average: reported.length ? total / reported.length : null,
    active: reported.length ? reported.filter((day) => day.tokens > 0).length : null,
  };
}

export function intensity(tokens) {
  if (tokens === null) return 'unknown';
  if (tokens === 0) return 0;
  if (tokens < 1e6) return 1;
  if (tokens < 1e7) return 2;
  if (tokens < 1e8) return 3;
  return 4;
}

export function calendarDays(days, now = new Date()) {
  const today = midnight(now);
  const first = today - 364 * DAY;
  const sunday = first - new Date(first).getUTCDay() * DAY;
  const end = today + (6 - new Date(today).getUTCDay()) * DAY;
  const values = new Map(days.map((day) => [day.date, day.tokens]));
  const result = [];
  for (let time = sunday; time <= end; time += DAY) {
    const key = iso(time);
    result.push({ date: key, tokens: values.get(key) ?? null, padding: time < first || time > today });
  }
  return result;
}

function render(data, now = new Date()) {
  const byId = (id) => document.getElementById(`activity-${id}`);
  const stats = recentStats(data.days, now);
  for (const key of ['total', 'average', 'active']) {
    const value = stats[key];
    byId(key).textContent = value === null ? '—' : compact.format(value);
    byId(key).title = value === null ? 'No reported daily data' : integer.format(Math.round(value));
  }
  byId('coverage').textContent = `${stats.reported} of 30 days reported`;
  byId('average-note').textContent = stats.reported ? `Across ${stats.reported} reported days` : 'No daily records available';
  const status = byId('status');
  const timestamp = data.updated_at && new Date(data.updated_at);
  if (!timestamp || !data.days.length) {
    status.textContent = 'Daily usage is not available yet.';
    status.dataset.state = 'empty';
  } else {
    const stale = now.getTime() - timestamp.getTime() > 48 * 60 * 60 * 1000;
    status.textContent = stale ? 'The last sync is over 48 hours old. Showing the last available data.' : 'Official account data · synced daily';
    status.dataset.state = stale ? 'stale' : 'ok';
    byId('updated').textContent = `Last synced ${timestamp.toISOString().slice(0, 16).replace('T', ' ')} UTC.`;
  }
  const cells = calendarDays(data.days, now);
  const visible = cells.filter((day) => !day.padding);
  byId('range').textContent = `${dateLabel.format(new Date(visible[0].date))} – ${dateLabel.format(new Date(visible.at(-1).date))}`;
  const grid = byId('grid');
  const months = byId('months');
  const fragment = document.createDocumentFragment();
  const buttons = [];
  const monthFormat = new Intl.DateTimeFormat('en-US', { month: 'short', timeZone: 'UTC' });
  let previousMonth = '';
  for (const [index, day] of cells.entries()) {
    if (index % 7 === 0) {
      const month = day.date.slice(0, 7);
      if (month !== previousMonth) {
        // Skip a short first month so adjacent month labels cannot overlap.
        if (index > 0 || cells[14]?.date.slice(0, 7) === month) {
          const label = document.createElement('span');
          label.textContent = monthFormat.format(new Date(day.date));
          label.style.gridColumn = String(index / 7 + 1);
          months.append(label);
        }
        previousMonth = month;
      }
    }
    const cell = document.createElement(day.padding ? 'span' : 'button');
    cell.className = `activity-cell level-${intensity(day.tokens)}${day.padding ? ' activity-padding' : ''}`;
    if (!day.padding) {
      cell.type = 'button';
      cell.tabIndex = -1;
      cell.dataset.date = day.date;
      const description = `${dateLabel.format(new Date(day.date))}: ${day.tokens === null ? 'not reported' : `${integer.format(day.tokens)} tokens`}`;
      cell.title = description;
      cell.setAttribute('aria-label', description);
      const describe = () => { byId('detail').textContent = description; };
      cell.addEventListener('mouseenter', describe);
      cell.addEventListener('click', describe);
      cell.addEventListener('focus', () => {
        for (const button of buttons) button.tabIndex = button === cell ? 0 : -1;
        describe();
      });
      buttons.push(cell);
    } else {
      cell.setAttribute('aria-hidden', 'true');
    }
    fragment.append(cell);
  }
  grid.append(fragment);
  buttons.at(-1).tabIndex = 0;
  grid.addEventListener('keydown', (event) => {
    const index = buttons.indexOf(event.target);
    if (index < 0) return;
    const offsets = { ArrowLeft: -7, ArrowRight: 7, ArrowUp: -1, ArrowDown: 1 };
    let target;
    if (event.key === 'Home') target = 0;
    else if (event.key === 'End') target = buttons.length - 1;
    else if (event.key in offsets) target = Math.max(0, Math.min(buttons.length - 1, index + offsets[event.key]));
    else return;
    event.preventDefault();
    buttons[target].focus();
  });
  // On a phone, start with the latest days in view.
  const scroll = document.querySelector('.activity-scroll');
  scroll.scrollLeft = scroll.scrollWidth;
}

async function boot() {
  const root = document.querySelector('[data-usage-url]');
  if (!root) return;
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), 15000);
  try {
    const response = await fetch(root.dataset.usageUrl, { cache: 'no-cache', signal: controller.signal });
    if (!response.ok) throw new Error('Usage data unavailable');
    render(validateDataset(await response.json()));
  } catch {
    const status = document.getElementById('activity-status');
    status.textContent = 'Usage data could not be loaded. Please try again later.';
    status.dataset.state = 'error';
  } finally {
    clearTimeout(timeout);
  }
}

if (typeof document !== 'undefined') boot();
