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
    _controller = AnimationController(vsync: this,duration: const Duration(milliseconds: 1800))..repeat();
  }

  @override
  void dispose() { _controller.dispose(); super.dispose(); }

  @override
  Widget build(BuildContext context) {
    return RepaintBoundary(
      child: AnimatedBuilder(
        animation: _controller,
        builder: (context, child) {
          final phase = _controller.value * math.pi * 2;
          return Transform.translate(
            offset: Offset(0, math.sin(phase) * 1.0),
            child: Transform.scale(scale: 1 + math.sin(phase) * 0.003, child: child),
          );
        },
        child: ClipRRect(
          borderRadius: BorderRadius.circular(18),
          child: Image.asset('assets/images/treadmill_runner_realistic.jpg',width: widget.width,height: widget.height,fit: BoxFit.cover,alignment: Alignment.center,filterQuality: FilterQuality.high),
        ),
      ),
    );
  }
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
p=pub.read_text().replace('version: 0.2.3+4','version: 0.2.5+6')
if 'assets/images/treadmill_runner_realistic.jpg' not in p:
    p=p.replace('flutter:\n  uses-material-design: true\n','flutter:\n  uses-material-design: true\n  assets:\n    - assets/images/treadmill_runner_realistic.jpg\n')
pub.write_text(p)
print('Prepared v0.2.5 preview sources with bundled runner asset')
