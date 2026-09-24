class UserProfile {
  final String name;

  const UserProfile({required this.name});

  Map<String, Object?> toMap() => {
        'id': 1,
        'name': name,
      };

  factory UserProfile.fromMap(Map<String, Object?> map) => UserProfile(
        name: (map['name'] as String?) ?? '',
      );
}

class ExerciseSetRecord {
  final int? id;
  final int? workoutId;
  final String exerciseName;
  final int setNumber;
  final int reps;
  final double weightKg;

  const ExerciseSetRecord({
    this.id,
    this.workoutId,
    required this.exerciseName,
    required this.setNumber,
    required this.reps,
    required this.weightKg,
  });

  Map<String, Object?> toMap(int parentWorkoutId) => {
        if (id != null) 'id': id,
        'workout_id': parentWorkoutId,
        'exercise_name': exerciseName,
        'set_number': setNumber,
        'reps': reps,
        'weight_kg': weightKg,
      };

  factory ExerciseSetRecord.fromMap(Map<String, Object?> map) => ExerciseSetRecord(
        id: map['id'] as int?,
        workoutId: map['workout_id'] as int?,
        exerciseName: map['exercise_name'] as String,
        setNumber: (map['set_number'] as num).toInt(),
        reps: (map['reps'] as num).toInt(),
        weightKg: (map['weight_kg'] as num).toDouble(),
      );
}

class WorkoutSession {
  final int? id;
  final DateTime date;
  final String workoutType;
  final int durationMin;
  final double? met;
  final String source;
  final int? fatigue;
  final int? sleepQuality;
  final int? muscleSoreness;
  final int? discomfort;
  final int? readiness;
  final double? sleepHours;
  final int? sessionRpe;
  final String notes;
  final List<ExerciseSetRecord> sets;

  const WorkoutSession({
    this.id,
    required this.date,
    required this.workoutType,
    required this.durationMin,
    this.met,
    this.source = 'Manual entry',
    this.fatigue,
    this.sleepQuality,
    this.muscleSoreness,
    this.discomfort,
    this.readiness,
    this.sleepHours,
    this.sessionRpe,
    this.notes = '',
    this.sets = const [],
  });

  Map<String, Object?> toMap() => {
        if (id != null) 'id': id,
        'date': date.toIso8601String(),
        'workout_type': workoutType,
        'duration_min': durationMin,
        'met': met,
        'source': source,
        'fatigue': fatigue,
        'sleep_quality': sleepQuality,
        'muscle_soreness': muscleSoreness,
        'discomfort': discomfort,
        'readiness': readiness,
        'sleep_hours': sleepHours,
        'session_rpe': sessionRpe,
        'notes': notes,
      };
}

class StrengthBest {
  final String exerciseName;
  final double e1rmKg;
  final DateTime date;

  const StrengthBest({
    required this.exerciseName,
    required this.e1rmKg,
    required this.date,
  });
}
