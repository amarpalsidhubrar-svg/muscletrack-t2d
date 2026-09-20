import 'package:flutter_test/flutter_test.dart';
import 'package:muscletrack_t2d/calculations.dart';
import 'package:muscletrack_t2d/models.dart';

void main() {
  test('Epley e1RM', () {
    expect(epleyE1rm(80, 8), closeTo(101.33, 0.01));
  });

  test('training volume', () {
    const sets = [
      ExerciseSetRecord(
        exerciseName: 'Leg press',
        setNumber: 1,
        reps: 10,
        weightKg: 100,
      ),
      ExerciseSetRecord(
        exerciseName: 'Leg press',
        setNumber: 2,
        reps: 8,
        weightKg: 110,
      ),
    ];
    expect(trainingVolume(sets), closeTo(1880, 0.001));
  });

  test('MET-min', () {
    expect(metMinutes(5, 30), closeTo(150, 0.001));
  });
}
