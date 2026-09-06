#!/usr/bin/env python3
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]

# ---------- Database/store: allow meal editing ----------
db = ROOT/'lib/app_database.dart'
s = db.read_text()
if 'Future<void> updateMeal(MealEntry entry)' not in s:
    s = s.replace(
        "  Future<void> deleteMeal(int mealId) async {\n",
        "  Future<void> updateMeal(MealEntry entry) async {\n"
        "    if (entry.id == null) return;\n"
        "    final db = await database;\n"
        "    final values = entry.toMap()..remove('id');\n"
        "    await db.update('meals', values, where: 'id = ?', whereArgs: [entry.id]);\n"
        "  }\n\n"
        "  Future<void> deleteMeal(int mealId) async {\n"
    )
db.write_text(s)

store = ROOT/'lib/app_store.dart'
s = store.read_text()
if 'Future<void> updateMeal(MealEntry value)' not in s:
    s = s.replace(
        "  Future<void> deleteMeal(int mealId) async {\n",
        "  Future<void> updateMeal(MealEntry value) async {\n"
        "    await db.updateMeal(value);\n"
        "    await refresh();\n"
        "  }\n\n"
        "  Future<void> deleteMeal(int mealId) async {\n"
    )
store.write_text(s)

# ---------- Meal screen: support editing an existing meal ----------
meal = ROOT/'lib/screens/meal_log_screen.dart'
m = meal.read_text()
m = m.replace(
    "class MealLogScreen extends StatefulWidget {\n  final AppStore store;\n\n  const MealLogScreen({super.key, required this.store});",
    "class MealLogScreen extends StatefulWidget {\n  final AppStore store;\n  final MealEntry? existing;\n\n  const MealLogScreen({super.key, required this.store, this.existing});"
)
if 'void initState()' not in m.split('class _MealLogScreenState',1)[1].split('@override\n  void dispose()',1)[0]:
    marker = "  int? _matchedFoods;"
    insertion = marker + "\n\n  @override\n  void initState() {\n    super.initState();\n    final existing = widget.existing;\n    if (existing != null) {\n      _mealType = existing.mealType;\n      _description.text = existing.description;\n      _calories.text = existing.calories.toStringAsFixed(0);\n      if (existing.proteinG != null) _protein.text = existing.proteinG!.toStringAsFixed(1);\n      if (existing.carbsG != null) _carbs.text = existing.carbsG!.toStringAsFixed(1);\n      if (existing.fatG != null) _fat.text = existing.fatG!.toStringAsFixed(1);\n      if (existing.fibreG != null) _fibre.text = existing.fibreG!.toStringAsFixed(1);\n    }\n  }"
    m = m.replace(marker, insertion)

m = m.replace(
    "    await widget.store.addMeal(\n      MealEntry(\n        date: DateTime.now(),",
    "    final entry = MealEntry(\n        id: widget.existing?.id,\n        date: widget.existing?.date ?? DateTime.now(),"
)
m = m.replace(
    "        fibreG: double.tryParse(_fibre.text),\n      ),\n    );",
    "        fibreG: double.tryParse(_fibre.text),\n      );\n\n    if (widget.existing == null) {\n      await widget.store.addMeal(entry);\n    } else {\n      await widget.store.updateMeal(entry);\n    }"
)
m = m.replace("appBar: AppBar(title: const Text('Log Meal'))", "appBar: AppBar(title: Text(widget.existing == null ? 'Log Meal' : 'Edit Meal'))")
m = m.replace("child: const Text('Save Meal'),", "child: Text(widget.existing == null ? 'Save Meal' : 'Save Changes'),")
m = m.replace(".showSnackBar(const SnackBar(content: Text('Meal logged.')));", ".showSnackBar(SnackBar(content: Text(widget.existing == null ? 'Meal logged.' : 'Meal updated.')));")
meal.write_text(m)

