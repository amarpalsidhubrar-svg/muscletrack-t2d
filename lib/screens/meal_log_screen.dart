import 'package:flutter/material.dart';

import '../app_store.dart';
import '../calculations.dart';
import '../models.dart';

class MealLogScreen extends StatefulWidget {
  final AppStore store;

  const MealLogScreen({super.key, required this.store});

  @override
  State<MealLogScreen> createState() => _MealLogScreenState();
}

class _MealLogScreenState extends State<MealLogScreen> {
  final _description = TextEditingController();
  final _calories = TextEditingController();
  final _protein = TextEditingController();
  final _carbs = TextEditingController();
  final _fat = TextEditingController();
  final _fibre = TextEditingController();

  String _mealType = 'Breakfast';
  double _activityFactor = 1.375;

  @override
  void dispose() {
    _description.dispose();
    _calories.dispose();
    _protein.dispose();
    _carbs.dispose();
    _fat.dispose();
    _fibre.dispose();
    super.dispose();
  }

  void _selectAll(TextEditingController controller) {
    if (controller.text.isEmpty) return;
    controller.selection = TextSelection(baseOffset: 0, extentOffset: controller.text.length);
  }

  Future<void> _save() async {
    final calories = double.tryParse(_calories.text);
    if (_description.text.trim().isEmpty || calories == null || calories <= 0) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Add a meal description and estimated calories.')),
      );
      return;
    }

    await widget.store.addMeal(
      MealEntry(
        date: DateTime.now(),
        mealType: _mealType,
        description: _description.text.trim(),
        calories: calories,
        proteinG: double.tryParse(_protein.text),
        carbsG: double.tryParse(_carbs.text),
        fatG: double.tryParse(_fat.text),
        fibreG: double.tryParse(_fibre.text),
      ),
    );

    _description.clear();
    _calories.clear();
    _protein.clear();
    _carbs.clear();
    _fat.clear();
    _fibre.clear();
    if (mounted) {
      setState(() {});
      ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('Meal logged.')));
    }
  }

  @override
  Widget build(BuildContext context) {
    final profile = widget.store.profile!;
    final estimatedDaily = estimatedDailyEnergyRequirement(
      weightKg: widget.store.currentWeightKg,
      heightCm: profile.heightCm,
      age: profile.age,
      sex: profile.sex,
      activityFactor: _activityFactor,
    );
    final calorieProgress = estimatedDaily <= 0
        ? 0.0
        : (widget.store.todayMealCalories / estimatedDaily).clamp(0.0, 1.0);

    return Scaffold(
      appBar: AppBar(title: const Text('Log Meal')),
      body: ListView(
        padding: const EdgeInsets.fromLTRB(16, 10, 16, 32),
        children: [
          Text(
            'Meal type',
            style: Theme.of(context).textTheme.titleSmall?.copyWith(fontWeight: FontWeight.w800),
          ),
          const SizedBox(height: 8),
          Wrap(
            spacing: 8,
            runSpacing: 8,
            children: ['Breakfast', 'Lunch', 'Dinner', 'Snack', 'Other']
                .map(
                  (type) => ChoiceChip(
                    label: Text(type),
                    selected: _mealType == type,
                    onSelected: (_) => setState(() => _mealType = type),
                  ),
                )
                .toList(),
          ),
          const SizedBox(height: 18),
          TextField(
            controller: _description,
            decoration: const InputDecoration(
              labelText: 'Food / meal description',
              hintText: 'e.g. Greek yoghurt, berries and oats',
            ),
          ),
          const SizedBox(height: 12),
          TextField(
            controller: _calories,
            keyboardType: const TextInputType.numberWithOptions(decimal: true),
            onTap: () => _selectAll(_calories),
            decoration: const InputDecoration(
              labelText: 'Calories',
              suffixText: 'kcal',
            ),
          ),
          const SizedBox(height: 12),
          Row(
            children: [
              Expanded(child: _numberField(_protein, 'Protein', 'g')),
              const SizedBox(width: 10),
              Expanded(child: _numberField(_carbs, 'Carbohydrate', 'g')),
            ],
          ),
          const SizedBox(height: 10),
          Row(
            children: [
              Expanded(child: _numberField(_fat, 'Fat', 'g')),
              const SizedBox(width: 10),
              Expanded(child: _numberField(_fibre, 'Fibre', 'g')),
            ],
          ),
          const SizedBox(height: 16),
          FilledButton(
            onPressed: _save,
            child: const Padding(
              padding: EdgeInsets.symmetric(vertical: 14),
              child: Text('Save Meal'),
            ),
          ),
          const SizedBox(height: 18),
          Card(
            color: const Color(0xFFEAF6F1),
            child: Padding(
              padding: const EdgeInsets.all(16),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Row(
                    children: [
                      Icon(Icons.bolt, color: Theme.of(context).colorScheme.primary),
                      const SizedBox(width: 7),
                      Text(
                        'Estimated daily energy requirement',
                        style: Theme.of(context).textTheme.titleSmall?.copyWith(
                              fontWeight: FontWeight.w900,
                            ),
                      ),
                    ],
                  ),
                  const SizedBox(height: 8),
                  Text(
                    '~ ${estimatedDaily.toStringAsFixed(0)} kcal/day',
                    style: Theme.of(context).textTheme.headlineSmall?.copyWith(
                          fontWeight: FontWeight.w900,
                          color: const Color(0xFF17312A),
                        ),
                  ),
                  const SizedBox(height: 10),
                  DropdownButtonFormField<double>(
                    initialValue: _activityFactor,
                    decoration: const InputDecoration(labelText: 'Usual activity level'),
                    items: const [
                      DropdownMenuItem(value: 1.2, child: Text('Sedentary')),
                      DropdownMenuItem(value: 1.375, child: Text('Lightly active')),
                      DropdownMenuItem(value: 1.55, child: Text('Moderately active')),
                      DropdownMenuItem(value: 1.725, child: Text('Very active')),
                    ],
                    onChanged: (v) => setState(() => _activityFactor = v ?? _activityFactor),
                  ),
                  const SizedBox(height: 8),
                  Text(
                    'Based on age, sex, height, current weight and activity level. Estimate only; individual energy requirements vary.',
                    style: Theme.of(context).textTheme.bodySmall,
                  ),
                ],
              ),
            ),
          ),
          const SizedBox(height: 14),
          Card(
            child: Padding(
              padding: const EdgeInsets.all(16),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    "Today's nutrition",
                    style: Theme.of(context).textTheme.titleMedium?.copyWith(fontWeight: FontWeight.w900),
                  ),
                  const SizedBox(height: 10),
                  Row(
                    children: [
                      Expanded(
                        child: Text(
                          '${widget.store.todayMealCalories.toStringAsFixed(0)} kcal',
                          style: Theme.of(context).textTheme.titleLarge?.copyWith(fontWeight: FontWeight.w900),
                        ),
                      ),
                      Text('${widget.store.todayMeals.length} meals'),
                    ],
                  ),
                  const SizedBox(height: 8),
                  ClipRRect(
                    borderRadius: BorderRadius.circular(20),
                    child: LinearProgressIndicator(
                      minHeight: 7,
                      value: calorieProgress,
                      backgroundColor: const Color(0xFFEAF0ED),
                    ),
                  ),
                  const SizedBox(height: 10),
                  Text('${widget.store.todayProteinG.toStringAsFixed(0)} g protein logged'),
                ],
              ),
            ),
          ),
          const SizedBox(height: 20),
          Text(
            'Recent meals',
            style: Theme.of(context).textTheme.titleMedium?.copyWith(fontWeight: FontWeight.w900),
          ),
          const SizedBox(height: 8),
          if (widget.store.meals.isEmpty)
            const Card(
              child: Padding(
                padding: EdgeInsets.all(16),
                child: Text('No meals logged yet.'),
              ),
            ),
          ...widget.store.meals.take(12).map(
                (meal) => Padding(
                  padding: const EdgeInsets.only(bottom: 8),
                  child: Card(
                    child: ListTile(
                      leading: CircleAvatar(
                        backgroundColor: const Color(0xFFE6F5EF),
                        child: Icon(
                          Icons.restaurant_outlined,
                          size: 18,
                          color: Theme.of(context).colorScheme.primary,
                        ),
                      ),
                      title: Text('${meal.mealType}: ${meal.description}'),
                      subtitle: Text(
                        '${shortDate(meal.date)} • ${meal.calories.toStringAsFixed(0)} kcal'
                        '${meal.proteinG == null ? '' : ' • ${meal.proteinG!.toStringAsFixed(0)} g protein'}',
                      ),
                      trailing: meal.id == null
                          ? null
                          : IconButton(
                              tooltip: 'Delete meal',
                              icon: const Icon(Icons.delete_outline),
                              onPressed: () async {
                                await widget.store.deleteMeal(meal.id!);
                                if (mounted) setState(() {});
                              },
                            ),
                    ),
                  ),
                ),
              ),
        ],
      ),
    );
  }

  Widget _numberField(TextEditingController controller, String label, String suffix) {
    return TextField(
      controller: controller,
      keyboardType: const TextInputType.numberWithOptions(decimal: true),
      onTap: () => _selectAll(controller),
      decoration: InputDecoration(labelText: label, hintText: 'Optional', suffixText: suffix),
    );
  }
}
