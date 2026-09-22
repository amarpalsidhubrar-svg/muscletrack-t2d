#!/usr/bin/env python3
from pathlib import Path
import base64, re

ROOT = Path(__file__).resolve().parents[1]

# Decode the compact preview body-map asset.
asset_b64 = (ROOT/'tool/bodymap_asset.b64').read_text().strip()
asset = ROOT/'assets/digital_twin_bodymap.webp'
asset.parent.mkdir(parents=True, exist_ok=True)
asset.write_bytes(base64.b64decode(asset_b64))

# Add asset + preview version.
pub = ROOT/'pubspec.yaml'
p = pub.read_text()
if 'assets/digital_twin_bodymap.webp' not in p:
    p = p.replace(
        '  uses-material-design: true',
        '  uses-material-design: true\n  assets:\n    - assets/digital_twin_bodymap.webp'
    )
p = re.sub(r'^version:\s*.*$', 'version: 0.3.5+15', p, flags=re.M)
pub.write_text(p)

# Add body-part tags to WorkoutSession.
models = ROOT/'lib/models.dart'
m = models.read_text()
if 'final List<String> bodyParts;' not in m:
    m = m.replace(
        "  final String notes;\n  final List<ExerciseSetRecord> sets;",
        "  final String notes;\n  final List<String> bodyParts;\n  final List<ExerciseSetRecord> sets;",
    )
    m = m.replace(
        "    this.notes = '',\n    this.sets = const [],",
        "    this.notes = '',\n    this.bodyParts = const [],\n    this.sets = const [],",
    )
    m = m.replace(
        "        'notes': notes,\n      };",
        "        'notes': notes,\n        'body_parts': bodyParts.join('|'),\n      };",
    )
models.write_text(m)

# Database migration for body-parts.
db = ROOT/'lib/app_database.dart'
d = db.read_text()
d = d.replace('version: 1,', 'version: 2,')
if "body_parts TEXT NOT NULL DEFAULT ''" not in d:
    d = d.replace(
        "            notes TEXT NOT NULL DEFAULT ''\n          )",
        "            notes TEXT NOT NULL DEFAULT '',\n            body_parts TEXT NOT NULL DEFAULT ''\n          )",
    )
if 'onUpgrade:' not in d:
    d = d.replace(
        "      },\n    );",
        """      },
      onUpgrade: (db, oldVersion, newVersion) async {
        if (oldVersion < 2) {
          await db.execute(
            "ALTER TABLE workouts ADD COLUMN body_parts TEXT NOT NULL DEFAULT ''",
          );
        }
      },
    );""",
        1,
    )
if 'bodyParts:' not in d:
    d = d.replace(
        "          notes: (row['notes'] as String?) ?? '',\n          sets:",
        """          notes: (row['notes'] as String?) ?? '',
          bodyParts: ((row['body_parts'] as String?) ?? '')
              .split('|')
              .where((e) => e.isNotEmpty)
              .toList(),
          sets:""",
    )
db.write_text(d)

