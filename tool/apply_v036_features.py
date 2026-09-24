#!/usr/bin/env python3
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]

# --- Dependencies + version -------------------------------------------------
pub = ROOT/'pubspec.yaml'
p = pub.read_text()
if 'shared_preferences:' not in p:
    p = p.replace("  path: ^1.9.1", "  path: ^1.9.1\n  shared_preferences: ^2.5.3")
p = re.sub(r'^version:\s*.*$', 'version: 0.3.6+16', p, flags=re.M)
pub.write_text(p)

# --- Theme controller -------------------------------------------------------
(ROOT/'lib/theme_controller.dart').write_text(r'''import 'package:flutter/foundation.dart';
import 'package:shared_preferences/shared_preferences.dart';

class ThemeController extends ChangeNotifier {
  ThemeController._();
  static final ThemeController instance = ThemeController._();

  static const _key = 'muscletrack_dark_mode';
  bool _isDark = false;

  bool get isDark => _isDark;

  Future<void> load() async {
    final prefs = await SharedPreferences.getInstance();
    _isDark = prefs.getBool(_key) ?? false;
  }

  Future<void> toggle() async {
    _isDark = !_isDark;
    notifyListeners();
    final prefs = await SharedPreferences.getInstance();
    await prefs.setBool(_key, _isDark);
  }
}
''')

# --- Persistent workout stopwatch ------------------------------------------
(ROOT/'lib/workout_timer_service.dart').write_text(r'''import 'dart:async';

import 'package:flutter/foundation.dart';
import 'package:shared_preferences/shared_preferences.dart';

class WorkoutTimerService extends ChangeNotifier {
  WorkoutTimerService._();
  static final WorkoutTimerService instance = WorkoutTimerService._();

  static const _runningKey = 'workout_timer_running';
  static const _startedKey = 'workout_timer_started_ms';
  static const _accumulatedKey = 'workout_timer_accumulated_seconds';

  bool _running = false;
  DateTime? _startedAt;
  int _accumulatedSeconds = 0;
  Timer? _ticker;

  bool get isRunning => _running;
  bool get isActive => _running || _accumulatedSeconds > 0;

  int get elapsedSeconds {
    if (!_running || _startedAt == null) return _accumulatedSeconds;
    final live = DateTime.now().difference(_startedAt!).inSeconds;
    return _accumulatedSeconds + (live < 0 ? 0 : live);
  }

  String get formatted {
    final seconds = elapsedSeconds;
    final h = seconds ~/ 3600;
    final m = (seconds % 3600) ~/ 60;
    final s = seconds % 60;
    return '${h.toString().padLeft(2, '0')}:'
        '${m.toString().padLeft(2, '0')}:'
        '${s.toString().padLeft(2, '0')}';
  }

  Future<void> load() async {
    final prefs = await SharedPreferences.getInstance();
    _running = prefs.getBool(_runningKey) ?? false;
    _accumulatedSeconds = prefs.getInt(_accumulatedKey) ?? 0;
    final startedMs = prefs.getInt(_startedKey);
    _startedAt = startedMs == null
        ? null
        : DateTime.fromMillisecondsSinceEpoch(startedMs);
    if (_running && _startedAt != null) _startTicker();
  }

  Future<void> startOrResume() async {
    if (_running) return;
    _running = true;
    _startedAt = DateTime.now();
    _startTicker();
    notifyListeners();
    await _persist();
  }

  Future<void> pause() async {
    if (!_running) return;
    _accumulatedSeconds = elapsedSeconds;
    _running = false;
    _startedAt = null;
    _ticker?.cancel();
    notifyListeners();
    await _persist();
  }

  Future<int> finish() async {
    final value = elapsedSeconds;
    await reset();
    return value;
  }

  Future<void> reset() async {
    _running = false;
    _startedAt = null;
    _accumulatedSeconds = 0;
    _ticker?.cancel();
    notifyListeners();
    final prefs = await SharedPreferences.getInstance();
    await prefs.remove(_runningKey);
    await prefs.remove(_startedKey);
    await prefs.remove(_accumulatedKey);
  }

  void _startTicker() {
    _ticker?.cancel();
    _ticker = Timer.periodic(const Duration(seconds: 1), (_) {
      notifyListeners();
    });
  }

  Future<void> _persist() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setBool(_runningKey, _running);
    await prefs.setInt(_accumulatedKey, _accumulatedSeconds);
    if (_startedAt != null) {
      await prefs.setInt(_startedKey, _startedAt!.millisecondsSinceEpoch);
    } else {
      await prefs.remove(_startedKey);
    }
  }
}
''')

