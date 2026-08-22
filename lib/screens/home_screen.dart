import 'dart:math' as math;

import 'package:flutter/material.dart';

import '../app_store.dart';
import '../calculations.dart';
import '../widgets/common.dart';
import 'log_activity_screen.dart';
import 'log_weight_screen.dart';
import 'strength_workout_screen.dart';

class HomeScreen extends StatelessWidget {
  final AppStore store;
  const HomeScreen({super.key, required this.store});

  @override
  Widget build(BuildContext context) {
    final profile = store.profile!;
    final latestStrength = store.latestStrengthBest;
    final activityGoal = math.max(store.goals.weeklyActivityMin, 1);
    final strengthGoal = math.max(store.goals.weeklyStrengthSessions, 1);

    return ListView(
      padding: const EdgeInsets.fromLTRB(16, 12, 16, 110),
      children: [
        Text('Hello, ${profile.name}',
            style: Theme.of(context).textTheme.headlineSmall?.copyWith(
                  fontWeight: FontWeight.w900,
                )),
        const SizedBox(height: 4),
        Text('Monitor weight, activity and strength together.',
            style: Theme.of(context).textTheme.bodyMedium),
        const SizedBox(height: 18),
        Card(
          color: Theme.of(context).colorScheme.primaryContainer,
          child: Padding(
            padding: const EdgeInsets.all(18),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text('Weight & strength trend',
                    style: Theme.of(context).textTheme.labelLarge),
                const SizedBox(height: 7),
                Text(
                  'Weight ${store.weightChangePct.toStringAsFixed(1)}% from baseline',
                  style: Theme.of(context).textTheme.titleLarge?.copyWith(
                        fontWeight: FontWeight.w900,
                      ),
                ),
                const SizedBox(height: 5),
                Text(
                  latestStrength == null
                      ? 'Log a strength session to begin tracking strength.'
                      : 'Best recorded e1RM: ${latestStrength.e1rmKg.toStringAsFixed(0)} kg (${latestStrength.exerciseName})',
                ),
              ],
            ),
          ),
        ),
        const SectionHeader('Today'),
        Row(
          children: [
            Expanded(
              child: MetricCard(
                label: 'Current weight',
                value: '${store.currentWeightKg.toStringAsFixed(1)} kg',
                subtitle: 'BMI ${store.currentBmi.toStringAsFixed(1)}',
                icon: Icons.monitor_weight_outlined,
              ),
            ),
            const SizedBox(width: 10),
            Expanded(
              child: MetricCard(
                label: 'Best strength',
                value: latestStrength == null
                    ? '—'
                    : '${latestStrength.e1rmKg.toStringAsFixed(0)} kg',
                subtitle: latestStrength?.exerciseName ?? 'No data yet',
                icon: Icons.fitness_center,
              ),
            ),
          ],
        ),
        const SizedBox(height: 10),
        Card(
          child: Padding(
            padding: const EdgeInsets.all(16),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text('This week',
                    style: Theme.of(context).textTheme.titleMedium?.copyWith(
                          fontWeight: FontWeight.w800,
                        )),
                const SizedBox(height: 14),
                _ProgressRow(
                  label: 'Activity minutes',
                  value: '${store.weeklyActivityMinutes} / $activityGoal min',
                  progress: store.weeklyActivityMinutes / activityGoal,
                ),
                const SizedBox(height: 14),
                _ProgressRow(
                  label: 'Strength sessions',
                  value: '${store.weeklyStrengthSessions} / $strengthGoal',
                  progress: store.weeklyStrengthSessions / strengthGoal,
                ),
                const SizedBox(height: 14),
                Row(
                  children: [
                    Expanded(child: _MiniStat(label: 'MET-min', value: store.weeklyMetMinutes.toStringAsFixed(0))),
                    const SizedBox(width: 8),
                    Expanded(child: _MiniStat(label: 'Energy', value: '${store.weeklyCalories.toStringAsFixed(0)} kcal')),
                  ],
                ),
              ],
            ),
          ),
        ),
        const SectionHeader('Quick log'),
        Wrap(
          spacing: 8,
          runSpacing: 8,
          children: [
            ActionChip(
              avatar: const Icon(Icons.monitor_weight_outlined, size: 18),
              label: const Text('Weight'),
              onPressed: () => Navigator.push(
                context,
                MaterialPageRoute(builder: (_) => LogWeightScreen(store: store)),
              ),
            ),
            ActionChip(
              avatar: const Icon(Icons.fitness_center, size: 18),
              label: const Text('Strength'),
              onPressed: () => Navigator.push(
                context,
                MaterialPageRoute(builder: (_) => StrengthWorkoutScreen(store: store)),
              ),
            ),
            ActionChip(
              avatar: const Icon(Icons.directions_run, size: 18),
              label: const Text('Activity'),
              onPressed: () => Navigator.push(
                context,
                MaterialPageRoute(builder: (_) => LogActivityScreen(store: store)),
              ),
            ),
          ],
        ),
        const SectionHeader('Recent medication'),
        Card(
          child: Padding(
            padding: const EdgeInsets.all(16),
            child: store.medications.isEmpty
                ? const Text('No medication exposure recorded yet.')
                : Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(store.medications.first.medicationName,
                          style: Theme.of(context).textTheme.titleMedium?.copyWith(fontWeight: FontWeight.w800)),
                      const SizedBox(height: 3),
                      Text('${store.medications.first.medicationClass} • ${store.medications.first.dose}'),
                      const SizedBox(height: 3),
                      Text('Recorded ${shortDate(store.medications.first.date)}',
                          style: Theme.of(context).textTheme.bodySmall),
                    ],
                  ),
          ),
        ),
        const SizedBox(height: 14),
        const MonitoringNotice(),
      ],
    );
  }
}

class _ProgressRow extends StatelessWidget {
  final String label;
  final String value;
  final double progress;
  const _ProgressRow({required this.label, required this.value, required this.progress});

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        Row(children: [Expanded(child: Text(label)), Text(value)]),
        const SizedBox(height: 7),
        LinearProgressIndicator(value: progress.clamp(0, 1).toDouble()),
      ],
    );
  }
}

class _MiniStat extends StatelessWidget {
  final String label;
  final String value;
  const _MiniStat({required this.label, required this.value});

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(12),
      decoration: BoxDecoration(
        color: Theme.of(context).colorScheme.surfaceContainerHighest,
        borderRadius: BorderRadius.circular(14),
      ),
      child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
        Text(value, style: Theme.of(context).textTheme.titleMedium?.copyWith(fontWeight: FontWeight.w900)),
        Text(label, style: Theme.of(context).textTheme.bodySmall),
      ]),
    );
  }
}
