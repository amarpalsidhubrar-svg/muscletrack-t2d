import 'dart:math' as math;

import 'package:flutter/material.dart';

import '../app_store.dart';
import '../calculations.dart';
import '../models.dart';
import '../widgets/treadmill_avatar.dart';
import 'log_weight_screen.dart';
import 'meal_log_screen.dart';
import 'progress_screen.dart';
import 'strength_workout_screen.dart';
import 'workout_history_screen.dart';

class HomeScreen extends StatelessWidget {
  final AppStore store;
  const HomeScreen({super.key, required this.store});

  bool _sameDay(DateTime a, DateTime b) =>
      a.year == b.year && a.month == b.month && a.day == b.day;

  String _greeting() {
    final hour = DateTime.now().hour;
    if (hour < 12) return 'Good morning';
    if (hour < 17) return 'Good afternoon';
    return 'Good evening';
  }

  String _weekday(DateTime value) {
    const names = [
      'Monday',
      'Tuesday',
      'Wednesday',
      'Thursday',
      'Friday',
      'Saturday',
      'Sunday',
    ];
    return names[value.weekday - 1];
  }

  WorkoutSession? get _latestWorkout =>
      store.workouts.isEmpty ? null : store.workouts.first;

  @override
  Widget build(BuildContext context) {
    final profile = store.profile!;
    final today = DateTime.now();
    final todayWorkouts =
        store.workouts.where((w) => _sameDay(w.date, today)).length;
    final todayActivity = store.workouts
        .where((w) => _sameDay(w.date, today))
        .fold<int>(0, (sum, w) => sum + w.durationMin);
    final dailyEnergy = estimatedDailyEnergyRequirement(
      weightKg: store.currentWeightKg,
      heightCm: profile.heightCm,
      age: profile.age,
      sex: profile.sex,
      activityFactor: 1.375,
    );
    final latest = _latestWorkout;

    return ListView(
      padding: const EdgeInsets.fromLTRB(14, 12, 14, 110),
      children: [
        _BrandHeader(initials: _initials(profile.name)),
        const SizedBox(height: 12),
        _HeroCard(
          greeting: '${_greeting()},',
          name: profile.name,
          date:
              '${_weekday(today)}, ${today.day} ${_month(today.month)} ${today.year}',
        ),
        const SizedBox(height: 12),
        _SummaryCard(
          calories: store.todayMealCalories,
          calorieGoal: dailyEnergy,
          workouts: todayWorkouts,
          meals: store.todayMeals.length,
          activityMinutes: todayActivity,
        ),
        const SizedBox(height: 12),
        Row(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Expanded(
              flex: 6,
              child: _ProgressPreview(store: store),
            ),
            const SizedBox(width: 10),
            Expanded(
              flex: 5,
              child: _ReadinessCard(workout: latest),
            ),
          ],
        ),
        const SizedBox(height: 12),
        _QuickActions(
          onWorkout: () => Navigator.push(
            context,
            MaterialPageRoute(
              builder: (_) => StrengthWorkoutScreen(store: store),
            ),
          ),
          onMeal: () => Navigator.push(
            context,
            MaterialPageRoute(builder: (_) => MealLogScreen(store: store)),
          ),
          onWeight: () => Navigator.push(
            context,
            MaterialPageRoute(builder: (_) => LogWeightScreen(store: store)),
          ),
          onProgress: () => Navigator.push(
            context,
            MaterialPageRoute(
              builder: (_) => Scaffold(
                appBar: AppBar(title: const Text('Progress')),
                body: ProgressScreen(store: store),
              ),
            ),
          ),
        ),
        const SizedBox(height: 12),
        Row(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Expanded(
              child: _RecentWorkoutCard(
                workout: latest,
                onTap: latest == null
                    ? () => Navigator.push(
                          context,
                          MaterialPageRoute(
                            builder: (_) => StrengthWorkoutScreen(store: store),
                          ),
                        )
                    : () => Navigator.push(
                          context,
                          MaterialPageRoute(
                            builder: (_) => StrengthWorkoutScreen(
                              store: store,
                              existing: latest,
                            ),
                          ),
                        ),
              ),
            ),
            const SizedBox(width: 10),
            Expanded(
              child: _RecentMealCard(
                meal: store.meals.isEmpty ? null : store.meals.first,
                onTap: () => Navigator.push(
                  context,
                  MaterialPageRoute(builder: (_) => MealLogScreen(store: store)),
                ),
              ),
            ),
          ],
        ),
        const SizedBox(height: 12),
        InkWell(
          borderRadius: BorderRadius.circular(18),
          onTap: () => Navigator.push(
            context,
            MaterialPageRoute(
              builder: (_) => WorkoutHistoryScreen(store: store),
            ),
          ),
          child: Container(
            padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 13),
            decoration: BoxDecoration(
              color: Colors.white,
              borderRadius: BorderRadius.circular(18),
              border: Border.all(color: const Color(0xFFE5EBE8)),
            ),
            child: Row(
              children: [
                Icon(
                  Icons.history_rounded,
                  color: Theme.of(context).colorScheme.primary,
                ),
                const SizedBox(width: 10),
                const Expanded(
                  child: Text(
                    'Workout history & editing',
                    style: TextStyle(fontWeight: FontWeight.w800),
                  ),
                ),
                const Icon(Icons.chevron_right_rounded),
              ],
            ),
          ),
        ),
      ],
    );
  }

  String _initials(String name) {
    final parts = name.trim().split(RegExp(r'\s+'));
    if (parts.isEmpty || parts.first.isEmpty) return 'MT';
    if (parts.length == 1) {
      return parts.first.substring(0, math.min(2, parts.first.length)).toUpperCase();
    }
    return '${parts.first[0]}${parts.last[0]}'.toUpperCase();
  }

  String _month(int month) {
    const values = [
      'January',
      'February',
      'March',
      'April',
      'May',
      'June',
      'July',
      'August',
      'September',
      'October',
      'November',
      'December'
    ];
    return values[month - 1];
  }
}

