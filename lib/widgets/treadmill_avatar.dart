import 'dart:math' as math;

import 'package:flutter/material.dart';

class TreadmillAvatar extends StatefulWidget {
  final double width;
  final double height;

  const TreadmillAvatar({
    super.key,
    this.width = 180,
    this.height = 160,
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
      duration: const Duration(milliseconds: 820),
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
          builder: (context, _) => CustomPaint(
            painter: _RunnerPainter(progress: _controller.value),
          ),
        ),
      ),
    );
  }
}

class _RunnerPainter extends CustomPainter {
  final double progress;
  const _RunnerPainter({required this.progress});

  @override
  void paint(Canvas canvas, Size size) {
    final w = size.width;
    final h = size.height;
    final phase = progress * math.pi * 2;
    final swing = math.sin(phase);
    final bounce = math.sin(phase * 2) * h * 0.012;

    final skin = const Color(0xFFD69A6A);
    final skinDark = const Color(0xFFB9794C);
    final hair = const Color(0xFF2C211B);
    final shirt = const Color(0xFF31393C);
    final shorts = const Color(0xFF20272A);
    final shoe = const Color(0xFFF7F7F5);
    final treadmill = const Color(0xFF343B3D);
    final treadmillDark = const Color(0xFF202628);
    final accent = const Color(0xFF087B55);

    // Ground shadow.
    canvas.drawOval(
      Rect.fromCenter(
        center: Offset(w * 0.58, h * 0.86),
        width: w * 0.72,
        height: h * 0.08,
      ),
      Paint()..color = const Color(0x18000000),
    );

    // Treadmill base and supports.
    final beltY = h * 0.76;
    final beltPaint = Paint()
      ..color = treadmill
      ..strokeWidth = h * 0.075
      ..strokeCap = StrokeCap.round;
    canvas.drawLine(Offset(w * 0.12, beltY), Offset(w * 0.88, beltY), beltPaint);

    final beltHighlight = Paint()
      ..color = const Color(0xFF596164)
      ..strokeWidth = h * 0.018
      ..strokeCap = StrokeCap.round;
    canvas.drawLine(
      Offset(w * 0.16, beltY - h * 0.012),
      Offset(w * 0.84, beltY - h * 0.012),
      beltHighlight,
    );

    final framePaint = Paint()
      ..color = treadmillDark
      ..strokeWidth = h * 0.034
      ..strokeCap = StrokeCap.round;
    canvas.drawLine(
      Offset(w * 0.77, beltY),
      Offset(w * 0.82, h * 0.35),
      framePaint,
    );
    canvas.drawLine(
      Offset(w * 0.82, h * 0.35),
      Offset(w * 0.95, h * 0.35),
      framePaint,
    );

    canvas.drawRRect(
      RRect.fromRectAndRadius(
        Rect.fromLTWH(w * 0.78, h * 0.24, w * 0.17, h * 0.13),
        Radius.circular(w * 0.025),
      ),
      Paint()..color = const Color(0xFF41494B),
    );
    canvas.drawRRect(
      RRect.fromRectAndRadius(
        Rect.fromLTWH(w * 0.81, h * 0.27, w * 0.11, h * 0.055),
        Radius.circular(w * 0.012),
      ),
      Paint()..color = const Color(0xFFB9D7CE),
    );

    // Moving belt markers.
    for (var i = 0; i < 5; i++) {
      final x = w * (0.13 + (((i / 5) + progress) % 1) * 0.68);
      canvas.drawLine(
        Offset(x, beltY),
        Offset(x + w * 0.045, beltY),
        Paint()
          ..color = const Color(0x80FFFFFF)
          ..strokeWidth = h * 0.012
          ..strokeCap = StrokeCap.round,
      );
    }

    // Body landmarks.
    final headCenter = Offset(w * 0.43, h * 0.22 + bounce);
    final shoulder = Offset(w * 0.43, h * 0.34 + bounce);
    final hip = Offset(w * 0.46, h * 0.52 + bounce);

    // Neck.
    canvas.drawRRect(
      RRect.fromRectAndRadius(
        Rect.fromCenter(
          center: Offset(w * 0.43, h * 0.285 + bounce),
          width: w * 0.045,
          height: h * 0.07,
        ),
        Radius.circular(w * 0.018),
      ),
      Paint()..color = skin,
    );

    // Head with subtle face shadow.
    canvas.drawOval(
      Rect.fromCenter(center: headCenter, width: w * 0.12, height: h * 0.15),
      Paint()..color = skin,
    );
    canvas.drawArc(
      Rect.fromCenter(center: headCenter, width: w * 0.12, height: h * 0.15),
      -math.pi / 2,
      math.pi,
      true,
      Paint()..color = skinDark.withOpacity(0.18),
    );

    // Hair.
    final hairPath = Path()
      ..moveTo(w * 0.37, h * 0.20 + bounce)
      ..quadraticBezierTo(w * 0.40, h * 0.12 + bounce, w * 0.48, h * 0.15 + bounce)
      ..quadraticBezierTo(w * 0.51, h * 0.17 + bounce, w * 0.49, h * 0.22 + bounce)
      ..quadraticBezierTo(w * 0.43, h * 0.17 + bounce, w * 0.37, h * 0.20 + bounce)
      ..close();
    canvas.drawPath(hairPath, Paint()..color = hair);

    // Ear and face details.
    canvas.drawCircle(
      Offset(w * 0.49, h * 0.23 + bounce),
      w * 0.012,
      Paint()..color = skinDark,
    );
    canvas.drawCircle(
      Offset(w * 0.462, h * 0.215 + bounce),
      w * 0.006,
      Paint()..color = const Color(0xFF201B18),
    );
    canvas.drawLine(
      Offset(w * 0.477, h * 0.245 + bounce),
      Offset(w * 0.493, h * 0.247 + bounce),
      Paint()
        ..color = const Color(0xFF8F4C3E)
        ..strokeWidth = 1.4
        ..strokeCap = StrokeCap.round,
    );

    // Torso shirt.
    final torso = Path()
      ..moveTo(w * 0.36, h * 0.33 + bounce)
      ..quadraticBezierTo(w * 0.43, h * 0.30 + bounce, w * 0.50, h * 0.34 + bounce)
      ..lineTo(w * 0.53, h * 0.52 + bounce)
      ..quadraticBezierTo(w * 0.46, h * 0.56 + bounce, w * 0.39, h * 0.52 + bounce)
      ..close();
    canvas.drawPath(torso, Paint()..color = shirt);

    // Shorts.
    canvas.drawRRect(
      RRect.fromRectAndRadius(
        Rect.fromLTWH(w * 0.39, h * 0.49 + bounce, w * 0.14, h * 0.11),
        Radius.circular(w * 0.028),
      ),
      Paint()..color = shorts,
    );

    // Arms: use upper/lower segments for a more natural running posture.
    final armSwing = swing * w * 0.075;
    _drawLimb(
      canvas,
      shoulder + Offset(-w * 0.045, h * 0.015),
      Offset(w * 0.33 - armSwing, h * 0.43 + bounce),
      Offset(w * 0.38 - armSwing, h * 0.51 + bounce),
      skin,
      h * 0.034,
    );
    _drawLimb(
      canvas,
      shoulder + Offset(w * 0.04, h * 0.012),
      Offset(w * 0.53 + armSwing, h * 0.40 + bounce),
      Offset(w * 0.59 + armSwing, h * 0.35 + bounce),
      skin,
      h * 0.034,
    );

    // Legs.
    final legSwing = swing * w * 0.115;
    final knee1 = Offset(w * 0.38 - legSwing, h * 0.64 + bounce);
    final foot1 = Offset(w * 0.29 - legSwing * 0.65, h * 0.74);
    final knee2 = Offset(w * 0.53 + legSwing, h * 0.63 + bounce);
    final foot2 = Offset(w * 0.61 + legSwing * 0.7, h * 0.74);

    _drawLimb(
      canvas,
      hip + Offset(-w * 0.035, 0),
      knee1,
      foot1,
      skin,
      h * 0.045,
    );
    _drawLimb(
      canvas,
      hip + Offset(w * 0.045, 0),
      knee2,
      foot2,
      skin,
      h * 0.045,
    );

    // Shoes.
    _drawShoe(canvas, foot1, shoe, accent, facingRight: false, h: h, w: w);
    _drawShoe(canvas, foot2, shoe, accent, facingRight: true, h: h, w: w);
  }

