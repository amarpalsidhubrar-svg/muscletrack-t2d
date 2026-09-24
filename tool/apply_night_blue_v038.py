#!/usr/bin/env python3
"""v0.3.8: blue night mode on top of the v0.3.6 build.

Day mode is left exactly as it is. Every hard-coded day colour in the screens
is routed through `context.tone(...)`, which swaps it for its blue night-mode
partner when the dark theme is active.

The night theme deliberately defines no TextStyles: v0.3.7 crashed when the
theme was toggled because its light and dark themes had TextStyles with
different `inherit` values, which ThemeData.lerp cannot animate between.
"""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]


def patch(path, old, new, count=1):
    f = ROOT/path
    text = f.read_text()
    if text.count(old) != count:
        raise SystemExit(f'{path}: expected {count} match(es) for {old!r}, found {text.count(old)}')
    f.write_text(text.replace(old, new))


# --- Night palette ----------------------------------------------------------
NIGHT = {
    # brand greens / teal -> blue
    0xFF087B55: 0xFF5AA9FF, 0xFF079669: 0xFF5AA9FF, 0xFF08765A: 0xFF5AA9FF,
    0xFF0B8C5E: 0xFF5AA9FF, 0xFF14A06F: 0xFF5AA9FF, 0xFF0A8FA3: 0xFF5AA9FF,
    0xFF79C6A4: 0xFF4D9BF0,
    # headings / body text
    0xFF092C2B: 0xFFEEF3FA, 0xFF17312A: 0xFFEEF3FA,
    0xFF314B43: 0xFFC5D0DE, 0xFF375149: 0xFFC5D0DE,
    # secondary text
    0xFF53665E: 0xFFA3B0C2, 0xFF5C6E67: 0xFFA3B0C2, 0xFF65766F: 0xFFA3B0C2,
    0xFF6D7D76: 0xFFA3B0C2, 0xFF687871: 0xFFA3B0C2, 0xFF5D6D67: 0xFFA3B0C2,
    0xFF60716A: 0xFFA3B0C2, 0xFF5F7068: 0xFFA3B0C2, 0xFF667871: 0xFFA3B0C2,
    0xFF76857F: 0xFFA3B0C2,
    # pale green / teal tints -> raised navy
    0xFFE2F5EB: 0xFF1A2A42, 0xFFDDF4E8: 0xFF1A2A42, 0xFFE6F5EF: 0xFF1A2A42,
    0xFFEAF6F1: 0xFF1A2A42, 0xFFEAF5F0: 0xFF1A2A42, 0xFFE1F7F9: 0xFF1A2A42,
    0xFFE7F7FA: 0xFF1A2A42,
    # hero card gradient
    0xFFF3FBF7: 0xFF172234, 0xFFE5F7EE: 0xFF111A28,
    # borders, tracks and dividers
    0xFFDCEFE6: 0xFF25324A, 0xFFE8EEEB: 0xFF25324A, 0xFFE7ECE9: 0xFF25324A,
    0xFFE6ECE9: 0xFF25324A, 0xFFDCE6E1: 0xFF25324A, 0xFFD6E9E0: 0xFF25324A,
    0xFFB7E7EE: 0xFF2B4A70,
    # rest days -> slate grey
    0xFF397ACB: 0xFF97A6BC, 0xFF87AEE1: 0xFF7F8CA0,
    0xFFE4EEFF: 0xFF1F2938, 0xFFE8F2FF: 0xFF1F2938,
    # locked rewards / trophy
    0xFFA3AEA9: 0xFF56647A, 0xFFFFF2CC: 0xFF3A2C10,
}

entries = '\n'.join(
    f'  0x{day:08X}: 0x{night:08X},' for day, night in NIGHT.items()
)
(ROOT/'lib/app_colors.dart').write_text(f'''import 'package:flutter/material.dart';

/// Day-mode colour -> night-mode (blue) partner.
const _nightTones = <int, int>{{
{entries}
}};

extension AppColors on BuildContext {{
  bool get isNight => Theme.of(this).brightness == Brightness.dark;

  /// A day-mode colour, swapped for its blue partner in night mode.
  Color tone(int day) => Color(isNight ? (_nightTones[day] ?? day) : day);

  /// Explicit day / night pair for colours with no shared mapping.
  Color pick(int day, int night) => Color(isNight ? night : day);
}}
''')

