#!/usr/bin/env python3
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
home=ROOT/'lib/screens/home_screen.dart'
s=home.read_text()
s=s.replace('height: 178,','height: 205,')
s=s.replace("right: -6,\n            bottom: -10,\n            child: const TreadmillAvatar(width: 185, height: 165),","right: 4,\n            bottom: 4,\n            child: const TreadmillAvatar(width: 168, height: 180),")
s=s.replace('padding: const EdgeInsets.fromLTRB(18, 15, 155, 14),','padding: const EdgeInsets.fromLTRB(18, 15, 146, 16),')
home.write_text(s)

(ROOT/'lib/widgets/treadmill_avatar.dart').write_text(r'''import 'dart:math' as math;
import 'package:flutter/material.dart';

class TreadmillAvatar extends StatefulWidget {
  final double width;
  final double height;
  const TreadmillAvatar({super.key, this.width = 168, this.height = 180});

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
      duration: const Duration(milliseconds: 760),
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
            painter: _RunnerPainter(_controller.value),
          ),
        ),
      ),
    );
  }
}

class _RunnerPainter extends CustomPainter {
  final double t;
  _RunnerPainter(this.t);

  @override
  void paint(Canvas canvas, Size size) {
    final w = size.width;
    final h = size.height;
    final phase = t * math.pi * 2;
    final swing = math.sin(phase);
    final bounce = math.sin(phase * 2) * h * 0.012;

    const skin = Color(0xFFC98655);
    const skinShade = Color(0xFFA8643E);
    const hair = Color(0xFF211915);
    const shirt = Color(0xFF173E39);
    const shorts = Color(0xFF152522);
    const shoe = Color(0xFFF4F5F4);
    const accent = Color(0xFF0B8C5E);
    const frame = Color(0xFF384341);
    const frameDark = Color(0xFF202927);

    // Soft background halo to integrate the runner with the dashboard card.
    canvas.drawOval(
      Rect.fromCenter(
        center: Offset(w * .55, h * .52),
        width: w * .9,
        height: h * .86,
      ),
      Paint()..color = const Color(0x0D0B8C5E),
    );

    // Floor shadow.
    canvas.drawOval(
      Rect.fromCenter(
        center: Offset(w * .57, h * .87),
        width: w * .74,
        height: h * .055,
      ),
      Paint()..color = const Color(0x16000000),
    );

    // Treadmill deck.
    final beltY = h * .79;
    canvas.drawRRect(
      RRect.fromRectAndRadius(
        Rect.fromLTWH(w * .12, beltY - h * .025, w * .72, h * .07),
        Radius.circular(h * .035),
      ),
      Paint()..color = frameDark,
    );
    canvas.drawRRect(
      RRect.fromRectAndRadius(
        Rect.fromLTWH(w * .14, beltY - h * .017, w * .68, h * .026),
        Radius.circular(h * .014),
      ),
      Paint()..color = const Color(0xFF646F6C),
    );

    // Moving belt marks.
    for (var i = 0; i < 5; i++) {
      final p = ((i / 5) + t) % 1;
      final x = w * (.16 + p * .60);
      canvas.drawLine(
        Offset(x, beltY - h * .005),
        Offset(x + w * .035, beltY - h * .005),
        Paint()
          ..color = const Color(0x7AFFFFFF)
          ..strokeWidth = h * .008
          ..strokeCap = StrokeCap.round,
      );
    }

    // Treadmill upright and console.
    final framePaint = Paint()
      ..color = frame
      ..strokeWidth = h * .032
      ..strokeCap = StrokeCap.round;
    canvas.drawLine(
      Offset(w * .76, beltY),
      Offset(w * .82, h * .35),
      framePaint,
    );
    canvas.drawLine(
      Offset(w * .82, h * .35),
      Offset(w * .94, h * .35),
      framePaint,
    );
    canvas.drawRRect(
      RRect.fromRectAndRadius(
        Rect.fromLTWH(w * .78, h * .25, w * .18, h * .13),
        Radius.circular(w * .025),
      ),
      Paint()..color = frameDark,
    );
    canvas.drawRRect(
      RRect.fromRectAndRadius(
        Rect.fromLTWH(w * .81, h * .275, w * .12, h * .055),
        Radius.circular(w * .012),
      ),
      Paint()..color = const Color(0xFFA9D3C5),
    );

    // Runner body landmarks.
    final head = Offset(w * .42, h * .225 + bounce);
    final shoulder = Offset(w * .43, h * .355 + bounce);
    final hip = Offset(w * .46, h * .56 + bounce);

    // Neck.
    canvas.drawRRect(
      RRect.fromRectAndRadius(
        Rect.fromCenter(
          center: Offset(w * .43, h * .295 + bounce),
          width: w * .045,
          height: h * .055,
        ),
        Radius.circular(w * .02),
      ),
      Paint()..color = skin,
    );

    // Head and face shading.
    canvas.drawOval(
      Rect.fromCenter(center: head, width: w * .12, height: h * .145),
      Paint()..color = skin,
    );
    canvas.drawArc(
      Rect.fromCenter(center: head, width: w * .12, height: h * .145),
      -.2,
      math.pi * .8,
      true,
      Paint()..color = skinShade.withOpacity(.12),
    );

    // Hair.
    final hairPath = Path()
      ..moveTo(w * .365, h * .205 + bounce)
      ..quadraticBezierTo(w * .39, h * .135 + bounce, w * .475, h * .155 + bounce)
      ..quadraticBezierTo(w * .505, h * .175 + bounce, w * .492, h * .225 + bounce)
      ..quadraticBezierTo(w * .43, h * .175 + bounce, w * .365, h * .205 + bounce)
      ..close();
    canvas.drawPath(hairPath, Paint()..color = hair);

    // Face details.
    canvas.drawCircle(
      Offset(w * .468, h * .218 + bounce),
      w * .005,
      Paint()..color = const Color(0xFF241A16),
    );
    canvas.drawLine(
      Offset(w * .475, h * .248 + bounce),
      Offset(w * .492, h * .246 + bounce),
      Paint()
        ..color = const Color(0xFF8B4B3D)
        ..strokeWidth = 1.3
        ..strokeCap = StrokeCap.round,
    );

    // Torso with slight forward lean.
    final torso = Path()
      ..moveTo(w * .365, h * .345 + bounce)
      ..quadraticBezierTo(w * .425, h * .315 + bounce, w * .505, h * .35 + bounce)
      ..lineTo(w * .535, h * .545 + bounce)
      ..quadraticBezierTo(w * .47, h * .575 + bounce, w * .395, h * .54 + bounce)
      ..close();
    canvas.drawPath(torso, Paint()..color = shirt);

    // Shirt highlight gives some depth.
    canvas.drawLine(
      Offset(w * .405, h * .36 + bounce),
      Offset(w * .43, h * .52 + bounce),
      Paint()
        ..color = const Color(0x3039B88B)
        ..strokeWidth = w * .014
        ..strokeCap = StrokeCap.round,
    );

    // Shorts.
    canvas.drawRRect(
      RRect.fromRectAndRadius(
        Rect.fromLTWH(w * .395, h * .51 + bounce, w * .145, h * .11),
        Radius.circular(w * .025),
      ),
      Paint()..color = shorts,
    );

    // Arms, opposite phase to legs.
    final arm = swing * w * .07;
    _limb(
      canvas,
      shoulder + Offset(-w * .045, h * .012),
      Offset(w * .33 - arm, h * .43 + bounce),
      Offset(w * .39 - arm, h * .50 + bounce),
      skin,
      h * .033,
    );
    _limb(
      canvas,
      shoulder + Offset(w * .045, h * .012),
      Offset(w * .535 + arm, h * .415 + bounce),
      Offset(w * .595 + arm, h * .365 + bounce),
      skin,
      h * .033,
    );

    // Running legs with bent knees.
    final leg = swing * w * .11;
    final kneeA = Offset(w * .39 - leg, h * .66 + bounce);
    final footA = Offset(w * .30 - leg * .55, h * .765);
    final kneeB = Offset(w * .535 + leg, h * .655 + bounce);
    final footB = Offset(w * .61 + leg * .60, h * .765);

    _limb(
      canvas,
      hip + Offset(-w * .035, 0),
      kneeA,
      footA,
      skin,
      h * .042,
    );
    _limb(
      canvas,
      hip + Offset(w * .045, 0),
      kneeB,
      footB,
      skin,
      h * .042,
    );

    _shoe(canvas, footA, false, shoe, accent, w, h);
    _shoe(canvas, footB, true, shoe, accent, w, h);
  }

  void _limb(
    Canvas canvas,
    Offset start,
    Offset joint,
    Offset end,
    Color color,
    double width,
  ) {
    final p = Paint()
      ..color = color
      ..strokeWidth = width
      ..strokeCap = StrokeCap.round
      ..strokeJoin = StrokeJoin.round;
    canvas.drawLine(start, joint, p);
    canvas.drawLine(joint, end, p);
    canvas.drawCircle(joint, width * .42, Paint()..color = color);
  }

  void _shoe(
    Canvas canvas,
    Offset foot,
    bool right,
    Color base,
    Color accent,
    double w,
    double h,
  ) {
    final dir = right ? 1.0 : -1.0;
    final rect = Rect.fromCenter(
      center: foot + Offset(dir * w * .015, 0),
      width: w * .10,
      height: h * .033,
    );
    canvas.drawRRect(
      RRect.fromRectAndRadius(rect, Radius.circular(h * .017)),
      Paint()..color = base,
    );
    canvas.drawLine(
      Offset(rect.left + w * .02, rect.bottom - h * .006),
      Offset(rect.right - w * .02, rect.bottom - h * .006),
      Paint()
        ..color = accent
        ..strokeWidth = h * .006
        ..strokeCap = StrokeCap.round,
    );
  }

  @override
  bool shouldRepaint(covariant _RunnerPainter oldDelegate) => oldDelegate.t != t;
}
''')