class _BrandHeader extends StatelessWidget {
  final String initials;
  const _BrandHeader({required this.initials});

  @override
  Widget build(BuildContext context) {
    return Row(
      children: [
        Expanded(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                'MuscleTrack T2D',
                style: Theme.of(context).textTheme.headlineSmall?.copyWith(
                      fontWeight: FontWeight.w900,
                      color: const Color(0xFF092C2B),
                      letterSpacing: -0.5,
                    ),
              ),
              Text(
                'Strength. Health. A Stronger You.',
                style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                      color: const Color(0xFF087B55),
                      fontWeight: FontWeight.w600,
                    ),
              ),
            ],
          ),
        ),
        IconButton(
          tooltip: 'Notifications',
          onPressed: () => ScaffoldMessenger.of(context).showSnackBar(
            const SnackBar(content: Text('No new notifications.')),
          ),
          icon: const Icon(Icons.notifications_none_rounded),
        ),
        CircleAvatar(
          radius: 20,
          backgroundColor: const Color(0xFF087B55),
          child: Text(
            initials,
            style: const TextStyle(
              color: Colors.white,
              fontWeight: FontWeight.w800,
            ),
          ),
        ),
      ],
    );
  }
}

class _HeroCard extends StatelessWidget {
  final String greeting;
  final String name;
  final String date;

