import 'package:flutter/material.dart';

import '../app_store.dart';
import '../calculations.dart';
import '../models.dart';

class LogActivityScreen extends StatefulWidget {
  final AppStore store;
  const LogActivityScreen({super.key, required this.store});

  @override
  State<LogActivityScreen> createState() => _LogActivityScreenState();
}

class _LogActivityScreenState extends State<LogActivityScreen> {
  String _type = 'Walking';
  String _source = 'Manual entry';
  final _duration = TextEditingController(text: '30');
  final _met = TextEditingController();
  final _deviceCalories = TextEditingController();
  DateTime _date = DateTime.now();

  @override
  void dispose() {
    _duration.dispose(); _met.dispose(); _deviceCalories.dispose();
    super.dispose();
  }

  Future<void> _save() async {
    final duration = int.tryParse(_duration.text) ?? 0;
    if (duration <= 0) return;
    await widget.store.addWorkout(
      WorkoutSession(
        date: _date,
        workoutType: _type,
        durationMin: duration,
        met: double.tryParse(_met.text),
        source: _source,
        deviceCalories: double.tryParse(_deviceCalories.text),
      ),
    );
    if (mounted) Navigator.pop(context);
  }

  @override
  Widget build(BuildContext context) {
    final duration = int.tryParse(_duration.text) ?? 0;
    final met = double.tryParse(_met.text);
    final est = estimatedCalories(met: met, minutes: duration, bodyWeightKg: widget.store.currentWeightKg);
    return Scaffold(
      appBar: AppBar(title: const Text('Log activity')),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          DropdownButtonFormField<String>(
            initialValue: _type,
            decoration: const InputDecoration(labelText: 'Activity type'),
            items: const [
              'Walking','Running','Cycling','Rowing','Swimming','Elliptical','HIIT','Other cardio'
            ].map((e) => DropdownMenuItem(value: e, child: Text(e))).toList(),
            onChanged: (v) => setState(() => _type = v ?? _type),
          ),
          const SizedBox(height: 12),
          Row(children: [
            Expanded(child: TextField(controller: _duration, keyboardType: TextInputType.number, onChanged: (_) => setState(() {}), decoration: const InputDecoration(labelText: 'Minutes'))),
            const SizedBox(width: 10),
            Expanded(child: TextField(controller: _met, keyboardType: const TextInputType.numberWithOptions(decimal: true), onChanged: (_) => setState(() {}), decoration: const InputDecoration(labelText: 'MET (optional)'))),
          ]),
          const SizedBox(height: 12),
          DropdownButtonFormField<String>(
            initialValue: _source,
            decoration: const InputDecoration(labelText: 'Source'),
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
            onChanged: (_) => setState(() {}),
            decoration: const InputDecoration(labelText: 'Calories from device (optional)'),
          ),
          const SizedBox(height: 12),
          ListTile(
            shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(14), side: BorderSide(color: Theme.of(context).dividerColor)),
            title: const Text('Date'),
            subtitle: Text('${_date.day}/${_date.month}/${_date.year}'),
            trailing: const Icon(Icons.calendar_month),
            onTap: () async {
              final picked = await showDatePicker(context: context, firstDate: DateTime(2020), lastDate: DateTime.now().add(const Duration(days: 1)), initialDate: _date);
              if (picked != null) setState(() => _date = picked);
            },
          ),
          const SizedBox(height: 18),
          Card(
            child: Padding(
              padding: const EdgeInsets.all(16),
              child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                Text('Exercise dose', style: Theme.of(context).textTheme.titleMedium?.copyWith(fontWeight: FontWeight.w800)),
                const SizedBox(height: 8),
                Text(met == null ? 'MET-min: not available' : 'MET-min: ${(met * duration).toStringAsFixed(0)}'),
                Text(_deviceCalories.text.trim().isNotEmpty
                    ? 'Energy: ${_deviceCalories.text} kcal (device-entered)'
                    : met == null ? 'Energy: not available' : 'Estimated energy: ${est.toStringAsFixed(0)} kcal'),
              ]),
            ),
          ),
          const SizedBox(height: 16),
          FilledButton(onPressed: _save, child: const Padding(padding: EdgeInsets.all(14), child: Text('Save activity'))),
        ],
      ),
    );
  }
}
