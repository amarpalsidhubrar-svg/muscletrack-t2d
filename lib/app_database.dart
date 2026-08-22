import 'package:path/path.dart';
import 'package:sqflite/sqflite.dart';

import 'models.dart';

class AppDatabase {
  Database? _database;

  Future<Database> get database async {
    if (_database != null) return _database!;
    final dbPath = join(await getDatabasesPath(), 'muscletrack_v01.db');
    _database = await openDatabase(
      dbPath,
      version: 1,
      onConfigure: (db) async => db.execute('PRAGMA foreign_keys = ON'),
      onCreate: (db, version) async {
        await db.execute('''
          CREATE TABLE profile(
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            sex TEXT NOT NULL,
            height_cm REAL NOT NULL,
            baseline_weight_kg REAL NOT NULL
          )
        ''');
        await db.execute('''
          CREATE TABLE weight_entries(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            weight_kg REAL NOT NULL,
            body_fat_pct REAL,
            lean_mass_kg REAL
          )
        ''');
        await db.execute('''
          CREATE TABLE medications(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            medication_name TEXT NOT NULL,
            medication_class TEXT NOT NULL,
            dose TEXT NOT NULL,
            note TEXT NOT NULL DEFAULT ''
          )
        ''');
        await db.execute('''
          CREATE TABLE workouts(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            workout_type TEXT NOT NULL,
            duration_min INTEGER NOT NULL,
            met REAL,
            source TEXT NOT NULL,
            device_calories REAL
          )
        ''');
        await db.execute('''
          CREATE TABLE exercise_sets(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            workout_id INTEGER NOT NULL,
            exercise_name TEXT NOT NULL,
            set_number INTEGER NOT NULL,
            reps INTEGER NOT NULL,
            weight_kg REAL NOT NULL,
            FOREIGN KEY(workout_id) REFERENCES workouts(id) ON DELETE CASCADE
          )
        ''');
        await db.execute('''
          CREATE TABLE goals(
            id INTEGER PRIMARY KEY,
            target_weight_kg REAL,
            weekly_activity_min INTEGER NOT NULL,
            weekly_strength_sessions INTEGER NOT NULL,
            target_exercise TEXT NOT NULL,
            target_e1rm_kg REAL
          )
        ''');
      },
    );
    return _database!;
  }

  Future<void> saveProfile(UserProfile profile) async {
    final db = await database;
    await db.insert(
      'profile',
      profile.toMap(),
      conflictAlgorithm: ConflictAlgorithm.replace,
    );
  }

  Future<UserProfile?> loadProfile() async {
    final db = await database;
    final rows = await db.query('profile', where: 'id = 1', limit: 1);
    return rows.isEmpty ? null : UserProfile.fromMap(rows.first);
  }

  Future<int> addWeight(WeightEntry entry) async {
    final db = await database;
    return db.insert('weight_entries', entry.toMap());
  }

  Future<List<WeightEntry>> loadWeights() async {
    final db = await database;
    final rows = await db.query('weight_entries', orderBy: 'date DESC');
    return rows.map(WeightEntry.fromMap).toList();
  }

  Future<int> addMedication(MedicationEntry entry) async {
    final db = await database;
    return db.insert('medications', entry.toMap());
  }

  Future<List<MedicationEntry>> loadMedications() async {
    final db = await database;
    final rows = await db.query('medications', orderBy: 'date DESC');
    return rows.map(MedicationEntry.fromMap).toList();
  }

  Future<int> addWorkout(WorkoutSession session) async {
    final db = await database;
    return db.transaction((txn) async {
      final workoutId = await txn.insert('workouts', session.toMap());
      for (final set in session.sets) {
        await txn.insert('exercise_sets', set.toMap(workoutId));
      }
      return workoutId;
    });
  }

  Future<List<WorkoutSession>> loadWorkouts() async {
    final db = await database;
    final workoutRows = await db.query('workouts', orderBy: 'date DESC');
    final result = <WorkoutSession>[];
    for (final row in workoutRows) {
      final workoutId = row['id'] as int;
      final setRows = await db.query(
        'exercise_sets',
        where: 'workout_id = ?',
        whereArgs: [workoutId],
        orderBy: 'exercise_name, set_number',
      );
      result.add(
        WorkoutSession(
          id: workoutId,
          date: DateTime.parse(row['date'] as String),
          workoutType: row['workout_type'] as String,
          durationMin: (row['duration_min'] as num).toInt(),
          met: (row['met'] as num?)?.toDouble(),
          source: row['source'] as String,
          deviceCalories: (row['device_calories'] as num?)?.toDouble(),
          sets: setRows.map(ExerciseSetRecord.fromMap).toList(),
        ),
      );
    }
    return result;
  }

  Future<void> saveGoals(Goals goals) async {
    final db = await database;
    await db.insert(
      'goals',
      goals.toMap(),
      conflictAlgorithm: ConflictAlgorithm.replace,
    );
  }

  Future<Goals> loadGoals() async {
    final db = await database;
    final rows = await db.query('goals', where: 'id = 1', limit: 1);
    return rows.isEmpty ? const Goals() : Goals.fromMap(rows.first);
  }

  Future<void> clearAll() async {
    final db = await database;
    await db.transaction((txn) async {
      await txn.delete('exercise_sets');
      await txn.delete('workouts');
      await txn.delete('medications');
      await txn.delete('weight_entries');
      await txn.delete('goals');
      await txn.delete('profile');
    });
  }
}