# Interactive body-map selector.
(ROOT/'lib/screens/body_map_picker_screen.dart').write_text(r'''import 'package:flutter/material.dart';

class BodyMapPickerScreen extends StatefulWidget {
  final Set<String> initial;
  const BodyMapPickerScreen({super.key, this.initial = const {}});

  @override
  State<BodyMapPickerScreen> createState() => _BodyMapPickerScreenState();
}

class _BodyMapPickerScreenState extends State<BodyMapPickerScreen> {
  late Set<String> selected;

  static const parts = <String>[
    'Chest',
    'Shoulders',
    'Biceps',
    'Triceps',
    'Forearms',
    'Core',
    'Upper back',
    'Lats',
    'Lower back',
    'Glutes',
    'Quads',
    'Hamstrings',
    'Calves',
  ];

  @override
  void initState() {
    super.initState();
    selected = {...widget.initial};
  }

  void toggle(String part) {
    setState(() {
      if (!selected.add(part)) selected.remove(part);
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFF07141B),
      appBar: AppBar(
        title: const Text('3D body map'),
        backgroundColor: const Color(0xFF07141B),
        foregroundColor: Colors.white,
        actions: [
          TextButton(
            onPressed: () => setState(selected.clear),
            child: const Text('Clear'),
          ),
        ],
      ),
      body: SafeArea(
        child: Column(
          children: [
            const Padding(
              padding: EdgeInsets.fromLTRB(16, 8, 16, 6),
              child: Text(
                'Tap the body or use the muscle-group chips below.',
                style: TextStyle(color: Color(0xFFC5D9E3)),
              ),
            ),
            Expanded(
              child: Center(
                child: AspectRatio(
                  aspectRatio: 180 / 318,
                  child: LayoutBuilder(
                    builder: (context, constraints) {
                      Widget hotspot(
                        String label,
                        double x,
                        double y,
                        double w,
                        double h,
                      ) {
                        final active = selected.contains(label);
                        return Positioned(
                          left: constraints.maxWidth * x,
                          top: constraints.maxHeight * y,
                          width: constraints.maxWidth * w,
                          height: constraints.maxHeight * h,
                          child: GestureDetector(
                            behavior: HitTestBehavior.translucent,
                            onTap: () => toggle(label),
                            child: AnimatedContainer(
                              duration: const Duration(milliseconds: 160),
                              decoration: BoxDecoration(
                                color: active
                                    ? const Color(0x8845E8FF)
                                    : Colors.transparent,
                                borderRadius: BorderRadius.circular(18),
                                border: active
                                    ? Border.all(
                                        color: const Color(0xFF7CF2FF),
                                        width: 2,
                                      )
                                    : null,
                                boxShadow: active
                                    ? const [
                                        BoxShadow(
                                          color: Color(0x8845E8FF),
                                          blurRadius: 16,
                                        )
                                      ]
                                    : null,
                              ),
                            ),
                          ),
                        );
                      }

                      return Stack(
                        fit: StackFit.expand,
                        children: [
                          Image.asset(
                            'assets/digital_twin_bodymap.webp',
                            fit: BoxFit.contain,
                          ),
                          hotspot('Shoulders', .27, .18, .46, .12),
                          hotspot('Chest', .34, .25, .34, .11),
                          hotspot('Biceps', .18, .29, .64, .13),
                          hotspot('Forearms', .13, .39, .74, .13),
                          hotspot('Core', .36, .37, .30, .16),
                          hotspot('Quads', .29, .55, .42, .16),
                          hotspot('Calves', .30, .73, .40, .18),
                        ],
                      );
                    },
                  ),
                ),
              ),
            ),
            Container(
              color: const Color(0xFF0E2029),
              padding: const EdgeInsets.fromLTRB(12, 10, 12, 14),
              child: Column(
                children: [
                  Wrap(
                    spacing: 7,
                    runSpacing: 7,
                    alignment: WrapAlignment.center,
                    children: parts.map((part) {
                      final active = selected.contains(part);
                      return FilterChip(
                        selected: active,
                        label: Text(part),
                        onSelected: (_) => toggle(part),
                        selectedColor: const Color(0xFF2CC6DB),
                        checkmarkColor: Colors.white,
                        labelStyle: TextStyle(
                          color: active
                              ? Colors.white
                              : const Color(0xFFDDECF2),
                          fontWeight: FontWeight.w700,
                        ),
                        backgroundColor: const Color(0xFF17313D),
                        side: BorderSide(
                          color: active
                              ? const Color(0xFF7CF2FF)
                              : const Color(0xFF31505D),
                        ),
                      );
                    }).toList(),
                  ),
                  const SizedBox(height: 12),
                  SizedBox(
                    width: double.infinity,
                    child: FilledButton.icon(
                      onPressed: selected.isEmpty
                          ? null
                          : () => Navigator.pop(context, selected),
                      icon: const Icon(Icons.check_rounded),
                      label: Text(
                        selected.isEmpty
                            ? 'Select body parts'
                            : 'Save ${selected.length} selected',
                      ),
                    ),
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}
''')

