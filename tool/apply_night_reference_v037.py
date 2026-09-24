#!/usr/bin/env python3
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]

(ROOT/'lib/theme.dart').write_text(r'''import 'package:flutter/material.dart';

ThemeData buildAppTheme() {
  const primary = Color(0xFF079669);
  const darkGreen = Color(0xFF075B49);
  const background = Color(0xFFF5F8F7);
  const border = Color(0xFFDCE7E2);

  final scheme = ColorScheme.fromSeed(
    seedColor: primary,
    brightness: Brightness.light,
  ).copyWith(
    primary: primary,
    onPrimary: Colors.white,
    secondary: darkGreen,
    surface: Colors.white,
    surfaceContainerHighest: const Color(0xFFEDF5F1),
    outline: border,
  );

  return ThemeData(
    useMaterial3: true,
    colorScheme: scheme,
    scaffoldBackgroundColor: background,
    fontFamily: 'Roboto',
    appBarTheme: const AppBarTheme(
      backgroundColor: background,
      foregroundColor: Color(0xFF17312A),
      elevation: 0,
      surfaceTintColor: Colors.transparent,
      centerTitle: false,
    ),
    cardTheme: const CardThemeData(
      color: Colors.white,
      surfaceTintColor: Colors.transparent,
      elevation: 0,
      margin: EdgeInsets.zero,
      shape: RoundedRectangleBorder(
        side: BorderSide(color: border),
        borderRadius: BorderRadius.all(Radius.circular(18)),
      ),
    ),
    inputDecorationTheme: const InputDecorationTheme(
      filled: true,
      fillColor: Colors.white,
      contentPadding: EdgeInsets.symmetric(horizontal: 14, vertical: 14),
      border: OutlineInputBorder(
        borderSide: BorderSide(color: border),
        borderRadius: BorderRadius.all(Radius.circular(12)),
      ),
      enabledBorder: OutlineInputBorder(
        borderSide: BorderSide(color: border),
        borderRadius: BorderRadius.all(Radius.circular(12)),
      ),
      focusedBorder: OutlineInputBorder(
        borderSide: BorderSide(color: primary, width: 1.5),
        borderRadius: BorderRadius.all(Radius.circular(12)),
      ),
    ),
    filledButtonTheme: FilledButtonThemeData(
      style: FilledButton.styleFrom(
        backgroundColor: primary,
        foregroundColor: Colors.white,
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(14)),
      ),
    ),
    outlinedButtonTheme: OutlinedButtonThemeData(
      style: OutlinedButton.styleFrom(
        foregroundColor: darkGreen,
        side: const BorderSide(color: border),
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(14)),
      ),
    ),
    navigationBarTheme: const NavigationBarThemeData(
      backgroundColor: Colors.white,
      indicatorColor: Color(0xFFDDF3E9),
      surfaceTintColor: Colors.transparent,
      elevation: 2,
      labelTextStyle: WidgetStatePropertyAll(
        TextStyle(fontSize: 11, fontWeight: FontWeight.w600),
      ),
    ),
    dividerColor: border,
  );
}

ThemeData buildDarkAppTheme() {
  const primary = Color(0xFF4DA6FF);
  const background = Color(0xFF071018);
  const surface = Color(0xFF101B25);
  const raisedSurface = Color(0xFF142331);
  const outline = Color(0xFF243544);
  const text = Color(0xFFF3F7FC);
  const muted = Color(0xFF9BAABB);

  final scheme = ColorScheme.fromSeed(
    seedColor: primary,
    brightness: Brightness.dark,
  ).copyWith(
    primary: primary,
    onPrimary: const Color(0xFF03111F),
    secondary: const Color(0xFF80BFFF),
    onSecondary: const Color(0xFF03111F),
    surface: surface,
    surfaceContainerHighest: raisedSurface,
    outline: outline,
    onSurface: text,
    onSurfaceVariant: muted,
  );

  return ThemeData(
    useMaterial3: true,
    brightness: Brightness.dark,
    colorScheme: scheme,
    scaffoldBackgroundColor: background,
    fontFamily: 'Roboto',
    textTheme: ThemeData.dark().textTheme.apply(
      bodyColor: text,
      displayColor: text,
    ),
    appBarTheme: const AppBarTheme(
      backgroundColor: background,
      foregroundColor: text,
      elevation: 0,
      surfaceTintColor: Colors.transparent,
      centerTitle: false,
      titleTextStyle: TextStyle(
        color: text,
        fontSize: 20,
        fontWeight: FontWeight.w800,
      ),
    ),
    cardTheme: const CardThemeData(
      color: surface,
      surfaceTintColor: Colors.transparent,
      elevation: 0,
      margin: EdgeInsets.zero,
      shape: RoundedRectangleBorder(
        side: BorderSide(color: outline),
        borderRadius: BorderRadius.all(Radius.circular(18)),
      ),
    ),
    inputDecorationTheme: const InputDecorationTheme(
      filled: true,
      fillColor: raisedSurface,
      contentPadding: EdgeInsets.symmetric(horizontal: 14, vertical: 14),
      labelStyle: TextStyle(color: muted),
      hintStyle: TextStyle(color: Color(0xFF748596)),
      border: OutlineInputBorder(
        borderSide: BorderSide(color: outline),
        borderRadius: BorderRadius.all(Radius.circular(12)),
      ),
      enabledBorder: OutlineInputBorder(
        borderSide: BorderSide(color: outline),
        borderRadius: BorderRadius.all(Radius.circular(12)),
      ),
      focusedBorder: OutlineInputBorder(
        borderSide: BorderSide(color: primary, width: 1.5),
        borderRadius: BorderRadius.all(Radius.circular(12)),
      ),
    ),
    filledButtonTheme: FilledButtonThemeData(
      style: FilledButton.styleFrom(
        backgroundColor: primary,
        foregroundColor: const Color(0xFF03111F),
        textStyle: const TextStyle(fontWeight: FontWeight.w800),
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(18)),
      ),
    ),
    outlinedButtonTheme: OutlinedButtonThemeData(
      style: OutlinedButton.styleFrom(
        foregroundColor: text,
        side: const BorderSide(color: Color(0xFF3B4D5D)),
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(18)),
      ),
    ),
    navigationBarTheme: const NavigationBarThemeData(
      backgroundColor: Color(0xFF09131C),
      indicatorColor: Color(0xFF173653),
      surfaceTintColor: Colors.transparent,
      elevation: 0,
      labelTextStyle: WidgetStatePropertyAll(
        TextStyle(
          color: Color(0xFFB5C2CF),
          fontSize: 11,
          fontWeight: FontWeight.w600,
        ),
      ),
    ),
    dividerColor: outline,
    chipTheme: const ChipThemeData(
      backgroundColor: raisedSurface,
      selectedColor: Color(0xFF194D73),
      side: BorderSide(color: outline),
      labelStyle: TextStyle(color: text),
    ),
    listTileTheme: const ListTileThemeData(
      textColor: text,
      iconColor: Color(0xFFB7C5D3),
    ),
  );
}
''')

