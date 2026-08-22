import 'package:flutter/material.dart';

import '../app_store.dart';
import 'about_screen.dart';
import 'goals_screen.dart';
import 'home_screen.dart';
import 'medications_screen.dart';
import 'progress_screen.dart';
import 'strength_workout_screen.dart';

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
      ProgressScreen(store: widget.store),
      MedicationsScreen(store: widget.store),
      GoalsScreen(store: widget.store),
      AboutScreen(store: widget.store),
    ];

    return Scaffold(
      appBar: AppBar(
        title: const Text('MuscleTrack T2D'),
        actions: [
          IconButton(
            tooltip: 'Log strength workout',
            onPressed: () => Navigator.push(
              context,
              MaterialPageRoute(builder: (_) => StrengthWorkoutScreen(store: widget.store)),
            ),
            icon: const Icon(Icons.add_circle_outline),
          ),
        ],
      ),
      body: IndexedStack(index: _index, children: pages),
      bottomNavigationBar: NavigationBar(
        selectedIndex: _index,
        onDestinationSelected: (value) => setState(() => _index = value),
        destinations: const [
          NavigationDestination(icon: Icon(Icons.home_outlined), selectedIcon: Icon(Icons.home), label: 'Home'),
          NavigationDestination(icon: Icon(Icons.insights_outlined), selectedIcon: Icon(Icons.insights), label: 'Progress'),
          NavigationDestination(icon: Icon(Icons.medication_outlined), selectedIcon: Icon(Icons.medication), label: 'Meds'),
          NavigationDestination(icon: Icon(Icons.flag_outlined), selectedIcon: Icon(Icons.flag), label: 'Goals'),
          NavigationDestination(icon: Icon(Icons.info_outline), selectedIcon: Icon(Icons.info), label: 'About'),
        ],
      ),
    );
  }
}
