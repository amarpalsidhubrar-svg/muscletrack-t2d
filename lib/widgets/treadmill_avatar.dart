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
      duration: const Duration(milliseconds: 2600),
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

  static const green = Color(0xFF087B55);
  static const dark = Color(0xFF17312A);
  static const skin = Color(0xFFD69A72);
  static const shirt = Color(0xFF0B8C5E);
  static const shorts = Color(0xFF203A34);

  @override
  void paint(Canvas canvas, Size size) {
    final centre = Offset(size.width * .52, size.height * .52);
    final s = math.min(size.width, size.height);
    final phase = t * math.pi * 2;

    _drawBackground(canvas, centre, s);

    switch (mood) {
      case TrainingAvatarMood.happy:
        _drawHappy(canvas, centre, s, phase);
        break;
      case TrainingAvatarMood.recovery:
        _drawRecovery(canvas, centre, s, phase);
        break;
      case TrainingAvatarMood.worried:
        _drawWorried(canvas, centre, s, phase);
        break;
    }
  }

  void _drawBackground(Canvas canvas, Offset c, double s) {
    final halo = switch (mood) {
      TrainingAvatarMood.happy => const Color(0x2231B77B),
      TrainingAvatarMood.recovery => const Color(0x222F80ED),
      TrainingAvatarMood.worried => const Color(0x22E6A23C),
    };
    canvas.drawCircle(c, s * .39, Paint()..color = halo);
    canvas.drawCircle(
      c,
      s * .31,
      Paint()
        ..color = Colors.white.withValues(alpha: .78)
        ..style = PaintingStyle.fill,
    );
  }

  Paint _stroke(Color color, double width) => Paint()
    ..color = color
    ..strokeWidth = width
    ..strokeCap = StrokeCap.round
    ..strokeJoin = StrokeJoin.round
    ..style = PaintingStyle.stroke;

  void _face(
    Canvas canvas,
    Offset head,
    double r, {
    required bool smile,
    bool closedEyes = false,
    bool worried = false,
  }) {
    canvas.drawCircle(head, r, Paint()..color = skin);
    final eye = Paint()
      ..color = dark
      ..strokeWidth = r * .12
      ..strokeCap = StrokeCap.round;

    if (closedEyes) {
      canvas.drawLine(
        head + Offset(-r * .48, -r * .08),
        head + Offset(-r * .18, -r * .08),
        eye,
      );
      canvas.drawLine(
        head + Offset(r * .18, -r * .08),
        head + Offset(r * .48, -r * .08),
        eye,
      );
    } else {
      canvas.drawCircle(head + Offset(-r * .3, -r * .12), r * .08, eye);
      canvas.drawCircle(head + Offset(r * .3, -r * .12), r * .08, eye);
    }

    final mouth = Path();
    if (smile) {
      mouth.moveTo(head.dx - r * .38, head.dy + r * .2);
      mouth.quadraticBezierTo(
        head.dx,
        head.dy + r * .55,
        head.dx + r * .38,
        head.dy + r * .2,
      );
    } else if (worried) {
      mouth.moveTo(head.dx - r * .35, head.dy + r * .38);
      mouth.quadraticBezierTo(
        head.dx,
        head.dy + r * .08,
        head.dx + r * .35,
        head.dy + r * .38,
      );
    } else {
      mouth.moveTo(head.dx - r * .3, head.dy + r * .26);
      mouth.lineTo(head.dx + r * .3, head.dy + r * .26);
    }
    canvas.drawPath(mouth, _stroke(dark, r * .1));

    if (worried) {
      canvas.drawLine(
        head + Offset(-r * .48, -r * .42),
        head + Offset(-r * .15, -r * .3),
        _stroke(dark, r * .09),
      );
      canvas.drawLine(
        head + Offset(r * .15, -r * .3),
        head + Offset(r * .48, -r * .42),
        _stroke(dark, r * .09),
      );
    }
  }

  void _drawHappy(Canvas canvas, Offset c, double s, double phase) {
    final bob = math.sin(phase * 2) * s * .012;
    final p = c + Offset(0, bob);
    final head = p + Offset(s * .06, -s * .18);
    _face(canvas, head, s * .055, smile: true);

    final body = _stroke(shirt, s * .055);
    final limb = _stroke(dark, s * .04);
    final shoulder = p + Offset(s * .015, -s * .105);
    final hip = p + Offset(-s * .015, s * .01);
    canvas.drawLine(shoulder, hip, body);

    final swing = math.sin(phase) * s * .04;
    canvas.drawLine(
      shoulder,
      p + Offset(-s * .10 - swing, -s * .015),
      limb,
    );
    canvas.drawLine(
      shoulder,
      p + Offset(s * .115 + swing, -s * .03),
      limb,
    );
    canvas.drawLine(
      hip,
      p + Offset(-s * .11 - swing * .7, s * .145),
      limb,
    );
    canvas.drawLine(
      hip,
      p + Offset(s * .12 + swing * .7, s * .11),
      limb,
    );

    canvas.drawCircle(
      p + Offset(-s * .23, -s * .18),
      s * .018,
      Paint()..color = const Color(0xFF31B77B),
    );
    canvas.drawCircle(
      p + Offset(-s * .27, -s * .11),
      s * .011,
      Paint()..color = const Color(0xFF31B77B),
    );
  }

  void _drawRecovery(Canvas canvas, Offset c, double s, double phase) {
    final breathe = math.sin(phase) * s * .006;
    final p = c + Offset(0, breathe);
    final head = p + Offset(0, -s * .18);
    _face(canvas, head, s * .058, smile: false, closedEyes: true);

    canvas.drawLine(
      p + Offset(0, -s * .105),
      p + Offset(0, s * .025),
      _stroke(shirt, s * .065),
    );

    final limb = _stroke(dark, s * .038);
    canvas.drawLine(
      p + Offset(0, -s * .07),
      p + Offset(-s * .12, s * .02),
      limb,
    );
    canvas.drawLine(
      p + Offset(0, -s * .07),
      p + Offset(s * .12, s * .02),
      limb,
    );

    final leftLeg = Path()
      ..moveTo(p.dx - s * .015, p.dy + s * .025)
      ..quadraticBezierTo(
        p.dx - s * .09,
        p.dy + s * .08,
        p.dx - s * .17,
        p.dy + s * .105,
      )
      ..quadraticBezierTo(
        p.dx - s * .08,
        p.dy + s * .135,
        p.dx,
        p.dy + s * .095,
      );
    canvas.drawPath(leftLeg, limb);

    final rightLeg = Path()
      ..moveTo(p.dx + s * .015, p.dy + s * .025)
      ..quadraticBezierTo(
        p.dx + s * .09,
        p.dy + s * .08,
        p.dx + s * .17,
        p.dy + s * .105,
      )
      ..quadraticBezierTo(
        p.dx + s * .08,
        p.dy + s * .135,
        p.dx,
        p.dy + s * .095,
      );
    canvas.drawPath(rightLeg, limb);

    for (var i = 0; i < 3; i++) {
      final radius = s * (.24 + i * .045 + (t * .025));
      canvas.drawArc(
        Rect.fromCircle(center: p, radius: radius),
        math.pi * 1.05,
        math.pi * .9,
        false,
        Paint()
          ..color = const Color(0xFF4AA3DF).withValues(alpha: .16 - i * .035)
          ..style = PaintingStyle.stroke
          ..strokeWidth = 2,
      );
    }
  }

  void _drawWorried(Canvas canvas, Offset c, double s, double phase) {
    final p = c + Offset(0, math.sin(phase) * s * .004);
    final head = p + Offset(s * .015, -s * .17);
    _face(canvas, head, s * .058, smile: false, worried: true);

    final torso = _stroke(const Color(0xFF63766E), s * .055);
    final limb = _stroke(dark, s * .038);
    canvas.drawLine(
      p + Offset(0, -s * .10),
      p + Offset(-s * .025, s * .03),
      torso,
    );
    canvas.drawLine(
      p + Offset(-s * .01, -s * .065),
      p + Offset(-s * .115, s * .015),
      limb,
    );
    canvas.drawLine(
      p + Offset(s * .005, -s * .07),
      head + Offset(s * .055, s * .04),
      limb,
    );
    canvas.drawLine(
      p + Offset(-s * .025, s * .03),
      p + Offset(-s * .09, s * .15),
      limb,
    );
    canvas.drawLine(
      p + Offset(-s * .025, s * .03),
      p + Offset(s * .075, s * .145),
      limb,
    );

    final q = TextPainter(
      text: const TextSpan(
        text: '?',
        style: TextStyle(
          color: Color(0xFFE59A2F),
          fontSize: 24,
          fontWeight: FontWeight.w900,
        ),
      ),
      textDirection: TextDirection.ltr,
    )..layout();
    q.paint(canvas, p + Offset(s * .17, -s * .20));
  }

  @override
  bool shouldRepaint(covariant _MoodAvatarPainter oldDelegate) =>
      oldDelegate.t != t || oldDelegate.mood != mood;
}
