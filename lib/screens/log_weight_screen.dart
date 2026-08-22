import 'package:flutter/material.dart';

import '../app_store.dart';
import '../models.dart';

class LogWeightScreen extends StatefulWidget {
  final AppStore store;
  const LogWeightScreen({super.key, required this.store});

  @override
  State<LogWeightScreen> createState() => _LogWeightScreenState();
}

class _LogWeightScreenState extends State<LogWeightScreen> {
  final _weight = TextEditingController();
  final _bodyFat = TextEditingController();
  final _leanMass = TextEditingController();
  DateTime _date = DateTime.now();

  @override
  void dispose() {
    _weight.dispose();
    _bodyFat.dispose();
    _leanMass.dispose();
    super.dispose();
  }

  Future<void> _save() async {
    final value = double.tryParse(_weight.text);
    if (value == null || value <= 0) return;
    await widget.store.addWeight(
      WeightEntry(
        date: _date,
        weightKg: value,
        bodyFatPct: double.tryParse(_bodyFat.text),
        leanMassKg: double.tryParse(_leanMass.text),
      ),
    );
    if (mounted) Navigator.pop(context);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Log weight')),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          TextField(
            controller: _weight,
            autofocus: true,
            keyboardType: const TextInputType.numberWithOptions(decimal: true),
            decoration: const InputDecoration(labelText: 'Weight (kg)'),
          ),
          const SizedBox(height: 12),
          TextField(
            controller: _bodyFat,
            keyboardType: const TextInputType.numberWithOptions(decimal: true),
            decoration: const InputDecoration(labelText: 'Body fat % (optional)'),
          ),
          const SizedBox(height: 12),
          TextField(
            controller: _leanMass,
            keyboardType: const TextInputType.numberWithOptions(decimal: true),
            decoration: const InputDecoration(labelText: 'Lean mass kg (optional)'),
          ),
          const SizedBox(height: 12),
          ListTile(
            shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(14), side: BorderSide(color: Theme.of(context).dividerColor)),
            title: const Text('Date'),
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
          const SizedBox(height: 20),
          FilledButton(onPressed: _save, child: const Padding(padding: EdgeInsets.all(14), child: Text('Save weight'))),
          const SizedBox(height: 10),
          Text(
            'Body composition values are stored exactly as entered and are not interpreted as a diagnosis.',
            style: Theme.of(context).textTheme.bodySmall,
          ),
        ],
      ),
    );
  }
}