# ---------- Today detail screen ----------
today = ROOT/'lib/screens/today_summary_screen.dart'
today.write_text(r'''import 'package:flutter/material.dart';

import '../app_store.dart';
import '../calculations.dart';
import 'meal_log_screen.dart';
import 'strength_workout_screen.dart';

class TodaySummaryScreen extends StatelessWidget {
  final AppStore store;
  const TodaySummaryScreen({super.key, required this.store});

  bool _sameDay(DateTime a, DateTime b) =>
      a.year == b.year && a.month == b.month && a.day == b.day;

  @override
  Widget build(BuildContext context) {
    final now = DateTime.now();
    final profile = store.profile!;
    final workouts = store.workouts.where((w) => _sameDay(w.date, now)).toList();
    final activity = workouts.fold<int>(0, (s, w) => s + w.durationMin);
    final dailyEnergy = estimatedDailyEnergyRequirement(
      weightKg: store.currentWeightKg,
      heightCm: profile.heightCm,
      age: profile.age,
      sex: profile.sex,
      activityFactor: 1.375,
    );
    final protein = store.todayProteinG;
    final carbs = store.todayMeals.fold<double>(0, (s, m) => s + (m.carbsG ?? 0));
    final fat = store.todayMeals.fold<double>(0, (s, m) => s + (m.fatG ?? 0));
    final fibre = store.todayMeals.fold<double>(0, (s, m) => s + (m.fibreG ?? 0));

    return Scaffold(
      backgroundColor: const Color(0xFFF7FAF8),
      appBar: AppBar(title: const Text("Today's summary")),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          _card(context, 'Nutrition', Icons.restaurant_rounded, [
            '${store.todayMealCalories.toStringAsFixed(0)} / ${dailyEnergy.toStringAsFixed(0)} kcal',
            'Protein ${protein.toStringAsFixed(0)} g',
            'Carbohydrate ${carbs.toStringAsFixed(0)} g',
            'Fat ${fat.toStringAsFixed(0)} g',
            'Fibre ${fibre.toStringAsFixed(0)} g',
          ], onTap: () => Navigator.push(context, MaterialPageRoute(builder: (_) => MealLogScreen(store: store)))),
          const SizedBox(height: 12),
          _card(context, 'Workout', Icons.fitness_center_rounded, [
            '${workouts.length} workout${workouts.length == 1 ? '' : 's'} today',
            '$activity activity minutes',
            workouts.isEmpty ? 'No workout logged yet' : workouts.map((w) => '${w.workoutType} • ${w.durationMin} min').join('\n'),
          ], onTap: () => Navigator.push(context, MaterialPageRoute(builder: (_) => StrengthWorkoutScreen(store: store)))),
          const SizedBox(height: 12),
          if (store.todayMeals.isNotEmpty) ...[
            Text('Meals today', style: Theme.of(context).textTheme.titleMedium?.copyWith(fontWeight: FontWeight.w900)),
            const SizedBox(height: 8),
            ...store.todayMeals.map((meal) => Card(
              child: ListTile(
                leading: const CircleAvatar(child: Icon(Icons.restaurant_rounded)),
                title: Text(meal.description, maxLines: 1, overflow: TextOverflow.ellipsis),
                subtitle: Text('${meal.mealType} • ${meal.calories.toStringAsFixed(0)} kcal'),
                trailing: const Icon(Icons.edit_outlined),
                onTap: () => Navigator.push(context, MaterialPageRoute(builder: (_) => MealLogScreen(store: store, existing: meal))),
              ),
            )),
          ],
        ],
      ),
    );
  }

  Widget _card(BuildContext context, String title, IconData icon, List<String> lines, {required VoidCallback onTap}) {
    return Card(
      child: InkWell(
        borderRadius: BorderRadius.circular(18),
        onTap: onTap,
        child: Padding(
          padding: const EdgeInsets.all(16),
          child: Row(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              CircleAvatar(backgroundColor: const Color(0xFFE2F5EB), child: Icon(icon, color: const Color(0xFF087B55))),
              const SizedBox(width: 12),
              Expanded(child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                Text(title, style: const TextStyle(fontWeight: FontWeight.w900, fontSize: 16)),
                const SizedBox(height: 6),
                ...lines.map((v) => Padding(padding: const EdgeInsets.only(bottom: 3), child: Text(v))),
              ])),
              const Icon(Icons.chevron_right_rounded),
            ],
          ),
        ),
      ),
    );
  }
}
''')

