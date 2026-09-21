import 'dart:math' as math;
import 'package:flutter/material.dart';

import '../streaks.dart';

class TreadmillAvatar extends StatefulWidget {
  final double width;
  final double height;
  final TrainingAvatarMood mood;

  const TreadmillAvatar({
    super.key,
    this.width = 168,
    this.height = 180,
    this.mood = TrainingAvatarMood.happy,
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
            painter: _MoodAvatarPainter(_controller.value, widget.mood),
          ),
        ),
      ),
    );
  }
}

class _MoodAvatarPainter extends CustomPainter {
  final double t;
  final TrainingAvatarMood mood;

  _MoodAvatarPainter(this.t, this.mood);

  static const dark = Color(0xFF17312A);
  static const skin = Color(0xFFD69A72);
  static const green = Color(0xFF0B8C5E);
  static const blue = Color(0xFF397ACB);
  static const amber = Color(0xFFE59A2F);

  Paint _stroke(Color color, double width) => Paint()
    ..color = color
    ..strokeWidth = width
    ..strokeCap = StrokeCap.round
    ..strokeJoin = StrokeJoin.round
    ..style = PaintingStyle.stroke;

  @override
  void paint(Canvas canvas, Size size) {
    final s = math.min(size.width, size.height);
    final c = Offset(size.width * .52, size.height * .54);
    final phase = t * math.pi * 2;

    switch (mood) {
      case TrainingAvatarMood.happy:
        _drawHappy(canvas, c, s, phase);
        break;
      case TrainingAvatarMood.recovery:
        _drawRecovery(canvas, c, s, phase);
        break;
      case TrainingAvatarMood.worried:
        _drawWorried(canvas, c, s, phase);
        break;
    }
  }

  void _halo(Canvas canvas, Offset c, double s, Color color) {
    canvas.drawCircle(c, s * .39, Paint()..color = color.withValues(alpha: .10));
    canvas.drawCircle(c, s * .31, Paint()..color = Colors.white.withValues(alpha: .82));
  }

  void _face(
    Canvas canvas,
    Offset head,
    double r, {
    required String expression,
    bool closedEyes = false,
  }) {
    canvas.drawCircle(head, r, Paint()..color = skin);

    final eye = Paint()
      ..color = dark
      ..strokeWidth = r * .12
      ..strokeCap = StrokeCap.round;

    if (closedEyes) {
      canvas.drawArc(
        Rect.fromCenter(center: head + Offset(-r * .3, -r * .08), width: r * .34, height: r * .18),
        0,
        math.pi,
        false,
        eye..style = PaintingStyle.stroke,
      );
      canvas.drawArc(
        Rect.fromCenter(center: head + Offset(r * .3, -r * .08), width: r * .34, height: r * .18),
        0,
        math.pi,
        false,
        eye,
      );
    } else {
      canvas.drawCircle(head + Offset(-r * .3, -r * .12), r * .075, Paint()..color = dark);
      canvas.drawCircle(head + Offset(r * .3, -r * .12), r * .075, Paint()..color = dark);
    }

    final mouth = Path();
    if (expression == 'happy') {
      mouth.moveTo(head.dx - r * .42, head.dy + r * .16);
      mouth.quadraticBezierTo(head.dx, head.dy + r * .62, head.dx + r * .42, head.dy + r * .16);
    } else if (expression == 'worried') {
      mouth.moveTo(head.dx - r * .35, head.dy + r * .38);
      mouth.quadraticBezierTo(head.dx, head.dy + r * .05, head.dx + r * .35, head.dy + r * .38);
      canvas.drawLine(
        head + Offset(-r * .48, -r * .43),
        head + Offset(-r * .12, -r * .29),
        _stroke(dark, r * .09),
      );
      canvas.drawLine(
        head + Offset(r * .12, -r * .29),
        head + Offset(r * .48, -r * .43),
        _stroke(dark, r * .09),
      );
    } else {
      mouth.moveTo(head.dx - r * .28, head.dy + r * .25);
      mouth.lineTo(head.dx + r * .28, head.dy + r * .25);
    }
    canvas.drawPath(mouth, _stroke(dark, r * .1));
  }

  void _drawHappy(Canvas canvas, Offset c, double s, double phase) {
    _halo(canvas, c, s, green);
    final jump = math.sin(phase).abs() * s * .025;
    final p = c - Offset(0, jump);
    final head = p + Offset(0, -s * .19);
    _face(canvas, head, s * .06, expression: 'happy');

    final torsoTop = p + Offset(0, -s * .11);
    final hip = p + Offset(0, s * .015);
    canvas.drawLine(torsoTop, hip, _stroke(green, s * .062));

    // Deliberately celebratory: both arms high in a wide V.
    canvas.drawLine(
      torsoTop + Offset(-s * .01, s * .01),
      p + Offset(-s * .15, -s * .20),
      _stroke(dark, s * .038),
    );
    canvas.drawLine(
      torsoTop + Offset(s * .01, s * .01),
      p + Offset(s * .15, -s * .20),
      _stroke(dark, s * .038),
    );

    // Legs spread slightly like a small victory jump.
    canvas.drawLine(
      hip,
      p + Offset(-s * .095, s * .15),
      _stroke(dark, s * .04),
    );
    canvas.drawLine(
      hip,
      p + Offset(s * .095, s * .15),
      _stroke(dark, s * .04),
    );

    // Confetti / achievement sparkles.
    for (final item in <(double,double,Color)>[
      (-.24,-.19,Color(0xFFF2B700)),
      (.24,-.16,Color(0xFF31B77B)),
      (-.20,-.04,Color(0xFF62A6F3)),
      (.22,.00,Color(0xFFF06C6C)),
    ]) {
      final q = p + Offset(s * item.$1, s * item.$2);
      canvas.drawCircle(q, s * .015, Paint()..color = item.$3);
    }
  }