# --- Night theme ------------------------------------------------------------
theme = ROOT/'lib/theme.dart'
t = theme.read_text()
start = t.index('ThemeData buildDarkAppTheme()')
theme.write_text(t[:start] + r'''ThemeData buildDarkAppTheme() {
  const primary = Color(0xFF5AA9FF);
  const background = Color(0xFF0B111A);
  const surface = Color(0xFF141C29);
  const raised = Color(0xFF1C2636);
  const border = Color(0xFF26324A);

  final scheme = ColorScheme.fromSeed(
    seedColor: primary,
    brightness: Brightness.dark,
  ).copyWith(
    primary: primary,
    onPrimary: const Color(0xFF07121F),
    primaryContainer: const Color(0xFF1D3553),
    onPrimaryContainer: const Color(0xFFA9D2FF),
    secondary: const Color(0xFF8CC4FF),
    onSecondary: const Color(0xFF07121F),
    secondaryContainer: const Color(0xFF1D3553),
    onSecondaryContainer: const Color(0xFFA9D2FF),
    surface: surface,
    onSurface: const Color(0xFFEEF3FA),
    onSurfaceVariant: const Color(0xFFA3B0C2),
    surfaceContainerHighest: raised,
    outline: border,
    outlineVariant: border,
  );

  return ThemeData(
    useMaterial3: true,
    brightness: Brightness.dark,
    colorScheme: scheme,
    scaffoldBackgroundColor: background,
    appBarTheme: const AppBarTheme(
      backgroundColor: background,
      foregroundColor: Color(0xFFEEF3FA),
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
      fillColor: raised,
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
      backgroundColor: Color(0xFF0F1622),
      indicatorColor: Color(0xFF1D3553),
      surfaceTintColor: Colors.transparent,
    ),
  );
}
''')

# --- Targeted fixes where one day colour needs a different night role -------
cal = 'lib/screens/calendar_screen.dart'
patch(cal, '''                      final fill = selected
                          ? const Color(0xFF17312A)''', '''                      final fill = selected
                          ? context.pick(0xFF17312A, 0xFF5AA9FF)''')
patch(cal, '''                      final border = selected
                          ? const Color(0xFF17312A)''', '''                      final border = selected
                          ? context.pick(0xFF17312A, 0xFF5AA9FF)''')
patch(cal, 'color: selected ? Colors.white : ',
      'color: selected ? context.pick(0xFFFFFFFF, 0xFF07121F) : ')
patch(cal, '''selected
                                        ? Colors.white''', '''selected
                                        ? context.pick(0xFFFFFFFF, 0xFF07121F)''', count=2)

home = 'lib/screens/home_screen.dart'
patch(home, '''                fontWeight: FontWeight.w900,
                color: const Color(0xFF092C2B),
                letterSpacing: -0.5,''', '''                fontWeight: FontWeight.w900,
                color: context.pick(0xFF092C2B, 0xFF5AA9FF),
                letterSpacing: -0.5,''')
patch(home, '''                          style: const TextStyle(
                            fontSize: 16,
                            fontWeight: FontWeight.w900,
                            color: Color(0xFF087B55),
                          ),''', '''                          style: TextStyle(
                            fontSize: 16,
                            fontWeight: FontWeight.w900,
                            color: context.pick(0xFF087B55, 0xFFEEF3FA),
                          ),''')
patch(home, '''                          style: const TextStyle(
                            fontSize: 24,
                            fontWeight: FontWeight.w900,
                            color: Color(0xFF092C2B),
                          ),''', '''                          style: TextStyle(
                            fontSize: 24,
                            fontWeight: FontWeight.w900,
                            color: context.pick(0xFF092C2B, 0xFF5AA9FF),
                          ),''')

sw = 'lib/screens/strength_workout_screen.dart'
patch(sw, 'tileColor: Colors.white,', 'tileColor: context.pick(0xFFFFFFFF, 0xFF1C2636),')
patch(sw, '''                          ? const Color(0xFFE6F5EF)
                          : Colors.white,''', '''                          ? const Color(0xFFE6F5EF)
                          : context.pick(0xFFFFFFFF, 0xFF1C2636),''')

# --- Route hard-coded day colours through context.tone() --------------------
COLOR = re.compile(r'(?<![\w.])(?:const\s+)?Color\((0x[0-9A-Fa-f]{8})\)')
CONST_OPENER = re.compile(r'\bconst\s+(?=[\w.]*(?:<[\w<>, ]*>)?\s*$)')


def strip_enclosing_const(text, pos):
    """Drop `const` from every constructor/list enclosing `pos`, up to the
    nearest statement or block boundary, so a non-const value can live there."""
    depth = 0
    i = pos - 1
    while i >= 0:
        ch = text[i]
        if ch in ')]':
            depth += 1
        elif ch in '([':
            if depth == 0:
                # `const Foo(`, `const Foo.bar(`, `const [` or `const <T>[`
                m = CONST_OPENER.search(text[:i])
                if m:
                    text = text[:m.start()] + text[m.end():]
                    i = m.start()
                    continue
            else:
                depth -= 1
        elif ch in '{;' and depth == 0:
            break
        i -= 1
    return text


FILES = [
    'lib/screens/home_screen.dart',
    'lib/screens/calendar_screen.dart',
    'lib/screens/onboarding_screen.dart',
    'lib/screens/rewards_screen.dart',
    'lib/screens/strength_workout_screen.dart',
    'lib/screens/body_progress_screen.dart',
    'lib/widgets/common.dart',
]