# Body-part progress summary.
(ROOT/'lib/screens/body_progress_screen.dart').write_text(r'''import 'package:flutter/material.dart';
import '../app_store.dart';

class BodyProgressScreen extends StatelessWidget {
  final AppStore store;
  const BodyProgressScreen({super.key, required this.store});

  @override
  Widget build(BuildContext context) {
    final counts = <String, int>{};
    for (final workout in store.workouts) {
      if (workout.workoutType.toLowerCase() == 'rest day') continue;
      for (final part in workout.bodyParts.toSet()) {
        counts[part] = (counts[part] ?? 0) + 1;
      }
    }
    final items = counts.entries.toList()
      ..sort((a, b) => b.value.compareTo(a.value));

    return Scaffold(
      appBar: AppBar(title: const Text('Body-part progress')),
      backgroundColor: const Color(0xFFF7FAF8),
      body: items.isEmpty
          ? const Center(
              child: Padding(
                padding: EdgeInsets.all(28),
                child: Text(
                  'Use the 3D body map when logging a workout to build your body-part training history.',
                  textAlign: TextAlign.center,
                ),
              ),
            )
          : ListView(
              padding: const EdgeInsets.all(16),
              children: [
                const Text(
                  'Training frequency',
                  style: TextStyle(fontSize: 20, fontWeight: FontWeight.w900),
                ),
                const SizedBox(height: 6),
                const Text(
                  'Number of workout sessions in which each body part was selected.',
                  style: TextStyle(color: Color(0xFF667871)),
                ),
                const SizedBox(height: 14),
                ...items.map(
                  (e) => Card(
                    child: ListTile(
                      leading: const CircleAvatar(
                        backgroundColor: Color(0xFFE1F7F9),
                        child: Icon(
                          Icons.accessibility_new_rounded,
                          color: Color(0xFF0A8FA3),
                        ),
                      ),
                      title: Text(
                        e.key,
                        style: const TextStyle(fontWeight: FontWeight.w800),
                      ),
                      trailing: Text(
                        '${e.value} session${e.value == 1 ? '' : 's'}',
                        style: const TextStyle(fontWeight: FontWeight.w900),
                      ),
                    ),
                  ),
                ),
              ],
            ),
    );
  }
}
''')

# Workout logger changes.
workout = ROOT/'lib/screens/strength_workout_screen.dart'
w = workout.read_text()
if "body_map_picker_screen.dart" not in w:
    w = w.replace(
        "import '../models.dart';",
        "import '../models.dart';\nimport 'body_map_picker_screen.dart';",
    )
