import assert from 'node:assert/strict';
import test from 'node:test';
import { calendarDays, intensity, recentStats, validateDataset } from '../assets/activity.mjs';

const now = new Date('2026-10-26T12:00:00Z');

test('30-day statistics exclude today and distinguish missing days from zero', () => {
  const result = recentStats([
    { date: '2026-09-25', tokens: 999 },
    { date: '2026-09-26', tokens: 0 },
    { date: '2026-10-25', tokens: 120 },
    { date: '2026-10-26', tokens: 999 },
  ], now);
  assert.deepEqual(result, { start: '2026-09-26', end: '2026-10-25', reported: 2, total: 120, average: 60, active: 1 });
  assert.equal(recentStats([], now).total, null);
});

test('calendar is week-aligned, spans 365 dates, and handles leap years and DST', () => {
  for (const value of [now, new Date('2024-03-31T23:30:00Z'), new Date('2026-01-01T00:00:00Z')]) {
    const cells = calendarDays([], value);
    const visible = cells.filter((day) => !day.padding);
    assert.equal(cells.length % 7, 0);
    assert.equal(new Date(cells[0].date).getUTCDay(), 0);
    assert.equal(visible.length, 365);
    assert.equal(new Set(visible.map((day) => day.date)).size, 365);
    assert.equal(visible.at(-1).date, value.toISOString().slice(0, 10));
  }
  const cells = calendarDays([{ date: '2026-10-25', tokens: 0 }], now);
  assert.equal(cells.find((day) => day.date === '2026-10-25').tokens, 0);
  assert.equal(cells.find((day) => day.date === '2026-10-24').tokens, null);
  assert.equal(intensity(null), 'unknown');
  assert.equal(intensity(0), 0);
  assert.equal(intensity(1e8), 4);
});

test('invalid, duplicate, and unversioned data are rejected', () => {
  const data = { schema_version: 1, source: { id: 'codex-account-usage' }, updated_at: now.toISOString(), days: [] };
  assert.equal(validateDataset(data), data);
  for (const days of [
    [{ date: '2026-02-30', tokens: 1 }],
    [{ date: '2026-10-25', tokens: -1 }],
    [{ date: '2026-10-25', tokens: 1 }, { date: '2026-10-25', tokens: 2 }],
  ]) assert.throws(() => validateDataset({ ...data, days }));
  assert.throws(() => validateDataset({ ...data, schema_version: 2 }));
});