# --- Themes -----------------------------------------------------------------
(ROOT/'lib/theme.dart').write_text(r'''import 'package:flutter/material.dart';

ThemeData buildAppTheme() {
  const primary = Color(0xFF079669);
  const darkGreen = Color(0xFF075B49);
  const background = Color(0xFFF5F8F7);
  const border = Color(0xFFDCE7E2);

  final scheme = ColorScheme.fromSeed(
    seedColor: primary,
    brightness: Brightness.light,
  ).copyWith(
    primary: primary,
    onPrimary: Colors.white,
    secondary: darkGreen,
    surface: Colors.white,
    surfaceContainerHighest: const Color(0xFFEDF5F1),
    outline: border,
  );

  return ThemeData(
    useMaterial3: true,
    colorScheme: scheme,
    scaffoldBackgroundColor: background,
    appBarTheme: const AppBarTheme(
      backgroundColor: background,
      foregroundColor: Color(0xFF17312A),
      elevation: 0,
      surfaceTintColor: Colors.transparent,
    ),
    cardTheme: const CardThemeData(
      color: Colors.white,
      surfaceTintColor: Colors.transparent,
      elevation: 0,
      shape: RoundedRectangleBorder(
        side: BorderSide(color: border),
        borderRadius: BorderRadius.all(Radius.circular(18)),
      ),
    ),
    inputDecorationTheme: const InputDecorationTheme(
      filled: true,
      fillColor: Colors.white,
      border: OutlineInputBorder(
        borderSide: BorderSide(color: border),
        borderRadius: BorderRadius.all(Radius.circular(12)),
      ),
    ),
    navigationBarTheme: const NavigationBarThemeData(
      backgroundColor: Colors.white,
      indicatorColor: Color(0xFFDDF3E9),
      surfaceTintColor: Colors.transparent,
    ),
  );
}

ThemeData buildDarkAppTheme() {
  const primary = Color(0xFF35D39A);
  const surface = Color(0xFF17211F);
  const background = Color(0xFF0D1413);
  const border = Color(0xFF31423D);

  final scheme = ColorScheme.fromSeed(
    seedColor: primary,
    brightness: Brightness.dark,
  ).copyWith(
    primary: primary,
    onPrimary: const Color(0xFF042118),
    surface: surface,
    surfaceContainerHighest: const Color(0xFF21302C),
    outline: border,
  );

  return ThemeData(
    useMaterial3: true,
    brightness: Brightness.dark,
    colorScheme: scheme,
    scaffoldBackgroundColor: background,
    appBarTheme: const AppBarTheme(
      backgroundColor: background,
      foregroundColor: Color(0xFFE7F2EE),
      elevation: 0,
      surfaceTintColor: Colors.transparent,
    ),
    cardTheme: const CardThemeData(
      color: surface,
      surfaceTintColor: Colors.transparent,
      elevation: 0,
      shape: RoundedRectangleBorder(
        side: BorderSide(color: border),
        borderRadius: BorderRadius.all(Radius.circular(18)),
      ),
    ),
    inputDecorationTheme: const InputDecorationTheme(
      filled: true,
      fillColor: Color(0xFF1E2B27),
      border: OutlineInputBorder(
        borderSide: BorderSide(color: border),
        borderRadius: BorderRadius.all(Radius.circular(12)),
      ),
      enabledBorder: OutlineInputBorder(
        borderSide: BorderSide(color: border),
        borderRadius: BorderRadius.all(Radius.circular(12)),
      ),
    ),
    navigationBarTheme: const NavigationBarThemeData(
      backgroundColor: Color(0xFF111B19),
      indicatorColor: Color(0xFF244D3F),
      surfaceTintColor: Colors.transparent,
    ),
  );
}
''')

# --- Main: initialise persistent theme + stopwatch ---------------------------
main = ROOT/'lib/main.dart'
m = main.read_text()
if "theme_controller.dart" not in m:
    m = m.replace("import 'theme.dart';", "import 'theme.dart';\nimport 'theme_controller.dart';\nimport 'workout_timer_service.dart';")
m = m.replace(
    "  final store = AppStore(AppDatabase());\n  await store.load();",
    "  final store = AppStore(AppDatabase());\n  await store.load();\n  await ThemeController.instance.load();\n  await WorkoutTimerService.instance.load();",
)
m = m.replace(
    "    widget.store.addListener(_refresh);",
    "    widget.store.addListener(_refresh);\n    ThemeController.instance.addListener(_refresh);",
)
m = m.replace(
    "    widget.store.removeListener(_refresh);",
    "    widget.store.removeListener(_refresh);\n    ThemeController.instance.removeListener(_refresh);",
)
m = m.replace(
    "      theme: buildAppTheme(),",
    "      theme: buildAppTheme(),\n      darkTheme: buildDarkAppTheme(),\n      themeMode: ThemeController.instance.isDark ? ThemeMode.dark : ThemeMode.light,",
)
main.write_text(m)

# --- Models: exact workout seconds + daily activity --------------------------
models = ROOT/'lib/models.dart'
md = models.read_text()
if 'final int? durationSeconds;' not in md:
    md = md.replace(
        "  final int durationMin;\n  final double? met;",
        "  final int durationMin;\n  final int? durationSeconds;\n  final double? met;",
    )
    md = md.replace(
        "    required this.durationMin,\n    this.met,",
        "    required this.durationMin,\n    this.durationSeconds,\n    this.met,",
    )
    md = md.replace(
        "        'duration_min': durationMin,\n        'met': met,",
        "        'duration_min': durationMin,\n        'duration_seconds': durationSeconds,\n        'met': met,",
    )
