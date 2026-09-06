import 'models.dart';

double bmi(double weightKg, double heightCm) {
  final metres = heightCm / 100;
  if (metres <= 0) return 0;
  return weightKg / (metres * metres);
}

double percentWeightChange(double baselineKg, double currentKg) {
  if (baselineKg <= 0) return 0;
  return ((currentKg - baselineKg) / baselineKg) * 100;
}

double epleyE1rm(double weightKg, int reps) {
  if (weightKg <= 0 || reps <= 0) return 0;
  if (reps == 1) return weightKg;
  return weightKg * (1 + reps / 30.0);
}

double trainingVolume(List<ExerciseSetRecord> sets) {
  return sets.fold<double>(
    0,
    (sum, set) => sum + (set.reps * set.weightKg),
  );
}

double metMinutes(double? met, int minutes) {
  if (met == null || met <= 0 || minutes <= 0) return 0;
  return met * minutes;
}

double estimatedCalories({
  required double? met,
  required int minutes,
  required double bodyWeightKg,
}) {
  if (met == null || met <= 0 || minutes <= 0 || bodyWeightKg <= 0) return 0;
  return ((met * 3.5 * bodyWeightKg) / 200) * minutes;
}

/// Mifflin-St Jeor resting energy estimate. This is an informational estimate,
/// not a prescription. For users who select 'Other / prefer not to say', the
/// midpoint of the male and female constants is used to avoid inferring sex.
double estimatedRestingEnergy({
  required double weightKg,
  required double heightCm,
  required int age,
  required String sex,
}) {
  if (weightKg <= 0 || heightCm <= 0 || age <= 0) return 0;
  final base = (10 * weightKg) + (6.25 * heightCm) - (5 * age);
  if (sex == 'Male') return base + 5;
  if (sex == 'Female') return base - 161;
  return base - 78;
}

double estimatedDailyEnergyRequirement({
  required double weightKg,
  required double heightCm,
  required int age,
  required String sex,
  required double activityFactor,
}) {
  if (activityFactor <= 0) return 0;
  return estimatedRestingEnergy(
        weightKg: weightKg,
        heightCm: heightCm,
        age: age,
        sex: sex,
      ) *
      activityFactor;
}

class NutritionEstimate {
  final double calories;
  final double proteinG;
  final double carbsG;
  final double fatG;
  final double fibreG;
  final int matchedFoods;

  const NutritionEstimate({
    required this.calories,
    required this.proteinG,
    required this.carbsG,
    required this.fatG,
    required this.fibreG,
    required this.matchedFoods,
  });
}

class _FoodProfile {
  final List<String> keywords;
  final double calories;
  final double protein;
  final double carbs;
  final double fat;
  final double fibre;
  final double defaultGrams;
  final bool countByUnit;

  const _FoodProfile({
    required this.keywords,
    required this.calories,
    required this.protein,
    required this.carbs,
    required this.fat,
    required this.fibre,
    this.defaultGrams = 100,
    this.countByUnit = false,
  });
}