# ---------- Home screen interactions ----------
home = ROOT/'lib/screens/home_screen.dart'
h = home.read_text()
if "import 'today_summary_screen.dart';" not in h:
    h = h.replace("import 'strength_workout_screen.dart';", "import 'strength_workout_screen.dart';\nimport 'today_summary_screen.dart';")

# Remove bell entirely.
h = re.sub(r"\n\s*IconButton\(\n\s*tooltip: 'Notifications',[\s\S]*?icon: const Icon\(Icons\.notifications_none_rounded\),\n\s*\),", "", h, count=1)

# Make summary card receive callback and make 'See details' a real button.
h = h.replace(
    "activityMinutes: todayActivity,\n        ),",
    "activityMinutes: todayActivity,\n          onTap: () => Navigator.push(\n            context,\n            MaterialPageRoute(builder: (_) => TodaySummaryScreen(store: store)),\n          ),\n        ),"
)
h = h.replace(
    "  final int activityMinutes;\n\n  const _SummaryCard({",
    "  final int activityMinutes;\n  final VoidCallback onTap;\n\n  const _SummaryCard({"
)
h = h.replace(
    "    required this.activityMinutes,\n  });",
    "    required this.activityMinutes,\n    required this.onTap,\n  });",
    1
)
old = """              Text(\n                'See details',\n                style: Theme.of(context).textTheme.bodySmall?.copyWith(\n                      color: const Color(0xFF52665E),\n                    ),\n              ),\n              const Icon(Icons.chevron_right, size: 18),"""
new = """              TextButton.icon(\n                onPressed: onTap,\n                iconAlignment: IconAlignment.end,\n                icon: const Icon(Icons.chevron_right, size: 18),\n                label: const Text('View today'),\n                style: TextButton.styleFrom(\n                  foregroundColor: const Color(0xFF087B55),\n                  padding: const EdgeInsets.symmetric(horizontal: 6),\n                  textStyle: const TextStyle(fontSize: 11, fontWeight: FontWeight.w800),\n                ),\n              ),"""
h = h.replace(old, new)