  const _HeroCard({
    required this.greeting,
    required this.name,
    required this.date,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      height: 178,
      clipBehavior: Clip.antiAlias,
      decoration: BoxDecoration(
        borderRadius: BorderRadius.circular(22),
        gradient: const LinearGradient(
          colors: [Color(0xFFF3FBF7), Color(0xFFE5F7EE)],
          begin: Alignment.topLeft,
          end: Alignment.bottomRight,
        ),
        border: Border.all(color: const Color(0xFFDCEFE6)),
      ),
      child: Stack(
        children: [
          const Positioned(
            right: -6,
            bottom: -10,
            child: TreadmillAvatar(width: 185, height: 165),
          ),
          Positioned.fill(
            child: Padding(
              padding: const EdgeInsets.fromLTRB(18, 15, 155, 14),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    date,
                    style: Theme.of(context).textTheme.bodySmall?.copyWith(
                          color: const Color(0xFF53665E),
                          fontWeight: FontWeight.w600,
                        ),
                  ),
                  const SizedBox(height: 12),
                  Text(
                    greeting,
                    style: Theme.of(context).textTheme.headlineSmall?.copyWith(
                          fontWeight: FontWeight.w900,
                          color: const Color(0xFF092C2B),
                          height: 1,
                        ),
                  ),
                  const SizedBox(height: 3),
                  Text(
                    '$name 👋',
                    maxLines: 1,
                    overflow: TextOverflow.ellipsis,
                    style: Theme.of(context).textTheme.headlineMedium?.copyWith(
                          fontWeight: FontWeight.w900,
                          color: const Color(0xFF092C2B),
                          height: 1.05,
                        ),
                  ),
                  const SizedBox(height: 10),
                  Text(
                    'Keep going!',
                    style: Theme.of(context).textTheme.titleLarge?.copyWith(
                          color: const Color(0xFF0B8C5E),
                          fontWeight: FontWeight.w900,
                        ),
                  ),
                  const SizedBox(height: 2),
                  Text(
                    'Small steps today,\nstronger tomorrow.',
                    style: Theme.of(context).textTheme.bodySmall?.copyWith(
                          color: const Color(0xFF314B43),
                          height: 1.25,
                        ),
                  ),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }
}

class _SummaryCard extends StatelessWidget {
  final double calories;
  final double calorieGoal;
  final int workouts;
  final int meals;
  final int activityMinutes;

  const _SummaryCard({
    required this.calories,
    required this.calorieGoal,
    required this.workouts,
    required this.meals,
    required this.activityMinutes,
  });

  @override
  Widget build(BuildContext context) {
    return _DashboardCard(
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              Text(
                "Today's summary",
                style: Theme.of(context).textTheme.titleMedium?.copyWith(
                      fontWeight: FontWeight.w900,
                      color: const Color(0xFF092C2B),
                    ),
              ),
              const Spacer(),
              Text(
                'See details',
                style: Theme.of(context).textTheme.bodySmall?.copyWith(
                      color: const Color(0xFF52665E),
                    ),
              ),
              const Icon(Icons.chevron_right, size: 18),
            ],
          ),
          const SizedBox(height: 14),
          Row(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Expanded(
                child: _SummaryMetric(
                  icon: Icons.local_fire_department_rounded,
                  iconColor: const Color(0xFFF59E0B),
                  iconBg: const Color(0xFFFFF0CF),
                  value: calories.toStringAsFixed(0),
                  label: 'Calories',
                  sublabel: 'of ${calorieGoal.toStringAsFixed(0)} kcal',
                  progress: calorieGoal <= 0 ? 0 : calories / calorieGoal,
                ),
              ),
              const _VSeparator(),
              Expanded(
                child: _SummaryMetric(
                  icon: Icons.fitness_center_rounded,
                  iconColor: const Color(0xFF079669),
                  iconBg: const Color(0xFFDDF7E9),
                  value: '$workouts',
                  label: 'Workout',
                  sublabel: 'today',
                  progress: workouts > 0 ? 1 : 0,
                ),
              ),
              const _VSeparator(),
              Expanded(
                child: _SummaryMetric(
                  icon: Icons.restaurant_rounded,
                  iconColor: const Color(0xFF2874D0),
                  iconBg: const Color(0xFFE0EEFF),
                  value: '$meals',
                  label: 'Meals',
                  sublabel: 'logged',
                  progress: (meals / 3).clamp(0, 1).toDouble(),
                ),
              ),
              const _VSeparator(),
              Expanded(
                child: _SummaryMetric(
                  icon: Icons.directions_run_rounded,
                  iconColor: const Color(0xFF7B55D9),
                  iconBg: const Color(0xFFEDE5FF),
                  value: '$activityMinutes',
                  label: 'Activity',
                  sublabel: 'minutes',
                  progress: (activityMinutes / 60).clamp(0, 1).toDouble(),
                ),
              ),
            ],
          ),
        ],
      ),
    );
  }
}

class _SummaryMetric extends StatelessWidget {
  final IconData icon;
  final Color iconColor;
  final Color iconBg;
  final String value;
  final String label;
  final String sublabel;
  final double progress;

