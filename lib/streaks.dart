import 'models.dart';

enum DailyLogKind { workout, rest }

enum TrainingAvatarMood { happy, recovery, worried }

class StreakSummary {
  final int currentStreak;
  final int longestStreak;
  final int consecutiveRestDays;
  final int missedDays;
  final int level;
  final String levelName;
  final int daysToNextLevel;
  final double levelProgress;
  final TrainingAvatarMood mood;

  const StreakSummary({
    required this.currentStreak,
    required this.longestStreak,
    required this.consecutiveRestDays,
    required this.missedDays,
    required this.level,
    required this.levelName,
    required this.daysToNextLevel,
    required this.levelProgress,
    required this.mood,
  });
}

DateTime dayOnly(DateTime value) =>
    DateTime(value.year, value.month, value.day);

Map<DateTime, DailyLogKind> dailyLogMap(List<WorkoutSession> sessions) {
  final result = <DateTime, DailyLogKind>{};
  for (final session in sessions) {
    final day = dayOnly(session.date);
    final isRest = session.workoutType.toLowerCase() == 'rest day';
    if (!isRest) {
      result[day] = DailyLogKind.workout;
    } else {
      result.putIfAbsent(day, () => DailyLogKind.rest);
    }
  }
  return result;
}

StreakSummary calculateStreak(
  List<WorkoutSession> sessions, {
  DateTime? now,
}) {
  final today = dayOnly(now ?? DateTime.now());
  final logs = dailyLogMap(sessions);
  final days = logs.keys.toList()..sort();

  var longest = 0;
  var running = 0;
  DateTime? previous;
  for (final day in days) {
    if (previous != null && day.difference(previous).inDays == 1) {
      running += 1;
    } else {
      running = 1;
    }
    if (running > longest) longest = running;
    previous = day;
  }

  final yesterday = today.subtract(const Duration(days: 1));
  DateTime? cursor;
  if (logs.containsKey(today)) {
    cursor = today;
  } else if (logs.containsKey(yesterday)) {
    cursor = yesterday;
  }

  var current = 0;
  while (cursor != null && logs.containsKey(cursor)) {
    current += 1;
    cursor = cursor.subtract(const Duration(days: 1));
  }

  var restDays = 0;
  var restCursor = logs[today] == DailyLogKind.rest
      ? today
      : (logs[yesterday] == DailyLogKind.rest ? yesterday : null);
  while (restCursor != null && logs[restCursor] == DailyLogKind.rest) {
    restDays += 1;
    restCursor = restCursor.subtract(const Duration(days: 1));
  }

  var missed = 0;
  if (days.isNotEmpty) {
    var missedCursor = yesterday;
    while (!logs.containsKey(missedCursor) &&
        !missedCursor.isBefore(days.first)) {
      missed += 1;
      missedCursor = missedCursor.subtract(const Duration(days: 1));
    }
  }

  final levelInfo = _levelFor(current);
  final todayKind = logs[today];
  final mood = todayKind == DailyLogKind.rest
      ? TrainingAvatarMood.recovery
      : todayKind == DailyLogKind.workout
          ? TrainingAvatarMood.happy
          : missed > 0
              ? TrainingAvatarMood.worried
              : TrainingAvatarMood.happy;

  return StreakSummary(
    currentStreak: current,
    longestStreak: longest,
    consecutiveRestDays: restDays,
    missedDays: missed,
    level: levelInfo.$1,
    levelName: levelInfo.$2,
    daysToNextLevel: levelInfo.$3,
    levelProgress: levelInfo.$4,
    mood: mood,
  );
}

(int, String, int, double) _levelFor(int days) {
  if (days <= 0) return (0, 'Start your streak', 1, 0);

  const levels = <(int, int?, String)>[
    (1, 30, 'Novice'),
    (31, 90, 'Noob Gainer'),
    (91, 150, 'Intermediate Bronze'),
    (151, 210, 'Intermediate Silver'),
    (211, 270, 'Intermediate Gold'),
    (271, 330, 'Advanced'),
    (331, null, 'Athlete'),
  ];

  for (var i = 0; i < levels.length; i++) {
    final start = levels[i].$1;
    final end = levels[i].$2;
    final name = levels[i].$3;
    if (days >= start && (end == null || days <= end)) {
      if (end == null) return (i + 1, name, 0, 1);
      final span = end - start + 1;
      final progress = ((days - start + 1) / span).clamp(0.0, 1.0);
      return (i + 1, name, end - days + 1, progress);
    }
  }
  return (7, 'Athlete', 0, 1);
}
