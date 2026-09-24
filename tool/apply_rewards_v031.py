#!/usr/bin/env python3
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]

(ROOT/'lib/screens/home_screen.dart').write_text(r'''import 'dart:math' as math;
import 'package:flutter/material.dart';

import '../app_store.dart';
import '../models.dart';
import '../streaks.dart';
import '../widgets/treadmill_avatar.dart';
import 'calendar_screen.dart';
import 'rewards_screen.dart';
import 'strength_workout_screen.dart';
import 'workout_history_screen.dart';

class HomeScreen extends StatelessWidget {
  final AppStore store;
  const HomeScreen({super.key, required this.store});

  String _greeting() {
    final hour = DateTime.now().hour;
    if (hour < 12) return 'Good morning';
    if (hour < 17) return 'Good afternoon';
    return 'Good evening';
  }

  String _initials(String name) {
    final parts = name.trim().split(RegExp(r'\s+'));
    if (parts.isEmpty || parts.first.isEmpty) return 'MT';
    if (parts.length == 1) {
      return parts.first.substring(0, math.min(2, parts.first.length)).toUpperCase();
    }
    return '${parts.first[0]}${parts.last[0]}'.toUpperCase();
  }

  String _dateLabel(DateTime d) {
    const months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
    const days = ['Mon','Tue','Wed','Thu','Fri','Sat','Sun'];
    return '${days[d.weekday - 1]}, ${d.day} ${months[d.month - 1]}';
  }

  @override
  Widget build(BuildContext context) {
    final profile = store.profile!;
    final today = DateTime.now();
    final todaySessions = store.workoutsForDay(today);
    final todayWorkouts = todaySessions.where((w) => w.workoutType.toLowerCase() != 'rest day').toList();
    final isRestDay = store.hasRestDayOn(today);
    final week = store.thisWeekWorkouts.where((w) => w.workoutType.toLowerCase() != 'rest day').toList();
    final totalSets = week.fold<int>(0, (sum, w) => sum + w.sets.length);
    final latest = store.workouts.where((w) => w.workoutType.toLowerCase() != 'rest day').cast<WorkoutSession?>().firstOrNull;
    final streak = store.streakSummary;

    return ListView(
      padding: const EdgeInsets.fromLTRB(14, 12, 14, 110),
      children: [
        _Header(initials: _initials(profile.name)),
        const SizedBox(height: 12),
        _Hero(
          greeting: _greeting(),
          name: profile.name,
          date: _dateLabel(today),
          mood: streak.mood,
          streak: streak.currentStreak,
        ),
        const SizedBox(height: 12),
        _HomeLogActions(
          restDay: isRestDay,
          hasWorkout: todayWorkouts.isNotEmpty,
          onWorkout: () => Navigator.push(
            context,
            MaterialPageRoute(builder: (_) => StrengthWorkoutScreen(store: store)),
          ),
          onRest: () async {
            await store.markRestDay(today);
          },
        ),
        const SizedBox(height: 12),
        _StreakCard(
          summary: streak,
          onTap: () => Navigator.push(
            context,
            MaterialPageRoute(builder: (_) => RewardsScreen(store: store)),
          ),
        ),
        const SizedBox(height: 12),
        _TodayCard(
          workouts: todayWorkouts.length,
          minutes: todayWorkouts.fold<int>(0, (s, w) => s + w.durationMin),
          sets: todayWorkouts.fold<int>(0, (s, w) => s + w.sets.length),
          restDay: isRestDay,
          onLog: () => Navigator.push(
            context,
            MaterialPageRoute(builder: (_) => StrengthWorkoutScreen(store: store)),
          ),
          onRest: () async {
            await store.markRestDay(today);
          },
        ),
        const SizedBox(height: 12),
        Row(
          children: [
            Expanded(
              child: _StatCard(
                icon: Icons.calendar_view_week_rounded,
                value: '${week.length}',
                label: 'Workouts this week',
              ),
            ),
            const SizedBox(width: 10),
            Expanded(
              child: _StatCard(
                icon: Icons.format_list_numbered_rounded,
                value: '$totalSets',
                label: 'Sets this week',
              ),
            ),
            const SizedBox(width: 10),
            Expanded(
              child: _StatCard(
                icon: Icons.timer_outlined,
                value: '${week.fold<int>(0, (s, w) => s + w.durationMin)}',
                label: 'Minutes this week',
              ),
            ),
          ],
        ),
        const SizedBox(height: 12),
        _ActionCard(
          icon: Icons.calendar_month_rounded,
          title: 'Training calendar',
          subtitle: 'Workouts, rest days and streak history',
          onTap: () => Navigator.push(
            context,
            MaterialPageRoute(builder: (_) => CalendarScreen(store: store)),
          ),
        ),
        const SizedBox(height: 10),
        _ActionCard(
          icon: Icons.history_rounded,
          title: 'Workout history',
          subtitle: 'View and edit your previous sessions',
          onTap: () => Navigator.push(
            context,
            MaterialPageRoute(builder: (_) => WorkoutHistoryScreen(store: store)),
          ),
        ),
        const SizedBox(height: 12),
        _RecentWorkout(
          workout: latest,
          onTap: latest == null
              ? () => Navigator.push(
                    context,
                    MaterialPageRoute(builder: (_) => StrengthWorkoutScreen(store: store)),
                  )
              : () => Navigator.push(
                    context,
                    MaterialPageRoute(
                      builder: (_) => StrengthWorkoutScreen(store: store, existing: latest),
                    ),
                  ),
        ),
      ],
    );
  }
}

extension _FirstOrNull<T> on Iterable<T> {
  T? get firstOrNull => isEmpty ? null : first;
}

class _Header extends StatelessWidget {
  final String initials;
  const _Header({required this.initials});

  @override
  Widget build(BuildContext context) => Row(
    children: [
      Expanded(
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              'MuscleTrack',
              style: Theme.of(context).textTheme.headlineSmall?.copyWith(
                fontWeight: FontWeight.w900,
                color: const Color(0xFF092C2B),
                letterSpacing: -0.5,
              ),
            ),
            const Text(
              'Your training, clearly tracked.',
              style: TextStyle(
                color: Color(0xFF087B55),
                fontWeight: FontWeight.w600,
              ),
            ),
          ],
        ),
      ),
      CircleAvatar(
        radius: 20,
        backgroundColor: const Color(0xFF087B55),
        child: Text(
          initials,
          style: const TextStyle(color: Colors.white, fontWeight: FontWeight.w800),
        ),
      ),
    ],
  );
}

class _Hero extends StatelessWidget {
  final String greeting;
  final String name;
  final String date;
  final TrainingAvatarMood mood;
  final int streak;

  const _Hero({
    required this.greeting,
    required this.name,
    required this.date,
    required this.mood,
    required this.streak,
  });

  String get title => switch (mood) {
    TrainingAvatarMood.happy => streak > 0 ? 'Streak alive!' : 'Ready to train?',
    TrainingAvatarMood.recovery => 'Recovery mode',
    TrainingAvatarMood.worried => 'We missed you',
  };

  String get subtitle => switch (mood) {
    TrainingAvatarMood.happy => streak > 0
        ? 'Keep logging each day to build your next level.'
        : 'Log a workout or rest day to start your streak.',
    TrainingAvatarMood.recovery => 'Rest counts. Recover today and come back stronger.',
    TrainingAvatarMood.worried => 'Log today to get your routine moving again.',
  };

  @override
  Widget build(BuildContext context) => Container(
    height: 205,
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
        Positioned(
          right: 4,
          bottom: 4,
          child: TreadmillAvatar(
            width: 168,
            height: 180,
            mood: mood,
          ),
        ),
        Positioned.fill(
          child: Padding(
            padding: const EdgeInsets.fromLTRB(18, 15, 146, 16),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  date,
                  style: const TextStyle(
                    color: Color(0xFF53665E),
                    fontWeight: FontWeight.w600,
                  ),
                ),
                const SizedBox(height: 12),
                Text(
                  greeting,
                  style: const TextStyle(
                    fontSize: 22,
                    fontWeight: FontWeight.w900,
                    color: Color(0xFF092C2B),
                  ),
                ),
                const SizedBox(height: 3),
                Text(
                  '$name 👋',
                  maxLines: 1,
                  overflow: TextOverflow.ellipsis,
                  style: const TextStyle(
                    fontSize: 27,
                    fontWeight: FontWeight.w900,
                    color: Color(0xFF092C2B),
                  ),
                ),
                const SizedBox(height: 10),
                Text(
                  title,
                  style: const TextStyle(
                    fontSize: 18,
                    color: Color(0xFF0B8C5E),
                    fontWeight: FontWeight.w900,
                  ),
                ),
                const SizedBox(height: 3),
                Text(
                  subtitle,
                  style: const TextStyle(
                    fontSize: 11,
                    color: Color(0xFF314B43),
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

class _HomeLogActions extends StatelessWidget {
  final bool restDay;
  final bool hasWorkout;
  final VoidCallback onWorkout;
  final VoidCallback onRest;

  const _HomeLogActions({
    required this.restDay,
    required this.hasWorkout,
    required this.onWorkout,
    required this.onRest,
  });

  @override
  Widget build(BuildContext context) {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(14),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text(
              "Log today",
              style: TextStyle(fontSize: 16, fontWeight: FontWeight.w900),
            ),
            const SizedBox(height: 4),
            const Text(
              "Choose a workout or an intentional rest day.",
              style: TextStyle(fontSize: 11, color: Color(0xFF65766F)),
            ),
            const SizedBox(height: 12),
            Row(
              children: [
                Expanded(
                  child: FilledButton.icon(
                    onPressed: restDay ? null : onWorkout,
                    icon: const Icon(Icons.fitness_center_rounded, size: 19),
                    label: Text(hasWorkout ? "Log another workout" : "Log workout"),
                  ),
                ),
                const SizedBox(width: 9),
                Expanded(
                  child: OutlinedButton.icon(
                    onPressed: (restDay || hasWorkout) ? null : onRest,
                    icon: const Icon(Icons.self_improvement_rounded, size: 19),
                    label: Text(restDay ? "Rest day logged" : "Rest day"),
                  ),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }
}

class _StreakCard extends StatelessWidget {
  final StreakSummary summary;
  final VoidCallback onTap;
  const _StreakCard({required this.summary, required this.onTap});

  @override
  Widget build(BuildContext context) {
    final hasLevel = summary.level > 0;
    final nextText = summary.daysToNextLevel == 0
        ? 'Top level reached'
        : summary.currentStreak == 0
            ? 'Log today to begin'
            : '${summary.daysToNextLevel} day${summary.daysToNextLevel == 1 ? '' : 's'} to next level';

    return Card(
      child: InkWell(
        borderRadius: BorderRadius.circular(16),
        onTap: onTap,
        child: Padding(
          padding: const EdgeInsets.all(16),
          child: Column(
            children: [
              Row(
                children: [
                  Container(
                    width: 54,
                    height: 54,
                    decoration: BoxDecoration(
                      color: const Color(0xFFFFF2CC),
                      borderRadius: BorderRadius.circular(16),
                    ),
                    child: const Icon(
                      Icons.emoji_events_rounded,
                      color: Color(0xFFD69700),
                      size: 34,
                    ),
                  ),
                  const SizedBox(width: 13),
                  Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          hasLevel
                              ? 'Level ${summary.level} • ${summary.levelName}'
                              : summary.levelName,
                          style: const TextStyle(
                            fontSize: 16,
                            fontWeight: FontWeight.w900,
                            color: Color(0xFF087B55),
                          ),
                        ),
                        const SizedBox(height: 2),
                        Text(
                          '${summary.currentStreak} day streak 🔥',
                          style: const TextStyle(
                            fontSize: 24,
                            fontWeight: FontWeight.w900,
                            color: Color(0xFF092C2B),
                          ),
                        ),
                      ],
                    ),
                  ),
                  const Icon(Icons.chevron_right_rounded),
                ],
              ),
              const SizedBox(height: 13),
              ClipRRect(
                borderRadius: BorderRadius.circular(12),
                child: LinearProgressIndicator(
                  minHeight: 9,
                  value: summary.levelProgress,
                  backgroundColor: const Color(0xFFE8EEEB),
                  color: const Color(0xFF14A06F),
                ),
              ),
              const SizedBox(height: 7),
              Align(
                alignment: Alignment.centerRight,
                child: Text(
                  nextText,
                  style: const TextStyle(
                    fontSize: 11,
                    color: Color(0xFF5C6E67),
                    fontWeight: FontWeight.w700,
                  ),
                ),
              ),
              const SizedBox(height: 12),
              Row(
                children: [
                  Expanded(
                    child: _MiniMetric(
                      icon: Icons.local_fire_department_rounded,
                      value: '${summary.currentStreak}',
                      label: 'Current streak',
                    ),
                  ),
                  Expanded(
                    child: _MiniMetric(
                      icon: Icons.workspace_premium_rounded,
                      value: '${summary.longestStreak}',
                      label: 'Longest streak',
                    ),
                  ),
                  Expanded(
                    child: _MiniMetric(
                      icon: Icons.flag_rounded,
                      value: summary.daysToNextLevel == 0
                          ? '✓'
                          : '${summary.daysToNextLevel}',
                      label: 'Days to level',
                    ),
                  ),
                ],
              ),
            ],
          ),
        ),
      ),
    );
  }
}

class _MiniMetric extends StatelessWidget {
  final IconData icon;
  final String value;
  final String label;
  const _MiniMetric({required this.icon, required this.value, required this.label});

  @override
  Widget build(BuildContext context) => Column(
    children: [
      Icon(icon, size: 19, color: const Color(0xFF087B55)),
      const SizedBox(height: 4),
      Text(value, style: const TextStyle(fontSize: 17, fontWeight: FontWeight.w900)),
      Text(
        label,
        textAlign: TextAlign.center,
        style: const TextStyle(fontSize: 9.5, color: Color(0xFF6D7D76)),
      ),
    ],
  );
}

class _TodayCard extends StatelessWidget {
  final int workouts;
  final int minutes;
  final int sets;
  final bool restDay;
  final VoidCallback onLog;
  final VoidCallback onRest;

  const _TodayCard({
    required this.workouts,
    required this.minutes,
    required this.sets,
    required this.restDay,
    required this.onLog,
    required this.onRest,
  });

  @override
  Widget build(BuildContext context) => Card(
    child: Padding(
      padding: const EdgeInsets.all(16),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Text(
            "Today's log",
            style: TextStyle(fontSize: 16, fontWeight: FontWeight.w900),
          ),
          const SizedBox(height: 12),
          if (restDay)
            Container(
              padding: const EdgeInsets.all(12),
              decoration: BoxDecoration(
                color: const Color(0xFFE8F2FF),
                borderRadius: BorderRadius.circular(14),
              ),
              child: const Row(
                children: [
                  Icon(Icons.self_improvement_rounded, color: Color(0xFF397ACB)),
                  SizedBox(width: 9),
                  Expanded(
                    child: Text(
                      'Rest day logged — recovery keeps your streak alive.',
                      style: TextStyle(fontWeight: FontWeight.w800),
                    ),
                  ),
                ],
              ),
            )
          else if (workouts > 0)
            Container(
              padding: const EdgeInsets.all(12),
              decoration: BoxDecoration(
                color: const Color(0xFFE2F5EB),
                borderRadius: BorderRadius.circular(14),
              ),
              child: const Row(
                children: [
                  Icon(Icons.check_circle_rounded, color: Color(0xFF087B55)),
                  SizedBox(width: 9),
                  Expanded(
                    child: Text(
                      'Workout logged — today counts toward your streak.',
                      style: TextStyle(fontWeight: FontWeight.w800),
                    ),
                  ),
                ],
              ),
            )
          else
            Row(
              children: [
                Expanded(
                  child: FilledButton.icon(
                    onPressed: onLog,
                    icon: const Icon(Icons.fitness_center_rounded, size: 18),
                    label: const Text('Log workout'),
                  ),
                ),
                const SizedBox(width: 8),
                Expanded(
                  child: OutlinedButton.icon(
                    onPressed: onRest,
                    icon: const Icon(Icons.self_improvement_rounded, size: 18),
                    label: const Text('Rest day'),
                  ),
                ),
              ],
            ),
          const SizedBox(height: 14),
          Row(
            children: [
              Expanded(child: _Metric(value: '$workouts', label: 'Workouts')),
              Expanded(child: _Metric(value: '$sets', label: 'Sets')),
              Expanded(child: _Metric(value: '$minutes', label: 'Minutes')),
            ],
          ),
        ],
      ),
    ),
  );
}

class _Metric extends StatelessWidget {
  final String value;
  final String label;
  const _Metric({required this.value, required this.label});

  @override
  Widget build(BuildContext context) => Column(
    children: [
      Text(
        value,
        style: const TextStyle(
          fontSize: 22,
          fontWeight: FontWeight.w900,
          color: Color(0xFF092C2B),
        ),
      ),
      const SizedBox(height: 2),
      Text(
        label,
        style: const TextStyle(
          fontSize: 11,
          color: Color(0xFF6D7D76),
          fontWeight: FontWeight.w700,
        ),
      ),
    ],
  );
}

class _StatCard extends StatelessWidget {
  final IconData icon;
  final String value;
  final String label;
  const _StatCard({required this.icon, required this.value, required this.label});

  @override
  Widget build(BuildContext context) => Card(
    child: Padding(
      padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 14),
      child: Column(
        children: [
          Icon(icon, color: const Color(0xFF087B55), size: 21),
          const SizedBox(height: 8),
          Text(value, style: const TextStyle(fontSize: 19, fontWeight: FontWeight.w900)),
          const SizedBox(height: 2),
          Text(
            label,
            textAlign: TextAlign.center,
            style: const TextStyle(fontSize: 9.5, color: Color(0xFF6D7D76)),
          ),
        ],
      ),
    ),
  );
}

class _ActionCard extends StatelessWidget {
  final IconData icon;
  final String title;
  final String subtitle;
  final VoidCallback onTap;
  const _ActionCard({
    required this.icon,
    required this.title,
    required this.subtitle,
    required this.onTap,
  });

  @override
  Widget build(BuildContext context) => Card(
    child: ListTile(
      onTap: onTap,
      leading: CircleAvatar(
        backgroundColor: const Color(0xFFE2F5EB),
        child: Icon(icon, color: const Color(0xFF087B55)),
      ),
      title: Text(title, style: const TextStyle(fontWeight: FontWeight.w900)),
      subtitle: Text(subtitle),
      trailing: const Icon(Icons.chevron_right_rounded),
    ),
  );
}

class _RecentWorkout extends StatelessWidget {
  final WorkoutSession? workout;
  final VoidCallback onTap;
  const _RecentWorkout({required this.workout, required this.onTap});

  @override
  Widget build(BuildContext context) {
    return Card(
      child: ListTile(
        onTap: onTap,
        leading: const CircleAvatar(
          backgroundColor: Color(0xFFE2F5EB),
          child: Icon(Icons.fitness_center_rounded, color: Color(0xFF087B55)),
        ),
        title: Text(
          workout == null ? 'No workout logged yet' : 'Most recent workout',
          style: const TextStyle(fontWeight: FontWeight.w900),
        ),
        subtitle: Text(
          workout == null
              ? 'Tap to log your first session'
              : '${workout!.workoutType} • ${workout!.durationMin} min • ${workout!.sets.length} sets',
        ),
        trailing: Icon(workout == null ? Icons.add_rounded : Icons.edit_outlined),
      ),
    );
  }
}
''')

