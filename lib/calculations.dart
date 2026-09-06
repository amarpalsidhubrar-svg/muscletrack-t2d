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

/// Mifflin-St Jeor resting energy estimate. This is an informational estimate,
/// not a prescription. For users who select 'Other / prefer not to say', the
/// midpoint of the male and female constants is used to avoid inferring sex.
double estimatedRestingEnergy({
  required double weightKg,
  required double heightCm,
  required int age,
  required String sex,
}) {
  if (weightKg <= 0 || heightCm <= 0 || age <= 0) return 0;
  final base = (10 * weightKg) + (6.25 * heightCm) - (5 * age);
  if (sex == 'Male') return base + 5;
  if (sex == 'Female') return base - 161;
  return base - 78;
}

double estimatedDailyEnergyRequirement({
  required double weightKg,
  required double heightCm,
  required int age,
  required String sex,
  required double activityFactor,
}) {
  if (activityFactor <= 0) return 0;
  return estimatedRestingEnergy(
        weightKg: weightKg,
        heightCm: heightCm,
        age: age,
        sex: sex,
      ) *
      activityFactor;
}

String shortDate(DateTime date) {
  const months = [
    'Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'
  ];
  return '${date.day} ${months[date.month - 1]} ${date.year}';
}