  const _SummaryMetric({
    required this.icon,
    required this.iconColor,
    required this.iconBg,
    required this.value,
    required this.label,
    required this.sublabel,
    required this.progress,
  });

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        Container(
          width: 38,
          height: 38,
          decoration: BoxDecoration(
            color: iconBg,
            shape: BoxShape.circle,
          ),
          child: Icon(icon, color: iconColor, size: 21),
        ),
        const SizedBox(height: 6),
        Text(
          value,
          style: const TextStyle(
            fontSize: 20,
            fontWeight: FontWeight.w900,
            color: Color(0xFF092C2B),
          ),
        ),
        Text(
          label,
          style: const TextStyle(
            fontSize: 11,
            fontWeight: FontWeight.w800,
          ),
        ),
        Text(
          sublabel,
          textAlign: TextAlign.center,
          style: const TextStyle(
            fontSize: 9.5,
            color: Color(0xFF788981),
          ),
        ),
        const SizedBox(height: 6),
        ClipRRect(
          borderRadius: BorderRadius.circular(8),
          child: LinearProgressIndicator(
            minHeight: 5,
            value: progress.clamp(0, 1),
            backgroundColor: const Color(0xFFE8EEEB),
            valueColor: AlwaysStoppedAnimation(iconColor),
          ),
        ),
      ],
    );
  }
}

class _VSeparator extends StatelessWidget {
  const _VSeparator();

  @override
  Widget build(BuildContext context) {
    return Container(
      width: 1,
      height: 102,
      margin: const EdgeInsets.symmetric(horizontal: 6),
      color: const Color(0xFFE9EFEC),
    );
  }
}

class _ProgressPreview extends StatelessWidget {
  final AppStore store;
  const _ProgressPreview({required this.store});

  @override
  Widget build(BuildContext context) {
    final values = store.weights.take(5).toList().reversed.toList();
    return _DashboardCard(
      padding: const EdgeInsets.fromLTRB(14, 14, 14, 12),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              Text(
                'Your progress',
                style: Theme.of(context).textTheme.titleSmall?.copyWith(
                      fontWeight: FontWeight.w900,
                    ),
              ),
              const Spacer(),
              const Text(
                'Past 4 weeks',
                style: TextStyle(fontSize: 10, color: Color(0xFF6D7D76)),
              ),
            ],
          ),
          const SizedBox(height: 9),
          const Row(
            children: [
              _TabPill(label: 'Weight', selected: true),
              SizedBox(width: 5),
              _TabPill(label: 'Strength'),
              SizedBox(width: 5),
              _TabPill(label: 'Activity'),
            ],
          ),
          const SizedBox(height: 10),
          SizedBox(
            height: 78,
            child: values.length < 2
                ? const Center(
                    child: Text(
                      'Log more weights to see a trend',
                      style: TextStyle(fontSize: 10),
                    ),
                  )
                : CustomPaint(
                    painter: _MiniWeightPainter(values),
                    child: const SizedBox.expand(),
                  ),
          ),
          const SizedBox(height: 7),
          Text(
            '${store.currentWeightKg.toStringAsFixed(1)} kg',
            style: const TextStyle(
              fontSize: 22,
              fontWeight: FontWeight.w900,
              color: Color(0xFF092C2B),
            ),
          ),
          Text(
            '${store.weightChangePct <= 0 ? '↓' : '↑'} ${store.weightChangePct.abs().toStringAsFixed(1)}% from baseline',
            style: TextStyle(
              fontSize: 10.5,
              fontWeight: FontWeight.w700,
              color: store.weightChangePct <= 0
                  ? const Color(0xFF079669)
                  : const Color(0xFF6D7D76),
            ),
          ),
        ],
      ),
    );
  }
}

class _TabPill extends StatelessWidget {
  final String label;
  final bool selected;
  const _TabPill({required this.label, this.selected = false});

  @override
  Widget build(BuildContext context) {
    return Expanded(
      child: Container(
        padding: const EdgeInsets.symmetric(vertical: 6),
        decoration: BoxDecoration(
          color: selected ? const Color(0xFF087B55) : const Color(0xFFF0F3F2),
          borderRadius: BorderRadius.circular(9),
        ),
        child: Text(
          label,
          textAlign: TextAlign.center,
          style: TextStyle(
            fontSize: 9.5,
            fontWeight: FontWeight.w700,
            color: selected ? Colors.white : const Color(0xFF314B43),
          ),
        ),
      ),
    );
  }
}