(ROOT/'lib/screens/calendar_screen.dart').write_text(r'''import 'package:flutter/material.dart';

import '../app_store.dart';
import '../models.dart';
import '../streaks.dart';
import 'strength_workout_screen.dart';

class CalendarScreen extends StatefulWidget {
  final AppStore store;
  const CalendarScreen({super.key, required this.store});

  @override
  State<CalendarScreen> createState() => _CalendarScreenState();
}

class _CalendarScreenState extends State<CalendarScreen> {
  late DateTime _month;
  late DateTime _selected;

  @override
  void initState() {
    super.initState();
    final now = DateTime.now();
    _month = DateTime(now.year, now.month);
    _selected = dayOnly(now);
  }

  bool _sameDay(DateTime a, DateTime b) => dayOnly(a) == dayOnly(b);

  @override
  Widget build(BuildContext context) {
    final first = DateTime(_month.year, _month.month, 1);
    final daysInMonth = DateTime(_month.year, _month.month + 1, 0).day;
    final leading = first.weekday - 1;
    final sessions = widget.store.workoutsForDay(_selected);
    final kind = widget.store.logKindFor(_selected);
    final today = dayOnly(DateTime.now());
    final canLog = !_selected.isAfter(today);

    return Scaffold(
      backgroundColor: const Color(0xFFF7FAF8),
      appBar: AppBar(title: const Text('Training calendar')),
      body: ListView(
        padding: const EdgeInsets.all(14),
        children: [
          Card(
            child: Padding(
              padding: const EdgeInsets.all(14),
              child: Column(
                children: [
                  Row(
                    children: [
                      IconButton(
                        onPressed: () => setState(() {
                          _month = DateTime(_month.year, _month.month - 1);
                          _selected = DateTime(_month.year, _month.month, 1);
                        }),
                        icon: const Icon(Icons.chevron_left_rounded),
                      ),
                      Expanded(
                        child: Text(
                          _monthLabel(_month),
                          textAlign: TextAlign.center,
                          style: const TextStyle(fontSize: 18, fontWeight: FontWeight.w900),
                        ),
                      ),
                      IconButton(
                        onPressed: () => setState(() {
                          _month = DateTime(_month.year, _month.month + 1);
                          _selected = DateTime(_month.year, _month.month, 1);
                        }),
                        icon: const Icon(Icons.chevron_right_rounded),
                      ),
                    ],
                  ),
                  const SizedBox(height: 8),
                  const Row(
                    children: [
                      _Dow('M'), _Dow('T'), _Dow('W'), _Dow('T'), _Dow('F'), _Dow('S'), _Dow('S'),
                    ],
                  ),
                  const SizedBox(height: 6),
                  GridView.builder(
                    shrinkWrap: true,
                    physics: const NeverScrollableScrollPhysics(),
                    itemCount: leading + daysInMonth,
                    gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
                      crossAxisCount: 7,
                      mainAxisSpacing: 5,
                      crossAxisSpacing: 5,
                    ),
                    itemBuilder: (_, index) {
                      if (index < leading) return const SizedBox.shrink();
                      final day = index - leading + 1;
                      final date = DateTime(_month.year, _month.month, day);
                      final dayKind = widget.store.logKindFor(date);
                      final selected = _sameDay(date, _selected);
                      final isWorkout = dayKind == DailyLogKind.workout;
                      final isRest = dayKind == DailyLogKind.rest;

                      final fill = selected
                          ? const Color(0xFF17312A)
                          : isWorkout
                              ? const Color(0xFFDDF4E8)
                              : isRest
                                  ? const Color(0xFFE4EEFF)
                                  : Colors.transparent;
                      final border = selected
                          ? const Color(0xFF17312A)
                          : isWorkout
                              ? const Color(0xFF79C6A4)
                              : isRest
                                  ? const Color(0xFF87AEE1)
                                  : const Color(0xFFE7ECE9);

                      return InkWell(
                        borderRadius: BorderRadius.circular(12),
                        onTap: () => setState(() => _selected = date),
                        child: Container(
                          decoration: BoxDecoration(
                            color: fill,
                            borderRadius: BorderRadius.circular(12),
                            border: Border.all(color: border),
                          ),
                          child: Stack(
                            alignment: Alignment.center,
                            children: [
                              Text(
                                '$day',
                                style: TextStyle(
                                  fontWeight: FontWeight.w800,
                                  color: selected ? Colors.white : const Color(0xFF17312A),
                                ),
                              ),
                              if (isWorkout || isRest)
                                Positioned(
                                  bottom: 3,
                                  child: Icon(
                                    isWorkout
                                        ? Icons.fitness_center_rounded
                                        : Icons.self_improvement_rounded,
                                    size: 9,
                                    color: selected
                                        ? Colors.white
                                        : isWorkout
                                            ? const Color(0xFF087B55)
                                            : const Color(0xFF397ACB),
                                  ),
                                ),
                            ],
                          ),
                        ),
                      );
                    },
                  ),
                  const SizedBox(height: 12),
                  const Row(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      _LegendDot(color: Color(0xFF79C6A4), label: 'Workout'),
                      SizedBox(width: 14),
                      _LegendDot(color: Color(0xFF87AEE1), label: 'Rest day'),
                    ],
                  ),
                ],
              ),
            ),
          ),
          const SizedBox(height: 14),
          Text(
            _dayLabel(_selected),
            style: const TextStyle(fontSize: 16, fontWeight: FontWeight.w900),
          ),
          const SizedBox(height: 8),
          if (kind == DailyLogKind.rest)
            Card(
              child: ListTile(
                leading: const CircleAvatar(
                  backgroundColor: Color(0xFFE4EEFF),
                  child: Icon(Icons.self_improvement_rounded, color: Color(0xFF397ACB)),
                ),
                title: const Text('Rest day', style: TextStyle(fontWeight: FontWeight.w900)),
                subtitle: const Text('Recovery day — this counts toward your streak.'),
                trailing: canLog
                    ? IconButton(
                        tooltip: 'Remove rest day',
                        icon: const Icon(Icons.delete_outline_rounded),
                        onPressed: () async {
                          await widget.store.removeRestDay(_selected);
                          if (mounted) setState(() {});
                        },
                      )
                    : null,
              ),
            )
          else if (sessions.isNotEmpty)
            ...sessions
                .where((w) => w.workoutType.toLowerCase() != 'rest day')
                .map(
                  (w) => Card(
                    child: ListTile(
                      onTap: () => Navigator.push(
                        context,
                        MaterialPageRoute(
                          builder: (_) => StrengthWorkoutScreen(
                            store: widget.store,
                            existing: w,
                          ),
                        ),
                      ),
                      leading: const CircleAvatar(
                        backgroundColor: Color(0xFFDDF4E8),
                        child: Icon(Icons.fitness_center_rounded, color: Color(0xFF087B55)),
                      ),
                      title: Text(w.workoutType, style: const TextStyle(fontWeight: FontWeight.w900)),
                      subtitle: Text('${w.durationMin} min • ${w.sets.length} sets'),
                      trailing: const Icon(Icons.chevron_right_rounded),
                    ),
                  ),
                )
          else
            Card(
              child: Padding(
                padding: const EdgeInsets.all(16),
                child: Column(
                  children: [
                    const Row(
                      children: [
                        Icon(Icons.event_available_outlined, color: Color(0xFF087B55)),
                        SizedBox(width: 10),
                        Expanded(child: Text('No entry logged for this day.')),
                      ],
                    ),
                    if (canLog) ...[
                      const SizedBox(height: 12),
                      Row(
                        children: [
                          Expanded(
                            child: FilledButton.icon(
                              onPressed: () => Navigator.push(
                                context,
                                MaterialPageRoute(
                                  builder: (_) => StrengthWorkoutScreen(store: widget.store),
                                ),
                              ),
                              icon: const Icon(Icons.fitness_center_rounded, size: 18),
                              label: const Text('Log workout'),
                            ),
                          ),
                          const SizedBox(width: 8),
                          Expanded(
                            child: OutlinedButton.icon(
                              onPressed: () async {
                                await widget.store.markRestDay(_selected);
                                if (mounted) setState(() {});
                              },
                              icon: const Icon(Icons.self_improvement_rounded, size: 18),
                              label: const Text('Rest day'),
                            ),
                          ),
                        ],
                      ),
                    ],
                  ],
                ),
              ),
            ),
        ],
      ),
    );
  }

  String _monthLabel(DateTime d) {
    const m = ['January','February','March','April','May','June','July','August','September','October','November','December'];
    return '${m[d.month - 1]} ${d.year}';
  }

  String _dayLabel(DateTime d) {
    const m = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
    return '${d.day} ${m[d.month - 1]} ${d.year}';
  }
}

class _Dow extends StatelessWidget {
  final String label;
  const _Dow(this.label);
  @override
  Widget build(BuildContext context) => Expanded(
    child: Text(
      label,
      textAlign: TextAlign.center,
      style: const TextStyle(
        fontSize: 11,
        fontWeight: FontWeight.w800,
        color: Color(0xFF6D7D76),
      ),
    ),
  );
}

class _LegendDot extends StatelessWidget {
  final Color color;
  final String label;
  const _LegendDot({required this.color, required this.label});

  @override
  Widget build(BuildContext context) => Row(
    children: [
      Container(
        width: 9,
        height: 9,
        decoration: BoxDecoration(color: color, shape: BoxShape.circle),
      ),
      const SizedBox(width: 5),
      Text(label, style: const TextStyle(fontSize: 10.5, color: Color(0xFF60716A))),
    ],
  );
}
''')