(ROOT/'lib/screens/home_screen.dart').write_text(r'''import 'dart:math' as math;
import 'dart:ui';

import 'package:flutter/material.dart';

import '../app_store.dart';
import '../models.dart';
import '../streaks.dart';
import '../theme_controller.dart';
import '../workout_timer_service.dart';
import '../widgets/treadmill_avatar.dart';
import 'activity_progress_screen.dart';
import 'body_progress_screen.dart';
import 'calendar_screen.dart';
import 'daily_activity_screen.dart';
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
    final todayWorkouts = todaySessions
        .where((w) => w.workoutType.toLowerCase() != 'rest day')
        .toList();
    final isRestDay = store.hasRestDayOn(today);
    final latest = store.workouts
        .where((w) => w.workoutType.toLowerCase() != 'rest day')
        .cast<WorkoutSession?>()
        .firstOrNull;
    final streak = store.streakSummary;
    final activity = store.activityForDay(today);

    return ListView(
      padding: const EdgeInsets.fromLTRB(15, 12, 15, 110),
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
          onRest: () => store.markRestDay(today),
        ),
        const SizedBox(height: 12),
        const _WorkoutTimerHomeCard(),
        _DailyActivityCard(
          activity: activity,
          onLog: () => Navigator.push(
            context,
            MaterialPageRoute(builder: (_) => DailyActivityScreen(store: store)),
          ),
          onProgress: () => Navigator.push(
            context,
            MaterialPageRoute(builder: (_) => ActivityProgressScreen(store: store)),
          ),
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
          minutes: todayWorkouts.fold<int>(0, (sum, w) => sum + w.durationMin),
          sets: todayWorkouts.fold<int>(0, (sum, w) => sum + w.sets.length),
          restDay: isRestDay,
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
        const SizedBox(height: 9),
        _ActionCard(
          icon: Icons.accessibility_new_rounded,
          title: 'Body progress',
          subtitle: 'See which body parts you train most often',
          onTap: () => Navigator.push(
            context,
            MaterialPageRoute(builder: (_) => BodyProgressScreen(store: store)),
          ),
        ),
        const SizedBox(height: 9),
        _ActionCard(
          icon: Icons.history_rounded,
          title: 'Workout history',
          subtitle: 'View and edit your previous sessions',
          onTap: () => Navigator.push(
            context,
            MaterialPageRoute(builder: (_) => WorkoutHistoryScreen(store: store)),
          ),
        ),
        const SizedBox(height: 9),
        _RecentWorkout(
          workout: latest,
          onTap: () {
            Navigator.push(
              context,
              MaterialPageRoute(
                builder: (_) => latest == null
                    ? StrengthWorkoutScreen(store: store)
                    : StrengthWorkoutScreen(store: store, existing: latest),
              ),
            );
          },
        ),
      ],
    );
  }
}

extension _FirstOrNull<T> on Iterable<T> {
  T? get firstOrNull => isEmpty ? null : first;
}

bool _dark(BuildContext context) =>
    Theme.of(context).brightness == Brightness.dark;

Color _muted(BuildContext context) =>
    _dark(context) ? const Color(0xFF9BAABB) : const Color(0xFF65766F);

Color _accent(BuildContext context) =>
    _dark(context) ? const Color(0xFF4DA6FF) : const Color(0xFF087B55);

Color _softAccent(BuildContext context) =>
    _dark(context) ? const Color(0xFF173653) : const Color(0xFFE2F5EB);

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
                color: _dark(context)
                    ? const Color(0xFF5FAEFF)
                    : const Color(0xFF092C2B),
                letterSpacing: -.5,
              ),
            ),
            Text(
              'Your training, clearly tracked.',
              style: TextStyle(
                color: _dark(context)
                    ? const Color(0xFF7D9CBD)
                    : const Color(0xFF087B55),
                fontWeight: FontWeight.w600,
              ),
            ),
          ],
        ),
      ),
      IconButton(
        tooltip: ThemeController.instance.isDark
            ? 'Switch to light mode'
            : 'Switch to dark mode',
        onPressed: ThemeController.instance.toggle,
        icon: Icon(
          ThemeController.instance.isDark
              ? Icons.light_mode_rounded
              : Icons.dark_mode_rounded,
          size: 27,
          color: _dark(context) ? Colors.white : const Color(0xFF17312A),
        ),
      ),
      CircleAvatar(
        radius: 21,
        backgroundColor: _dark(context)
            ? const Color(0xFF245B9A)
            : const Color(0xFF087B55),
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

  String get subtitle => streak > 0
      ? 'Keep logging each day to\nbuild your next level.'
      : 'Log a workout or rest day\nto start your streak.';

  @override
  Widget build(BuildContext context) {
    final dark = _dark(context);
    return Container(
      height: 192,
      clipBehavior: Clip.antiAlias,
      decoration: BoxDecoration(
        borderRadius: BorderRadius.circular(22),
        gradient: LinearGradient(
          colors: dark
              ? const [Color(0xFF111D29), Color(0xFF172533)]
              : const [Color(0xFFF3FBF7), Color(0xFFE5F7EE)],
          begin: Alignment.topLeft,
          end: Alignment.bottomRight,
        ),
        border: Border.all(
          color: dark ? const Color(0xFF253748) : const Color(0xFFDCEFE6),
        ),
      ),
      child: Stack(
        children: [
          Positioned(
            right: 3,
            bottom: 0,
            child: TreadmillAvatar(width: 157, height: 172, mood: mood),
          ),
          Positioned.fill(
            child: Padding(
              padding: const EdgeInsets.fromLTRB(16, 15, 140, 15),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    date,
                    style: TextStyle(
                      color: _muted(context),
                      fontWeight: FontWeight.w600,
                    ),
                  ),
                  const SizedBox(height: 12),
                  Text(
                    greeting,
                    style: TextStyle(
                      fontSize: 22,
                      fontWeight: FontWeight.w900,
                      color: dark ? const Color(0xFFF4F7FB) : const Color(0xFF092C2B),
                    ),
                  ),
                  const SizedBox(height: 4),
                  Text(
                    '$name 👋',
                    maxLines: 1,
                    overflow: TextOverflow.ellipsis,
                    style: TextStyle(
                      fontSize: 27,
                      fontWeight: FontWeight.w900,
                      color: dark ? const Color(0xFFF4F7FB) : const Color(0xFF092C2B),
                    ),
                  ),
                  const SizedBox(height: 12),
                  Text(
                    subtitle,
                    style: TextStyle(
                      fontSize: 12,
                      color: _muted(context),
                      height: 1.35,
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
  Widget build(BuildContext context) => Card(
    child: Padding(
      padding: const EdgeInsets.all(15),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Text(
            'Log today',
            style: TextStyle(fontSize: 17, fontWeight: FontWeight.w900),
          ),
          const SizedBox(height: 4),
          Text(
            'Choose a workout or an intentional rest day.',
            style: TextStyle(fontSize: 11.5, color: _muted(context)),
          ),
          const SizedBox(height: 13),
          Row(
            children: [
              Expanded(
                child: FilledButton.icon(
                  onPressed: restDay ? null : onWorkout,
                  icon: const Icon(Icons.fitness_center_rounded, size: 18),
                  label: Text(
                    hasWorkout ? 'Log another\nworkout' : 'Log workout',
                    textAlign: TextAlign.center,
                  ),
                ),
              ),
              const SizedBox(width: 9),
              Expanded(
                child: OutlinedButton.icon(
                  onPressed: (restDay || hasWorkout) ? null : onRest,
                  icon: const Icon(Icons.self_improvement_rounded, size: 18),
                  label: Text(restDay ? 'Rest day logged' : 'Rest day'),
                ),
              ),
            ],
          ),
        ],
      ),
    ),
  );
}

class _WorkoutTimerHomeCard extends StatefulWidget {
  const _WorkoutTimerHomeCard();

  @override
  State<_WorkoutTimerHomeCard> createState() => _WorkoutTimerHomeCardState();
}

class _WorkoutTimerHomeCardState extends State<_WorkoutTimerHomeCard> {
  final timer = WorkoutTimerService.instance;

  @override
  void initState() {
    super.initState();
    timer.addListener(_refresh);
  }

  @override
  void dispose() {
    timer.removeListener(_refresh);
    super.dispose();
  }

  void _refresh() {
    if (mounted) setState(() {});
  }

  @override
  Widget build(BuildContext context) {
    if (!timer.isActive) return const SizedBox.shrink();
    return Padding(
      padding: const EdgeInsets.only(bottom: 12),
      child: Card(
        child: ListTile(
          leading: CircleAvatar(
            backgroundColor: _softAccent(context),
            child: Icon(Icons.timer_rounded, color: _accent(context)),
          ),
          title: Text(
            timer.isRunning ? 'Workout in progress' : 'Workout timer paused',
            style: const TextStyle(fontWeight: FontWeight.w900),
          ),
          subtitle: Text(
            timer.formatted,
            style: TextStyle(
              fontSize: 23,
              fontWeight: FontWeight.w900,
              color: _accent(context),
              fontFeatures: const [FontFeature.tabularFigures()],
            ),
          ),
          trailing: Icon(
            timer.isRunning
                ? Icons.play_circle_fill_rounded
                : Icons.pause_circle_filled_rounded,
            color: _accent(context),
          ),
        ),
      ),
    );
  }
}

class _DailyActivityCard extends StatelessWidget {
  final DailyActivity? activity;
  final VoidCallback onLog;
  final VoidCallback onProgress;

  const _DailyActivityCard({
    required this.activity,
    required this.onLog,
    required this.onProgress,
  });

  Widget metric(
    BuildContext context, {
    required IconData icon,
    required String value,
    required String label,
    required double progress,
    required String goal,
  }) => Expanded(
    child: Column(
      children: [
        Icon(icon, color: _accent(context), size: 23),
        const SizedBox(height: 5),
        Text(value, style: const TextStyle(fontSize: 21, fontWeight: FontWeight.w900)),
        Text(label, style: TextStyle(fontSize: 10.5, color: _muted(context))),
        const SizedBox(height: 7),
        ClipRRect(
          borderRadius: BorderRadius.circular(12),
          child: LinearProgressIndicator(
            minHeight: 7,
            value: progress.clamp(0, 1),
            backgroundColor: _dark(context)
                ? const Color(0xFF203141)
                : const Color(0xFFE7ECEA),
            color: _accent(context),
          ),
        ),
        const SizedBox(height: 5),
        Text(goal, style: TextStyle(fontSize: 10, color: _muted(context))),
      ],
    ),
  );

  @override
  Widget build(BuildContext context) {
    final steps = activity?.steps ?? 0;
    final mins = activity?.activeMinutes ?? 0;
    final kcal = activity?.activeCalories ?? 0;
    return Card(
      child: Padding(
        padding: const EdgeInsets.fromLTRB(15, 14, 15, 15),
        child: Column(
          children: [
            Row(
              children: [
                Icon(
                  Icons.directions_walk_rounded,
                  color: _dark(context) ? Colors.white : _accent(context),
                ),
                const SizedBox(width: 8),
                const Expanded(
                  child: Text(
                    'Daily activity',
                    style: TextStyle(fontSize: 17, fontWeight: FontWeight.w900),
                  ),
                ),
                TextButton(
                  onPressed: onProgress,
                  child: const Text('Progress'),
                ),
                const Icon(Icons.chevron_right_rounded, size: 18),
              ],
            ),
            const SizedBox(height: 11),
            Row(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                metric(
                  context,
                  icon: Icons.directions_walk_rounded,
                  value: '$steps',
                  label: 'Steps',
                  progress: steps / 10000,
                  goal: '/ 10,000',
                ),
                const SizedBox(width: 18),
                metric(
                  context,
                  icon: Icons.timer_rounded,
                  value: '$mins',
                  label: 'Active mins',
                  progress: mins / 60,
                  goal: '/ 60',
                ),
                const SizedBox(width: 18),
                metric(
                  context,
                  icon: Icons.local_fire_department_rounded,
                  value: kcal.toStringAsFixed(0),
                  label: 'Active kcal',
                  progress: kcal / 500,
                  goal: '/ 500',
                ),
              ],
            ),
            const SizedBox(height: 14),
            SizedBox(
              width: double.infinity,
              child: OutlinedButton.icon(
                onPressed: onLog,
                icon: const Icon(Icons.watch_rounded),
                label: Text(
                  activity == null
                      ? 'Enter smartwatch activity'
                      : 'Edit smartwatch activity',
                ),
              ),
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
    final next = summary.daysToNextLevel == 0
        ? 'Top level reached'
        : '${summary.daysToNextLevel} days to next level';
    return Card(
      child: InkWell(
        borderRadius: BorderRadius.circular(18),
        onTap: onTap,
        child: Padding(
          padding: const EdgeInsets.all(15),
          child: Column(
            children: [
              Row(
                children: [
                  Container(
                    width: 50,
                    height: 50,
                    decoration: BoxDecoration(
                      color: _dark(context)
                          ? const Color(0xFF513916)
                          : const Color(0xFFFFF2CC),
                      borderRadius: BorderRadius.circular(14),
                    ),
                    child: const Icon(
                      Icons.emoji_events_rounded,
                      color: Color(0xFFFFB21A),
                      size: 31,
                    ),
                  ),
                  const SizedBox(width: 12),
                  Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          summary.level > 0
                              ? 'Level ${summary.level} - ${summary.levelName}'
                              : 'Start your streak',
                          style: const TextStyle(
                            fontSize: 15,
                            fontWeight: FontWeight.w900,
                          ),
                        ),
                        const SizedBox(height: 3),
                        Text(
                          '${summary.currentStreak} day streak 🔥',
                          style: TextStyle(
                            fontSize: 20,
                            fontWeight: FontWeight.w900,
                            color: _accent(context),
                          ),
                        ),
                      ],
                    ),
                  ),
                  const Icon(Icons.chevron_right_rounded),
                ],
              ),
              const SizedBox(height: 12),
              ClipRRect(
                borderRadius: BorderRadius.circular(10),
                child: LinearProgressIndicator(
                  minHeight: 8,
                  value: summary.levelProgress,
                  backgroundColor: _dark(context)
                      ? const Color(0xFF203141)
                      : const Color(0xFFE8EEEB),
                  color: _accent(context),
                ),
              ),
              const SizedBox(height: 5),
              Align(
                alignment: Alignment.centerRight,
                child: Text(
                  next,
                  style: TextStyle(color: _muted(context), fontSize: 10.5),
                ),
              ),
              const SizedBox(height: 13),
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
                      icon: Icons.star_rounded,
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
  const _MiniMetric({
    required this.icon,
    required this.value,
    required this.label,
  });

  @override
  Widget build(BuildContext context) => Column(
    children: [
      Icon(icon, size: 20, color: _accent(context)),
      const SizedBox(height: 5),
      Text(value, style: const TextStyle(fontSize: 17, fontWeight: FontWeight.w900)),
      Text(
        label,
        textAlign: TextAlign.center,
        style: TextStyle(fontSize: 9.5, color: _muted(context)),
      ),
    ],
  );
}

class _TodayCard extends StatelessWidget {
  final int workouts;
  final int minutes;
  final int sets;
  final bool restDay;

  const _TodayCard({
    required this.workouts,
    required this.minutes,
    required this.sets,
    required this.restDay,
  });

  @override
  Widget build(BuildContext context) => Card(
    child: Padding(
      padding: const EdgeInsets.all(15),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Text(
            "Today's log",
            style: TextStyle(fontSize: 17, fontWeight: FontWeight.w900),
          ),
          const SizedBox(height: 11),
          Container(
            width: double.infinity,
            padding: const EdgeInsets.all(12),
            decoration: BoxDecoration(
              color: _dark(context)
                  ? const Color(0xFF152A41)
                  : restDay
                      ? const Color(0xFFE8F2FF)
                      : const Color(0xFFE2F5EB),
              borderRadius: BorderRadius.circular(12),
            ),
            child: Row(
              children: [
                Icon(
                  restDay
                      ? Icons.self_improvement_rounded
                      : Icons.check_circle_rounded,
                  color: _accent(context),
                ),
                const SizedBox(width: 9),
                Expanded(
                  child: Text(
                    restDay
                        ? 'Rest day logged — recovery keeps your streak alive.'
                        : workouts > 0
                            ? 'Workout logged — today counts towards your streak.'
                            : 'No workout or rest day logged yet.',
                    style: const TextStyle(fontWeight: FontWeight.w700),
                  ),
                ),
              ],
            ),
          ),
          const SizedBox(height: 13),
          Row(
            children: [
              Expanded(
                child: _Metric(
                  icon: Icons.fitness_center_rounded,
                  value: '$workouts',
                  label: 'Workouts',
                ),
              ),
              Expanded(
                child: _Metric(
                  icon: Icons.format_list_numbered_rounded,
                  value: '$sets',
                  label: 'Sets',
                ),
              ),
              Expanded(
                child: _Metric(
                  icon: Icons.schedule_rounded,
                  value: '$minutes',
                  label: 'Minutes',
                ),
              ),
            ],
          ),
        ],
      ),
    ),
  );
}

class _Metric extends StatelessWidget {
  final IconData icon;
  final String value;
  final String label;
  const _Metric({
    required this.icon,
    required this.value,
    required this.label,
  });

  @override
  Widget build(BuildContext context) => Column(
    children: [
      Icon(icon, color: _accent(context), size: 22),
      const SizedBox(height: 5),
      Text(value, style: const TextStyle(fontSize: 20, fontWeight: FontWeight.w900)),
      Text(label, style: TextStyle(fontSize: 10.5, color: _muted(context))),
    ],
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
        backgroundColor: _dark(context)
            ? const Color(0xFFE8EEF5)
            : _softAccent(context),
        child: Icon(
          icon,
          color: _dark(context)
              ? const Color(0xFF28669D)
              : _accent(context),
        ),
      ),
      title: Text(title, style: const TextStyle(fontWeight: FontWeight.w900)),
      subtitle: Text(subtitle, style: TextStyle(color: _muted(context))),
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
    final body = workout?.bodyParts ?? const <String>[];
    final detail = workout == null
        ? 'Tap to log your first session'
        : body.isNotEmpty
            ? '${workout!.workoutType} • ${workout!.durationMin} min • ${body.join(', ')}'
            : '${workout!.workoutType} • ${workout!.durationMin} min • ${workout!.sets.length} sets';

    return Card(
      child: ListTile(
        onTap: onTap,
        leading: CircleAvatar(
          backgroundColor: _dark(context)
              ? const Color(0xFFE8EEF5)
              : _softAccent(context),
          child: Icon(
            Icons.fitness_center_rounded,
            color: _dark(context)
                ? const Color(0xFF28669D)
                : _accent(context),
          ),
        ),
        title: Text(
          workout == null ? 'No workout logged yet' : 'Most recent workout',
          style: const TextStyle(fontWeight: FontWeight.w900),
        ),
        subtitle: Text(
          detail,
          maxLines: 2,
          overflow: TextOverflow.ellipsis,
          style: TextStyle(color: _muted(context)),
        ),
        trailing: Icon(
          workout == null ? Icons.add_rounded : Icons.edit_outlined,
        ),
      ),
    );
  }
}
''')

