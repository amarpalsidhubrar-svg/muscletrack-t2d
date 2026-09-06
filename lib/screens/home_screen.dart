import 'dart:math' as math;

import 'package:flutter/material.dart';

import '../app_store.dart';
import '../calculations.dart';
import '../widgets/common.dart';
import 'log_activity_screen.dart';
import 'log_weight_screen.dart';
import 'meal_log_screen.dart';
import 'strength_workout_screen.dart';
import 'workout_history_screen.dart';

class HomeScreen extends StatelessWidget {
  final AppStore store;
  const HomeScreen({super.key, required this.store});

  bool _sameDay(DateTime a, DateTime b) =>
      a.year == b.year && a.month == b.month && a.day == b.day;

  @override
  Widget build(BuildContext context) {
    final profile = store.profile!;
    final latestStrength = store.latestStrengthBest;
    final activityGoal = math.max(store.goals.weeklyActivityMin, 1);
    final strengthGoal = math.max(store.goals.weeklyStrengthSessions, 1);
    final today = DateTime.now();
    final todayWorkouts = store.workouts.where((w) => _sameDay(w.date, today)).length;
    final estimatedDailyEnergy = estimatedDailyEnergyRequirement(
      weightKg: store.currentWeightKg,
      heightCm: profile.heightCm,
      age: profile.age,
      sex: profile.sex,
      activityFactor: 1.375,
    );
    final calorieProgress = estimatedDailyEnergy <= 0
        ? 0.0
        : (store.todayMealCalories / estimatedDailyEnergy).clamp(0.0, 1.0);

    return ListView(
      padding: const EdgeInsets.fromLTRB(16, 12, 16, 110),
      children: [
        Row(
          children: [
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    'Hello, ${profile.name}',
                    style: Theme.of(context).textTheme.headlineSmall?.copyWith(
                          fontWeight: FontWeight.w900,
                          color: const Color(0xFF17312A),
                        ),
                  ),
                  const SizedBox(height: 2),
                  Text(
                    'Today • ${today.day}/${today.month}/${today.year}',
                    style: Theme.of(context).textTheme.bodySmall?.copyWith(
                          color: Theme.of(context).colorScheme.primary,
                          fontWeight: FontWeight.w700,
                        ),
                  ),
                ],
              ),
            ),
            Container(
              width: 42,
              height: 42,
              decoration: BoxDecoration(
                color: const Color(0xFFE7F5EF),
                borderRadius: BorderRadius.circular(13),
              ),
              child: Icon(
                Icons.fitness_center,
                color: Theme.of(context).colorScheme.primary,
              ),
            ),
          ],
        ),
        const SizedBox(height: 16),
        Card(
          child: Padding(
            padding: const EdgeInsets.all(16),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  "Today's progress",
                  style: Theme.of(context).textTheme.titleMedium?.copyWith(
                        fontWeight: FontWeight.w900,
                        color: const Color(0xFF17312A),
                      ),
                ),
                const SizedBox(height: 14),
                _TodayRow(
                  icon: Icons.fitness_center,
                  label: 'Workouts',
                  value: '$todayWorkouts completed',
                ),
                const SizedBox(height: 12),
                _TodayRow(
                  icon: Icons.restaurant_outlined,
                  label: 'Meals',
                  value: '${store.todayMeals.length} logged',
                ),
                const SizedBox(height: 12),
                _TodayRow(
                  icon: Icons.local_fire_department_outlined,
                  label: 'Calories',
                  value: '${store.todayMealCalories.toStringAsFixed(0)} kcal',
                  detail: 'Estimated daily energy ~${estimatedDailyEnergy.toStringAsFixed(0)} kcal',
                  progress: calorieProgress,
                ),
                const SizedBox(height: 12),
                _TodayRow(
                  icon: Icons.egg_alt_outlined,
                  label: 'Protein',
                  value: '${store.todayProteinG.toStringAsFixed(0)} g logged',
                ),
              ],
            ),
          ),
        ),
        const SectionHeader('Quick actions'),
        GridView.count(
          crossAxisCount: 2,
          shrinkWrap: true,
          physics: const NeverScrollableScrollPhysics(),
          crossAxisSpacing: 10,
          mainAxisSpacing: 10,
          childAspectRatio: 1.8,
          children: [
            _QuickAction(
              icon: Icons.fitness_center,
              label: 'Log workout',
              onTap: () => Navigator.push(
                context,
                MaterialPageRoute(builder: (_) => StrengthWorkoutScreen(store: store)),
              ),
            ),
            _QuickAction(
              icon: Icons.restaurant_outlined,
              label: 'Log meal',
              onTap: () => Navigator.push(
                context,
                MaterialPageRoute(builder: (_) => MealLogScreen(store: store)),
              ),
            ),
            _QuickAction(
              icon: Icons.monitor_weight_outlined,
              label: 'Log weight',
              onTap: () => Navigator.push(
                context,
                MaterialPageRoute(builder: (_) => LogWeightScreen(store: store)),
              ),
            ),
            _QuickAction(
              icon: Icons.history,
              label: 'Workout history',
              onTap: () => Navigator.push(
                context,
                MaterialPageRoute(builder: (_) => WorkoutHistoryScreen(store: store)),
              ),
            ),
          ],
        ),
        const SectionHeader('At a glance'),
        Row(
          children: [
            Expanded(
              child: MetricCard(
                label: 'Current weight',
                value: '${store.currentWeightKg.toStringAsFixed(1)} kg',
                subtitle: '${store.weightChangePct.toStringAsFixed(1)}% from baseline',
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
                subtitle: latestStrength?.exerciseName ?? 'No strength data yet',
                icon: Icons.fitness_center,
              ),
            ),
          ],
        ),
        const SectionHeader('This week'),
        Card(
          child: Padding(
            padding: const EdgeInsets.all(16),
            child: Column(
              children: [
                _ProgressRow(
                  label: 'Activity minutes',
                  value: '${store.weeklyActivityMinutes} / $activityGoal min',
                  progress: store.weeklyActivityMinutes / activityGoal,
                ),
                const SizedBox(height: 16),
                _ProgressRow(
                  label: 'Strength sessions',
                  value: '${store.weeklyStrengthSessions} / $strengthGoal',
                  progress: store.weeklyStrengthSessions / strengthGoal,
                ),
                const SizedBox(height: 14),
                Row(
                  children: [
                    Expanded(
                      child: _MiniStat(
                        label: 'MET-min',
                        value: store.weeklyMetMinutes.toStringAsFixed(0),
                      ),
                    ),
                    const SizedBox(width: 8),
                    Expanded(
                      child: _MiniStat(
                        label: 'Exercise energy',
                        value: '${store.weeklyCalories.toStringAsFixed(0)} kcal',
                      ),
                    ),
                  ],
                ),
              ],
            ),
          ),
        ),
        const SectionHeader('More logging'),
        Card(
          child: ListTile(
            leading: _IconTile(icon: Icons.directions_run),
            title: const Text('Log physical activity'),
            subtitle: const Text('Track duration, MET-minutes and energy'),
            trailing: const Icon(Icons.chevron_right),
            onTap: () => Navigator.push(
              context,
              MaterialPageRoute(builder: (_) => LogActivityScreen(store: store)),
            ),
          ),
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
                      Text(
                        store.medications.first.medicationName,
                        style: Theme.of(context).textTheme.titleMedium?.copyWith(
                              fontWeight: FontWeight.w800,
                            ),
                      ),
                      const SizedBox(height: 3),
                      Text(
                        '${store.medications.first.medicationClass} • ${store.medications.first.dose}',
                      ),
                      const SizedBox(height: 3),
                      Text(
                        'Recorded ${shortDate(store.medications.first.date)}',
                        style: Theme.of(context).textTheme.bodySmall,
                      ),
                    ],
                  ),
          ),
        ),
        const SizedBox(height: 16),
        const MonitoringNotice(),
      ],
    );
  }
}

