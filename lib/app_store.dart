import 'package:flutter/foundation.dart';

import 'app_database.dart';
import 'calculations.dart';
import 'models.dart';

class AppStore extends ChangeNotifier {
  final AppDatabase db;

  AppStore(this.db);

  bool loading = true;
  UserProfile? profile;
  List<WeightEntry> weights = [];
  List<MedicationEntry> medications = [];
  List<WorkoutSession> workouts = [];
  Goals goals = const Goals();

  Future<void> load() async {
    loading = true;
    notifyListeners();
    profile = await db.loadProfile();
    weights = await db.loadWeights();
    medications = await db.loadMedications();
    workouts = await db.loadWorkouts();
    goals = await db.loadGoals();
    loading = false;
    notifyListeners();
  }

  Future<void> saveProfile(UserProfile value) async {
    profile = value;
    await db.saveProfile(value);
    if (weights.isEmpty) {
      await db.addWeight(
        WeightEntry(date: DateTime.now(), weightKg: value.baselineWeightKg),
      );
    }
    await refresh();
  }

  Future<void> addWeight(WeightEntry value) async {
    await db.addWeight(value);
    await refresh();
  }

  Future<void> addMedication(MedicationEntry value) async {
    await db.addMedication(value);
    await refresh();
  }

  Future<void> addWorkout(WorkoutSession value) async {
    await db.addWorkout(value);
    await refresh();
  }

  Future<void> saveGoals(Goals value) async {
    goals = value;
    await db.saveGoals(value);
    notifyListeners();
  }

  Future<void> refresh() async {
    weights = await db.loadWeights();
    medications = await db.loadMedications();
    workouts = await db.loadWorkouts();
    goals = await db.loadGoals();
    notifyListeners();
  }

  Future<void> reset() async {
    await db.clearAll();
    await load();
  }

  double get currentWeightKg =>
      weights.isNotEmpty ? weights.first.weightKg : (profile?.baselineWeightKg ?? 0);

  double get currentBmi => profile == null ? 0 : bmi(currentWeightKg, profile!.heightCm);

  double get weightChangePct => profile == null
      ? 0
      : percentWeightChange(profile!.baselineWeightKg, currentWeightKg);

  DateTime get startOfCurrentWeek {
    final now = DateTime.now();
    final day = DateTime(now.year, now.month, now.day);
    return day.subtract(Duration(days: day.weekday - 1));
  }

  List<WorkoutSession> get thisWeekWorkouts => workouts
      .where((w) => !w.date.isBefore(startOfCurrentWeek))
      .toList();

  int get weeklyActivityMinutes =>
      thisWeekWorkouts.fold<int>(0, (sum, w) => sum + w.durationMin);

  int get weeklyStrengthSessions => thisWeekWorkouts
      .where((w) => w.workoutType == 'Strength')
      .length;

  double get weeklyMetMinutes => thisWeekWorkouts.fold<double>(
        0,
        (sum, w) => sum + metMinutes(w.met, w.durationMin),
      );

  double get weeklyCalories => thisWeekWorkouts.fold<double>(0, (sum, w) {
        if (w.deviceCalories != null) return sum + w.deviceCalories!;
        return sum + estimatedCalories(
          met: w.met,
          minutes: w.durationMin,
          bodyWeightKg: currentWeightKg,
        );
      });

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
        if (set.exerciseName.toLowerCase() != exerciseName.toLowerCase()) continue;
        final value = epleyE1rm(set.weightKg, set.reps);
        if (best == null || value > best) best = value;
      }
    }
    return best;
  }
}