  void _drawLimb(
    Canvas canvas,
    Offset start,
    Offset joint,
    Offset end,
    Color color,
    double width,
  ) {
    final paint = Paint()
      ..color = color
      ..strokeWidth = width
      ..strokeCap = StrokeCap.round
      ..strokeJoin = StrokeJoin.round;
    canvas.drawLine(start, joint, paint);
    canvas.drawLine(joint, end, paint);
    canvas.drawCircle(joint, width * 0.42, Paint()..color = color);
  }

  void _drawShoe(
    Canvas canvas,
    Offset foot,
    Color base,
    Color accent, {
    required bool facingRight,
    required double h,
    required double w,
  }) {
    final direction = facingRight ? 1.0 : -1.0;
    final rect = Rect.fromCenter(
      center: foot + Offset(direction * w * 0.015, 0),
      width: w * 0.10,
      height: h * 0.035,
    );
    canvas.drawRRect(
      RRect.fromRectAndRadius(rect, Radius.circular(h * 0.018)),
      Paint()..color = base,
    );
    canvas.drawLine(
      Offset(rect.left + w * 0.02, rect.bottom - h * 0.007),
      Offset(rect.right - w * 0.02, rect.bottom - h * 0.007),
      Paint()
        ..color = accent
        ..strokeWidth = h * 0.006
        ..strokeCap = StrokeCap.round,
    );
  }

  @override
  bool shouldRepaint(covariant _RunnerPainter oldDelegate) =>
      oldDelegate.progress != progress;
}
