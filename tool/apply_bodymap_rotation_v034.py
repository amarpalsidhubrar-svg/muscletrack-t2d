#!/usr/bin/env python3
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]

(ROOT/'lib/screens/body_map_picker_screen.dart').write_text(r'''import 'dart:math' as math;
import 'package:flutter/material.dart';

enum BodyOrientation { front, side, back }

class BodyMapPickerScreen extends StatefulWidget {
  final Set<String> initial;
  const BodyMapPickerScreen({super.key, this.initial = const {}});

  @override
  State<BodyMapPickerScreen> createState() => _BodyMapPickerScreenState();
}

class _BodyMapPickerScreenState extends State<BodyMapPickerScreen> {
  late Set<String> selected;
  int _viewIndex = 0;
  double _dragDx = 0;

  static const parts = <String>[
    'Chest',
    'Shoulders',
    'Biceps',
    'Triceps',
    'Forearms',
    'Core',
    'Upper back',
    'Lats',
    'Lower back',
    'Glutes',
    'Quads',
    'Hamstrings',
    'Calves',
  ];

  BodyOrientation get orientation => BodyOrientation.values[_viewIndex];

  String get orientationLabel => switch (orientation) {
        BodyOrientation.front => 'FRONT',
        BodyOrientation.side => 'SIDE',
        BodyOrientation.back => 'BACK',
      };

  @override
  void initState() {
    super.initState();
    selected = {...widget.initial};
  }

  void toggle(String part) {
    setState(() {
      if (!selected.add(part)) selected.remove(part);
    });
  }

  void _rotateBy(int direction) {
    setState(() {
      _viewIndex = (_viewIndex + direction) % 3;
      if (_viewIndex < 0) _viewIndex = 2;
      _dragDx = 0;
    });
  }

  void _onDragUpdate(DragUpdateDetails details) {
    setState(() => _dragDx += details.delta.dx);
  }

  void _onDragEnd(DragEndDetails details) {
    final velocity = details.primaryVelocity ?? 0;
    if (_dragDx.abs() > 42 || velocity.abs() > 450) {
      _rotateBy((_dragDx < 0 || velocity < -450) ? 1 : -1);
    } else {
      setState(() => _dragDx = 0);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFF07141B),
      appBar: AppBar(
        title: const Text('3D body map'),
        backgroundColor: const Color(0xFF07141B),
        foregroundColor: Colors.white,
        actions: [
          TextButton(
            onPressed: () => setState(selected.clear),
            child: const Text('Clear'),
          ),
        ],
      ),
      body: SafeArea(
        child: Column(
          children: [
            Padding(
              padding: const EdgeInsets.fromLTRB(14, 8, 14, 4),
              child: Row(
                children: [
                  const Icon(
                    Icons.swipe_rounded,
                    color: Color(0xFF7CF2FF),
                    size: 18,
                  ),
                  const SizedBox(width: 7),
                  const Expanded(
                    child: Text(
                      'Swipe across the body to rotate. Tap muscles to select them.',
                      style: TextStyle(
                        color: Color(0xFFC5D9E3),
                        fontSize: 12,
                      ),
                    ),
                  ),
                  Container(
                    padding: const EdgeInsets.symmetric(
                      horizontal: 10,
                      vertical: 5,
                    ),
                    decoration: BoxDecoration(
                      color: const Color(0xFF17313D),
                      borderRadius: BorderRadius.circular(20),
                      border: Border.all(color: const Color(0xFF31505D)),
                    ),
                    child: Text(
                      orientationLabel,
                      style: const TextStyle(
                        color: Color(0xFF7CF2FF),
                        fontSize: 10,
                        fontWeight: FontWeight.w900,
                        letterSpacing: 1,
                      ),
                    ),
                  ),
                ],
              ),
            ),
            Expanded(
              child: GestureDetector(
                behavior: HitTestBehavior.opaque,
                onHorizontalDragUpdate: _onDragUpdate,
                onHorizontalDragEnd: _onDragEnd,
                child: Center(
                  child: AspectRatio(
                    aspectRatio: 180 / 318,
                    child: LayoutBuilder(
                      builder: (context, constraints) {
                        final dragFraction =
                            (_dragDx / constraints.maxWidth).clamp(-0.55, 0.55);
                        final previewAngle = dragFraction * math.pi * .42;

                        return TweenAnimationBuilder<double>(
                          tween: Tween(begin: 0, end: previewAngle),
                          duration: _dragDx == 0
                              ? const Duration(milliseconds: 230)
                              : Duration.zero,
                          builder: (context, angle, child) {
                            return Transform(
                              alignment: Alignment.center,
                              transform: Matrix4.identity()
                                ..setEntry(3, 2, .001)
                                ..rotateY(angle),
                              child: child,
                            );
                          },
                          child: _BodyView(
                            orientation: orientation,
                            selected: selected,
                            onToggle: toggle,
                            width: constraints.maxWidth,
                            height: constraints.maxHeight,
                          ),
                        );
                      },
                    ),
                  ),
                ),
              ),
            ),
            Container(
              color: const Color(0xFF0E2029),
              padding: const EdgeInsets.fromLTRB(12, 8, 12, 14),
              child: Column(
                children: [
                  Row(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: List.generate(
                      3,
                      (i) => GestureDetector(
                        onTap: () => setState(() => _viewIndex = i),
                        child: AnimatedContainer(
                          duration: const Duration(milliseconds: 160),
                          width: i == _viewIndex ? 24 : 8,
                          height: 8,
                          margin: const EdgeInsets.symmetric(horizontal: 3),
                          decoration: BoxDecoration(
                            color: i == _viewIndex
                                ? const Color(0xFF45E8FF)
                                : const Color(0xFF47616D),
                            borderRadius: BorderRadius.circular(10),
                          ),
                        ),
                      ),
                    ),
                  ),
                  const SizedBox(height: 8),
                  SingleChildScrollView(
                    scrollDirection: Axis.horizontal,
                    child: Row(
                      children: parts.map((part) {
                        final active = selected.contains(part);
                        return Padding(
                          padding: const EdgeInsets.only(right: 6),
                          child: FilterChip(
                            selected: active,
                            label: Text(part),
                            onSelected: (_) => toggle(part),
                            selectedColor: const Color(0xFF2CC6DB),
                            checkmarkColor: Colors.white,
                            labelStyle: TextStyle(
                              color: active
                                  ? Colors.white
                                  : const Color(0xFFDDECF2),
                              fontWeight: FontWeight.w700,
                            ),
                            backgroundColor: const Color(0xFF17313D),
                            side: BorderSide(
                              color: active
                                  ? const Color(0xFF7CF2FF)
                                  : const Color(0xFF31505D),
                            ),
                          ),
                        );
                      }).toList(),
                    ),
                  ),
                  const SizedBox(height: 10),
                  SizedBox(
                    width: double.infinity,
                    child: FilledButton.icon(
                      onPressed: selected.isEmpty
                          ? null
                          : () => Navigator.pop(context, selected),
                      icon: const Icon(Icons.check_rounded),
                      label: Text(
                        selected.isEmpty
                            ? 'Select body parts'
                            : 'Save ${selected.length} selected',
                      ),
                    ),
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}

class _BodyView extends StatelessWidget {
  final BodyOrientation orientation;
  final Set<String> selected;
  final ValueChanged<String> onToggle;
  final double width;
  final double height;

  const _BodyView({
    required this.orientation,
    required this.selected,
    required this.onToggle,
    required this.width,
    required this.height,
  });

  Widget hotspot(
    String label,
    double x,
    double y,
    double w,
    double h,
  ) {
    final active = selected.contains(label);
    return Positioned(
      left: width * x,
      top: height * y,
      width: width * w,
      height: height * h,
      child: GestureDetector(
        behavior: HitTestBehavior.translucent,
        onTap: () => onToggle(label),
        child: AnimatedContainer(
          duration: const Duration(milliseconds: 150),
          decoration: BoxDecoration(
            color: active
                ? const Color(0x8845E8FF)
                : Colors.transparent,
            borderRadius: BorderRadius.circular(18),
            border: active
                ? Border.all(
                    color: const Color(0xFF7CF2FF),
                    width: 2,
                  )
                : null,
            boxShadow: active
                ? const [
                    BoxShadow(
                      color: Color(0xAA45E8FF),
                      blurRadius: 20,
                      spreadRadius: 2,
                    )
                  ]
                : null,
          ),
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    switch (orientation) {
      case BodyOrientation.front:
        return Stack(
          fit: StackFit.expand,
          children: [
            Image.asset(
              'assets/digital_twin_bodymap.webp',
              fit: BoxFit.contain,
            ),
            hotspot('Shoulders', .27, .18, .46, .12),
            hotspot('Chest', .34, .25, .34, .11),
            hotspot('Biceps', .18, .29, .64, .13),
            hotspot('Forearms', .13, .39, .74, .13),
            hotspot('Core', .36, .37, .30, .16),
            hotspot('Quads', .29, .55, .42, .16),
            hotspot('Calves', .30, .73, .40, .18),
          ],
        );

      case BodyOrientation.side:
        return Stack(
          fit: StackFit.expand,
          children: [
            Transform.scale(
              scaleX: .72,
              alignment: Alignment.center,
              child: Opacity(
                opacity: .92,
                child: Image.asset(
                  'assets/digital_twin_bodymap.webp',
                  fit: BoxFit.contain,
                ),
              ),
            ),
            hotspot('Shoulders', .34, .18, .34, .12),
            hotspot('Triceps', .54, .29, .18, .14),
            hotspot('Forearms', .58, .39, .19, .13),
            hotspot('Core', .39, .37, .25, .15),
            hotspot('Glutes', .42, .51, .24, .12),
            hotspot('Quads', .39, .56, .20, .16),
            hotspot('Hamstrings', .50, .56, .18, .16),
            hotspot('Calves', .43, .74, .19, .17),
          ],
        );

      case BodyOrientation.back:
        return Stack(
          fit: StackFit.expand,
          children: [
            CustomPaint(
              painter: const _PosteriorTwinPainter(),
            ),
            hotspot('Shoulders', .27, .18, .46, .11),
            hotspot('Upper back', .32, .25, .38, .11),
            hotspot('Triceps', .17, .28, .66, .14),
            hotspot('Forearms', .12, .39, .76, .13),
            hotspot('Lats', .29, .31, .42, .17),
            hotspot('Lower back', .37, .43, .28, .11),
            hotspot('Glutes', .34, .50, .34, .12),
            hotspot('Hamstrings', .31, .58, .38, .15),
            hotspot('Calves', .30, .74, .40, .17),
          ],
        );
    }
  }
}

class _PosteriorTwinPainter extends CustomPainter {
  const _PosteriorTwinPainter();

  static const cyan = Color(0xFF36D6FF);
  static const magenta = Color(0xFFFF3B9A);

  @override
  void paint(Canvas canvas, Size size) {
    final sx = size.width;
    final sy = size.height;
    Offset p(double x, double y) => Offset(sx * x, sy * y);

    final glow = Paint()
      ..color = cyan.withValues(alpha: .18)
      ..maskFilter = const MaskFilter.blur(BlurStyle.normal, 18);

    final bodyFill = Paint()
      ..shader = const LinearGradient(
        colors: [Color(0xFF052A74), Color(0xFF00152F)],
        begin: Alignment.topCenter,
        end: Alignment.bottomCenter,
      ).createShader(Rect.fromLTWH(0, 0, sx, sy))
      ..style = PaintingStyle.fill;

    final outline = Paint()
      ..color = cyan
      ..style = PaintingStyle.stroke
      ..strokeWidth = 2.2
      ..strokeCap = StrokeCap.round
      ..strokeJoin = StrokeJoin.round;

    final grid = Paint()
      ..color = cyan.withValues(alpha: .28)
      ..style = PaintingStyle.stroke
      ..strokeWidth = .8;

    final vessels = Paint()
      ..color = magenta.withValues(alpha: .85)
      ..style = PaintingStyle.stroke
      ..strokeWidth = 1.3
      ..strokeCap = StrokeCap.round;

    final body = Path()
      ..moveTo(p(.50, .09).dx, p(.50, .09).dy)
      ..cubicTo(p(.42, .09).dx, p(.42, .09).dy, p(.39, .14).dx, p(.39, .14).dy, p(.40, .19).dx, p(.40, .19).dy)
      ..cubicTo(p(.33, .21).dx, p(.33, .21).dy, p(.27, .24).dx, p(.27, .24).dy, p(.24, .31).dx, p(.24, .31).dy)
      ..cubicTo(p(.20, .40).dx, p(.20, .40).dy, p(.20, .45).dx, p(.20, .45).dy, p(.24, .48).dx, p(.24, .48).dy)
      ..cubicTo(p(.28, .51).dx, p(.28, .51).dy, p(.31, .49).dx, p(.31, .49).dy, p(.33, .44).dx, p(.33, .44).dy)
      ..cubicTo(p(.35, .40).dx, p(.35, .40).dy, p(.37, .45).dx, p(.37, .45).dy, p(.37, .51).dx, p(.37, .51).dy)
      ..cubicTo(p(.35, .60).dx, p(.35, .60).dy, p(.34, .66).dx, p(.34, .66).dy, p(.36, .74).dx, p(.36, .74).dy)
      ..cubicTo(p(.37, .83).dx, p(.37, .83).dy, p(.38, .88).dx, p(.38, .88).dy, p(.38, .94).dx, p(.38, .94).dy)
      ..cubicTo(p(.40, .97).dx, p(.40, .97).dy, p(.46, .97).dx, p(.46, .97).dy, p(.47, .94).dx, p(.47, .94).dy)
      ..lineTo(p(.49, .62).dx, p(.49, .62).dy)
      ..lineTo(p(.51, .62).dx, p(.51, .62).dy)
      ..lineTo(p(.53, .94).dx, p(.53, .94).dy)
      ..cubicTo(p(.54, .97).dx, p(.54, .97).dy, p(.60, .97).dx, p(.60, .97).dy, p(.62, .94).dx, p(.62, .94).dy)
      ..cubicTo(p(.62, .88).dx, p(.62, .88).dy, p(.63, .83).dx, p(.63, .83).dy, p(.64, .74).dx, p(.64, .74).dy)
      ..cubicTo(p(.66, .66).dx, p(.66, .66).dy, p(.65, .60).dx, p(.65, .60).dy, p(.63, .51).dx, p(.63, .51).dy)
      ..cubicTo(p(.63, .45).dx, p(.63, .45).dy, p(.65, .40).dx, p(.65, .40).dy, p(.67, .44).dx, p(.67, .44).dy)
      ..cubicTo(p(.69, .49).dx, p(.69, .49).dy, p(.72, .51).dx, p(.72, .51).dy, p(.76, .48).dx, p(.76, .48).dy)
      ..cubicTo(p(.80, .45).dx, p(.80, .45).dy, p(.80, .40).dx, p(.80, .40).dy, p(.76, .31).dx, p(.76, .31).dy)
      ..cubicTo(p(.73, .24).dx, p(.73, .24).dy, p(.67, .21).dx, p(.67, .21).dy, p(.60, .19).dx, p(.60, .19).dy)
      ..cubicTo(p(.61, .14).dx, p(.61, .14).dy, p(.58, .09).dx, p(.58, .09).dy, p(.50, .09).dx, p(.50, .09).dy)
      ..close();

    canvas.drawPath(body, glow);
    canvas.drawPath(body, bodyFill);
    canvas.drawPath(body, outline);

    final spine = Path()
      ..moveTo(p(.50, .20).dx, p(.50, .20).dy)
      ..cubicTo(p(.49, .34).dx, p(.49, .34).dy, p(.51, .43).dx, p(.51, .43).dy, p(.50, .55).dx, p(.50, .55).dy)
      ..lineTo(p(.50, .62).dx, p(.50, .62).dy);
    canvas.drawPath(spine, vessels);

    for (var y = .18; y < .90; y += .055) {
      canvas.drawLine(p(.37, y), p(.63, y), grid);
    }
    for (final x in [.42, .46, .50, .54, .58]) {
      canvas.drawLine(p(x, .18), p(x, .92), grid);
    }

    canvas.drawLine(p(.50, .50), p(.50, .62), grid);
    canvas.drawLine(p(.42, .58), p(.44, .78), grid);
    canvas.drawLine(p(.58, .58), p(.56, .78), grid);

    final node = Paint()..color = cyan;
    for (final q in [
      p(.40, .24), p(.60, .24), p(.36, .34), p(.64, .34),
      p(.42, .46), p(.58, .46), p(.40, .62), p(.60, .62),
      p(.40, .78), p(.60, .78), p(.42, .90), p(.58, .90),
    ]) {
      canvas.drawCircle(q, 2.2, node);
    }
  }

  @override
  bool shouldRepaint(covariant _PosteriorTwinPainter oldDelegate) => false;
}
''')

pub = ROOT/'pubspec.yaml'
p = pub.read_text()
p = re.sub(r'^version:\s*.*$', 'version: 0.3.5+15', p, flags=re.M)
pub.write_text(p)

print('Applied v0.3.5 swipe rotation with posterior digital-twin muscle map')
