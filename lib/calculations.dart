import 'models.dart';

double bmi(double weightKg, double heightCm) {
  final metres = heightCm / 100;
  if (metres <= 0) return 0;
  return weightKg / (metres * metres);
}

double percentWeightChange(double baselineKg, double currentKg) {
  if (baselineKg <= 0) return 0;
  return ((currentKg - baselineKg) / baselineKg) * 100;
}

double epleyE1rm(double weightKg, int reps) {
  if (weightKg <= 0 || reps <= 0) return 0;
  if (reps == 1) return weightKg;
  return weightKg * (1 + reps / 30.0);
}

double trainingVolume(List<ExerciseSetRecord> sets) {
  return sets.fold<double>(
    0,
    (sum, set) => sum + (set.reps * set.weightKg),
  );
}

double metMinutes(double? met, int minutes) {
  if (met == null || met <= 0 || minutes <= 0) return 0;
  return met * minutes;
}

double estimatedCalories({
  required double? met,
  required int minutes,
  required double bodyWeightKg,
}) {
  if (met == null || met <= 0 || minutes <= 0 || bodyWeightKg <= 0) return 0;
  return ((met * 3.5 * bodyWeightKg) / 200) * minutes;
}

String shortDate(DateTime date) {
  const months = [
    'Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'
  ];
  return '${date.day} ${months[date.month - 1]} ${date.year}';
}