class _ReadinessCard extends StatelessWidget {
  final WorkoutSession? workout;
  const _ReadinessCard({required this.workout});

  @override
  Widget build(BuildContext context) {
    final energy = workout?.readiness;
    final sleep = workout?.sleepQuality;
    final soreness = workout?.muscleSoreness;

    return _DashboardCard(
      padding: const EdgeInsets.fromLTRB(12, 14, 12, 12),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              Expanded(
                child: Text(
                  'Readiness today',
                  style: Theme.of(context).textTheme.titleSmall?.copyWith(
                        fontWeight: FontWeight.w900,
                      ),
                ),
              ),
              const Icon(
                Icons.info_outline_rounded,
                size: 17,
                color: Color(0xFF73857C),
              ),
            ],
          ),
          const SizedBox(height: 14),
          _ReadinessLine(
            icon: Icons.bolt_rounded,
            label: 'Energy',
            value: energy,
            color: const Color(0xFF08A466),
            bg: const Color(0xFFE0F7EA),
          ),
          const SizedBox(height: 13),
          _ReadinessLine(
            icon: Icons.bed_rounded,
            label: 'Sleep',
            value: sleep,
            color: const Color(0xFF378BE8),
            bg: const Color(0xFFE2F0FF),
          ),
          const SizedBox(height: 13),
          _ReadinessLine(
            icon: Icons.fitness_center_rounded,
            label: 'Soreness',
            value: soreness,
            color: const Color(0xFFF2A900),
            bg: const Color(0xFFFFF0D5),
          ),
          if (workout == null) ...[
            const SizedBox(height: 12),
            const Text(
              'Complete a pre-workout check-in to populate readiness.',
              style: TextStyle(fontSize: 9.5, color: Color(0xFF72837B)),
            ),
          ],
        ],
      ),
    );
  }
}

class _ReadinessLine extends StatelessWidget {
  final IconData icon;
  final String label;
  final int? value;
  final Color color;
  final Color bg;

  const _ReadinessLine({
    required this.icon,
    required this.label,
    required this.value,
    required this.color,
    required this.bg,
  });

  @override
  Widget build(BuildContext context) {
    final score = value ?? 0;
    return Row(
      children: [
        Container(
          width: 30,
          height: 30,
          decoration: BoxDecoration(color: bg, shape: BoxShape.circle),
          child: Icon(icon, color: color, size: 18),
        ),
        const SizedBox(width: 8),
        Expanded(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Row(
                children: [
                  Expanded(
                    child: Text(
                      label,
                      style: const TextStyle(
                        fontSize: 10.5,
                        fontWeight: FontWeight.w700,
                      ),
                    ),
                  ),
                  Text(
                    value == null ? '—' : '$score/5',
                    style: const TextStyle(fontSize: 10),
                  ),
                ],
              ),
              const SizedBox(height: 4),
              ClipRRect(
                borderRadius: BorderRadius.circular(10),
                child: LinearProgressIndicator(
                  minHeight: 6,
                  value: (score / 5).clamp(0, 1),
                  backgroundColor: const Color(0xFFEDF1EF),
                  valueColor: AlwaysStoppedAnimation(color),
                ),
              ),
            ],
          ),
        ),
      ],
    );
  }
}

class _QuickActions extends StatelessWidget {
  final VoidCallback onWorkout;
  final VoidCallback onMeal;
  final VoidCallback onWeight;
  final VoidCallback onProgress;

  const _QuickActions({
    required this.onWorkout,
    required this.onMeal,
    required this.onWeight,
    required this.onProgress,
  });