# Replace Progress preview with a truly interactive tabbed version.
progress_re = re.compile(r"class _ProgressPreview extends StatelessWidget \{[\s\S]*?\nclass _ReadinessCard extends StatelessWidget \{", re.M)
progress_block = r'''class _ProgressPreview extends StatefulWidget {
  final AppStore store;
  const _ProgressPreview({required this.store});

  @override
  State<_ProgressPreview> createState() => _ProgressPreviewState();
}

class _ProgressPreviewState extends State<_ProgressPreview> {
  String _selected = 'Weight';

  @override
  Widget build(BuildContext context) {
    final store = widget.store;
    return _DashboardCard(
      padding: const EdgeInsets.fromLTRB(14, 14, 14, 12),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(children: [
            Text('Your progress', style: Theme.of(context).textTheme.titleSmall?.copyWith(fontWeight: FontWeight.w900)),
            const Spacer(),
            const Text('Past 4 weeks', style: TextStyle(fontSize: 10, color: Color(0xFF6D7D76))),
          ]),
          const SizedBox(height: 9),
          Row(children: [
            _ProgressTab(label: 'Weight', selected: _selected == 'Weight', onTap: () => setState(() => _selected = 'Weight')),
            const SizedBox(width: 5),
            _ProgressTab(label: 'Strength', selected: _selected == 'Strength', onTap: () => setState(() => _selected = 'Strength')),
            const SizedBox(width: 5),
            _ProgressTab(label: 'Activity', selected: _selected == 'Activity', onTap: () => setState(() => _selected = 'Activity')),
          ]),
          const SizedBox(height: 12),
          _progressBody(store),
        ],
      ),
    );
  }

  Widget _progressBody(AppStore store) {
    if (_selected == 'Strength') {
      final best = store.latestStrengthBest;
      return SizedBox(
        height: 112,
        child: best == null
            ? const Center(child: Text('Log a strength workout to see progress', textAlign: TextAlign.center, style: TextStyle(fontSize: 10)))
            : Column(crossAxisAlignment: CrossAxisAlignment.start, mainAxisAlignment: MainAxisAlignment.center, children: [
                Text(best.exerciseName, maxLines: 1, overflow: TextOverflow.ellipsis, style: const TextStyle(fontWeight: FontWeight.w800, fontSize: 11)),
                const SizedBox(height: 6),
                Text('${best.e1rmKg.toStringAsFixed(1)} kg', style: const TextStyle(fontSize: 22, fontWeight: FontWeight.w900, color: Color(0xFF092C2B))),
                const Text('Best estimated 1RM', style: TextStyle(fontSize: 10, color: Color(0xFF6D7D76))),
              ]),
      );
    }
    if (_selected == 'Activity') {
      final min = store.weeklyActivityMinutes;
      final met = store.weeklyMetMinutes;
      return SizedBox(
        height: 112,
        child: Column(crossAxisAlignment: CrossAxisAlignment.start, mainAxisAlignment: MainAxisAlignment.center, children: [
          Text('$min min', style: const TextStyle(fontSize: 22, fontWeight: FontWeight.w900, color: Color(0xFF092C2B))),
          const Text('Activity this week', style: TextStyle(fontSize: 10, color: Color(0xFF6D7D76))),
          const SizedBox(height: 8),
          Text('${met.toStringAsFixed(0)} MET-min', style: const TextStyle(fontWeight: FontWeight.w800, fontSize: 11, color: Color(0xFF087B55))),
        ]),
      );
    }

    final values = store.weights.take(5).toList().reversed.toList();
    return Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
      SizedBox(
        height: 70,
        child: values.length < 2
            ? const Center(child: Text('Log more weights to see a trend', style: TextStyle(fontSize: 10)))
            : CustomPaint(painter: _MiniWeightPainter(values), child: const SizedBox.expand()),
      ),
      Text('${store.currentWeightKg.toStringAsFixed(1)} kg', style: const TextStyle(fontSize: 22, fontWeight: FontWeight.w900, color: Color(0xFF092C2B))),
      Text('${store.weightChangePct <= 0 ? '↓' : '↑'} ${store.weightChangePct.abs().toStringAsFixed(1)}% from baseline', style: TextStyle(fontSize: 10.5, fontWeight: FontWeight.w700, color: store.weightChangePct <= 0 ? const Color(0xFF079669) : const Color(0xFF6D7D76))),
    ]);
  }
}

class _ProgressTab extends StatelessWidget {
  final String label;
  final bool selected;
  final VoidCallback onTap;
  const _ProgressTab({required this.label, required this.selected, required this.onTap});

  @override
  Widget build(BuildContext context) {
    return Expanded(
      child: InkWell(
        borderRadius: BorderRadius.circular(9),
        onTap: onTap,
        child: Container(
          padding: const EdgeInsets.symmetric(vertical: 7),
          decoration: BoxDecoration(
            color: selected ? const Color(0xFF087B55) : const Color(0xFFF0F3F2),
            borderRadius: BorderRadius.circular(9),
            border: Border.all(color: selected ? const Color(0xFF087B55) : const Color(0xFFE1E7E4)),
          ),
          child: Text(label, textAlign: TextAlign.center, style: TextStyle(fontSize: 9.5, fontWeight: FontWeight.w800, color: selected ? Colors.white : const Color(0xFF314B43))),
        ),
      ),
    );
  }
}

class _ReadinessCard extends StatelessWidget {'''
h, n = progress_re.subn(progress_block, h, count=1)
if n != 1:
    raise RuntimeError('Could not replace progress preview')

