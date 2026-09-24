import 'models.dart';

double epleyE1rm(double weightKg, int reps) {
  if (weightKg <= 0 || reps <= 0) return 0;
  if (reps == 1) return weightKg;
  return weightKg * (1 + reps / 30.0);
}

double trainingVolume(List<ExerciseSetRecord> sets) =>
    sets.fold<double>(0, (sum, set) => sum + (set.reps * set.weightKg));

double metMinutes(double? met, int minutes) {
  if (met == null || met <= 0 || minutes <= 0) return 0;
  return met * minutes;
}

String shortDate(DateTime date) {
  const months = [
    'Jan','Feb','Mar','Apr','May','Jun',
    'Jul','Aug','Sep','Oct','Nov','Dec'
  ];
  return '${date.day} ${months[date.month - 1]} ${date.year}';
}
