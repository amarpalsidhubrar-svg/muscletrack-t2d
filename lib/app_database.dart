import 'dart:io';

import 'package:path/path.dart';
import 'package:sqflite/sqflite.dart';

import 'models.dart';

class AppDatabase {
  Database? _database;

  Future<String> get _newPath async =>
      join(await getDatabasesPath(), 'muscletrack_v03.db');

  Future<String> get _oldPath async =>
      join(await getDatabasesPath(), 'muscletrack_v01.db');

  Future<Database> get database async {
    if (_database != null) return _database!;

    final newPath = await _newPath;
    final wasNew = !await databaseExists(newPath);

    _database = await openDatabase(
      newPath,
      version: 1,
      onConfigure: (db) async => db.execute('PRAGMA foreign_keys = ON'),
      onCreate: (db, version) async {
        await db.execute('''
          CREATE TABLE profile(
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL
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
            fatigue INTEGER,
            sleep_quality INTEGER,
            muscle_soreness INTEGER,
            discomfort INTEGER,
            readiness INTEGER,
            sleep_hours REAL,
            session_rpe INTEGER,
            notes TEXT NOT NULL DEFAULT ''
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
      },
    );

    if (wasNew) {
      await _migrateLegacyWorkoutData(_database!);
    }

    return _database!;
  }

  Future<void> _migrateLegacyWorkoutData(Database target) async {
    final oldPath = await _oldPath;
    if (!await databaseExists(oldPath)) return;

    Database? oldDb;
    try {
      oldDb = await openDatabase(oldPath, readOnly: true);

      final profileRows = await oldDb.query('profile', where: 'id = 1', limit: 1);
      if (profileRows.isNotEmpty) {
        final name = (profileRows.first['name'] as String?)?.trim() ?? '';
        if (name.isNotEmpty) {
          await target.insert(
            'profile',
            {'id': 1, 'name': name},
            conflictAlgorithm: ConflictAlgorithm.replace,
          );
        }
      }

      final columns = await oldDb.rawQuery('PRAGMA table_info(workouts)');
      final available = columns
          .map((row) => row['name'] as String?)
          .whereType<String>()
          .toSet();

      Object? read(Map<String, Object?> row, String key) =>
          available.contains(key) ? row[key] : null;

      final workoutRows = await oldDb.query('workouts', orderBy: 'date ASC');
      for (final row in workoutRows) {
        final oldWorkoutId = row['id'] as int;
        final newWorkoutId = await target.insert('workouts', {
          'date': row['date'],
          'workout_type': row['workout_type'],
          'duration_min': row['duration_min'],
          'met': read(row, 'met'),
          'source': read(row, 'source') ?? 'Manual entry',
          'fatigue': read(row, 'fatigue'),
          'sleep_quality': read(row, 'sleep_quality'),
          'muscle_soreness': read(row, 'muscle_soreness'),
          'discomfort': read(row, 'discomfort'),
          'readiness': read(row, 'readiness'),
          'sleep_hours': read(row, 'sleep_hours'),
          'session_rpe': read(row, 'session_rpe'),
          'notes': read(row, 'notes') ?? '',
        });

        final setRows = await oldDb.query(
          'exercise_sets',
          where: 'workout_id = ?',
          whereArgs: [oldWorkoutId],
          orderBy: 'exercise_name, set_number',
        );
        for (final set in setRows) {
          await target.insert('exercise_sets', {
            'workout_id': newWorkoutId,
            'exercise_name': set['exercise_name'],
            'set_number': set['set_number'],
            'reps': set['reps'],
            'weight_kg': set['weight_kg'],
          });
        }
      }
    } catch (_) {
      // A legacy database is optional; a clean Version 0.3 database remains usable.
    } finally {
      await oldDb?.close();
    }
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

  Future<void> updateWorkout(WorkoutSession session) async {
    if (session.id == null) return;
    final db = await database;
    await db.transaction((txn) async {
      final values = session.toMap()..remove('id');
      await txn.update(
        'workouts',
        values,
        where: 'id = ?',
        whereArgs: [session.id],
      );
      await txn.delete(
        'exercise_sets',
        where: 'workout_id = ?',
        whereArgs: [session.id],
      );
      for (final set in session.sets) {
        await txn.insert('exercise_sets', set.toMap(session.id!));
      }
    });
  }

  Future<void> deleteWorkout(int workoutId) async {
    final db = await database;
    await db.delete('workouts', where: 'id = ?', whereArgs: [workoutId]);
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
          source: (row['source'] as String?) ?? 'Manual entry',
          fatigue: (row['fatigue'] as num?)?.toInt(),
          sleepQuality: (row['sleep_quality'] as num?)?.toInt(),
          muscleSoreness: (row['muscle_soreness'] as num?)?.toInt(),
          discomfort: (row['discomfort'] as num?)?.toInt(),
          readiness: (row['readiness'] as num?)?.toInt(),
          sleepHours: (row['sleep_hours'] as num?)?.toDouble(),
          sessionRpe: (row['session_rpe'] as num?)?.toInt(),
          notes: (row['notes'] as String?) ?? '',
          sets: setRows.map(ExerciseSetRecord.fromMap).toList(),
        ),
      );
    }
    return result;
  }

  Future<void> clearAll() async {
    final db = await database;
    await db.transaction((txn) async {
      await txn.delete('exercise_sets');
      await txn.delete('workouts');
      await txn.delete('profile');
    });

    final oldPath = await _oldPath;
    if (await File(oldPath).exists()) {
      await deleteDatabase(oldPath);
    }
  }
}
