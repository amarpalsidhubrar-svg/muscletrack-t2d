import 'package:flutter/material.dart';

import '../app_store.dart';
import '../calculations.dart';
import '../models.dart';

class _DraftSet {
  final reps = TextEditingController(text: '10');
  final weight = TextEditingController(text: '0');
  void dispose() { reps.dispose(); weight.dispose(); }
}

class _DraftExercise {
  final name = TextEditingController();
  final List<_DraftSet> sets = [_DraftSet(), _DraftSet(), _DraftSet()];
  void dispose() { name.dispose(); for (final s in sets) { s.dispose(); } }
}

class StrengthWorkoutScreen extends StatefulWidget {
  final AppStore store;
  const StrengthWorkoutScreen({super.key, required this.store});

  @override
  State<StrengthWorkoutScreen> createState() => _StrengthWorkoutScreenState();
}

class _StrengthWorkoutScreenState extends State<StrengthWorkoutScreen> {
  final _duration = TextEditingController(text: '45');
  final _met = TextEditingController(text: '3.5');
  final _deviceCalories = TextEditingController();
  DateTime _date = DateTime.now();
  String _source = 'Manual entry';
  final List<_DraftExercise> _exercises = [_DraftExercise()];

  @override
  void dispose() {
    _duration.dispose();
    _met.dispose();
    _deviceCalories.dispose();
    for (final e in _exercises) { e.dispose(); }
    super.dispose();
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
    await widget.store.addWorkout(
      WorkoutSession(
        date: _date,
        workoutType: 'Strength',
        durationMin: duration,
        met: double.tryParse(_met.text),
        source: _source,
        deviceCalories: double.tryParse(_deviceCalories.text),
        sets: sets,
      ),
    );
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
      appBar: AppBar(title: const Text('Log strength session')),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          Row(children: [
            Expanded(child: TextField(controller: _duration, keyboardType: TextInputType.number, onChanged: (_) => setState(() {}), decoration: const InputDecoration(labelText: 'Duration (min)'))),
            const SizedBox(width: 10),
            Expanded(child: TextField(controller: _met, keyboardType: const TextInputType.numberWithOptions(decimal: true), onChanged: (_) => setState(() {}), decoration: const InputDecoration(labelText: 'MET (optional)'))),
          ]),
          const SizedBox(height: 12),
          ListTile(
            shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(14), side: BorderSide(color: Theme.of(context).dividerColor)),
            title: const Text('Workout date'),
            subtitle: Text('${_date.day}/${_date.month}/${_date.year}'),
            trailing: const Icon(Icons.calendar_month),
            onTap: () async {
              final picked = await showDatePicker(context: context, firstDate: DateTime(2020), lastDate: DateTime.now().add(const Duration(days: 1)), initialDate: _date);
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
          FilledButton(onPressed: _save, child: const Padding(padding: EdgeInsets.all(14), child: Text('Save strength session'))),
          const SizedBox(height: 10),
          Text('Estimated 1RM values use the Epley formula for monitoring trends only.', style: Theme.of(context).textTheme.bodySmall),
        ],
      ),
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
              Expanded(child: TextField(controller: exercise.name, onChanged: (_) => setState(() {}), decoration: const InputDecoration(labelText: 'Exercise name', hintText: 'e.g. Leg press'))),
              if (_exercises.length > 1)
                IconButton(onPressed: () { exercise.dispose(); setState(() => _exercises.removeAt(index)); }, icon: const Icon(Icons.delete_outline)),
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
                  Expanded(child: TextField(controller: set.reps, keyboardType: TextInputType.number, onChanged: (_) => setState(() {}), textAlign: TextAlign.center)),
                  const SizedBox(width: 8),
                  Expanded(child: TextField(controller: set.weight, keyboardType: const TextInputType.numberWithOptions(decimal: true), onChanged: (_) => setState(() {}), textAlign: TextAlign.center)),
                  SizedBox(width: 44, child: IconButton(onPressed: exercise.sets.length <= 1 ? null : () { set.dispose(); setState(() => exercise.sets.removeAt(setIndex)); }, icon: const Icon(Icons.remove_circle_outline, size: 20))),
                ]),
              );
            }),
            const SizedBox(height: 8),
            Row(children: [
              TextButton.icon(onPressed: () => setState(() => exercise.sets.add(_DraftSet())), icon: const Icon(Icons.add), label: const Text('Set')),
              const Spacer(),
              if (best > 0) Text('Best e1RM ${best.toStringAsFixed(0)} kg', style: Theme.of(context).textTheme.labelMedium),
            ]),
          ],
        ),
      ),
    );
  }
}