# Readiness card: functional info + clear check-in action.
h = h.replace(
    "  final WorkoutSession? workout;\n  const _ReadinessCard({required this.workout});",
    "  final WorkoutSession? workout;\n  const _ReadinessCard({required this.workout});\n\n  void _showInfo(BuildContext context) {\n    showDialog(\n      context: context,\n      builder: (_) => AlertDialog(\n        title: const Text('Readiness today'),\n        content: const Text('Energy reflects how ready you feel to train. Sleep records perceived sleep quality. Soreness records muscle soreness before training. These check-ins help you compare workout performance with recovery and fatigue over time.'),\n        actions: [TextButton(onPressed: () => Navigator.pop(context), child: const Text('Got it'))],\n      ),\n    );\n  }"
)
h = h.replace(
    "              const Icon(\n                Icons.info_outline_rounded,\n                size: 17,\n                color: Color(0xFF73857C),\n              ),",
    "              IconButton(\n                tooltip: 'What is readiness?',\n                visualDensity: VisualDensity.compact,\n                padding: EdgeInsets.zero,\n                constraints: const BoxConstraints(minWidth: 30, minHeight: 30),\n                onPressed: () => _showInfo(context),\n                icon: const Icon(Icons.info_outline_rounded, size: 18, color: Color(0xFF087B55)),\n              ),"
)
h = h.replace(
    "            const Text(\n              'Complete a pre-workout check-in to populate readiness.',\n              style: TextStyle(fontSize: 9.5, color: Color(0xFF72837B)),\n            ),",
    "            const Text('No check-in yet', style: TextStyle(fontSize: 9.5, color: Color(0xFF72837B))),\n            const SizedBox(height: 7),\n            SizedBox(\n              width: double.infinity,\n              child: FilledButton.tonal(\n                onPressed: () => Navigator.push(context, MaterialPageRoute(builder: (_) => StrengthWorkoutScreen(store: store))),\n                child: const Text('Complete check-in', style: TextStyle(fontSize: 10, fontWeight: FontWeight.w800)),\n              ),\n            ),"
)
# The readiness class needs store to navigate; add field and pass it.
h = h.replace("child: _ReadinessCard(workout: latest),", "child: _ReadinessCard(store: store, workout: latest),")
h = h.replace("class _ReadinessCard extends StatelessWidget {\n  final WorkoutSession? workout;\n  const _ReadinessCard({required this.workout});", "class _ReadinessCard extends StatelessWidget {\n  final AppStore store;\n  final WorkoutSession? workout;\n  const _ReadinessCard({required this.store, required this.workout});")

# Recent meal: existing entry opens edit screen.
h = h.replace(
    "onTap: () => Navigator.push(\n                  context,\n                  MaterialPageRoute(builder: (_) => MealLogScreen(store: store)),\n                ),",
    "onTap: () {\n                  final meal = store.meals.isEmpty ? null : store.meals.first;\n                  Navigator.push(\n                    context,\n                    MaterialPageRoute(builder: (_) => MealLogScreen(store: store, existing: meal)),\n                  );\n                },",
    1
)

# Make empty-state wording more explicit and reduce mystery icon feel.
h = h.replace("'No workout yet.\\nTap to log one.'", "'No workout yet.\\n+ Log your first workout'")
h = h.replace("'No meal yet.\\nTap to log one.'", "'No meal yet.\\n+ Log your first meal'")

# Make quick action labels explicit and increase touch height a bit.
h = h.replace("height: 78,", "height: 84,")
h = h.replace("fontSize: 9.5,\n                fontWeight: FontWeight.w800,", "fontSize: 10.5,\n                fontWeight: FontWeight.w800,")

home.write_text(h)
print('Applied dashboard interaction improvements without changing Option 2 animation')
