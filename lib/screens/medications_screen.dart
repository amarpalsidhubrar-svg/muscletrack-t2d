import 'package:flutter/material.dart';

import '../app_store.dart';
import '../calculations.dart';
import '../models.dart';
import '../widgets/common.dart';

class MedicationsScreen extends StatefulWidget {
  final AppStore store;
  const MedicationsScreen({super.key, required this.store});

  @override
  State<MedicationsScreen> createState() => _MedicationsScreenState();
}

class _MedicationsScreenState extends State<MedicationsScreen> {
  final _name = TextEditingController();
  final _dose = TextEditingController();
  final _note = TextEditingController();
  String _class = 'GLP-1RA';
  DateTime _date = DateTime.now();

  @override
  void dispose() { _name.dispose(); _dose.dispose(); _note.dispose(); super.dispose(); }

  Future<void> _save() async {
    if (_name.text.trim().isEmpty || _dose.text.trim().isEmpty) return;
    await widget.store.addMedication(MedicationEntry(
      date: _date,
      medicationName: _name.text.trim(),
      medicationClass: _class,
      dose: _dose.text.trim(),
      note: _note.text.trim(),
    ));
    _name.clear(); _dose.clear(); _note.clear();
    if (mounted) setState(() {});
  }

  @override
  Widget build(BuildContext context) {
    return ListView(
      padding: const EdgeInsets.fromLTRB(16, 12, 16, 110),
      children: [
        Text('Medication exposure', style: Theme.of(context).textTheme.headlineSmall?.copyWith(fontWeight: FontWeight.w900)),
        const SizedBox(height: 4),
        Text('Record medication and dose changes for longitudinal monitoring.', style: Theme.of(context).textTheme.bodyMedium),
        const SizedBox(height: 16),
        Card(
          child: Padding(
            padding: const EdgeInsets.all(16),
            child: Column(children: [
              DropdownButtonFormField<String>(
                initialValue: _class,
                decoration: const InputDecoration(labelText: 'Medication class'),
                items: const [
                  'GLP-1RA','Dual GIP/GLP-1','SGLT2 inhibitor','Metformin','Insulin','Sulfonylurea','Other'
                ].map((e) => DropdownMenuItem(value: e, child: Text(e))).toList(),
                onChanged: (v) => setState(() => _class = v ?? _class),
              ),
              const SizedBox(height: 10),
              TextField(controller: _name, decoration: const InputDecoration(labelText: 'Medication name', hintText: 'e.g. semaglutide')),
              const SizedBox(height: 10),
              TextField(controller: _dose, decoration: const InputDecoration(labelText: 'Dose / frequency', hintText: 'e.g. 1 mg weekly')),
              const SizedBox(height: 10),
              TextField(controller: _note, maxLines: 2, decoration: const InputDecoration(labelText: 'Optional note')),
              const SizedBox(height: 10),
              ListTile(
                contentPadding: EdgeInsets.zero,
                title: const Text('Effective / recorded date'),
                subtitle: Text(shortDate(_date)),
                trailing: const Icon(Icons.calendar_month),
                onTap: () async {
                  final picked = await showDatePicker(context: context, firstDate: DateTime(2020), lastDate: DateTime.now().add(const Duration(days: 1)), initialDate: _date);
                  if (picked != null) setState(() => _date = picked);
                },
              ),
              const SizedBox(height: 8),
              SizedBox(width: double.infinity, child: FilledButton.icon(onPressed: _save, icon: const Icon(Icons.add), label: const Text('Add medication record'))),
            ]),
          ),
        ),
        const SectionHeader('Timeline'),
        if (widget.store.medications.isEmpty)
          const Card(child: Padding(padding: EdgeInsets.all(16), child: Text('No medication entries yet.'))),
        ...widget.store.medications.map((entry) => Card(
          margin: const EdgeInsets.only(bottom: 8),
          child: ListTile(
            leading: const CircleAvatar(child: Icon(Icons.medication_outlined, size: 19)),
            title: Text(entry.medicationName),
            subtitle: Text('${entry.medicationClass} • ${entry.dose}\n${shortDate(entry.date)}${entry.note.isEmpty ? '' : ' • ${entry.note}'}'),
            isThreeLine: entry.note.isNotEmpty,
          ),
        )),
        const SizedBox(height: 14),
        const MonitoringNotice(),
      ],
    );
  }
}