/// A deliberately simple local food-description estimator for preview/testing.
/// It recognises common whole foods and common serving descriptions. The result
/// is a rough estimate and should remain editable by the user.
NutritionEstimate? estimateNutritionFromDescription(String description) {
  final text = description.toLowerCase().replaceAll(',', ' ');
  if (text.trim().isEmpty) return null;

  const foods = <_FoodProfile>[
    _FoodProfile(
      keywords: ['egg white', 'egg whites'],
      calories: 17, protein: 3.6, carbs: 0.2, fat: 0.1, fibre: 0,
      countByUnit: true,
    ),
    _FoodProfile(
      keywords: ['egg', 'eggs'],
      calories: 72, protein: 6.3, carbs: 0.4, fat: 4.8, fibre: 0,
      countByUnit: true,
    ),
    _FoodProfile(
      keywords: ['toast', 'wholemeal bread', 'whole wheat bread', 'bread'],
      calories: 90, protein: 4, carbs: 16, fat: 1.2, fibre: 2.5,
      countByUnit: true,
    ),
    _FoodProfile(
      keywords: ['oats', 'oatmeal'],
      calories: 190, protein: 6.5, carbs: 32, fat: 3.5, fibre: 5,
      defaultGrams: 50,
    ),
    _FoodProfile(
      keywords: ['greek yoghurt', 'greek yogurt', 'yoghurt', 'yogurt'],
      calories: 120, protein: 15, carbs: 8, fat: 3, fibre: 0,
      defaultGrams: 170,
    ),
    _FoodProfile(
      keywords: ['banana', 'bananas'],
      calories: 105, protein: 1.3, carbs: 27, fat: 0.4, fibre: 3.1,
      countByUnit: true,
    ),
    _FoodProfile(
      keywords: ['apple', 'apples'],
      calories: 95, protein: 0.5, carbs: 25, fat: 0.3, fibre: 4.4,
      countByUnit: true,
    ),
    _FoodProfile(
      keywords: ['chicken breast', 'chicken'],
      calories: 198, protein: 37, carbs: 0, fat: 4.3, fibre: 0,
      defaultGrams: 120,
    ),
    _FoodProfile(
      keywords: ['tuna'],
      calories: 132, protein: 29, carbs: 0, fat: 1, fibre: 0,
      defaultGrams: 120,
    ),
    _FoodProfile(
      keywords: ['salmon'],
      calories: 250, protein: 26, carbs: 0, fat: 16, fibre: 0,
      defaultGrams: 120,
    ),
    _FoodProfile(
      keywords: ['tofu'],
      calories: 145, protein: 16, carbs: 4, fat: 9, fibre: 2,
      defaultGrams: 150,
    ),
    _FoodProfile(
      keywords: ['beef', 'steak'],
      calories: 300, protein: 32, carbs: 0, fat: 19, fibre: 0,
      defaultGrams: 150,
    ),
    _FoodProfile(
      keywords: ['rice'],
      calories: 205, protein: 4.3, carbs: 45, fat: 0.4, fibre: 0.6,
      defaultGrams: 160,
    ),
    _FoodProfile(
      keywords: ['pasta'],
      calories: 240, protein: 8, carbs: 47, fat: 1.3, fibre: 3,
      defaultGrams: 150,
    ),
    _FoodProfile(
      keywords: ['lentils'],
      calories: 180, protein: 14, carbs: 31, fat: 0.8, fibre: 12,
      defaultGrams: 150,
    ),
    _FoodProfile(
      keywords: ['beans'],
      calories: 190, protein: 12, carbs: 34, fat: 1, fibre: 11,
      defaultGrams: 150,
    ),
    _FoodProfile(
      keywords: ['protein shake', 'protein powder', 'whey'],
      calories: 130, protein: 25, carbs: 4, fat: 2, fibre: 1,
      countByUnit: true,
    ),
    _FoodProfile(
      keywords: ['milk'],
      calories: 125, protein: 8.5, carbs: 12, fat: 5, fibre: 0,
      defaultGrams: 250,
    ),
    _FoodProfile(
      keywords: ['peanut butter'],
      calories: 95, protein: 4, carbs: 3.5, fat: 8, fibre: 1,
      countByUnit: true,
    ),
    _FoodProfile(
      keywords: ['avocado'],
      calories: 160, protein: 2, carbs: 8.5, fat: 15, fibre: 7,
      defaultGrams: 100,
    ),
    _FoodProfile(
      keywords: ['cheese'],
      calories: 120, protein: 7, carbs: 1, fat: 10, fibre: 0,
      defaultGrams: 30,
    ),
    _FoodProfile(
      keywords: ['salad', 'vegetables', 'veggies'],
      calories: 80, protein: 3, carbs: 14, fat: 1, fibre: 5,
      defaultGrams: 200,
    ),
  ];

  var calories = 0.0;
  var protein = 0.0;
  var carbs = 0.0;
  var fat = 0.0;
  var fibre = 0.0;
  var matched = 0;

  for (final food in foods) {
    String? keyword;
    for (final candidate in food.keywords) {
      if (text.contains(candidate)) {
        keyword = candidate;
        break;
      }
    }
    if (keyword == null) continue;

    if ((keyword == 'egg' || keyword == 'eggs') &&
        (text.contains('egg white') || text.contains('egg whites'))) {
      continue;
    }

    var multiplier = 1.0;
    final escaped = RegExp.escape(keyword);

    final gramsMatch = RegExp(
      r'(\d+(?:\.\d+)?)\s*g(?:rams?)?\s+(?:of\s+)?' + escaped,
    ).firstMatch(text);
    if (gramsMatch != null && !food.countByUnit) {
      final grams = double.tryParse(gramsMatch.group(1) ?? '');
      if (grams != null && grams > 0) {
        multiplier = grams / food.defaultGrams;
      }
    } else {
      final numberMatch = RegExp(
        r'(\d+(?:\.\d+)?)\s*(?:x\s*)?(?:slices?\s+(?:of\s+)?)?' + escaped,
      ).firstMatch(text);
      if (numberMatch != null) {
        final value = double.tryParse(numberMatch.group(1) ?? '');
        if (value != null && value > 0) multiplier = value;
      }
    }

    calories += food.calories * multiplier;
    protein += food.protein * multiplier;
    carbs += food.carbs * multiplier;
    fat += food.fat * multiplier;
    fibre += food.fibre * multiplier;
    matched += 1;
  }

  if (matched == 0) return null;
  return NutritionEstimate(
    calories: calories,
    proteinG: protein,
    carbsG: carbs,
    fatG: fat,
    fibreG: fibre,
    matchedFoods: matched,
  );
}

String shortDate(DateTime date) {
  const months = [
    'Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'
  ];
  return '${date.day} ${months[date.month - 1]} ${date.year}';
}