class _TodayRow extends StatelessWidget {
  final IconData icon;
  final String label;
  final String value;
  final String? detail;
  final double? progress;

  const _TodayRow({
    required this.icon,
    required this.label,
    required this.value,
    this.detail,
    this.progress,
  });

  @override
  Widget build(BuildContext context) {
    return Row(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        _IconTile(icon: icon),
        const SizedBox(width: 11),
        Expanded(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Row(
                children: [
                  Expanded(
                    child: Text(
                      label,
                      style: const TextStyle(fontWeight: FontWeight.w700),
                    ),
                  ),
                  Text(
                    value,
                    style: TextStyle(
                      fontWeight: FontWeight.w800,
                      color: Theme.of(context).colorScheme.primary,
                    ),
                  ),
                ],
              ),
              if (detail != null) ...[
                const SizedBox(height: 3),
                Text(
                  detail!,
                  style: Theme.of(context).textTheme.bodySmall?.copyWith(
                        color: const Color(0xFF687871),
                      ),
                ),
              ],
              if (progress != null) ...[
                const SizedBox(height: 7),
                ClipRRect(
                  borderRadius: BorderRadius.circular(20),
                  child: LinearProgressIndicator(
                    minHeight: 6,
                    value: progress!.clamp(0.0, 1.0),
                    backgroundColor: const Color(0xFFEAF0ED),
                  ),
                ),
              ],
            ],
          ),
        ),
      ],
    );
  }
}

class _QuickAction extends StatelessWidget {
  final IconData icon;
  final String label;
  final VoidCallback onTap;

  const _QuickAction({required this.icon, required this.label, required this.onTap});

  @override
  Widget build(BuildContext context) {
    return Card(
      child: InkWell(
        borderRadius: BorderRadius.circular(18),
        onTap: onTap,
        child: Padding(
          padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 12),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Icon(icon, color: Theme.of(context).colorScheme.primary, size: 24),
              const SizedBox(height: 7),
              Text(
                label,
                textAlign: TextAlign.center,
                style: const TextStyle(fontWeight: FontWeight.w700),
              ),
            ],
          ),
        ),
      ),
    );
  }
}

class _IconTile extends StatelessWidget {
  final IconData icon;
  const _IconTile({required this.icon});

  @override
  Widget build(BuildContext context) {
    return Container(
      width: 34,
      height: 34,
      decoration: BoxDecoration(
        color: const Color(0xFFE6F5EF),
        borderRadius: BorderRadius.circular(10),
      ),
      child: Icon(icon, size: 19, color: Theme.of(context).colorScheme.primary),
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
        Row(
          children: [
            Expanded(child: Text(label, style: const TextStyle(fontWeight: FontWeight.w700))),
            Text(value),
          ],
        ),
        const SizedBox(height: 7),
        ClipRRect(
          borderRadius: BorderRadius.circular(20),
          child: LinearProgressIndicator(
            minHeight: 7,
            value: progress.clamp(0, 1).toDouble(),
            backgroundColor: const Color(0xFFEAF0ED),
          ),
        ),
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
        color: const Color(0xFFF0F7F4),
        borderRadius: BorderRadius.circular(14),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            value,
            style: Theme.of(context).textTheme.titleMedium?.copyWith(
                  fontWeight: FontWeight.w900,
                  color: const Color(0xFF17312A),
                ),
          ),
          Text(label, style: Theme.of(context).textTheme.bodySmall),
        ],
      ),
    );
  }
}
