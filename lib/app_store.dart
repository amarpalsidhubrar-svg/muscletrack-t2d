import 'package:flutter/foundation.dart';

import 'app_database.dart';
import 'calculations.dart';
import 'models.dart';

class AppStore extends ChangeNotifier {
  final AppDatabase db;

  AppStore(this.db);

  bool loading = true;
  UserProfile? profile;
  List<WorkoutSession> workouts = [];

  Future<void> load() async {
    loading = true;
    notifyListeners();
    profile = await db.loadProfile();
    workouts = await db.loadWorkouts();
    loading = false;
    notifyListeners();
  }

  Future<void> saveProfile(UserProfile value) async {
    profile = value;
    await db.saveProfile(value);
    await refresh();
  }

  Future<void> addWorkout(WorkoutSession value) async {
    await db.addWorkout(value);
    await refresh();
  }

  Future<void> updateWorkout(WorkoutSession value) async {
    await db.updateWorkout(value);
    await refresh();
  }

  Future<void> deleteWorkout(int workoutId) async {
    await db.deleteWorkout(workoutId);
    await refresh();
  }

  Future<void> refresh() async {
    profile = await db.loadProfile();
    workouts = await db.loadWorkouts();
    notifyListeners();
  }

  Future<void> reset() async {
    await db.clearAll();
    await load();
  }

  DateTime get startOfCurrentWeek {
    final now = DateTime.now();
    final day = DateTime(now.year, now.month, now.day);
    return day.subtract(Duration(days: day.weekday - 1));
  }

  List<WorkoutSession> get thisWeekWorkouts =>
      workouts.where((w) => !w.date.isBefore(startOfCurrentWeek)).toList();

  int get weeklyActivityMinutes =>
      thisWeekWorkouts.fold<int>(0, (sum, w) => sum + w.durationMin);

  StrengthBest? get latestStrengthBest {
    StrengthBest? best;
    for (final workout in workouts) {
      for (final set in workout.sets) {
        final value = epleyE1rm(set.weightKg, set.reps);
        if (best == null || value > best.e1rmKg) {
          best = StrengthBest(
            exerciseName: set.exerciseName,
            e1rmKg: value,
            date: workout.date,
          );
        }
      }
    }
    return best;
  }

  double? latestE1rmFor(String exerciseName) {
    double? best;
    for (final workout in workouts) {
      for (final set in workout.sets) {
        if (set.exerciseName.toLowerCase() != exerciseName.toLowerCase()) {
          continue;
        }
        final value = epleyE1rm(set.weightKg, set.reps);
        if (best == null || value > best) best = value;
      }
    }
    return best;
  }
}