if 'class DailyActivity' not in md:
    md += r'''

class DailyActivity {
  final DateTime date;
  final int steps;
  final int activeMinutes;
  final double activeCalories;
  final String source;

  const DailyActivity({
    required this.date,
    required this.steps,
    required this.activeMinutes,
    required this.activeCalories,
    this.source = 'Smartwatch',
  });

  Map<String, Object?> toMap() => {
        'date': DateTime(date.year, date.month, date.day).toIso8601String(),
        'steps': steps,
        'active_minutes': activeMinutes,
        'active_calories': activeCalories,
        'source': source,
      };

  factory DailyActivity.fromMap(Map<String, Object?> map) => DailyActivity(
        date: DateTime.parse(map['date'] as String),
        steps: (map['steps'] as num).toInt(),
        activeMinutes: (map['active_minutes'] as num).toInt(),
        activeCalories: (map['active_calories'] as num).toDouble(),
        source: (map['source'] as String?) ?? 'Smartwatch',
      );
}
'''
models.write_text(md)

# --- Database migration ------------------------------------------------------
db = ROOT/'lib/app_database.dart'
d = db.read_text()
d = d.replace('version: 2,', 'version: 3,')
if 'duration_seconds INTEGER' not in d:
    d = d.replace(
        "            duration_min INTEGER NOT NULL,\n            met REAL,",
        "            duration_min INTEGER NOT NULL,\n            duration_seconds INTEGER,\n            met REAL,",
    )
if 'CREATE TABLE daily_activity' not in d:
    # Add table to fresh database.
    anchor = """        await db.execute('''
          CREATE TABLE exercise_sets("""
    table = """        await db.execute('''
          CREATE TABLE daily_activity(
            date TEXT PRIMARY KEY,
            steps INTEGER NOT NULL DEFAULT 0,
            active_minutes INTEGER NOT NULL DEFAULT 0,
            active_calories REAL NOT NULL DEFAULT 0,
            source TEXT NOT NULL DEFAULT 'Smartwatch'
          )
        ''');
"""
    d = d.replace(anchor, table + anchor, 1)
    # Upgrade existing v2 database.
    upgrade_anchor = """        if (oldVersion < 2) {
          await db.execute(
            "ALTER TABLE workouts ADD COLUMN body_parts TEXT NOT NULL DEFAULT ''",
          );
        }"""
    upgrade_new = upgrade_anchor + """
        if (oldVersion < 3) {
          await db.execute(
            "ALTER TABLE workouts ADD COLUMN duration_seconds INTEGER",
          );
          await db.execute('''
            CREATE TABLE IF NOT EXISTS daily_activity(
              date TEXT PRIMARY KEY,
              steps INTEGER NOT NULL DEFAULT 0,
              active_minutes INTEGER NOT NULL DEFAULT 0,
              active_calories REAL NOT NULL DEFAULT 0,
              source TEXT NOT NULL DEFAULT 'Smartwatch'
            )
          ''');
        }"""
    d = d.replace(upgrade_anchor, upgrade_new)
if 'durationSeconds:' not in d:
    d = d.replace(
        "          durationMin: (row['duration_min'] as num).toInt(),\n          met:",
        "          durationMin: (row['duration_min'] as num).toInt(),\n          durationSeconds: (row['duration_seconds'] as num?)?.toInt(),\n          met:",
    )
if 'Future<void> saveDailyActivity' not in d:
    insert_point = "\n  Future<void> clearAll() async {"
    methods = r'''
  Future<void> saveDailyActivity(DailyActivity activity) async {
    final db = await database;
    await db.insert(
      'daily_activity',
      activity.toMap(),
      conflictAlgorithm: ConflictAlgorithm.replace,
    );
  }

  Future<List<DailyActivity>> loadDailyActivities() async {
    final db = await database;
    final rows = await db.query('daily_activity', orderBy: 'date DESC');
    return rows.map(DailyActivity.fromMap).toList();
  }

  Future<void> deleteDailyActivity(DateTime date) async {
    final db = await database;
    final day = DateTime(date.year, date.month, date.day).toIso8601String();
    await db.delete('daily_activity', where: 'date = ?', whereArgs: [day]);
  }
'''
    d = d.replace(insert_point, methods + insert_point)
if "await txn.delete('daily_activity');" not in d:
    d = d.replace(
        "    await db.transaction((txn) async {\n      await txn.delete('exercise_sets');",
        "    await db.transaction((txn) async {\n      await txn.delete('daily_activity');\n      await txn.delete('exercise_sets');",
    )
db.write_text(d)

