import 'package:flutter/material.dart';

import '../app_store.dart';
import '../calculations.dart';
import '../models.dart';

class _DraftSet {
  final TextEditingController reps;
  final TextEditingController weight;

  _DraftSet({int? repsValue, double? weightValue})
      : reps = TextEditingController(text: repsValue?.toString() ?? ''),
        weight = TextEditingController(
          text: weightValue == null
              ? ''
              : (weightValue % 1 == 0
                  ? weightValue.toStringAsFixed(0)
                  : weightValue.toString()),
        );

  void dispose() {
    reps.dispose();
    weight.dispose();
  }
}

class _DraftExercise {
  final TextEditingController name;
  final List<_DraftSet> sets;

  _DraftExercise({String nameValue = '', List<_DraftSet>? initialSets})
      : name = TextEditingController(text: nameValue),
        sets = initialSets ?? [_DraftSet(), _DraftSet(), _DraftSet()];

  void dispose() {
    name.dispose();
    for (final s in sets) {
      s.dispose();
    }
  }
}

class StrengthWorkoutScreen extends StatefulWidget {
  final AppStore store;
  final WorkoutSession? existing;

  const StrengthWorkoutScreen({
    super.key,
    required this.store,
    this.existing,
  });

  @override
  State<StrengthWorkoutScreen> createState() => _StrengthWorkoutScreenState();
}

class _StrengthWorkoutScreenState extends State<StrengthWorkoutScreen> {
  late final TextEditingController _duration;
  late final TextEditingController _met;
  late final TextEditingController _deviceCalories;
  late final TextEditingController _sleepHours;
  late DateTime _date;
  late String _source;
  late List<_DraftExercise> _exercises;

  int? _fatigue;
  int? _sleepQuality;
  int? _muscleSoreness;
  int? _discomfort;
  int? _readiness;
  int? _sessionRpe;

  bool get _editing => widget.existing != null;

  @override
  void initState() {
    super.initState();
    final existing = widget.existing;
    _duration = TextEditingController(text: existing?.durationMin.toString() ?? '45');
    _met = TextEditingController(text: existing?.met?.toString() ?? '3.5');
    _deviceCalories = TextEditingController(text: existing?.deviceCalories?.toString() ?? '');
    _sleepHours = TextEditingController(text: existing?.sleepHours?.toString() ?? '');
    _date = existing?.date ?? DateTime.now();
    _source = existing?.source ?? 'Manual entry';
    _fatigue = existing?.fatigue;
    _sleepQuality = existing?.sleepQuality;
    _muscleSoreness = existing?.muscleSoreness;
    _discomfort = existing?.discomfort;
    _readiness = existing?.readiness;
    _sessionRpe = existing?.sessionRpe;
    _exercises = existing == null ? [_DraftExercise()] : _draftExercises(existing.sets);
  }

  List<_DraftExercise> _draftExercises(List<ExerciseSetRecord> sets) {
    final grouped = <String, List<ExerciseSetRecord>>{};
    for (final set in sets) {
      grouped.putIfAbsent(set.exerciseName, () => []).add(set);
    }
    if (grouped.isEmpty) return [_DraftExercise()];
    return grouped.entries.map((entry) {
      final ordered = [...entry.value]..sort((a, b) => a.setNumber.compareTo(b.setNumber));
      return _DraftExercise(
        nameValue: entry.key,
        initialSets: ordered
            .map((s) => _DraftSet(repsValue: s.reps, weightValue: s.weightKg))
            .toList(),
      );
    }).toList();
  }

  @override
  void dispose() {
    _duration.dispose();
    _met.dispose();
    _deviceCalories.dispose();
    _sleepHours.dispose();
    for (final e in _exercises) {
      e.dispose();
    }
    super.dispose();
  }

  void _selectAll(TextEditingController controller) {
    if (controller.text.isEmpty) return;
    controller.selection = TextSelection(baseOffset: 0, extentOffset: controller.text.length);
  }

