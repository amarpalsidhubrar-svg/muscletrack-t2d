import 'package:flutter/material.dart';

import '../app_store.dart';
import '../models.dart';
import '../widgets/common.dart';

class OnboardingScreen extends StatefulWidget {
  final AppStore store;
  const OnboardingScreen({super.key, required this.store});

  @override
  State<OnboardingScreen> createState() => _OnboardingScreenState();
}

class _OnboardingScreenState extends State<OnboardingScreen> {
  final _formKey = GlobalKey<FormState>();
  final _name = TextEditingController();
  final _age = TextEditingController();
  final _height = TextEditingController();
  final _weight = TextEditingController();
  String _sex = 'Male';
  bool _accepted = false;
  bool _saving = false;

  @override
  void dispose() {
    _name.dispose();
    _age.dispose();
    _height.dispose();
    _weight.dispose();
    super.dispose();
  }

  Future<void> _save() async {
    if (!_formKey.currentState!.validate() || !_accepted) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Complete the profile and acknowledge the monitoring notice.')),
      );
      return;
    }
    setState(() => _saving = true);
    await widget.store.saveProfile(
      UserProfile(
        name: _name.text.trim(),
        age: int.parse(_age.text),
        sex: _sex,
        heightCm: double.parse(_height.text),
        baselineWeightKg: double.parse(_weight.text),
      ),
    );
    if (mounted) setState(() => _saving = false);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: SafeArea(
        child: ListView(
          padding: const EdgeInsets.all(20),
          children: [
            const SizedBox(height: 18),
            Icon(Icons.monitor_heart_outlined,
                size: 52, color: Theme.of(context).colorScheme.primary),
            const SizedBox(height: 16),
            Text(
              'MuscleTrack T2D',
              textAlign: TextAlign.center,
              style: Theme.of(context).textTheme.headlineMedium?.copyWith(
                    fontWeight: FontWeight.w900,
                  ),
            ),
            const SizedBox(height: 8),
            Text(
              'Track weight, muscle-related measures, activity, strength and medication exposure in one place.',
              textAlign: TextAlign.center,
              style: Theme.of(context).textTheme.bodyMedium,
            ),
            const SizedBox(height: 24),
            const MonitoringNotice(),
            const SizedBox(height: 20),
            Form(
              key: _formKey,
              child: Column(
                children: [
                  TextFormField(
                    controller: _name,
                    decoration: const InputDecoration(labelText: 'Name or nickname'),
                    validator: (v) => v == null || v.trim().isEmpty ? 'Required' : null,
                  ),
                  const SizedBox(height: 12),
                  Row(
                    children: [
                      Expanded(
                        child: TextFormField(
                          controller: _age,
                          keyboardType: TextInputType.number,
                          decoration: const InputDecoration(labelText: 'Age'),
                          validator: (v) {
                            final value = int.tryParse(v ?? '');
                            return value == null || value < 18 || value > 120
                                ? 'Enter adult age'
                                : null;
                          },
                        ),
                      ),
                      const SizedBox(width: 12),
                      Expanded(
                        child: DropdownButtonFormField<String>(
                          initialValue: _sex,
                          decoration: const InputDecoration(labelText: 'Sex'),
                          items: const [
                            DropdownMenuItem(value: 'Male', child: Text('Male')),
                            DropdownMenuItem(value: 'Female', child: Text('Female')),
                            DropdownMenuItem(value: 'Other / prefer not to say', child: Text('Other')),
                          ],
                          onChanged: (v) => setState(() => _sex = v ?? _sex),
                        ),
                      ),
                    ],
                  ),
                  const SizedBox(height: 12),
                  Row(
                    children: [
                      Expanded(
                        child: TextFormField(
                          controller: _height,
                          keyboardType: const TextInputType.numberWithOptions(decimal: true),
                          decoration: const InputDecoration(labelText: 'Height (cm)'),
                          validator: (v) {
                            final value = double.tryParse(v ?? '');
                            return value == null || value < 100 || value > 250
                                ? 'Check height'
                                : null;
                          },
                        ),
                      ),
                      const SizedBox(width: 12),
                      Expanded(
                        child: TextFormField(
                          controller: _weight,
                          keyboardType: const TextInputType.numberWithOptions(decimal: true),
                          decoration: const InputDecoration(labelText: 'Baseline weight (kg)'),
                          validator: (v) {
                            final value = double.tryParse(v ?? '');
                            return value == null || value < 25 || value > 400
                                ? 'Check weight'
                                : null;
                          },
                        ),
                      ),
                    ],
                  ),
                ],
              ),
            ),
            const SizedBox(height: 14),
            CheckboxListTile(
              contentPadding: EdgeInsets.zero,
              value: _accepted,
              onChanged: (v) => setState(() => _accepted = v ?? false),
              title: const Text(
                'I understand this app is for monitoring only and does not provide diagnosis or treatment advice.',
                style: TextStyle(fontSize: 13),
              ),
              controlAffinity: ListTileControlAffinity.leading,
            ),
            const SizedBox(height: 8),
            FilledButton.icon(
              onPressed: _saving ? null : _save,
              icon: _saving
                  ? const SizedBox.square(
                      dimension: 18,
                      child: CircularProgressIndicator(strokeWidth: 2),
                    )
                  : const Icon(Icons.arrow_forward),
              label: const Padding(
                padding: EdgeInsets.symmetric(vertical: 14),
                child: Text('Create local profile'),
              ),
            ),
            const SizedBox(height: 10),
            Text(
              'Version 0.1 stores data on this device only. No account or cloud sync is used.',
              textAlign: TextAlign.center,
              style: Theme.of(context).textTheme.bodySmall,
            ),
          ],
        ),
      ),
    );
  }
}