# --- Store ------------------------------------------------------------------
store = ROOT/'lib/app_store.dart'
s = store.read_text()
if 'List<DailyActivity> dailyActivities' not in s:
    s = s.replace(
        "  List<WorkoutSession> workouts = [];",
        "  List<WorkoutSession> workouts = [];\n  List<DailyActivity> dailyActivities = [];",
    )
    s = s.replace(
        "    workouts = await db.loadWorkouts();",
        "    workouts = await db.loadWorkouts();\n    dailyActivities = await db.loadDailyActivities();",
        1,
    )
    # refresh() has a second loadWorkouts occurrence
    refresh_old = """  Future<void> refresh() async {
    profile = await db.loadProfile();
    workouts = await db.loadWorkouts();
    notifyListeners();
  }"""
    refresh_new = """  Future<void> refresh() async {
    profile = await db.loadProfile();
    workouts = await db.loadWorkouts();
    dailyActivities = await db.loadDailyActivities();
    notifyListeners();
  }"""
    s = s.replace(refresh_old, refresh_new)
    methods = r'''
  DailyActivity? activityForDay(DateTime value) {
    final day = DateTime(value.year, value.month, value.day);
    for (final activity in dailyActivities) {
      final d = DateTime(activity.date.year, activity.date.month, activity.date.day);
      if (d == day) return activity;
    }
    return null;
  }

  Future<void> saveDailyActivity(DailyActivity value) async {
    await db.saveDailyActivity(value);
    await refresh();
  }

  Future<void> deleteDailyActivity(DateTime value) async {
    await db.deleteDailyActivity(value);
    await refresh();
  }

  List<DailyActivity> get last7DaysActivity {
    final now = DateTime.now();
    final today = DateTime(now.year, now.month, now.day);
    final start = today.subtract(const Duration(days: 6));
    return dailyActivities.where((a) {
      final d = DateTime(a.date.year, a.date.month, a.date.day);
      return !d.isBefore(start) && !d.isAfter(today);
    }).toList();
  }

'''
    s = s.replace("\n  StrengthBest? get latestStrengthBest", "\n" + methods + "  StrengthBest? get latestStrengthBest")
store.write_text(s)

# --- Daily activity entry screen --------------------------------------------
(ROOT/'lib/screens/daily_activity_screen.dart').write_text(r'''import 'package:flutter/material.dart';

import '../app_store.dart';
import '../models.dart';

class DailyActivityScreen extends StatefulWidget {
  final AppStore store;
  final DateTime? initialDate;

  const DailyActivityScreen({
    super.key,
    required this.store,
    this.initialDate,
  });

  @override
  State<DailyActivityScreen> createState() => _DailyActivityScreenState();
}

class _DailyActivityScreenState extends State<DailyActivityScreen> {
  late DateTime _date;
  late final TextEditingController _steps;
  late final TextEditingController _minutes;
  late final TextEditingController _calories;

  @override
  void initState() {
    super.initState();
    final now = widget.initialDate ?? DateTime.now();
    _date = DateTime(now.year, now.month, now.day);
    final existing = widget.store.activityForDay(_date);
    _steps = TextEditingController(text: existing?.steps.toString() ?? '');
    _minutes =
        TextEditingController(text: existing?.activeMinutes.toString() ?? '');
    _calories = TextEditingController(
      text: existing == null
          ? ''
          : existing.activeCalories.toStringAsFixed(
              existing.activeCalories % 1 == 0 ? 0 : 1,
            ),
    );
  }

  @override
  void dispose() {
    _steps.dispose();
    _minutes.dispose();
    _calories.dispose();
    super.dispose();
  }

  void _reloadForDate(DateTime value) {
    final existing = widget.store.activityForDay(value);
    _steps.text = existing?.steps.toString() ?? '';
    _minutes.text = existing?.activeMinutes.toString() ?? '';
    _calories.text = existing == null
        ? ''
        : existing.activeCalories.toStringAsFixed(
            existing.activeCalories % 1 == 0 ? 0 : 1,
          );
  }

  Future<void> _save() async {
    final steps = int.tryParse(_steps.text) ?? 0;
    final minutes = int.tryParse(_minutes.text) ?? 0;
    final calories = double.tryParse(_calories.text) ?? 0;
    if (steps < 0 || minutes < 0 || calories < 0 ||
        (steps == 0 && minutes == 0 && calories == 0)) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text('Enter at least one smartwatch activity value.'),
        ),
      );
      return;
    }

    await widget.store.saveDailyActivity(
      DailyActivity(
        date: _date,
        steps: steps,
        activeMinutes: minutes,
        activeCalories: calories,
      ),
    );
    if (mounted) Navigator.pop(context);
  }

  @override
  Widget build(BuildContext context) {
    final existing = widget.store.activityForDay(_date);
    return Scaffold(
      appBar: AppBar(title: const Text('Daily activity')),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          Card(
            child: Padding(
              padding: const EdgeInsets.all(16),
              child: Column(
                children: [
                  ListTile(
                    contentPadding: EdgeInsets.zero,
                    leading: const Icon(Icons.watch_rounded),
                    title: const Text(
                      'Smartwatch activity',
                      style: TextStyle(fontWeight: FontWeight.w900),
                    ),
                    subtitle: const Text(
                      'Enter the daily values shown on your watch.',
                    ),
                    trailing: const Chip(label: Text('Smartwatch')),
                  ),
                  const SizedBox(height: 8),
                  ListTile(
                    contentPadding: EdgeInsets.zero,
                    title: const Text('Date'),
                    subtitle: Text(
                      '${_date.day}/${_date.month}/${_date.year}',
                    ),
                    trailing: const Icon(Icons.calendar_month_rounded),
                    onTap: () async {
                      final picked = await showDatePicker(
                        context: context,
                        firstDate: DateTime(2020),
                        lastDate: DateTime.now(),
                        initialDate: _date,
                      );
                      if (picked != null) {
                        setState(() {
                          _date = DateTime(
                            picked.year,
                            picked.month,
                            picked.day,
                          );
                          _reloadForDate(_date);
                        });
                      }
                    },
                  ),
                  const SizedBox(height: 10),
                  TextField(
                    controller: _steps,
                    keyboardType: TextInputType.number,
                    decoration: const InputDecoration(
                      labelText: 'Daily step count',
                      prefixIcon: Icon(Icons.directions_walk_rounded),
                      suffixText: 'steps',
                    ),
                  ),
                  const SizedBox(height: 10),
                  TextField(
                    controller: _minutes,
                    keyboardType: TextInputType.number,
                    decoration: const InputDecoration(
                      labelText: 'Active time',
                      prefixIcon: Icon(Icons.timer_outlined),
                      suffixText: 'min',
                    ),
                  ),
                  const SizedBox(height: 10),
                  TextField(
                    controller: _calories,
                    keyboardType:
                        const TextInputType.numberWithOptions(decimal: true),
                    decoration: const InputDecoration(
                      labelText: 'Active calories',
                      prefixIcon: Icon(Icons.local_fire_department_rounded),
                      suffixText: 'kcal',
                    ),
                  ),
                ],
              ),
            ),
          ),
          const SizedBox(height: 14),
          FilledButton.icon(
            onPressed: _save,
            icon: const Icon(Icons.save_rounded),
            label: Text(existing == null ? 'Save activity' : 'Update activity'),
          ),
          if (existing != null) ...[
            const SizedBox(height: 8),
            OutlinedButton.icon(
              onPressed: () async {
                await widget.store.deleteDailyActivity(_date);
                if (mounted) Navigator.pop(context);
              },
              icon: const Icon(Icons.delete_outline_rounded),
              label: const Text('Delete this day'),
            ),
          ],
        ],
      ),
    );
  }
}
''')