  @override
  Widget build(BuildContext context) {
    return _DashboardCard(
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            'Quick actions',
            style: Theme.of(context).textTheme.titleMedium?.copyWith(
                  fontWeight: FontWeight.w900,
                ),
          ),
          const SizedBox(height: 12),
          Row(
            children: [
              Expanded(
                child: _ActionTile(
                  icon: Icons.fitness_center_rounded,
                  label: 'Log Workout',
                  color: const Color(0xFFE1F7E9),
                  foreground: const Color(0xFF087B55),
                  onTap: onWorkout,
                ),
              ),
              const SizedBox(width: 8),
              Expanded(
                child: _ActionTile(
                  icon: Icons.restaurant_rounded,
                  label: 'Log Meal',
                  color: const Color(0xFFE5F0FF),
                  foreground: const Color(0xFF286CC5),
                  onTap: onMeal,
                ),
              ),
              const SizedBox(width: 8),
              Expanded(
                child: _ActionTile(
                  icon: Icons.monitor_weight_rounded,
                  label: 'Log Weight',
                  color: const Color(0xFFECE5FF),
                  foreground: const Color(0xFF7552C9),
                  onTap: onWeight,
                ),
              ),
              const SizedBox(width: 8),
              Expanded(
                child: _ActionTile(
                  icon: Icons.bar_chart_rounded,
                  label: 'Progress',
                  color: const Color(0xFFE0F5EA),
                  foreground: const Color(0xFF087B55),
                  onTap: onProgress,
                ),
              ),
            ],
          ),
        ],
      ),
    );
  }
}

class _ActionTile extends StatelessWidget {
  final IconData icon;
  final String label;
  final Color color;
  final Color foreground;
  final VoidCallback onTap;

  const _ActionTile({
    required this.icon,
    required this.label,
    required this.color,
    required this.foreground,
    required this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    return InkWell(
      borderRadius: BorderRadius.circular(14),
      onTap: onTap,
      child: Container(
        height: 78,
        padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 10),
        decoration: BoxDecoration(
          color: color,
          borderRadius: BorderRadius.circular(14),
        ),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(icon, color: foreground, size: 23),
            const SizedBox(height: 7),
            Text(
              label,
              maxLines: 1,
              overflow: TextOverflow.fade,
              textAlign: TextAlign.center,
              style: TextStyle(
                color: foreground,
                fontSize: 9.5,
                fontWeight: FontWeight.w800,
              ),
            ),
          ],
        ),
      ),
    );
  }
}

class _RecentWorkoutCard extends StatelessWidget {
  final WorkoutSession? workout;
  final VoidCallback onTap;
  const _RecentWorkoutCard({required this.workout, required this.onTap});

  @override
  Widget build(BuildContext context) {
    final exerciseNames =
        workout?.sets.map((s) => s.exerciseName).toSet().take(3).join(', ');

    return _DashboardCard(
      padding: const EdgeInsets.all(13),
      child: InkWell(
        onTap: onTap,
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text(
              'Recent workout',
              style: TextStyle(fontWeight: FontWeight.w900),
            ),
            const SizedBox(height: 9),
            Row(
              children: [
                Container(
                  width: 46,
                  height: 46,
                  decoration: BoxDecoration(
                    color: const Color(0xFFE2F4EA),
                    borderRadius: BorderRadius.circular(12),
                  ),
                  child: const Icon(
                    Icons.fitness_center_rounded,
                    color: Color(0xFF087B55),
                  ),
                ),
                const SizedBox(width: 9),
                Expanded(
                  child: workout == null
                      ? const Text(
                          'No workout yet.\nTap to log one.',
                          style: TextStyle(fontSize: 10.5),
                        )
                      : Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            const Text(
                              'Strength workout',
                              style: TextStyle(
                                fontWeight: FontWeight.w800,
                                fontSize: 11,
                              ),
                            ),
                            Text(
                              exerciseNames == null || exerciseNames.isEmpty
                                  ? '${workout!.durationMin} min'
                                  : exerciseNames,
                              maxLines: 2,
                              overflow: TextOverflow.ellipsis,
                              style: const TextStyle(
                                fontSize: 9.5,
                                color: Color(0xFF687A72),
                              ),
                            ),
                          ],
                        ),
                ),
                const Icon(Icons.chevron_right_rounded, size: 18),
              ],
            ),
          ],
        ),
      ),
    );
  }
}

class _RecentMealCard extends StatelessWidget {
  final MealEntry? meal;
  final VoidCallback onTap;
  const _RecentMealCard({required this.meal, required this.onTap});