(ROOT/'lib/screens/rewards_screen.dart').write_text(r'''import 'package:flutter/material.dart';

import '../app_store.dart';

class RewardsScreen extends StatelessWidget {
  final AppStore store;
  const RewardsScreen({super.key, required this.store});

  static const levels = <(int, String, String)>[
    (1, 'Novice', 'Days 1–30'),
    (2, 'Noob Gainer', 'Days 31–90'),
    (3, 'Intermediate Bronze', 'Days 91–150'),
    (4, 'Intermediate Silver', 'Days 151–210'),
    (5, 'Intermediate Gold', 'Days 211–270'),
    (6, 'Advanced', 'Days 271–330'),
    (7, 'Athlete', 'Days 331–365+'),
  ];

  @override
  Widget build(BuildContext context) {
    final current = store.streakSummary;

    return Scaffold(
      appBar: AppBar(title: const Text('Streak rewards')),
      backgroundColor: const Color(0xFFF7FAF8),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          Card(
            child: Padding(
              padding: const EdgeInsets.all(18),
              child: Row(
                children: [
                  const Icon(
                    Icons.emoji_events_rounded,
                    size: 52,
                    color: Color(0xFFD69700),
                  ),
                  const SizedBox(width: 14),
                  Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          current.level > 0
                              ? 'Level ${current.level} • ${current.levelName}'
                              : 'Start your streak',
                          style: const TextStyle(
                            fontSize: 18,
                            fontWeight: FontWeight.w900,
                          ),
                        ),
                        const SizedBox(height: 3),
                        Text(
                          '${current.currentStreak} consecutive logged days',
                          style: const TextStyle(color: Color(0xFF5F7068)),
                        ),
                      ],
                    ),
                  ),
                ],
              ),
            ),
          ),
          const SizedBox(height: 12),
          const Text(
            'Log either a workout or an intentional rest day every calendar day to keep your streak going.',
            style: TextStyle(color: Color(0xFF5F7068), height: 1.4),
          ),
          const SizedBox(height: 16),
          ...levels.map((level) {
            final unlocked = current.level >= level.$1;
            final active = current.level == level.$1;
            return Card(
              color: active ? const Color(0xFFE2F5EB) : null,
              child: ListTile(
                leading: CircleAvatar(
                  backgroundColor: unlocked
                      ? const Color(0xFF087B55)
                      : const Color(0xFFE6ECE9),
                  child: Text(
                    '${level.$1}',
                    style: TextStyle(
                      color: unlocked ? Colors.white : const Color(0xFF76857F),
                      fontWeight: FontWeight.w900,
                    ),
                  ),
                ),
                title: Text(
                  level.$2,
                  style: const TextStyle(fontWeight: FontWeight.w900),
                ),
                subtitle: Text(level.$3),
                trailing: Icon(
                  unlocked ? Icons.verified_rounded : Icons.lock_outline_rounded,
                  color: unlocked ? const Color(0xFF087B55) : const Color(0xFFA3AEA9),
                ),
              ),
            );
          }),
        ],
      ),
    );
  }
}
''')

pub = ROOT/'pubspec.yaml'
p = pub.read_text()
p = re.sub(r'^version:\s*.*$', 'version: 0.3.2+12', p, flags=re.M)
pub.write_text(p)

print('Applied v0.3.2 home log actions and stronger dynamic avatar moods')
