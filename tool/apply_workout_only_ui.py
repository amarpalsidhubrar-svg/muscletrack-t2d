#!/usr/bin/env python3
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]

# Workout-only app shell.
(ROOT/'lib/screens/app_shell.dart').write_text(r'''import 'package:flutter/material.dart';

import '../app_store.dart';
import 'about_screen.dart';
import 'calendar_screen.dart';
import 'home_screen.dart';
import 'workout_history_screen.dart';

class AppShell extends StatefulWidget {
  final AppStore store;
  const AppShell({super.key, required this.store});

  @override
  State<AppShell> createState() => _AppShellState();
}

class _AppShellState extends State<AppShell> {
  int _index = 0;

  @override
  Widget build(BuildContext context) {
    final pages = [
      HomeScreen(store: widget.store),
      CalendarScreen(store: widget.store),
      WorkoutHistoryScreen(store: widget.store),
      AboutScreen(store: widget.store),
    ];

    return Scaffold(
      body: SafeArea(
        bottom: false,
        child: IndexedStack(index: _index, children: pages),
      ),
      bottomNavigationBar: NavigationBar(
        height: 70,
        selectedIndex: _index,
        onDestinationSelected: (value) => setState(() => _index = value),
        destinations: const [
          NavigationDestination(
            icon: Icon(Icons.home_outlined),
            selectedIcon: Icon(Icons.home_rounded),
            label: 'Home',
          ),
          NavigationDestination(
            icon: Icon(Icons.calendar_month_outlined),
            selectedIcon: Icon(Icons.calendar_month_rounded),
            label: 'Calendar',
          ),
          NavigationDestination(
            icon: Icon(Icons.fitness_center_outlined),
            selectedIcon: Icon(Icons.fitness_center_rounded),
            label: 'Workouts',
          ),
          NavigationDestination(
            icon: Icon(Icons.more_horiz_rounded),
            selectedIcon: Icon(Icons.more_horiz_rounded),
            label: 'More',
          ),
        ],
      ),
    );
  }
}
''')

