import 'package:flutter/material.dart';

import '../app_store.dart';
import '../models.dart';
import '../widgets/common.dart';

class GoalsScreen extends StatefulWidget {
  final AppStore store;
  const GoalsScreen({super.key, required this.store});

  @override
  State<GoalsScreen> createState() => _GoalsScreenState();
}

class _GoalsScreenState extends State<GoalsScreen> {
  late final TextEditingController _targetWeight;
  late final TextEditingController _weeklyMinutes;
  late final TextEditingController _strengthSessions;
  late final TextEditingController _exercise;
  late final TextEditingController _targetE1rm;

  @override
  void initState() {
    super.initState();
    final g = widget.store.goals;
    _targetWeight = TextEditingController(text: g.targetWeightKg?.toString() ?? '');
    _weeklyMinutes = TextEditingController(text: g.weeklyActivityMin.toString());
    _strengthSessions = TextEditingController(text: g.weeklyStrengthSessions.toString());
    _exercise = TextEditingController(text: g.targetExercise);
    _targetE1rm = TextEditingController(text: g.targetE1rmKg?.toString() ?? '');
  }

  @override
  void dispose() {
    _targetWeight.dispose(); _weeklyMinutes.dispose(); _strengthSessions.dispose(); _exercise.dispose(); _targetE1rm.dispose();
    super.dispose();
  }

  Future<void> _save() async {
    await widget.store.saveGoals(Goals(
      targetWeightKg: double.tryParse(_targetWeight.text),
      weeklyActivityMin: int.tryParse(_weeklyMinutes.text) ?? 150,
      weeklyStrengthSessions: int.tryParse(_strengthSessions.text) ?? 2,
      targetExercise: _exercise.text.trim(),
      targetE1rmKg: double.tryParse(_targetE1rm.text),
    ));
    if (mounted) ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('Goals saved')));
  }

  @override
  Widget build(BuildContext context) {
    final targetWeight = double.tryParse(_targetWeight.text);
    final targetExercise = _exercise.text.trim();
    final currentE1rm = targetExercise.isEmpty ? null : widget.store.latestE1rmFor(targetExercise);
    return ListView(
      padding: const EdgeInsets.fromLTRB(16, 12, 16, 110),
      children: [
        Text('Personal goals', style: Theme.of(context).textTheme.headlineSmall?.copyWith(fontWeight: FontWeight.w900)),
        const SizedBox(height: 4),
        Text('Goals are user-defined monitoring targets, not treatment recommendations.', style: Theme.of(context).textTheme.bodyMedium),
        const SizedBox(height: 16),
        Card(
          child: Padding(
            padding: const EdgeInsets.all(16),
            child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
              Text('Weight', style: Theme.of(context).textTheme.titleMedium?.copyWith(fontWeight: FontWeight.w800)),
              const SizedBox(height: 10),
              TextField(controller: _targetWeight, onChanged: (_) => setState(() {}), keyboardType: const TextInputType.numberWithOptions(decimal: true), decoration: const InputDecoration(labelText: 'Target weight (kg, optional)')),
              if (targetWeight != null) ...[
                const SizedBox(height: 8),
                Text('Current ${widget.store.currentWeightKg.toStringAsFixed(1)} kg • Target ${targetWeight.toStringAsFixed(1)} kg', style: Theme.of(context).textTheme.bodySmall),
              ],
            ]),
          ),
        ),
        const SizedBox(height: 10),
        Card(
          child: Padding(
            padding: const EdgeInsets.all(16),
            child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
              Text('Weekly activity', style: Theme.of(context).textTheme.titleMedium?.copyWith(fontWeight: FontWeight.w800)),
              const SizedBox(height: 10),
              Row(children: [
                Expanded(child: TextField(controller: _weeklyMinutes, keyboardType: TextInputType.number, decoration: const InputDecoration(labelText: 'Activity min/week'))),
                const SizedBox(width: 10),
                Expanded(child: TextField(controller: _strengthSessions, keyboardType: TextInputType.number, decoration: const InputDecoration(labelText: 'Strength sessions/week'))),
              ]),
            ]),
          ),
        ),
        const SizedBox(height: 10),
        Card(
          child: Padding(
            padding: const EdgeInsets.all(16),
            child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
              Text('Strength', style: Theme.of(context).textTheme.titleMedium?.copyWith(fontWeight: FontWeight.w800)),
              const SizedBox(height: 10),
              TextField(controller: _exercise, onChanged: (_) => setState(() {}), decoration: const InputDecoration(labelText: 'Target exercise', hintText: 'e.g. Leg press')),
              const SizedBox(height: 10),
              TextField(controller: _targetE1rm, keyboardType: const TextInputType.numberWithOptions(decimal: true), decoration: const InputDecoration(labelText: 'Target estimated 1RM (kg)')),
              if (currentE1rm != null) ...[
                const SizedBox(height: 8),
                Text('Current best recorded e1RM: ${currentE1rm.toStringAsFixed(0)} kg', style: Theme.of(context).textTheme.bodySmall),
              ],
            ]),
          ),
        ),
        const SizedBox(height: 16),
        FilledButton.icon(onPressed: _save, icon: const Icon(Icons.save_outlined), label: const Padding(padding: EdgeInsets.all(14), child: Text('Save goals'))),
        const SizedBox(height: 14),
        const MonitoringNotice(),
      ],
    );
  }
}
