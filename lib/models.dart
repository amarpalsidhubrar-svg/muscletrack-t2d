class UserProfile {
  final String name;
  final int age;
  final String sex;
  final double heightCm;
  final double baselineWeightKg;

  const UserProfile({
    required this.name,
    required this.age,
    required this.sex,
    required this.heightCm,
    required this.baselineWeightKg,
  });

  Map<String, Object?> toMap() => {
        'id': 1,
        'name': name,
        'age': age,
        'sex': sex,
        'height_cm': heightCm,
        'baseline_weight_kg': baselineWeightKg,
      };

  factory UserProfile.fromMap(Map<String, Object?> map) => UserProfile(
        name: (map['name'] as String?) ?? '',
        age: (map['age'] as num).toInt(),
        sex: map['sex'] as String,
        heightCm: (map['height_cm'] as num).toDouble(),
        baselineWeightKg: (map['baseline_weight_kg'] as num).toDouble(),
      );
}

class WeightEntry {
  final int? id;
  final DateTime date;
  final double weightKg;
  final double? bodyFatPct;
  final double? leanMassKg;

  const WeightEntry({
    this.id,
    required this.date,
    required this.weightKg,
    this.bodyFatPct,
    this.leanMassKg,
  });

  Map<String, Object?> toMap() => {
        if (id != null) 'id': id,
        'date': date.toIso8601String(),
        'weight_kg': weightKg,
        'body_fat_pct': bodyFatPct,
        'lean_mass_kg': leanMassKg,
      };

  factory WeightEntry.fromMap(Map<String, Object?> map) => WeightEntry(
        id: map['id'] as int?,
        date: DateTime.parse(map['date'] as String),
        weightKg: (map['weight_kg'] as num).toDouble(),
        bodyFatPct: (map['body_fat_pct'] as num?)?.toDouble(),
        leanMassKg: (map['lean_mass_kg'] as num?)?.toDouble(),
      );
}

class MedicationEntry {
  final int? id;
  final DateTime date;
  final String medicationName;
  final String medicationClass;
  final String dose;
  final String note;

  const MedicationEntry({
    this.id,
    required this.date,
    required this.medicationName,
    required this.medicationClass,
    required this.dose,
    this.note = '',
  });

  Map<String, Object?> toMap() => {
        if (id != null) 'id': id,
        'date': date.toIso8601String(),
        'medication_name': medicationName,
        'medication_class': medicationClass,
        'dose': dose,
        'note': note,
      };

  factory MedicationEntry.fromMap(Map<String, Object?> map) => MedicationEntry(
        id: map['id'] as int?,
        date: DateTime.parse(map['date'] as String),
        medicationName: map['medication_name'] as String,
        medicationClass: map['medication_class'] as String,
        dose: map['dose'] as String,
        note: (map['note'] as String?) ?? '',
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
  final double? deviceCalories;
  final List<ExerciseSetRecord> sets;

  const WorkoutSession({
    this.id,
    required this.date,
    required this.workoutType,
    required this.durationMin,
    this.met,
    this.source = 'Manual entry',
    this.deviceCalories,
    this.sets = const [],
  });

  Map<String, Object?> toMap() => {
        if (id != null) 'id': id,
        'date': date.toIso8601String(),
        'workout_type': workoutType,
        'duration_min': durationMin,
        'met': met,
        'source': source,
        'device_calories': deviceCalories,
      };
}

class Goals {
  final double? targetWeightKg;
  final int weeklyActivityMin;
  final int weeklyStrengthSessions;
  final String targetExercise;
  final double? targetE1rmKg;

  const Goals({
    this.targetWeightKg,
    this.weeklyActivityMin = 150,
    this.weeklyStrengthSessions = 2,
    this.targetExercise = '',
    this.targetE1rmKg,
  });

  Map<String, Object?> toMap() => {
        'id': 1,
        'target_weight_kg': targetWeightKg,
        'weekly_activity_min': weeklyActivityMin,
        'weekly_strength_sessions': weeklyStrengthSessions,
        'target_exercise': targetExercise,
        'target_e1rm_kg': targetE1rmKg,
      };

  factory Goals.fromMap(Map<String, Object?> map) => Goals(
        targetWeightKg: (map['target_weight_kg'] as num?)?.toDouble(),
        weeklyActivityMin: (map['weekly_activity_min'] as num?)?.toInt() ?? 150,
        weeklyStrengthSessions:
            (map['weekly_strength_sessions'] as num?)?.toInt() ?? 2,
        targetExercise: (map['target_exercise'] as String?) ?? '',
        targetE1rmKg: (map['target_e1rm_kg'] as num?)?.toDouble(),
      );
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