  void _drawRecovery(Canvas canvas, Offset c, double s, double phase) {
    _halo(canvas, c, s, blue);
    final p = c + Offset(0, math.sin(phase) * s * .005);
    final head = p + Offset(0, -s * .18);
    _face(canvas, head, s * .058, expression: 'neutral', closedEyes: true);

    canvas.drawLine(
      p + Offset(0, -s * .10),
      p + Offset(0, s * .025),
      _stroke(blue, s * .065),
    );

    final limb = _stroke(dark, s * .037);
    // Hands resting on knees.
    canvas.drawLine(p + Offset(0, -s * .07), p + Offset(-s * .13, s * .045), limb);
    canvas.drawLine(p + Offset(0, -s * .07), p + Offset(s * .13, s * .045), limb);

    final left = Path()
      ..moveTo(p.dx, p.dy + s * .02)
      ..quadraticBezierTo(p.dx - s * .08, p.dy + s * .07, p.dx - s * .17, p.dy + s * .11)
      ..quadraticBezierTo(p.dx - s * .07, p.dy + s * .14, p.dx, p.dy + s * .10);
    final right = Path()
      ..moveTo(p.dx, p.dy + s * .02)
      ..quadraticBezierTo(p.dx + s * .08, p.dy + s * .07, p.dx + s * .17, p.dy + s * .11)
      ..quadraticBezierTo(p.dx + s * .07, p.dy + s * .14, p.dx, p.dy + s * .10);
    canvas.drawPath(left, limb);
    canvas.drawPath(right, limb);

    // Calm breathing waves.
    for (var i = 0; i < 3; i++) {
      canvas.drawArc(
        Rect.fromCircle(center: p, radius: s * (.24 + i * .04)),
        math.pi * 1.05,
        math.pi * .9,
        false,
        Paint()
          ..color = blue.withValues(alpha: .18 - i * .04)
          ..style = PaintingStyle.stroke
          ..strokeWidth = 2,
      );
    }
  }

  void _drawWorried(Canvas canvas, Offset c, double s, double phase) {
    _halo(canvas, c, s, amber);
    final p = c + Offset(0, s * .04);
    final head = p + Offset(-s * .015, -s * .11);
    _face(canvas, head, s * .061, expression: 'worried');

    // Slumped seated pose: intentionally very different from the happy state.
    final shoulder = p + Offset(-s * .02, -s * .04);
    final hip = p + Offset(0, s * .075);
    canvas.drawLine(
      shoulder,
      hip,
      _stroke(const Color(0xFF7B817E), s * .06),
    );

    // One hand holding the head, the other resting on the knee.
    canvas.drawLine(
      shoulder,
      head + Offset(s * .05, -s * .01),
      _stroke(dark, s * .038),
    );
    canvas.drawLine(
      shoulder + Offset(0, s * .015),
      p + Offset(-s * .14, s * .10),
      _stroke(dark, s * .038),
    );

    // Bent legs / seated posture.
    canvas.drawLine(
      hip,
      p + Offset(-s * .11, s * .14),
      _stroke(dark, s * .042),
    );
    canvas.drawLine(
      p + Offset(-s * .11, s * .14),
      p + Offset(-s * .02, s * .19),
      _stroke(dark, s * .042),
    );
    canvas.drawLine(
      hip,
      p + Offset(s * .11, s * .14),
      _stroke(dark, s * .042),
    );
    canvas.drawLine(
      p + Offset(s * .11, s * .14),
      p + Offset(s * .18, s * .18),
      _stroke(dark, s * .042),
    );

    // Sweat drop and floating question mark make the state unmistakable.
    final sweat = Path()
      ..moveTo(head.dx + s * .075, head.dy - s * .045)
      ..quadraticBezierTo(
        head.dx + s * .11,
        head.dy,
        head.dx + s * .075,
        head.dy + s * .025,
      )
      ..quadraticBezierTo(
        head.dx + s * .04,
        head.dy,
        head.dx + s * .075,
        head.dy - s * .045,
      );
    canvas.drawPath(sweat, Paint()..color = const Color(0xFF62A6F3));

    final q = TextPainter(
      text: const TextSpan(
        text: '?',
        style: TextStyle(
          color: amber,
          fontSize: 30,
          fontWeight: FontWeight.w900,
        ),
      ),
      textDirection: TextDirection.ltr,
    )..layout();
    q.paint(canvas, p + Offset(s * .18, -s * .20 + math.sin(phase) * 2));
  }

  @override
  bool shouldRepaint(covariant _MoodAvatarPainter oldDelegate) =>
      oldDelegate.t != t || oldDelegate.mood != mood;
}
