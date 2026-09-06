import 'package:flutter/material.dart';

import '../app_store.dart';
import '../calculations.dart';
import 'strength_workout_screen.dart';

class WorkoutHistoryScreen extends StatefulWidget {
  final AppStore store;

  const WorkoutHistoryScreen({super.key, required this.store});

  @override
  State<WorkoutHistoryScreen> createState() => _WorkoutHistoryScreenState();
}

class _WorkoutHistoryScreenState extends State<WorkoutHistoryScreen> {
  Future<void> _editWorkout(BuildContext context, dynamic workout) async {
    await Navigator.push(
      context,
      MaterialPageRoute(
        builder: (_) => StrengthWorkoutScreen(store: widget.store, existing: workout),
      ),
    );
    if (mounted) setState(() {});
  }

  @override
  Widget build(BuildContext context) {
    final workouts = widget.store.workouts.where((w) => w.workoutType == 'Strength').toList();

    return Scaffold(
      appBar: AppBar(title: const Text('Workout history')),
      body: workouts.isEmpty
          ? const Center(child: Text('No strength workouts logged yet.'))
          : ListView.separated(
              padding: const EdgeInsets.all(16),
              itemCount: workouts.length,
              separatorBuilder: (_, __) => const SizedBox(height: 8),
              itemBuilder: (context, index) {
                final workout = workouts[index];
                final volume = trainingVolume(workout.sets);
                final exerciseCount = workout.sets.map((s) => s.exerciseName).toSet().length;
                return Card(
                  child: ListTile(
                    leading: const CircleAvatar(child: Icon(Icons.fitness_center, size: 18)),
                    title: Text(shortDate(workout.date)),
                    subtitle: Text(
                      '$exerciseCount exercise${exerciseCount == 1 ? '' : 's'} • '
                      '${workout.durationMin} min • ${volume.toStringAsFixed(0)} kg volume'
                      '${workout.readiness == null ? '' : ' • readiness ${workout.readiness}/5'}',
                    ),
                    trailing: PopupMenuButton<String>(
                      onSelected: (value) async {
                        if (value == 'edit') {
                          await _editWorkout(context, workout);
                        } else if (value == 'delete' && workout.id != null) {
                          final confirmed = await showDialog<bool>(
                            context: context,
                            builder: (dialogContext) => AlertDialog(
                              title: const Text('Delete workout?'),
                              content: Text('Delete the workout from ${shortDate(workout.date)}? This cannot be undone.'),
                              actions: [
                                TextButton(
                                  onPressed: () => Navigator.pop(dialogContext, false),
                                  child: const Text('Cancel'),
                                ),
                                FilledButton(
                                  onPressed: () => Navigator.pop(dialogContext, true),
                                  child: const Text('Delete'),
                                ),
                              ],
                            ),
                          );
                          if (confirmed == true) {
                            await widget.store.deleteWorkout(workout.id!);
                            if (mounted) setState(() {});
                          }
                        }
                      },
                      itemBuilder: (_) => const [
                        PopupMenuItem(value: 'edit', child: Text('Edit workout')),
                        PopupMenuItem(value: 'delete', child: Text('Delete workout')),
                      ],
                    ),
                    onTap: () => _editWorkout(context, workout),
                  ),
                );
              },
            ),
      floatingActionButton: FloatingActionButton.extended(
        onPressed: () async {
          await Navigator.push(
            context,
            MaterialPageRoute(builder: (_) => StrengthWorkoutScreen(store: widget.store)),
          );
          if (mounted) setState(() {});
        },
        icon: const Icon(Icons.add),
        label: const Text('Workout'),
      ),
    );
  }
}