  List<ExerciseSetRecord> _buildSets() {
    final records = <ExerciseSetRecord>[];
    for (final exercise in _exercises) {
      final name = exercise.name.text.trim();
      if (name.isEmpty) continue;
      for (var i = 0; i < exercise.sets.length; i++) {
        final reps = int.tryParse(exercise.sets[i].reps.text) ?? 0;
        final kg = double.tryParse(exercise.sets[i].weight.text) ?? 0;
        if (reps > 0 && kg >= 0) {
          records.add(ExerciseSetRecord(
            exerciseName: name,
            setNumber: i + 1,
            reps: reps,
            weightKg: kg,
          ));
        }
      }
    }
    return records;
  }

  Future<void> _save() async {
    final duration = int.tryParse(_duration.text) ?? 0;
    final sets = _buildSets();
    if (duration <= 0 || sets.isEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Add a duration and at least one valid exercise set.')),
      );
      return;
    }

    final session = WorkoutSession(
      id: widget.existing?.id,
      date: _date,
      workoutType: 'Strength',
      durationMin: duration,
      met: double.tryParse(_met.text),
      source: _source,
      deviceCalories: double.tryParse(_deviceCalories.text),
      fatigue: _fatigue,
      sleepQuality: _sleepQuality,
      muscleSoreness: _muscleSoreness,
      discomfort: _discomfort,
      readiness: _readiness,
      sleepHours: double.tryParse(_sleepHours.text),
      sessionRpe: _sessionRpe,
      sets: sets,
    );