(ROOT/'lib/calculations.dart').write_text(r'''import 'models.dart';
export 'afcd_reference.dart' show NutritionEstimate, AfcdMatch, estimateNutritionFromDescription;

double bmi(double weightKg, double heightCm) { final metres=heightCm/100; if(metres<=0)return 0; return weightKg/(metres*metres); }
double percentWeightChange(double baselineKg,double currentKg){if(baselineKg<=0)return 0;return((currentKg-baselineKg)/baselineKg)*100;}
double epleyE1rm(double weightKg,int reps){if(weightKg<=0||reps<=0)return 0;if(reps==1)return weightKg;return weightKg*(1+reps/30.0);}
double trainingVolume(List<ExerciseSetRecord> sets)=>sets.fold<double>(0,(sum,set)=>sum+(set.reps*set.weightKg));
double metMinutes(double? met,int minutes){if(met==null||met<=0||minutes<=0)return 0;return met*minutes;}
double estimatedCalories({required double? met,required int minutes,required double bodyWeightKg}){if(met==null||met<=0||minutes<=0||bodyWeightKg<=0)return 0;return((met*3.5*bodyWeightKg)/200)*minutes;}
double estimatedRestingEnergy({required double weightKg,required double heightCm,required int age,required String sex}){if(weightKg<=0||heightCm<=0||age<=0)return 0;final base=(10*weightKg)+(6.25*heightCm)-(5*age);if(sex=='Male')return base+5;if(sex=='Female')return base-161;return base-78;}
double estimatedDailyEnergyRequirement({required double weightKg,required double heightCm,required int age,required String sex,required double activityFactor}){if(activityFactor<=0)return 0;return estimatedRestingEnergy(weightKg:weightKg,heightCm:heightCm,age:age,sex:sex)*activityFactor;}
String shortDate(DateTime date){const months=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];return '${date.day} ${months[date.month-1]} ${date.year}';}
''')

