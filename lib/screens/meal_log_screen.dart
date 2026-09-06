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

    return Scaffold(
      appBar: AppBar(title: const Text('Meals & nutrition')),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          Card(
            color: Theme.of(context).colorScheme.primaryContainer,
            child: Padding(
              padding: const EdgeInsets.all(16),
              child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                Text('Estimated daily energy', style: Theme.of(context).textTheme.titleMedium?.copyWith(fontWeight: FontWeight.w800)),
                const SizedBox(height: 6),
                Text('${estimatedDaily.toStringAsFixed(0)} kcal/day', style: Theme.of(context).textTheme.headlineSmall?.copyWith(fontWeight: FontWeight.w900)),
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
                  'Informational estimate based on age, sex, height, current weight and activity level. Individual energy needs vary; this is not a prescribed calorie target.',
                  style: Theme.of(context).textTheme.bodySmall,
                ),
              ]),
            ),
          ),
          const SizedBox(height: 12),
          Card(
            child: Padding(
              padding: const EdgeInsets.all(16),
              child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                Text('Today', style: Theme.of(context).textTheme.titleMedium?.copyWith(fontWeight: FontWeight.w800)),
                const SizedBox(height: 8),
                Text('${widget.store.todayMealCalories.toStringAsFixed(0)} kcal logged'),
                Text('${widget.store.todayProteinG.toStringAsFixed(0)} g protein logged'),
              ]),
            ),
          ),
          const SizedBox(height: 16),
          DropdownButtonFormField<String>(
            initialValue: _mealType,
            decoration: const InputDecoration(labelText: 'Meal'),
            items: const [
              DropdownMenuItem(value: 'Breakfast', child: Text('Breakfast')),
              DropdownMenuItem(value: 'Lunch', child: Text('Lunch')),
              DropdownMenuItem(value: 'Dinner', child: Text('Dinner')),
              DropdownMenuItem(value: 'Snack', child: Text('Snack')),
              DropdownMenuItem(value: 'Other', child: Text('Other')),
            ],
            onChanged: (v) => setState(() => _mealType = v ?? _mealType),
          ),
          const SizedBox(height: 12),
          TextField(
            controller: _description,
            decoration: const InputDecoration(labelText: 'Meal or food', hintText: 'e.g. tuna sandwich and fruit'),
          ),
          const SizedBox(height: 12),
          TextField(
            controller: _calories,
            keyboardType: const TextInputType.numberWithOptions(decimal: true),
            onTap: () => _selectAll(_calories),
            decoration: const InputDecoration(labelText: 'Estimated calories (kcal)'),
          ),
          const SizedBox(height: 12),
          Row(children: [
            Expanded(child: _numberField(_protein, 'Protein (g)')),
            const SizedBox(width: 10),
            Expanded(child: _numberField(_carbs, 'Carbs (g)')),
          ]),
          const SizedBox(height: 10),
          Row(children: [
            Expanded(child: _numberField(_fat, 'Fat (g)')),
            const SizedBox(width: 10),
            Expanded(child: _numberField(_fibre, 'Fibre (g)')),
          ]),
          const SizedBox(height: 16),
          FilledButton.icon(
            onPressed: _save,
            icon: const Icon(Icons.restaurant),
            label: const Padding(
              padding: EdgeInsets.symmetric(vertical: 14),
              child: Text('Log meal'),
            ),
          ),
          const SizedBox(height: 20),
          Text('Recent meals', style: Theme.of(context).textTheme.titleMedium?.copyWith(fontWeight: FontWeight.w800)),
          const SizedBox(height: 8),
          if (widget.store.meals.isEmpty)
            const Card(child: Padding(padding: EdgeInsets.all(16), child: Text('No meals logged yet.'))),
          ...widget.store.meals.take(12).map((meal) => Card(
                child: ListTile(
                  leading: const CircleAvatar(child: Icon(Icons.restaurant_outlined, size: 18)),
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
              )),
        ],
      ),
    );
  }

  Widget _numberField(TextEditingController controller, String label) {
    return TextField(
      controller: controller,
      keyboardType: const TextInputType.numberWithOptions(decimal: true),
      onTap: () => _selectAll(controller),
      decoration: InputDecoration(labelText: label, hintText: 'Optional'),
    );
  }
}