# --- Daily activity progress -------------------------------------------------
(ROOT/'lib/screens/activity_progress_screen.dart').write_text(r'''import 'package:flutter/material.dart';

import '../app_store.dart';

class ActivityProgressScreen extends StatelessWidget {
  final AppStore store;
  const ActivityProgressScreen({super.key, required this.store});

  @override
  Widget build(BuildContext context) {
    final days = store.last7DaysActivity;
    final totalSteps = days.fold<int>(0, (s, a) => s + a.steps);
    final totalMinutes = days.fold<int>(0, (s, a) => s + a.activeMinutes);
    final totalCalories =
        days.fold<double>(0, (s, a) => s + a.activeCalories);
    final divisor = days.isEmpty ? 1 : days.length;

    return Scaffold(
      appBar: AppBar(title: const Text('Daily activity progress')),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          const Text(
            'Last 7 days',
            style: TextStyle(fontSize: 20, fontWeight: FontWeight.w900),
          ),
          const SizedBox(height: 12),
          Row(
            children: [
              Expanded(
                child: _Metric(
                  icon: Icons.directions_walk_rounded,
                  value: '${(totalSteps / divisor).round()}',
                  label: 'Avg steps/day',
                ),
              ),
              const SizedBox(width: 8),
              Expanded(
                child: _Metric(
                  icon: Icons.timer_outlined,
                  value: '${(totalMinutes / divisor).round()}',
                  label: 'Avg active min',
                ),
              ),
              const SizedBox(width: 8),
              Expanded(
                child: _Metric(
                  icon: Icons.local_fire_department_rounded,
                  value: (totalCalories / divisor).round().toString(),
                  label: 'Avg active kcal',
                ),
              ),
            ],
          ),
          const SizedBox(height: 16),
          if (days.isEmpty)
            const Card(
              child: Padding(
                padding: EdgeInsets.all(20),
                child: Text(
                  'No smartwatch activity has been entered yet.',
                  textAlign: TextAlign.center,
                ),
              ),
            )
          else
            ...days.map(
              (a) => Card(
                child: ListTile(
                  leading: const CircleAvatar(
                    child: Icon(Icons.watch_rounded),
                  ),
                  title: Text(
                    '${a.date.day}/${a.date.month}/${a.date.year}',
                    style: const TextStyle(fontWeight: FontWeight.w900),
                  ),
                  subtitle: Text(
                    '${a.steps} steps • ${a.activeMinutes} min',
                  ),
                  trailing: Text(
                    '${a.activeCalories.toStringAsFixed(0)} kcal',
                    style: const TextStyle(fontWeight: FontWeight.w800),
                  ),
                ),
              ),
            ),
        ],
      ),
    );
  }
}

class _Metric extends StatelessWidget {
  final IconData icon;
  final String value;
  final String label;
  const _Metric({
    required this.icon,
    required this.value,
    required this.label,
  });

  @override
  Widget build(BuildContext context) => Card(
        child: Padding(
          padding: const EdgeInsets.symmetric(vertical: 14, horizontal: 8),
          child: Column(
            children: [
              Icon(icon, color: Theme.of(context).colorScheme.primary),
              const SizedBox(height: 6),
              Text(
                value,
                style: const TextStyle(
                  fontSize: 18,
                  fontWeight: FontWeight.w900,
                ),
              ),
              Text(
                label,
                textAlign: TextAlign.center,
                style: Theme.of(context).textTheme.labelSmall,
              ),
            ],
          ),
        ),
      );
}
''')

