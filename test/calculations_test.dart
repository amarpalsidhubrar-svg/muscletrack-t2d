import 'package:flutter_test/flutter_test.dart';
import 'package:muscletrack_t2d/calculations.dart';
import 'package:muscletrack_t2d/models.dart';

void main() {
  test('BMI calculation', () {
    expect(bmi(80, 180), closeTo(24.69, 0.01));
  });

  test('percentage weight change', () {
    expect(percentWeightChange(100, 92), closeTo(-8.0, 0.001));
  });

  test('Epley e1RM', () {
    expect(epleyE1rm(80, 8), closeTo(101.33, 0.01));
  });

  test('training volume', () {
    const sets = [
      ExerciseSetRecord(exerciseName: 'Leg press', setNumber: 1, reps: 10, weightKg: 100),
      ExerciseSetRecord(exerciseName: 'Leg press', setNumber: 2, reps: 8, weightKg: 110),
    ];
    expect(trainingVolume(sets), closeTo(1880, 0.001));
  });

  test('MET-min', () {
    expect(metMinutes(5, 30), closeTo(150, 0.001));
  });

  test('estimated calories', () {
    expect(
      estimatedCalories(met: 5, minutes: 30, bodyWeightKg: 80),
      closeTo(210, 0.01),
    );
  });
}