if "_selectedBodyParts" not in w:
    w = w.replace(
        "  late List<_DraftExercise> _exercises;",
        "  late List<_DraftExercise> _exercises;\n  late Set<String> _selectedBodyParts;",
    )
    w = w.replace(
        "    _exercises =\n        existing == null ? [_DraftExercise()] : _draftExercises(existing.sets);",
        "    _exercises =\n        existing == null ? [_DraftExercise()] : _draftExercises(existing.sets);\n    _selectedBodyParts = {...?existing?.bodyParts};",
    )
    w = w.replace(
        "    if (duration <= 0 || sets.isEmpty) {",
        "    if (duration <= 0 || (sets.isEmpty && _selectedBodyParts.isEmpty)) {",
    )
    w = w.replace(
        "Text('Add a duration and at least one valid exercise set.'),",
        "Text('Add a duration and either a valid exercise set or body-part selection.'),",
    )
    w = w.replace(
        "      workoutType: 'Strength',",
        "      workoutType: sets.isEmpty && _selectedBodyParts.isNotEmpty ? 'Body Map' : 'Strength',",
    )
    w = w.replace(
        "      source: _source,",
        "      source: sets.isEmpty && _selectedBodyParts.isNotEmpty ? '3D body map' : _source,",
    )
    w = w.replace(
        "                    DropdownMenuItem(\n                        value: 'Other device', child: Text('Other device')),",
        "                    DropdownMenuItem(\n                        value: 'Other device', child: Text('Other device')),\n                    DropdownMenuItem(\n                        value: '3D body map',\n                        enabled: false,\n                        child: Text('3D body map')),",
    )
    w = w.replace(
        "      notes: _notes.text.trim(),\n      sets: sets,",
        "      notes: _notes.text.trim(),\n      bodyParts: _selectedBodyParts.toList()..sort(),\n      sets: sets,",
    )

    old = """          OutlinedButton.icon(
            onPressed: () =>
                setState(() => _exercises.add(_DraftExercise())),
            icon: const Icon(Icons.add),
            label: const Text('Add exercise'),
          ),"""
    new = """          Row(
            children: [
              Expanded(
                child: OutlinedButton.icon(
                  onPressed: () =>
                      setState(() => _exercises.add(_DraftExercise())),
                  icon: const Icon(Icons.add),
                  label: const Text('Add exercise'),
                ),
              ),
              const SizedBox(width: 8),
              OutlinedButton.icon(
                onPressed: () async {
                  final selected = await Navigator.push<Set<String>>(
                    context,
                    MaterialPageRoute(
                      builder: (_) => BodyMapPickerScreen(
                        initial: _selectedBodyParts,
                      ),
                    ),
                  );
                  if (selected != null && mounted) {
                    setState(() => _selectedBodyParts = selected);
                  }
                },
                icon: const Icon(Icons.view_in_ar_rounded),
                label: const Text('3D'),
              ),
            ],
          ),
          if (_selectedBodyParts.isNotEmpty) ...[
            const SizedBox(height: 10),
            Container(
              width: double.infinity,
              padding: const EdgeInsets.all(12),
              decoration: BoxDecoration(
                color: const Color(0xFFE7F7FA),
                borderRadius: BorderRadius.circular(14),
                border: Border.all(color: const Color(0xFFB7E7EE)),
              ),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const Text(
                    'Body parts worked',
                    style: TextStyle(fontWeight: FontWeight.w900),
                  ),
                  const SizedBox(height: 8),
                  Wrap(
                    spacing: 6,
                    runSpacing: 6,
                    children: _selectedBodyParts
                        .map(
                          (part) => Chip(
                            visualDensity: VisualDensity.compact,
                            label: Text(part),
                            onDeleted: () => setState(
                              () => _selectedBodyParts.remove(part),
                            ),
                          ),
                        )
                        .toList(),
                  ),
                ],
              ),
            ),
          ],"""
    w = w.replace(old, new)
workout.write_text(w)

# Calendar body-part recording.
cal = ROOT/'lib/screens/calendar_screen.dart'
cc = cal.read_text()
cc = cc.replace(
    "subtitle: Text('${w.durationMin} min • ${w.sets.length} sets'),",
    """subtitle: Text(
                        w.bodyParts.isNotEmpty
                            ? '${w.durationMin} min • ${w.bodyParts.join(', ')}'
                            : '${w.durationMin} min • ${w.sets.length} sets',
                      ),""",
)
cal.write_text(cc)

# Workout history summary.
hist = ROOT/'lib/screens/workout_history_screen.dart'
hh = hist.read_text()
hh = hh.replace(
    "subtitle: Text('${w.durationMin} min • ${w.sets.length} sets'),",
    """subtitle: Text(
              w.bodyParts.isNotEmpty
                  ? '${w.durationMin} min • ${w.bodyParts.join(', ')}'
                  : '${w.durationMin} min • ${w.sets.length} sets',
            ),""",
)
hist.write_text(hh)

# Home navigation to body progress.
home = ROOT/'lib/screens/home_screen.dart'
h = home.read_text()
if "body_progress_screen.dart" not in h:
    h = h.replace(
        "import 'calendar_screen.dart';",
        "import 'calendar_screen.dart';\nimport 'body_progress_screen.dart';",
    )
    marker = """        _ActionCard(
          icon: Icons.history_rounded,
          title: 'Workout history',"""
    insertion = """        _ActionCard(
          icon: Icons.accessibility_new_rounded,
          title: 'Body progress',
          subtitle: 'See which body parts you train most often',
          onTap: () => Navigator.push(
            context,
            MaterialPageRoute(
              builder: (_) => BodyProgressScreen(store: store),
            ),
          ),
        ),
        const SizedBox(height: 10),
"""
    h = h.replace(marker, insertion + marker)
home.write_text(h)

print('Applied v0.3.5 body-map logging with safe 3D source dropdown')
