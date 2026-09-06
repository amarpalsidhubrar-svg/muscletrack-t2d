import 'dart:math' as math;

import 'package:flutter/material.dart';

class TreadmillAvatar extends StatefulWidget {
  final double size;

  const TreadmillAvatar({super.key, this.size = 92});

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
      duration: const Duration(milliseconds: 900),
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
        width: widget.size,
        height: widget.size,
        child: AnimatedBuilder(
          animation: _controller,
          builder: (context, _) => CustomPaint(
            painter: _TreadmillPainter(
              progress: _controller.value,
              primary: Theme.of(context).colorScheme.primary,
            ),
          ),
        ),
      ),
    );
  }
}

class _TreadmillPainter extends CustomPainter {
  final double progress;
  final Color primary;

  _TreadmillPainter({
    required this.progress,
    required this.primary,
  });

  @override
  void paint(Canvas canvas, Size size) {
    final w = size.width;
    final h = size.height;
    final dark = const Color(0xFF17312A);
    final soft = const Color(0xFFE6F5EF);

    final bg = Paint()..color = soft;
    canvas.drawRRect(
      RRect.fromRectAndRadius(
        Rect.fromLTWH(0, 0, w, h),
        Radius.circular(w * 0.2),
      ),
      bg,
    );

    final beltY = h * 0.73;
    final belt = Paint()
      ..color = const Color(0xFF40514B)
      ..strokeWidth = h * 0.075
      ..strokeCap = StrokeCap.round;
    canvas.drawLine(
      Offset(w * 0.13, beltY),
      Offset(w * 0.84, beltY),
      belt,
    );

    final rail = Paint()
      ..color = dark
      ..strokeWidth = h * 0.035
      ..strokeCap = StrokeCap.round;
    canvas.drawLine(
      Offset(w * 0.77, beltY - h * 0.02),
      Offset(w * 0.82, h * 0.34),
      rail,
    );
    canvas.drawLine(
      Offset(w * 0.82, h * 0.34),
      Offset(w * 0.93, h * 0.34),
      rail,
    );

    final dashPaint = Paint()
      ..color = Colors.white.withOpacity(0.72)
      ..strokeWidth = h * 0.018
      ..strokeCap = StrokeCap.round;
    for (var i = 0; i < 4; i++) {
      final phase = (i / 4 + progress) % 1;
      final x = w * (0.18 + 0.58 * phase);
      canvas.drawLine(
        Offset(x, beltY),
        Offset(x + w * 0.055, beltY),
        dashPaint,
      );
    }

    final bounce = math.sin(progress * math.pi * 2) * h * 0.018;
    final hip = Offset(w * 0.47, h * 0.49 + bounce);
    final shoulder = Offset(w * 0.47, h * 0.35 + bounce);
    final head = Offset(w * 0.48, h * 0.24 + bounce);

    final bodyPaint = Paint()
      ..color = primary
      ..strokeWidth = h * 0.055
      ..strokeCap = StrokeCap.round;
    final limbPaint = Paint()
      ..color = dark
      ..strokeWidth = h * 0.035
      ..strokeCap = StrokeCap.round;

    canvas.drawCircle(
      head,
      h * 0.065,
      Paint()..color = const Color(0xFFD9A06F),
    );
    canvas.drawLine(shoulder, hip, bodyPaint);

    final swing = math.sin(progress * math.pi * 2);
    final armSwing = swing * w * 0.095;
    final legSwing = swing * w * 0.13;

    canvas.drawLine(
      shoulder,
      Offset(w * 0.39 - armSwing, h * 0.48 + bounce),
      limbPaint,
    );
    canvas.drawLine(
      shoulder,
      Offset(w * 0.58 + armSwing, h * 0.47 + bounce),
      limbPaint,
    );

    canvas.drawLine(
      hip,
      Offset(w * 0.38 - legSwing, h * 0.69),
      limbPaint,
    );
    canvas.drawLine(
      hip,
      Offset(w * 0.59 + legSwing, h * 0.69),
      limbPaint,
    );

    final shoePaint = Paint()
      ..color = primary
      ..strokeWidth = h * 0.025
      ..strokeCap = StrokeCap.round;
    canvas.drawLine(
      Offset(w * 0.33 - legSwing, h * 0.70),
      Offset(w * 0.42 - legSwing, h * 0.70),
      shoePaint,
    );
    canvas.drawLine(
      Offset(w * 0.54 + legSwing, h * 0.70),
      Offset(w * 0.63 + legSwing, h * 0.70),
      shoePaint,
    );
  }

  @override
  bool shouldRepaint(covariant _TreadmillPainter oldDelegate) =>
      oldDelegate.progress != progress || oldDelegate.primary != primary;
}