# Workout-focused home screen. Keep the existing Option 2 activity animation widget untouched.
(ROOT/'lib/screens/home_screen.dart').write_text(r'''import 'dart:math' as math;
import 'package:flutter/material.dart';

import '../app_store.dart';
import '../models.dart';
import '../widgets/treadmill_avatar.dart';
import 'calendar_screen.dart';
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

  @override
  Widget build(BuildContext context) {
    final profile = store.profile!;
    final today = DateTime.now();
    final todayWorkouts = store.workouts.where((w) => _sameDay(w.date, today)).toList();
    final week = store.thisWeekWorkouts;
    final latest = store.workouts.isEmpty ? null : store.workouts.first;
    final totalSets = week.fold<int>(0, (sum, w) => sum + w.sets.length);

    return ListView(
      padding: const EdgeInsets.fromLTRB(14, 12, 14, 110),
      children: [
        _Header(initials: _initials(profile.name)),
        const SizedBox(height: 12),
        _Hero(
          greeting: _greeting(),
          name: profile.name,
          date: _dateLabel(today),
        ),
        const SizedBox(height: 12),
        _TodayCard(
          workouts: todayWorkouts.length,
          minutes: todayWorkouts.fold<int>(0, (s, w) => s + w.durationMin),
          sets: todayWorkouts.fold<int>(0, (s, w) => s + w.sets.length),
          onLog: () => Navigator.push(
            context,
            MaterialPageRoute(builder: (_) => StrengthWorkoutScreen(store: store)),
          ),
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
                value: '${store.weeklyActivityMinutes}',
                label: 'Minutes this week',
              ),
            ),
          ],
        ),
        const SizedBox(height: 12),
        _ActionCard(
          icon: Icons.calendar_month_rounded,
          title: 'Training calendar',
          subtitle: 'See your workout days at a glance',
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
          onTap: () => Navigator.push(
            context,
            MaterialPageRoute(
              builder: (_) => StrengthWorkoutScreen(store: store, existing: latest),
            ),
          ),
          onEmptyTap: () => Navigator.push(
            context,
            MaterialPageRoute(builder: (_) => StrengthWorkoutScreen(store: store)),
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

  String _dateLabel(DateTime d) {
    const months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
    const days = ['Mon','Tue','Wed','Thu','Fri','Sat','Sun'];
    return '${days[d.weekday - 1]}, ${d.day} ${months[d.month - 1]}';
  }
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
            Text('MuscleTrack',
              style: Theme.of(context).textTheme.headlineSmall?.copyWith(
                fontWeight: FontWeight.w900,
                color: const Color(0xFF092C2B),
                letterSpacing: -0.5,
              ),
            ),
            const Text('Your training, clearly tracked.',
              style: TextStyle(color: Color(0xFF087B55), fontWeight: FontWeight.w600),
            ),
          ],
        ),
      ),
      CircleAvatar(
        radius: 20,
        backgroundColor: const Color(0xFF087B55),
        child: Text(initials,
          style: const TextStyle(color: Colors.white, fontWeight: FontWeight.w800),
        ),
      ),
    ],
  );
}

class _Hero extends StatelessWidget {
  final String greeting, name, date;
  const _Hero({required this.greeting, required this.name, required this.date});

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
        const Positioned(
          right: 4,
          bottom: 4,
          child: TreadmillAvatar(width: 168, height: 180),
        ),
        Positioned.fill(
          child: Padding(
            padding: const EdgeInsets.fromLTRB(18, 15, 146, 16),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(date, style: const TextStyle(color: Color(0xFF53665E), fontWeight: FontWeight.w600)),
                const SizedBox(height: 12),
                Text(greeting, style: const TextStyle(fontSize: 22, fontWeight: FontWeight.w900, color: Color(0xFF092C2B))),
                const SizedBox(height: 3),
                Text('$name 👋', maxLines: 1, overflow: TextOverflow.ellipsis,
                  style: const TextStyle(fontSize: 27, fontWeight: FontWeight.w900, color: Color(0xFF092C2B))),
                const SizedBox(height: 10),
                const Text('Ready to train?',
                  style: TextStyle(fontSize: 18, color: Color(0xFF0B8C5E), fontWeight: FontWeight.w900)),
                const SizedBox(height: 3),
                const Text('Log today’s workout and keep your streak moving.',
                  style: TextStyle(fontSize: 11, color: Color(0xFF314B43), height: 1.25)),
              ],
            ),
          ),
        ),
      ],
    ),
  );
}

class _TodayCard extends StatelessWidget {
  final int workouts, minutes, sets;
  final VoidCallback onLog;
  const _TodayCard({required this.workouts, required this.minutes, required this.sets, required this.onLog});

  @override
  Widget build(BuildContext context) => Card(
    child: Padding(
      padding: const EdgeInsets.all(16),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(children: [
            const Expanded(child: Text("Today's training", style: TextStyle(fontSize: 16, fontWeight: FontWeight.w900))),
            FilledButton.icon(onPressed: onLog, icon: const Icon(Icons.add, size: 18), label: const Text('Log workout')),
          ]),
          const SizedBox(height: 16),
          Row(children: [
            Expanded(child: _Metric(value: '$workouts', label: 'Workouts')),
            Expanded(child: _Metric(value: '$sets', label: 'Sets')),
            Expanded(child: _Metric(value: '$minutes', label: 'Minutes')),
          ]),
        ],
      ),
    ),
  );
}

class _Metric extends StatelessWidget {
  final String value, label;
  const _Metric({required this.value, required this.label});
  @override
  Widget build(BuildContext context) => Column(children: [
    Text(value, style: const TextStyle(fontSize: 22, fontWeight: FontWeight.w900, color: Color(0xFF092C2B))),
    const SizedBox(height: 2),
    Text(label, style: const TextStyle(fontSize: 11, color: Color(0xFF6D7D76), fontWeight: FontWeight.w700)),
  ]);
}

class _StatCard extends StatelessWidget {
  final IconData icon;
  final String value, label;
  const _StatCard({required this.icon, required this.value, required this.label});
  @override
  Widget build(BuildContext context) => Card(
    child: Padding(
      padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 14),
      child: Column(children: [
        Icon(icon, color: const Color(0xFF087B55), size: 21),
        const SizedBox(height: 8),
        Text(value, style: const TextStyle(fontSize: 19, fontWeight: FontWeight.w900)),
        const SizedBox(height: 2),
        Text(label, textAlign: TextAlign.center, style: const TextStyle(fontSize: 9.5, color: Color(0xFF6D7D76))),
      ]),
    ),
  );
}

class _ActionCard extends StatelessWidget {
  final IconData icon;
  final String title, subtitle;
  final VoidCallback onTap;
  const _ActionCard({required this.icon, required this.title, required this.subtitle, required this.onTap});
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
  final VoidCallback onTap, onEmptyTap;
  const _RecentWorkout({required this.workout, required this.onTap, required this.onEmptyTap});

  @override
  Widget build(BuildContext context) {
    if (workout == null) {
      return Card(
        child: ListTile(
          onTap: onEmptyTap,
          leading: const CircleAvatar(child: Icon(Icons.fitness_center_rounded)),
          title: const Text('No workout logged yet', style: TextStyle(fontWeight: FontWeight.w900)),
          subtitle: const Text('Tap to log your first session'),
          trailing: const Icon(Icons.add_rounded),
        ),
      );
    }
    return Card(
      child: ListTile(
        onTap: onTap,
        leading: const CircleAvatar(
          backgroundColor: Color(0xFFE2F5EB),
          child: Icon(Icons.fitness_center_rounded, color: Color(0xFF087B55)),
        ),
        title: const Text('Most recent workout', style: TextStyle(fontWeight: FontWeight.w900)),
        subtitle: Text('${workout!.workoutType} • ${workout!.durationMin} min • ${workout!.sets.length} sets'),
        trailing: const Icon(Icons.edit_outlined),
      ),
    );
  }
}
''')