  @override
  Widget build(BuildContext context) {
    return _DashboardCard(
      padding: const EdgeInsets.all(13),
      child: InkWell(
        onTap: onTap,
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text(
              'Recent meal',
              style: TextStyle(fontWeight: FontWeight.w900),
            ),
            const SizedBox(height: 9),
            Row(
              children: [
                Container(
                  width: 46,
                  height: 46,
                  decoration: BoxDecoration(
                    color: const Color(0xFFFFF1DC),
                    borderRadius: BorderRadius.circular(12),
                  ),
                  child: const Icon(
                    Icons.rice_bowl_rounded,
                    color: Color(0xFFDE8A00),
                  ),
                ),
                const SizedBox(width: 9),
                Expanded(
                  child: meal == null
                      ? const Text(
                          'No meal yet.\nTap to log one.',
                          style: TextStyle(fontSize: 10.5),
                        )
                      : Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Text(
                              meal!.description,
                              maxLines: 1,
                              overflow: TextOverflow.ellipsis,
                              style: const TextStyle(
                                fontWeight: FontWeight.w800,
                                fontSize: 11,
                              ),
                            ),
                            Text(
                              '${meal!.calories.toStringAsFixed(0)} kcal'
                              '${meal!.proteinG == null ? '' : '  •  P ${meal!.proteinG!.toStringAsFixed(0)}g'}',
                              style: const TextStyle(
                                fontSize: 9.5,
                                color: Color(0xFF687A72),
                              ),
                            ),
                          ],
                        ),
                ),
                const Icon(Icons.chevron_right_rounded, size: 18),
              ],
            ),
          ],
        ),
      ),
    );
  }
}

class _DashboardCard extends StatelessWidget {
  final Widget child;
  final EdgeInsets padding;

  const _DashboardCard({
    required this.child,
    this.padding = const EdgeInsets.all(14),
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: padding,
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(19),
        border: Border.all(color: const Color(0xFFE4EBE7)),
        boxShadow: const [
          BoxShadow(
            color: Color(0x100B3428),
            blurRadius: 14,
            offset: Offset(0, 5),
          ),
        ],
      ),
      child: child,
    );
  }
}

class _MiniWeightPainter extends CustomPainter {
  final List<WeightEntry> entries;
  _MiniWeightPainter(this.entries);

  @override
  void paint(Canvas canvas, Size size) {
    final values = entries.map((e) => e.weightKg).toList();
    var minValue = values.reduce(math.min);
    var maxValue = values.reduce(math.max);
    if ((maxValue - minValue).abs() < 0.2) {
      minValue -= 1;
      maxValue += 1;
    }

    final grid = Paint()
      ..color = const Color(0xFFE7EDEA)
      ..strokeWidth = 1;
    for (var i = 1; i < 4; i++) {
      final y = size.height * i / 4;
      canvas.drawLine(Offset(0, y), Offset(size.width, y), grid);
    }

    final path = Path();
    final fillPath = Path();
    for (var i = 0; i < values.length; i++) {
      final x = size.width * i / (values.length - 1);
      final y = size.height -
          ((values[i] - minValue) / (maxValue - minValue) * size.height * 0.82) -
          size.height * 0.08;
      if (i == 0) {
        path.moveTo(x, y);
        fillPath.moveTo(x, size.height);
        fillPath.lineTo(x, y);
      } else {
        path.lineTo(x, y);
        fillPath.lineTo(x, y);
      }
    }
    fillPath.lineTo(size.width, size.height);
    fillPath.close();

    canvas.drawPath(
      fillPath,
      Paint()
        ..shader = const LinearGradient(
          colors: [Color(0x4433B887), Color(0x0033B887)],
          begin: Alignment.topCenter,
          end: Alignment.bottomCenter,
        ).createShader(Offset.zero & size),
    );

    canvas.drawPath(
      path,
      Paint()
        ..color = const Color(0xFF087B55)
        ..strokeWidth = 2.2
        ..style = PaintingStyle.stroke
        ..strokeCap = StrokeCap.round
        ..strokeJoin = StrokeJoin.round,
    );
  }

  @override
  bool shouldRepaint(covariant _MiniWeightPainter oldDelegate) =>
      oldDelegate.entries != entries;
}