meal=ROOT/'lib/screens/meal_log_screen.dart'
m=meal.read_text()
m=m.replace('  int? _matchedFoods;','  int? _matchedFoods;\n  List<AfcdMatch> _afcdMatches = const [];')
m=m.replace('      _matchedFoods = estimate.matchedFoods;','      _matchedFoods = estimate.matchedFoods;\n      _afcdMatches = estimate.matches;')
m=m.replace('      setState(() => _matchedFoods = null);','      setState(() { _matchedFoods = null; _afcdMatches = const []; });')
m=m.replace("icon: const Icon(Icons.auto_awesome_outlined),\n                    label: const Text('Estimate nutrition from description'),","icon: const Icon(Icons.calculate_outlined),\n                    label: const Text('Estimate from AFCD Release 3'),")
m=m.replace("_matchedFoods == null\n                        ? 'The estimate runs locally on your device. Review and edit the values before saving.'\n                        : 'Estimated from $_matchedFoods recognised food item${_matchedFoods == 1 ? '' : 's'}. Review and edit the values before saving.',","_matchedFoods == null\n                        ? 'Uses Australian Food Composition Database (AFCD) Release 3 reference values. Add quantities (for example 150 g chicken, 1 cup rice) for a better estimate.'\n                        : 'AFCD estimate from $_matchedFoods matched food item${_matchedFoods == 1 ? '' : 's'}. Values remain editable before saving.',")
anchor="""                  const SizedBox(height: 14),
                  TextField(
                    controller: _calories,"""
insert="""                  if (_afcdMatches.isNotEmpty) ...[
                    const SizedBox(height: 8),
                    Container(
                      width: double.infinity,
                      padding: const EdgeInsets.all(10),
                      decoration: BoxDecoration(color: const Color(0xFFF0F7F4),borderRadius: BorderRadius.circular(12)),
                      child: Column(crossAxisAlignment: CrossAxisAlignment.start,children: [
                        const Row(children: [Icon(Icons.info_outline,size:16),SizedBox(width:6),Text('AFCD matches',style: TextStyle(fontWeight: FontWeight.w800))]),
                        const SizedBox(height:5),
                        ..._afcdMatches.take(4).map((match)=>Text('${match.grams.toStringAsFixed(0)} g • ${match.foodName} (${match.foodKey})',style: const TextStyle(fontSize:11))),
                        const SizedBox(height:5),
                        const Text('Reference values are per 100 g edible portion. Portion assumptions and product variation can change the estimate.',style: TextStyle(fontSize:10,color: Color(0xFF687871))),
                      ]),
                    ),
                  ],
                  const SizedBox(height: 14),
                  TextField(
                    controller: _calories,"""
m=m.replace(anchor,insert)
meal.write_text(m)

pub=ROOT/'pubspec.yaml'
p=pub.read_text().replace('version: 0.2.3+4','version: 0.2.6+7')
# The runner is now entirely code-driven; no external image asset is required.
p=p.replace('  assets:\n    - assets/images/treadmill_runner_realistic.jpg\n','')
pub.write_text(p)
print('Prepared v0.2.6 preview with true vector runner animation')