# Calendar for completed workout logs only (no new database schema required).
(ROOT/'lib/screens/calendar_screen.dart').write_text(r'''import 'package:flutter/material.dart';

import '../app_store.dart';
import '../models.dart';
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
    _selected = DateTime(now.year, now.month, now.day);
  }

  bool _sameDay(DateTime a, DateTime b) =>
      a.year == b.year && a.month == b.month && a.day == b.day;

  List<WorkoutSession> _forDay(DateTime day) =>
      widget.store.workouts.where((w) => _sameDay(w.date, day)).toList();

  @override
  Widget build(BuildContext context) {
    final first = DateTime(_month.year, _month.month, 1);
    final daysInMonth = DateTime(_month.year, _month.month + 1, 0).day;
    final leading = first.weekday - 1;
    final selectedWorkouts = _forDay(_selected);

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
                      final hasWorkout = _forDay(date).isNotEmpty;
                      final selected = _sameDay(date, _selected);
                      return InkWell(
                        borderRadius: BorderRadius.circular(12),
                        onTap: () => setState(() => _selected = date),
                        child: Container(
                          decoration: BoxDecoration(
                            color: selected
                                ? const Color(0xFF087B55)
                                : hasWorkout
                                    ? const Color(0xFFE2F5EB)
                                    : Colors.transparent,
                            borderRadius: BorderRadius.circular(12),
                            border: Border.all(
                              color: selected
                                  ? const Color(0xFF087B55)
                                  : hasWorkout
                                      ? const Color(0xFFB7E4CF)
                                      : const Color(0xFFE7ECE9),
                            ),
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
                              if (hasWorkout)
                                Positioned(
                                  bottom: 4,
                                  child: Container(
                                    width: 5,
                                    height: 5,
                                    decoration: BoxDecoration(
                                      shape: BoxShape.circle,
                                      color: selected ? Colors.white : const Color(0xFF087B55),
                                    ),
                                  ),
                                ),
                            ],
                          ),
                        ),
                      );
                    },
                  ),
                ],
              ),
            ),
          ),
          const SizedBox(height: 14),
          Row(
            children: [
              Expanded(
                child: Text(
                  _dayLabel(_selected),
                  style: const TextStyle(fontSize: 16, fontWeight: FontWeight.w900),
                ),
              ),
              TextButton.icon(
                onPressed: () => Navigator.push(
                  context,
                  MaterialPageRoute(builder: (_) => StrengthWorkoutScreen(store: widget.store)),
                ),
                icon: const Icon(Icons.add, size: 18),
                label: const Text('Log workout'),
              ),
            ],
          ),
          const SizedBox(height: 6),
          if (selectedWorkouts.isEmpty)
            const Card(
              child: Padding(
                padding: EdgeInsets.all(18),
                child: Row(
                  children: [
                    Icon(Icons.event_available_outlined, color: Color(0xFF087B55)),
                    SizedBox(width: 12),
                    Expanded(child: Text('No workout logged on this day.')),
                  ],
                ),
              ),
            )
          else
            ...selectedWorkouts.map((w) => Card(
              child: ListTile(
                onTap: () => Navigator.push(
                  context,
                  MaterialPageRoute(
                    builder: (_) => StrengthWorkoutScreen(store: widget.store, existing: w),
                  ),
                ),
                leading: const CircleAvatar(
                  backgroundColor: Color(0xFFE2F5EB),
                  child: Icon(Icons.fitness_center_rounded, color: Color(0xFF087B55)),
                ),
                title: Text(w.workoutType, style: const TextStyle(fontWeight: FontWeight.w900)),
                subtitle: Text('${w.durationMin} min • ${w.sets.length} sets'),
                trailing: const Icon(Icons.chevron_right_rounded),
              ),
            )),
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
    child: Text(label, textAlign: TextAlign.center,
      style: const TextStyle(fontSize: 11, fontWeight: FontWeight.w800, color: Color(0xFF6D7D76))),
  );
}
''')

# Preview version only.
pub = ROOT/'pubspec.yaml'
p = pub.read_text()
p = re.sub(r'^version:\s*.*$', 'version: 0.2.9+9', p, flags=re.M)
pub.write_text(p)

print('Applied MuscleTrack v0.3 workout-only UI, calendar, and general fitness branding')