# --- Home: theme toggle, stopwatch status, daily activity --------------------
home = ROOT/'lib/screens/home_screen.dart'
h = home.read_text()
if "theme_controller.dart" not in h:
    h = h.replace(
        "import '../models.dart';",
        "import '../models.dart';\nimport '../theme_controller.dart';\nimport '../workout_timer_service.dart';",
    )
    h = h.replace(
        "import 'calendar_screen.dart';",
        "import 'calendar_screen.dart';\nimport 'daily_activity_screen.dart';\nimport 'activity_progress_screen.dart';",
    )

# Top-right light/dark toggle.
if "tooltip: 'Switch to" not in h:
    old = """      CircleAvatar(
        radius: 20,"""
    new = """      IconButton(
        tooltip: ThemeController.instance.isDark
            ? 'Switch to light mode'
            : 'Switch to dark mode',
        onPressed: ThemeController.instance.toggle,
        icon: Icon(
          ThemeController.instance.isDark
              ? Icons.light_mode_rounded
              : Icons.dark_mode_rounded,
        ),
      ),
      CircleAvatar(
        radius: 20,"""
    h = h.replace(old, new, 1)

# Add current activity calculation.
if "final todayActivity = store.activityForDay(today);" not in h:
    h = h.replace(
        "    final streak = store.streakSummary;",
        "    final streak = store.streakSummary;\n    final todayActivity = store.activityForDay(today);",
    )

# Add timer home card + daily activity after quick logging buttons.
if "_WorkoutTimerHomeCard(" not in h:
    marker = """        const SizedBox(height: 12),
        _StreakCard("""
    insertion = """        const SizedBox(height: 12),
        const _WorkoutTimerHomeCard(),
        const SizedBox(height: 12),
        _DailyActivityCard(
          activity: todayActivity,
          onLog: () => Navigator.push(
            context,
            MaterialPageRoute(
              builder: (_) => DailyActivityScreen(store: store),
            ),
          ),
          onProgress: () => Navigator.push(
            context,
            MaterialPageRoute(
              builder: (_) => ActivityProgressScreen(store: store),
            ),
          ),
        ),
        const SizedBox(height: 12),
        _StreakCard("""
    h = h.replace(marker, insertion, 1)

# Add widgets before streak card.
if "class _DailyActivityCard" not in h:
    marker = "class _StreakCard extends StatelessWidget {"
    widgets = r'''class _WorkoutTimerHomeCard extends StatefulWidget {
  const _WorkoutTimerHomeCard();

  @override
  State<_WorkoutTimerHomeCard> createState() => _WorkoutTimerHomeCardState();
}

class _WorkoutTimerHomeCardState extends State<_WorkoutTimerHomeCard> {
  final timer = WorkoutTimerService.instance;

  @override
  void initState() {
    super.initState();
    timer.addListener(_refresh);
  }

  @override
  void dispose() {
    timer.removeListener(_refresh);
    super.dispose();
  }

  void _refresh() {
    if (mounted) setState(() {});
  }

  @override
  Widget build(BuildContext context) {
    if (!timer.isActive) return const SizedBox.shrink();
    return Card(
      child: ListTile(
        leading: const CircleAvatar(
          child: Icon(Icons.timer_rounded),
        ),
        title: Text(
          timer.isRunning ? 'Workout timer running' : 'Workout timer paused',
          style: const TextStyle(fontWeight: FontWeight.w900),
        ),
        subtitle: Text(
          timer.formatted,
          style: const TextStyle(
            fontSize: 22,
            fontWeight: FontWeight.w900,
            fontFeatures: [FontFeature.tabularFigures()],
          ),
        ),
        trailing: Icon(
          timer.isRunning
              ? Icons.play_circle_fill_rounded
              : Icons.pause_circle_filled_rounded,
        ),
      ),
    );
  }
}

class _DailyActivityCard extends StatelessWidget {
  final DailyActivity? activity;
  final VoidCallback onLog;
  final VoidCallback onProgress;

  const _DailyActivityCard({
    required this.activity,
    required this.onLog,
    required this.onProgress,
  });

  @override
  Widget build(BuildContext context) => Card(
        child: Padding(
          padding: const EdgeInsets.all(15),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Row(
                children: [
                  const Icon(Icons.watch_rounded),
                  const SizedBox(width: 8),
                  const Expanded(
                    child: Text(
                      'Daily activity',
                      style: TextStyle(
                        fontSize: 16,
                        fontWeight: FontWeight.w900,
                      ),
                    ),
                  ),
                  TextButton(
                    onPressed: onProgress,
                    child: const Text('Progress'),
                  ),
                ],
              ),
              const SizedBox(height: 10),
              Row(
                children: [
                  Expanded(
                    child: _MiniMetric(
                      icon: Icons.directions_walk_rounded,
                      value: '${activity?.steps ?? 0}',
                      label: 'Steps',
                    ),
                  ),
                  Expanded(
                    child: _MiniMetric(
                      icon: Icons.timer_outlined,
                      value: '${activity?.activeMinutes ?? 0}',
                      label: 'Active min',
                    ),
                  ),
                  Expanded(
                    child: _MiniMetric(
                      icon: Icons.local_fire_department_rounded,
                      value: (activity?.activeCalories ?? 0)
                          .toStringAsFixed(0),
                      label: 'Active kcal',
                    ),
                  ),
                ],
              ),
              const SizedBox(height: 12),
              SizedBox(
                width: double.infinity,
                child: OutlinedButton.icon(
                  onPressed: onLog,
                  icon: const Icon(Icons.edit_rounded),
                  label: Text(
                    activity == null
                        ? 'Enter smartwatch activity'
                        : 'Edit smartwatch activity',
                  ),
                ),
              ),
            ],
          ),
        ),
      );
}

'''
    h = h.replace(marker, widgets + marker)
