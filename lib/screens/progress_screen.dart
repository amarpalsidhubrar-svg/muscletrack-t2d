import 'dart:math' as math;

import 'package:flutter/material.dart';

import '../app_store.dart';
import '../calculations.dart';
import '../models.dart';
import '../widgets/common.dart';
import 'log_weight_screen.dart';

class ProgressScreen extends StatelessWidget {
  final AppStore store;
  const ProgressScreen({super.key, required this.store});

  @override
  Widget build(BuildContext context) {
    final sorted = [...store.weights]..sort((a, b) => a.date.compareTo(b.date));
    final latestLean = store.weights.where((e) => e.leanMassKg != null).toList();
    final latestFat = store.weights.where((e) => e.bodyFatPct != null).toList();
    return ListView(
      padding: const EdgeInsets.fromLTRB(16, 12, 16, 110),
      children: [
        Row(
          children: [
            Expanded(
              child: Text('Progress', style: Theme.of(context).textTheme.headlineSmall?.copyWith(fontWeight: FontWeight.w900)),
            ),
            FilledButton.tonalIcon(
              onPressed: () => Navigator.push(context, MaterialPageRoute(builder: (_) => LogWeightScreen(store: store))),
              icon: const Icon(Icons.add),
              label: const Text('Weight'),
            ),
          ],
        ),
        const SizedBox(height: 16),
        Card(
          child: Padding(
            padding: const EdgeInsets.all(16),
            child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
              Text('Weight trend', style: Theme.of(context).textTheme.titleMedium?.copyWith(fontWeight: FontWeight.w800)),
              const SizedBox(height: 16),
              SizedBox(height: 180, child: WeightChart(entries: sorted)),
              const SizedBox(height: 8),
              Text('${store.currentWeightKg.toStringAsFixed(1)} kg • ${store.weightChangePct.toStringAsFixed(1)}% from baseline', style: Theme.of(context).textTheme.bodySmall),
            ]),
          ),
        ),
        const SectionHeader('Body composition'),
        Row(children: [
          Expanded(child: MetricCard(label: 'Lean mass', value: latestLean.isEmpty ? '—' : '${latestLean.first.leanMassKg!.toStringAsFixed(1)} kg', subtitle: latestLean.isEmpty ? 'Optional entry' : 'Latest entered', icon: Icons.accessibility_new)),
          const SizedBox(width: 10),
          Expanded(child: MetricCard(label: 'Body fat', value: latestFat.isEmpty ? '—' : '${latestFat.first.bodyFatPct!.toStringAsFixed(1)}%', subtitle: latestFat.isEmpty ? 'Optional entry' : 'Latest entered', icon: Icons.pie_chart_outline)),
        ]),
        const SectionHeader('Strength bests'),
        ..._strengthBests(store).map((best) => Card(
          margin: const EdgeInsets.only(bottom: 8),
          child: ListTile(
            leading: const CircleAvatar(child: Icon(Icons.fitness_center, size: 18)),
            title: Text(best.exerciseName),
            subtitle: Text('Best recorded ${shortDate(best.date)}'),
            trailing: Text('${best.e1rmKg.toStringAsFixed(0)} kg e1RM', style: const TextStyle(fontWeight: FontWeight.w800)),
          ),
        )),
        if (_strengthBests(store).isEmpty)
          const Card(child: Padding(padding: EdgeInsets.all(16), child: Text('No strength data yet.'))),
        const SizedBox(height: 14),
        const MonitoringNotice(),
      ],
    );
  }

  List<StrengthBest> _strengthBests(AppStore store) {
    final map = <String, StrengthBest>{};
    for (final workout in store.workouts) {
      for (final set in workout.sets) {
        final value = epleyE1rm(set.weightKg, set.reps);
        final current = map[set.exerciseName.toLowerCase()];
        if (current == null || value > current.e1rmKg) {
          map[set.exerciseName.toLowerCase()] = StrengthBest(
            exerciseName: set.exerciseName,
            e1rmKg: value,
            date: workout.date,
          );
        }
      }
    }
    final list = map.values.toList()..sort((a, b) => b.e1rmKg.compareTo(a.e1rmKg));
    return list.take(6).toList();
  }
}

class WeightChart extends StatelessWidget {
  final List<WeightEntry> entries;
  const WeightChart({super.key, required this.entries});

  @override
  Widget build(BuildContext context) {
    if (entries.length < 2) {
      return Center(child: Text(entries.isEmpty ? 'No weight data yet' : 'Add another weight entry to see a trend'));
    }
    return CustomPaint(
      painter: _WeightChartPainter(entries, Theme.of(context).colorScheme.primary),
      child: const SizedBox.expand(),
    );
  }
}

class _WeightChartPainter extends CustomPainter {
  final List<WeightEntry> entries;
  final Color color;
  _WeightChartPainter(this.entries, this.color);

  @override
  void paint(Canvas canvas, Size size) {
    final values = entries.map((e) => e.weightKg).toList();
    var minV = values.reduce(math.min);
    var maxV = values.reduce(math.max);
    if ((maxV - minV).abs() < 0.1) { minV -= 1; maxV += 1; }
    final grid = Paint()..color = Colors.black12..strokeWidth = 1;
    for (var i = 1; i < 4; i++) {
      final y = size.height * i / 4;
      canvas.drawLine(Offset(0, y), Offset(size.width, y), grid);
    }
    final path = Path();
    for (var i = 0; i < values.length; i++) {
      final x = values.length == 1 ? 0.0 : size.width * i / (values.length - 1);
      final y = size.height - ((values[i] - minV) / (maxV - minV) * size.height);
      if (i == 0) { path.moveTo(x, y); } else { path.lineTo(x, y); }
    }
    canvas.drawPath(path, Paint()..color = color..strokeWidth = 3..style = PaintingStyle.stroke..strokeCap = StrokeCap.round..strokeJoin = StrokeJoin.round);
  }

  @override
  bool shouldRepaint(covariant _WeightChartPainter oldDelegate) => oldDelegate.entries != entries || oldDelegate.color != color;
}
