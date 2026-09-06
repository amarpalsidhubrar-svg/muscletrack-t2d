#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
widget = ROOT / 'lib/widgets/treadmill_avatar.dart'
widget.write_text(r'''import 'dart:math' as math;
import 'package:flutter/material.dart';

/// Lightweight animated activity badge used in the dashboard hero card.
/// Kept under the historical class name so the Home screen needs no API change.
class TreadmillAvatar extends StatefulWidget {
  final double width;
  final double height;

  const TreadmillAvatar({
    super.key,
    this.width = 168,
    this.height = 180,
  });

  @override
  State<TreadmillAvatar> createState() => _TreadmillAvatarState();
}

class _TreadmillAvatarState extends State<TreadmillAvatar>
    with SingleTickerProviderStateMixin {
  late final AnimationController _controller;

  @override
  void initState() {
    super.initState();
    _controller = AnimationController(
      vsync: this,
      duration: const Duration(milliseconds: 2400),
    )..repeat();
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return RepaintBoundary(
      child: SizedBox(
        width: widget.width,
        height: widget.height,
        child: AnimatedBuilder(
          animation: _controller,
          builder: (_, __) => CustomPaint(
            painter: _ActivityPulsePainter(_controller.value),
          ),
        ),
      ),
    );
  }
}

class _ActivityPulsePainter extends CustomPainter {
  final double t;
  _ActivityPulsePainter(this.t);

  @override
  void paint(Canvas canvas, Size size) {
    final w = size.width;
    final h = size.height;
    final centre = Offset(w * .50, h * .48);
    final minSide = math.min(w, h);

    const green = Color(0xFF0B8C5E);
    const darkGreen = Color(0xFF087652);
    const mint = Color(0xFFDDF5E9);
    const mint2 = Color(0xFFBEEBD7);
    const pale = Color(0xFFF3FBF7);

    // Soft halo behind the badge.
    canvas.drawCircle(
      centre,
      minSide * .43,
      Paint()..color = const Color(0x120B8C5E),
    );

    // Breathing outer pulse rings.
    for (var i = 0; i < 3; i++) {
      final p = (t + i / 3) % 1.0;
      final radius = minSide * (.28 + p * .13);
      final opacity = ((1 - p) * 0.20).clamp(0.0, 0.20);
      canvas.drawCircle(
        centre,
        radius,
        Paint()
          ..color = green.withOpacity(opacity)
          ..style = PaintingStyle.stroke
          ..strokeWidth = minSide * .016,
      );
    }

    // Main badge background.
    canvas.drawCircle(
      centre,
      minSide * .295,
      Paint()..color = pale,
    );
    canvas.drawCircle(
      centre,
      minSide * .268,
      Paint()
        ..color = mint
        ..style = PaintingStyle.stroke
        ..strokeWidth = minSide * .030,
    );

    // Progress ring rotates slowly to keep the visual alive without distraction.
    final start = -math.pi / 2 + t * math.pi * 2;
    final progressRect = Rect.fromCircle(
      center: centre,
      radius: minSide * .268,
    );
    canvas.drawArc(
      progressRect,
      start,
      math.pi * 1.15,
      false,
      Paint()
        ..shader = const SweepGradient(
          colors: [green, Color(0xFF4CC493), green],
        ).createShader(progressRect)
        ..style = PaintingStyle.stroke
        ..strokeWidth = minSide * .030
        ..strokeCap = StrokeCap.round,
    );

    // Inner white disc.
    canvas.drawCircle(
      centre,
      minSide * .205,
      Paint()..color = Colors.white,
    );
    canvas.drawCircle(
      centre,
      minSide * .205,
      Paint()
        ..color = const Color(0x160B8C5E)
        ..style = PaintingStyle.stroke
        ..strokeWidth = 1,
    );

    // Animated runner icon. The whole mark shifts subtly to imply motion.
    final phase = t * math.pi * 2;
    final bob = math.sin(phase * 2) * minSide * .010;
    final swing = math.sin(phase) * minSide * .028;
    final iconCentre = centre + Offset(0, bob);

    final stroke = Paint()
      ..color = darkGreen
      ..strokeWidth = minSide * .038
      ..strokeCap = StrokeCap.round
      ..strokeJoin = StrokeJoin.round
      ..style = PaintingStyle.stroke;

    // Head.
    canvas.drawCircle(
      iconCentre + Offset(minSide * .055, -minSide * .095),
      minSide * .035,
      Paint()..color = darkGreen,
    );

    // Torso diagonal.
    final shoulder = iconCentre + Offset(minSide * .020, -minSide * .045);
    final hip = iconCentre + Offset(-minSide * .010, minSide * .045);
    canvas.drawLine(shoulder, hip, stroke);

    // Arms.
    canvas.drawLine(
      shoulder,
      iconCentre + Offset(-minSide * .070 - swing, minSide * .005),
      stroke,
    );
    canvas.drawLine(
      shoulder + Offset(minSide * .008, minSide * .006),
      iconCentre + Offset(minSide * .095 + swing, -minSide * .005),
      stroke,
    );

    // Legs.
    canvas.drawLine(
      hip,
      iconCentre + Offset(-minSide * .085 - swing * .7, minSide * .125),
      stroke,
    );
    canvas.drawLine(
      hip,
      iconCentre + Offset(minSide * .100 + swing * .7, minSide * .095),
      stroke,
    );

    // Small energy sparks orbit around the badge.
    for (var i = 0; i < 3; i++) {
      final angle = t * math.pi * 2 + i * math.pi * 2 / 3;
      final r = minSide * .355;
      final dot = centre + Offset(math.cos(angle) * r, math.sin(angle) * r);
      canvas.drawCircle(
        dot,
        minSide * .014,
        Paint()..color = i == 1 ? mint2 : green.withOpacity(.55),
      );
    }
  }

  @override
  bool shouldRepaint(covariant _ActivityPulsePainter oldDelegate) =>
      oldDelegate.t != t;
}
''')

# Version bump for the new test build.
pubspec = ROOT / 'pubspec.yaml'
p = pubspec.read_text()
for old in ['version: 0.2.5+6', 'version: 0.2.4+5', 'version: 0.2.3+4']:
    if old in p:
        p = p.replace(old, 'version: 0.2.7+8')
        break
pubspec.write_text(p)

print('Applied Option 2 activity pulse dashboard animation')