for rel in FILES:
    f = ROOT/rel
    text = f.read_text()
    while True:
        m = next((m for m in COLOR.finditer(text) if int(m.group(1), 16) in NIGHT), None)
        if m is None:
            break
        text = text[:m.start()] + f'context.tone({m.group(1)})' + text[m.end():]
        text = strip_enclosing_const(text, m.start())
    if "app_colors.dart'" not in text:
        prefix = '../' if rel.count('/') == 2 else ''
        text = text.replace("import 'package:flutter/material.dart';",
                            "import 'package:flutter/material.dart';\n\n"
                            f"import '{prefix}app_colors.dart';", 1)
    f.write_text(text)

# --- Avatar: navy halo and light limbs at night -----------------------------
av = 'lib/widgets/treadmill_avatar.dart'
patch(av, 'painter: _MoodAvatarPainter(_controller.value, widget.mood),',
      'painter: _MoodAvatarPainter(\n'
      '              _controller.value,\n'
      '              widget.mood,\n'
      '              Theme.of(context).brightness == Brightness.dark,\n'
      '            ),')
patch(av, '''  _MoodAvatarPainter(this.t, this.mood);
''', '''  final bool night;

  _MoodAvatarPainter(this.t, this.mood, this.night);

  Color get bodyInk => night ? const Color(0xFFC9D6E6) : dark;
  Color get green => night ? const Color(0xFF4D9BF0) : _dayGreen;
''')
patch(av, 'static const green = Color(0xFF0B8C5E);', 'static const _dayGreen = Color(0xFF0B8C5E);')
patch(av, "Paint()..color = Colors.white.withValues(alpha: .82)",
      "Paint()..color = (night ? const Color(0xFF1C2638) : Colors.white).withValues(alpha: .82)")
f = ROOT/av
f.write_text(re.sub(r'_stroke\(dark, s \*', '_stroke(bodyInk, s *', f.read_text()))
patch(av, 'oldDelegate.t != t || oldDelegate.mood != mood;',
      'oldDelegate.t != t || oldDelegate.mood != mood || oldDelegate.night != night;')

# --- Night-mode regression test (runs in the preview build) -----------------
(ROOT/'test/night_mode_test.dart').write_text(r'''import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:muscletrack_t2d/app_database.dart';
import 'package:muscletrack_t2d/app_store.dart';
import 'package:muscletrack_t2d/main.dart';
import 'package:muscletrack_t2d/models.dart';
import 'package:muscletrack_t2d/theme_controller.dart';
import 'package:shared_preferences/shared_preferences.dart';

class _MemoryDb extends AppDatabase {
  final List<WorkoutSession> workouts = [
    WorkoutSession(
      id: 1,
      date: DateTime.now(),
      workoutType: 'Strength',
      durationMin: 28,
      bodyParts: const ['Chest'],
      sets: const [
        ExerciseSetRecord(exerciseName: 'Bench press', setNumber: 1, reps: 10, weightKg: 40),
      ],
    ),
  ];

  @override
  Future<UserProfile?> loadProfile() async => const UserProfile(name: 'AS');
  @override
  Future<List<WorkoutSession>> loadWorkouts() async => List.of(workouts);
  @override
  Future<List<DailyActivity>> loadDailyActivities() async => [];
}

Future<AppStore> _pumpApp(WidgetTester tester, {required bool dark}) async {
  SharedPreferences.setMockInitialValues({'muscletrack_dark_mode': dark});
  await ThemeController.instance.load();
  final store = AppStore(_MemoryDb());
  await store.load();
  await tester.pumpWidget(MuscleTrackApp(store: store));
  await tester.pump();
  return store;
}

void main() {
  testWidgets('switching night mode on and off does not throw', (tester) async {
    await _pumpApp(tester, dark: false);
    for (var i = 0; i < 2; i++) {
      await ThemeController.instance.toggle();
      for (var frame = 0; frame < 20; frame++) {
        await tester.pump(const Duration(milliseconds: 20));
      }
      expect(tester.takeException(), isNull);
    }
  });

  testWidgets('every tab renders in night mode', (tester) async {
    await _pumpApp(tester, dark: true);
    for (final tab in ['Calendar', 'Workouts', 'More', 'Home']) {
      await tester.tap(find.text(tab).last);
      await tester.pump(const Duration(milliseconds: 300));
      expect(tester.takeException(), isNull);
    }
  });

  testWidgets('night mode uses the blue accent', (tester) async {
    await _pumpApp(tester, dark: true);
    final context = tester.element(find.text('MuscleTrack'));
    expect(Theme.of(context).colorScheme.primary, const Color(0xFF5AA9FF));
  });
}
''')

# --- Version ----------------------------------------------------------------
pub = ROOT/'pubspec.yaml'
p = pub.read_text()
p = re.sub(r'^version:\s*.*$', 'version: 0.3.8+18', p, flags=re.M)
pub.write_text(p)

print('Applied v0.3.8 blue night mode')