home.write_text(h)

# FontFeature import required by timer home card.
h = home.read_text()
if "dart:ui" not in h:
    h = h.replace("import 'dart:math' as math;", "import 'dart:math' as math;\nimport 'dart:ui' show FontFeature;")
home.write_text(h)

# --- Workout screen stopwatch ------------------------------------------------
workout = ROOT/'lib/screens/strength_workout_screen.dart'
w = workout.read_text()
if "workout_timer_service.dart" not in w:
    w = w.replace(
        "import '../models.dart';",
        "import '../models.dart';\nimport '../workout_timer_service.dart';",
    )
if "_timerRecordedSeconds" not in w:
    w = w.replace(
        "  int? _sessionRpe;",
        "  int? _sessionRpe;\n  int _timerRecordedSeconds = 0;",
    )
    w = w.replace(
        "    _sessionRpe = existing?.sessionRpe;",
        "    _sessionRpe = existing?.sessionRpe;\n    _timerRecordedSeconds = existing?.durationSeconds ?? 0;\n    WorkoutTimerService.instance.addListener(_timerRefresh);",
    )
    w = w.replace(
        "    _notes.dispose();",
        "    WorkoutTimerService.instance.removeListener(_timerRefresh);\n    _notes.dispose();",
    )
    # Insert methods before _selectAll.
    w = w.replace(
        "  void _selectAll(TextEditingController controller) {",
        r'''  void _timerRefresh() {
    if (mounted) setState(() {});
  }

  Future<void> _finishTimer() async {
    final seconds = await WorkoutTimerService.instance.finish();
    if (seconds <= 0) return;
    setState(() {
      _timerRecordedSeconds = seconds;
      _duration.text = ((seconds + 59) ~/ 60).toString();
    });
  }

  String _formatSeconds(int seconds) {
    final h = seconds ~/ 3600;
    final m = (seconds % 3600) ~/ 60;
    final s = seconds % 60;
    return '${h.toString().padLeft(2, '0')}:'
        '${m.toString().padLeft(2, '0')}:'
        '${s.toString().padLeft(2, '0')}';
  }

  void _selectAll(TextEditingController controller) {''',
    )
    # Capture running timer if user directly saves.
    w = w.replace(
        "  Future<void> _save() async {\n    final duration",
        """  Future<void> _save() async {
    if (WorkoutTimerService.instance.isActive) {
      final seconds = await WorkoutTimerService.instance.finish();
      if (seconds > 0) {
        _timerRecordedSeconds = seconds;
        _duration.text = ((seconds + 59) ~/ 60).toString();
      }
    }
    final duration""",
    )
    w = w.replace(
        "      durationMin: duration,\n      met:",
        "      durationMin: duration,\n      durationSeconds: _timerRecordedSeconds > 0 ? _timerRecordedSeconds : duration * 60,\n      met:",
    )
    # Add timer card before pre-workout section.
    first_section = """        children: [
          _sectionCard(
            context,
            title: 'Pre-workout check-in',"""
    timer_ui = r'''        children: [
          Card(
            child: Padding(
              padding: const EdgeInsets.all(16),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const Row(
                    children: [
                      Icon(Icons.timer_rounded),
                      SizedBox(width: 8),
                      Text(
                        'Workout timer',
                        style: TextStyle(
                          fontSize: 16,
                          fontWeight: FontWeight.w900,
                        ),
                      ),
                    ],
                  ),
                  const SizedBox(height: 10),
                  Center(
                    child: Text(
                      WorkoutTimerService.instance.isActive
                          ? WorkoutTimerService.instance.formatted
                          : _formatSeconds(_timerRecordedSeconds),
                      style: const TextStyle(
                        fontSize: 38,
                        fontWeight: FontWeight.w900,
                        letterSpacing: 1,
                      ),
                    ),
                  ),
                  const SizedBox(height: 10),
                  Row(
                    children: [
                      Expanded(
                        child: FilledButton.icon(
                          onPressed: WorkoutTimerService.instance.isRunning
                              ? null
                              : WorkoutTimerService.instance.startOrResume,
                          icon: Icon(
                            WorkoutTimerService.instance.isActive
                                ? Icons.play_arrow_rounded
                                : Icons.play_circle_outline_rounded,
                          ),
                          label: Text(
                            WorkoutTimerService.instance.isActive
                                ? 'Resume'
                                : 'Start',
                          ),
                        ),
                      ),
                      const SizedBox(width: 8),
                      Expanded(
                        child: OutlinedButton.icon(
                          onPressed: WorkoutTimerService.instance.isRunning
                              ? WorkoutTimerService.instance.pause
                              : null,
                          icon: const Icon(Icons.pause_rounded),
                          label: const Text('Pause'),
                        ),
                      ),
                      const SizedBox(width: 8),
                      Expanded(
                        child: OutlinedButton.icon(
                          onPressed: WorkoutTimerService.instance.isActive
                              ? _finishTimer
                              : null,
                          icon: const Icon(Icons.stop_rounded),
                          label: const Text('Finish'),
                        ),
                      ),
                    ],
                  ),
                  if (_timerRecordedSeconds > 0 &&
                      !WorkoutTimerService.instance.isActive) ...[
                    const SizedBox(height: 8),
                    Center(
                      child: Text(
                        'Saved timer: ${_formatSeconds(_timerRecordedSeconds)}',
                        style: Theme.of(context).textTheme.bodySmall,
                      ),
                    ),
                  ],
                ],
              ),
            ),
          ),
          const SizedBox(height: 14),
          _sectionCard(
            context,
            title: 'Pre-workout check-in','''
    w = w.replace(first_section, timer_ui, 1)