    if (_editing) {
      await widget.store.updateWorkout(session);
    } else {
      await widget.store.addWorkout(session);
    }
    if (mounted) Navigator.pop(context);
  }

  @override
  Widget build(BuildContext context) {
    final sets = _buildSets();
    final volume = trainingVolume(sets);
    final mets = metMinutes(double.tryParse(_met.text), int.tryParse(_duration.text) ?? 0);
    final estimated = estimatedCalories(
      met: double.tryParse(_met.text),
      minutes: int.tryParse(_duration.text) ?? 0,
      bodyWeightKg: widget.store.currentWeightKg,
    );

    return Scaffold(
      appBar: AppBar(title: Text(_editing ? 'Edit strength session' : 'Log strength session')),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          Card(
            child: Padding(
              padding: const EdgeInsets.all(16),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text('Pre-workout check-in', style: Theme.of(context).textTheme.titleMedium?.copyWith(fontWeight: FontWeight.w800)),
                  const SizedBox(height: 4),
                  Text('Optional. These scores are used to observe recovery and performance patterns over time.', style: Theme.of(context).textTheme.bodySmall),
                  const SizedBox(height: 14),
                  Row(children: [
                    Expanded(child: _scoreField('Fatigue', _fatigue, 1, 5, (v) => setState(() => _fatigue = v), helper: '1 low • 5 high')),
                    const SizedBox(width: 10),
                    Expanded(child: _scoreField('Readiness', _readiness, 1, 5, (v) => setState(() => _readiness = v), helper: '1 low • 5 high')),
                  ]),
                  const SizedBox(height: 10),
                  Row(children: [
                    Expanded(child: _scoreField('Sleep quality', _sleepQuality, 1, 5, (v) => setState(() => _sleepQuality = v), helper: '1 poor • 5 excellent')),
                    const SizedBox(width: 10),
                    Expanded(
                      child: TextField(
                        controller: _sleepHours,
                        keyboardType: const TextInputType.numberWithOptions(decimal: true),
                        onTap: () => _selectAll(_sleepHours),
                        decoration: const InputDecoration(labelText: 'Sleep hours', hintText: 'Optional'),
                      ),
                    ),
                  ]),
                  const SizedBox(height: 10),
                  Row(children: [
                    Expanded(child: _scoreField('Muscle soreness', _muscleSoreness, 1, 5, (v) => setState(() => _muscleSoreness = v), helper: '1 low • 5 high')),
                    const SizedBox(width: 10),
                    Expanded(child: _scoreField('Joint/tendon discomfort', _discomfort, 0, 10, (v) => setState(() => _discomfort = v), helper: '0 none • 10 severe')),
                  ]),
                ],
              ),
            ),
          ),
          const SizedBox(height: 12),
          Row(children: [
            Expanded(
              child: TextField(
                controller: _duration,
                keyboardType: TextInputType.number,
                onTap: () => _selectAll(_duration),
                onChanged: (_) => setState(() {}),
                decoration: const InputDecoration(labelText: 'Duration (min)'),
              ),
            ),
            const SizedBox(width: 10),
            Expanded(
              child: TextField(
                controller: _met,
                keyboardType: const TextInputType.numberWithOptions(decimal: true),
                onTap: () => _selectAll(_met),
                onChanged: (_) => setState(() {}),
                decoration: const InputDecoration(labelText: 'MET (optional)'),
              ),
            ),
          ]),
          const SizedBox(height: 12),
          ListTile(
            shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(14), side: BorderSide(color: Theme.of(context).dividerColor)),
            title: const Text('Workout date'),
            subtitle: Text('${_date.day}/${_date.month}/${_date.year}'),
            trailing: const Icon(Icons.calendar_month),
            onTap: () async {
              final picked = await showDatePicker(
                context: context,
                firstDate: DateTime(2020),
                lastDate: DateTime.now().add(const Duration(days: 1)),
                initialDate: _date,
              );
              if (picked != null) setState(() => _date = picked);
            },
          ),
          const SizedBox(height: 12),
          DropdownButtonFormField<String>(
            initialValue: _source,
            decoration: const InputDecoration(labelText: 'Activity data source'),
            items: const [
              DropdownMenuItem(value: 'Manual entry', child: Text('Manual entry')),
              DropdownMenuItem(value: 'Smartwatch', child: Text('Smartwatch')),
              DropdownMenuItem(value: 'Cardio machine', child: Text('Cardio machine')),
              DropdownMenuItem(value: 'Other device', child: Text('Other device')),
            ],
            onChanged: (v) => setState(() => _source = v ?? _source),
          ),
          const SizedBox(height: 12),
          TextField(
            controller: _deviceCalories,
            keyboardType: const TextInputType.numberWithOptions(decimal: true),
            onTap: () => _selectAll(_deviceCalories),
            decoration: const InputDecoration(labelText: 'Device calories (optional)'),
          ),
          const SizedBox(height: 18),
          ...List.generate(_exercises.length, (index) => _exerciseCard(index)),
          OutlinedButton.icon(
            onPressed: () => setState(() => _exercises.add(_DraftExercise())),
            icon: const Icon(Icons.add),
            label: const Text('Add exercise'),
          ),
          const SizedBox(height: 18),
          DropdownButtonFormField<int>(
            initialValue: _sessionRpe,
            decoration: const InputDecoration(
              labelText: 'Session RPE (optional)',
              helperText: 'How hard did the overall workout feel? 1 easy • 10 maximal',
            ),
            items: List.generate(10, (i) => DropdownMenuItem(value: i + 1, child: Text('${i + 1}'))),
            onChanged: (v) => setState(() => _sessionRpe = v),
          ),
          const SizedBox(height: 18),
          Card(
            child: Padding(
              padding: const EdgeInsets.all(16),
              child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                Text('Session summary', style: Theme.of(context).textTheme.titleMedium?.copyWith(fontWeight: FontWeight.w800)),
                const SizedBox(height: 10),
                Text('Training volume: ${volume.toStringAsFixed(0)} kg'),
                Text('MET-min: ${mets.toStringAsFixed(0)}'),
                Text(_deviceCalories.text.trim().isNotEmpty
                    ? 'Energy: ${_deviceCalories.text} kcal (device-entered)'
                    : 'Estimated energy: ${estimated.toStringAsFixed(0)} kcal'),
              ]),
            ),
          ),
          const SizedBox(height: 16),
          FilledButton(
            onPressed: _save,
            child: Padding(
              padding: const EdgeInsets.all(14),
              child: Text(_editing ? 'Save workout changes' : 'Save strength session'),
            ),
          ),
          const SizedBox(height: 10),
          Text('Estimated 1RM values use the Epley formula for monitoring trends only.', style: Theme.of(context).textTheme.bodySmall),
        ],
      ),
    );
  }

  Widget _scoreField(
    String label,
    int? value,
    int min,
    int max,
    ValueChanged<int?> onChanged, {
    required String helper,
  }) {
    return DropdownButtonFormField<int>(
      initialValue: value,
      decoration: InputDecoration(labelText: label, helperText: helper),
      items: [for (var i = min; i <= max; i++) DropdownMenuItem(value: i, child: Text('$i'))],
      onChanged: onChanged,
    );
  }

  Widget _exerciseCard(int index) {
    final exercise = _exercises[index];
    double best = 0;
    for (final set in exercise.sets) {
      final reps = int.tryParse(set.reps.text) ?? 0;
      final kg = double.tryParse(set.weight.text) ?? 0;
      final e1rm = epleyE1rm(kg, reps);
      if (e1rm > best) best = e1rm;
    }
    return Card(
      margin: const EdgeInsets.only(bottom: 12),
      child: Padding(
        padding: const EdgeInsets.all(14),
        child: Column(
          children: [
            Row(children: [
              Expanded(
                child: TextField(
                  controller: exercise.name,
                  onChanged: (_) => setState(() {}),
                  decoration: const InputDecoration(labelText: 'Exercise name', hintText: 'e.g. Bench press'),
                ),
              ),
              if (_exercises.length > 1)
                IconButton(
                  onPressed: () {
                    exercise.dispose();
                    setState(() => _exercises.removeAt(index));
                  },
                  icon: const Icon(Icons.delete_outline),
                ),
            ]),
            const SizedBox(height: 10),
            Row(children: [
              const SizedBox(width: 34),
              Expanded(child: Text('Reps', textAlign: TextAlign.center, style: Theme.of(context).textTheme.labelSmall)),
              const SizedBox(width: 8),
              Expanded(child: Text('Weight kg', textAlign: TextAlign.center, style: Theme.of(context).textTheme.labelSmall)),
              const SizedBox(width: 44),
            ]),
            ...List.generate(exercise.sets.length, (setIndex) {
              final set = exercise.sets[setIndex];
              return Padding(
                padding: const EdgeInsets.only(top: 7),
                child: Row(children: [
                  SizedBox(width: 34, child: Text('${setIndex + 1}', textAlign: TextAlign.center)),
                  Expanded(
                    child: TextField(
                      controller: set.reps,
                      keyboardType: TextInputType.number,
                      onTap: () => _selectAll(set.reps),
                      onChanged: (_) => setState(() {}),
                      textAlign: TextAlign.center,
                      decoration: const InputDecoration(hintText: 'Reps'),
                    ),
                  ),
                  const SizedBox(width: 8),
                  Expanded(
                    child: TextField(
                      controller: set.weight,
                      keyboardType: const TextInputType.numberWithOptions(decimal: true),
                      onTap: () => _selectAll(set.weight),
                      onChanged: (_) => setState(() {}),
                      textAlign: TextAlign.center,
                      decoration: const InputDecoration(hintText: 'kg'),
                    ),
                  ),
                  SizedBox(
                    width: 44,
                    child: IconButton(
                      onPressed: exercise.sets.length <= 1
                          ? null
                          : () {
                              set.dispose();
                              setState(() => exercise.sets.removeAt(setIndex));
                            },
                      icon: const Icon(Icons.remove_circle_outline, size: 20),
                    ),
                  ),
                ]),
              );
            }),
            const SizedBox(height: 8),
            Row(children: [
              TextButton.icon(
                onPressed: () => setState(() => exercise.sets.add(_DraftSet())),
                icon: const Icon(Icons.add),
                label: const Text('Set'),
              ),
              const Spacer(),
              if (best > 0) Text('Best e1RM ${best.toStringAsFixed(0)} kg', style: Theme.of(context).textTheme.labelMedium),
            ]),
          ],
        ),
      ),
    );
  }
}