(ROOT/'lib/screens/calendar_screen.dart').write_text(r'''import 'package:flutter/material.dart';

import '../app_store.dart';
import '../streaks.dart';
import 'daily_activity_screen.dart';
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

  bool _same(DateTime a, DateTime b) => dayOnly(a) == dayOnly(b);
  bool get _isDark => Theme.of(context).brightness == Brightness.dark;
  Color get _blue =>
      _isDark ? const Color(0xFF4DA6FF) : const Color(0xFF087B55);
  Color get _muted =>
      _isDark ? const Color(0xFF9BAABB) : const Color(0xFF667871);

  @override
  Widget build(BuildContext context) {
    final first = DateTime(_month.year, _month.month, 1);
    final days = DateTime(_month.year, _month.month + 1, 0).day;
    final leading = first.weekday - 1;
    final sessions = widget.store.workoutsForDay(_selected);
    final kind = widget.store.logKindFor(_selected);
    final activity = widget.store.activityForDay(_selected);
    final today = dayOnly(DateTime.now());
    final canLog = !_selected.isAfter(today);

    return Scaffold(
      appBar: AppBar(title: const Text('Training calendar')),
      body: ListView(
        padding: const EdgeInsets.fromLTRB(14, 8, 14, 100),
        children: [
          Card(
            child: Padding(
              padding: const EdgeInsets.all(13),
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
                          style: const TextStyle(
                            fontSize: 16,
                            fontWeight: FontWeight.w900,
                          ),
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
                      _Dow('Mon'), _Dow('Tue'), _Dow('Wed'), _Dow('Thu'),
                      _Dow('Fri'), _Dow('Sat'), _Dow('Sun'),
                    ],
                  ),
                  const SizedBox(height: 7),
                  GridView.builder(
                    shrinkWrap: true,
                    physics: const NeverScrollableScrollPhysics(),
                    itemCount: leading + days,
                    gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
                      crossAxisCount: 7,
                      mainAxisSpacing: 6,
                      crossAxisSpacing: 6,
                    ),
                    itemBuilder: (_, index) {
                      if (index < leading) return const SizedBox.shrink();
                      final day = index - leading + 1;
                      final date = DateTime(_month.year, _month.month, day);
                      final selected = _same(date, _selected);
                      final dayKind = widget.store.logKindFor(date);
                      final hasActivity = widget.store.activityForDay(date) != null;
                      final workout = dayKind == DailyLogKind.workout;
                      final rest = dayKind == DailyLogKind.rest;
                      final partial = hasActivity && !workout && !rest;

                      final fill = selected
                          ? _blue
                          : _isDark
                              ? const Color(0xFF15222E)
                              : Colors.transparent;
                      final border = selected
                          ? _blue
                          : _isDark
                              ? const Color(0xFF1C2C39)
                              : const Color(0xFFE1E8E5);

                      return InkWell(
                        borderRadius: BorderRadius.circular(11),
                        onTap: () => setState(() => _selected = date),
                        child: Container(
                          decoration: BoxDecoration(
                            color: fill,
                            borderRadius: BorderRadius.circular(11),
                            border: Border.all(color: border),
                          ),
                          child: Stack(
                            alignment: Alignment.center,
                            children: [
                              Text(
                                '$day',
                                style: TextStyle(
                                  fontWeight: FontWeight.w800,
                                  color: selected
                                      ? (_isDark
                                          ? const Color(0xFF06111D)
                                          : Colors.white)
                                      : null,
                                ),
                              ),
                              if (workout || rest || partial)
                                Positioned(
                                  bottom: 4,
                                  child: Container(
                                    width: 6,
                                    height: 6,
                                    decoration: BoxDecoration(
                                      shape: BoxShape.circle,
                                      color: workout
                                          ? const Color(0xFF4DA6FF)
                                          : rest
                                              ? const Color(0xFF91A6C2)
                                              : const Color(0xFFFF9F2E),
                                    ),
                                  ),
                                ),
                            ],
                          ),
                        ),
                      );
                    },
                  ),
                  const SizedBox(height: 14),
                  const Wrap(
                    spacing: 18,
                    runSpacing: 8,
                    alignment: WrapAlignment.center,
                    children: [
                      _Legend(color: Color(0xFF4DA6FF), label: 'Workout'),
                      _Legend(color: Color(0xFF91A6C2), label: 'Rest day'),
                      _Legend(color: Color(0xFFFF9F2E), label: 'Activity'),
                    ],
                  ),
                ],
              ),
            ),
          ),
          const SizedBox(height: 13),
          Text(
            _dayLabel(_selected),
            style: const TextStyle(fontSize: 16, fontWeight: FontWeight.w900),
          ),
          const SizedBox(height: 8),
          if (activity != null)
            Card(
              child: ListTile(
                onTap: () async {
                  await Navigator.push(
                    context,
                    MaterialPageRoute(
                      builder: (_) => DailyActivityScreen(
                        store: widget.store,
                        initialDate: _selected,
                      ),
                    ),
                  );
                  if (mounted) setState(() {});
                },
                leading: CircleAvatar(
                  backgroundColor: _isDark
                      ? const Color(0xFF173653)
                      : const Color(0xFFE2F5EB),
                  child: Icon(Icons.watch_rounded, color: _blue),
                ),
                title: const Text(
                  'Daily activity',
                  style: TextStyle(fontWeight: FontWeight.w900),
                ),
                subtitle: Text(
                  '${activity.steps} steps • ${activity.activeMinutes} min • '
                  '${activity.activeCalories.toStringAsFixed(0)} active kcal',
                ),
                trailing: const Icon(Icons.chevron_right_rounded),
              ),
            ),
          if (activity != null && sessions.isNotEmpty)
            const SizedBox(height: 8),
          if (kind == DailyLogKind.rest)
            Card(
              child: ListTile(
                leading: CircleAvatar(
                  backgroundColor: _isDark
                      ? const Color(0xFF263545)
                      : const Color(0xFFE4EEFF),
                  child: const Icon(
                    Icons.self_improvement_rounded,
                    color: Color(0xFF91A6C2),
                  ),
                ),
                title: const Text(
                  'Rest day',
                  style: TextStyle(fontWeight: FontWeight.w900),
                ),
                subtitle: const Text(
                  'Recovery day — this counts toward your streak.',
                ),
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
          else if (sessions.where((w) => w.workoutType.toLowerCase() != 'rest day').isNotEmpty)
            ...sessions
                .where((w) => w.workoutType.toLowerCase() != 'rest day')
                .map(
                  (w) => Padding(
                    padding: const EdgeInsets.only(bottom: 8),
                    child: Card(
                      color: _isDark ? const Color(0xFF132237) : null,
                      child: ListTile(
                        onTap: () async {
                          await Navigator.push(
                            context,
                            MaterialPageRoute(
                              builder: (_) => StrengthWorkoutScreen(
                                store: widget.store,
                                existing: w,
                              ),
                            ),
                          );
                          if (mounted) setState(() {});
                        },
                        leading: CircleAvatar(
                          backgroundColor: _isDark
                              ? const Color(0xFF173653)
                              : const Color(0xFFDDF4E8),
                          child: Icon(Icons.fitness_center_rounded, color: _blue),
                        ),
                        title: Text(
                          w.workoutType,
                          style: const TextStyle(fontWeight: FontWeight.w900),
                        ),
                        subtitle: Text(
                          w.bodyParts.isNotEmpty
                              ? '${w.durationMin} min • ${w.bodyParts.join(', ')}'
                              : '${w.durationMin} min • ${w.sets.length} sets',
                        ),
                        trailing: const Icon(Icons.chevron_right_rounded),
                      ),
                    ),
                  ),
                )
          else if (activity == null)
            Card(
              child: Padding(
                padding: const EdgeInsets.all(15),
                child: Column(
                  children: [
                    Row(
                      children: [
                        Icon(Icons.event_available_outlined, color: _blue),
                        const SizedBox(width: 10),
                        const Expanded(
                          child: Text('No entry logged for this day.'),
                        ),
                      ],
                    ),
                    if (canLog) ...[
                      const SizedBox(height: 12),
                      Row(
                        children: [
                          Expanded(
                            child: FilledButton.icon(
                              onPressed: () async {
                                await Navigator.push(
                                  context,
                                  MaterialPageRoute(
                                    builder: (_) => StrengthWorkoutScreen(
                                      store: widget.store,
                                    ),
                                  ),
                                );
                                if (mounted) setState(() {});
                              },
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
    const dow = ['Mon','Tue','Wed','Thu','Fri','Sat','Sun'];
    return '${dow[d.weekday - 1]}, ${d.day} ${m[d.month - 1]} ${d.year}';
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
      style: TextStyle(
        fontSize: 10,
        fontWeight: FontWeight.w700,
        color: Theme.of(context).brightness == Brightness.dark
            ? const Color(0xFF8FA1B2)
            : const Color(0xFF6D7D76),
      ),
    ),
  );
}

class _Legend extends StatelessWidget {
  final Color color;
  final String label;
  const _Legend({required this.color, required this.label});

  @override
  Widget build(BuildContext context) => Row(
    mainAxisSize: MainAxisSize.min,
    children: [
      Container(
        width: 9,
        height: 9,
        decoration: BoxDecoration(color: color, shape: BoxShape.circle),
      ),
      const SizedBox(width: 6),
      Text(
        label,
        style: TextStyle(
          fontSize: 10.5,
          color: Theme.of(context).brightness == Brightness.dark
              ? const Color(0xFFAAB8C5)
              : const Color(0xFF60716A),
        ),
      ),
    ],
  );
}
''')

pub = ROOT/'pubspec.yaml'
p = pub.read_text()
p = re.sub(r'^version:\s*.*$', 'version: 0.3.7+17', p, flags=re.M)
pub.write_text(p)

print('Applied v0.3.7 reference night-mode visual treatment')
