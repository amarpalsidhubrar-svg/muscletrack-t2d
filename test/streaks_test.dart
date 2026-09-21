import 'package:flutter_test/flutter_test.dart';
import 'package:muscletrack_t2d/models.dart';
import 'package:muscletrack_t2d/streaks.dart';

WorkoutSession log(DateTime date, {bool rest = false}) => WorkoutSession(
  date: date,
  workoutType: rest ? 'Rest Day' : 'Strength',
  durationMin: rest ? 0 : 45,
);

void main() {
  test('day 1 to 30 is Novice', () {
    final now = DateTime(2026, 9, 30);
    final sessions = List.generate(
      30,
      (i) => log(DateTime(2026, 9, 1).add(Duration(days: i))),
    );
    final result = calculateStreak(sessions, now: now);
    expect(result.currentStreak, 30);
    expect(result.level, 1);
    expect(result.levelName, 'Novice');
  });

  test('day 31 is Noob Gainer', () {
    final now = DateTime(2026, 10, 1);
    final sessions = List.generate(
      31,
      (i) => log(DateTime(2026, 9, 1).add(Duration(days: i))),
    );
    final result = calculateStreak(sessions, now: now);
    expect(result.currentStreak, 31);
    expect(result.level, 2);
    expect(result.levelName, 'Noob Gainer');
  });

  test('rest day keeps streak and shows recovery mood', () {
    final now = DateTime(2026, 9, 21);
    final sessions = [
      log(DateTime(2026, 9, 19)),
      log(DateTime(2026, 9, 20), rest: true),
      log(DateTime(2026, 9, 21), rest: true),
    ];
    final result = calculateStreak(sessions, now: now);
    expect(result.currentStreak, 3);
    expect(result.consecutiveRestDays, 2);
    expect(result.mood, TrainingAvatarMood.recovery);
  });

  test('missed full day shows worried mood', () {
    final now = DateTime(2026, 9, 21);
    final sessions = [
      log(DateTime(2026, 9, 18)),
      log(DateTime(2026, 9, 19)),
    ];
    final result = calculateStreak(sessions, now: now);
    expect(result.missedDays, 1);
    expect(result.currentStreak, 0);
    expect(result.mood, TrainingAvatarMood.worried);
  });

  test('Athlete starts on day 331', () {
    final now = DateTime(2026, 12, 27);
    final start = now.subtract(const Duration(days: 330));
    final sessions = List.generate(
      331,
      (i) => log(start.add(Duration(days: i))),
    );
    final result = calculateStreak(sessions, now: now);
    expect(result.level, 7);
    expect(result.levelName, 'Athlete');
  });
}