workout.write_text(w)

# --- Calendar: daily activity summary ---------------------------------------
cal = ROOT/'lib/screens/calendar_screen.dart'
cc = cal.read_text()
if "final activity = widget.store.activityForDay(_selected);" not in cc:
    cc = cc.replace(
        "    final canLog = !_selected.isAfter(today);",
        "    final canLog = !_selected.isAfter(today);\n    final activity = widget.store.activityForDay(_selected);",
    )
    cc = cc.replace(
        "                      final isRest = dayKind == DailyLogKind.rest;",
        "                      final isRest = dayKind == DailyLogKind.rest;\n                      final hasActivity = widget.store.activityForDay(date) != null;",
    )
    target = """                              if (isWorkout || isRest)
                                Positioned(
                                  bottom: 3,"""
    replacement = """                              if (hasActivity)
                                Positioned(
                                  top: 2,
                                  right: 2,
                                  child: Icon(
                                    Icons.directions_walk_rounded,
                                    size: 8,
                                    color: selected
                                        ? Colors.white
                                        : const Color(0xFF0A8FA3),
                                  ),
                                ),
                              if (isWorkout || isRest)
                                Positioned(
                                  bottom: 3,"""
    cc = cc.replace(target, replacement, 1)
    header = """          const SizedBox(height: 8),
          if (kind == DailyLogKind.rest)"""
    activity_card = """          const SizedBox(height: 8),
          if (activity != null) ...[
            Card(
              child: ListTile(
                leading: const CircleAvatar(
                  child: Icon(Icons.watch_rounded),
                ),
                title: const Text(
                  'Smartwatch activity',
                  style: TextStyle(fontWeight: FontWeight.w900),
                ),
                subtitle: Text(
                  '${activity.steps} steps • ${activity.activeMinutes} min • '
                  '${activity.activeCalories.toStringAsFixed(0)} kcal',
                ),
              ),
            ),
            const SizedBox(height: 8),
          ],
          if (kind == DailyLogKind.rest)"""
    cc = cc.replace(header, activity_card, 1)
cal.write_text(cc)

# --- Better dark backgrounds on key screens --------------------------------
for rel in [
    'lib/screens/calendar_screen.dart',
    'lib/screens/rewards_screen.dart',
    'lib/screens/body_progress_screen.dart',
    'lib/screens/strength_workout_screen.dart',
    'lib/screens/workout_history_screen.dart',
    'lib/screens/about_screen.dart',
]:
    path = ROOT/rel
    if not path.exists():
        continue
    txt = path.read_text()
    txt = txt.replace(
        "backgroundColor: const Color(0xFFF7FAF8),",
        "backgroundColor: Theme.of(context).scaffoldBackgroundColor,",
    )
    path.write_text(txt)

print('Applied v0.3.6 dark toggle, persistent workout timer, and smartwatch daily activity')
