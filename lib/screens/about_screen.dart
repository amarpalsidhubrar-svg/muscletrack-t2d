import 'package:flutter/material.dart';

import '../app_store.dart';

class AboutScreen extends StatelessWidget {
  final AppStore store;
  const AboutScreen({super.key, required this.store});

  @override
  Widget build(BuildContext context) {
    return ListView(
      padding: const EdgeInsets.fromLTRB(16, 12, 16, 110),
      children: [
        Text(
          'About MuscleTrack',
          style: Theme.of(context)
              .textTheme
              .headlineSmall
              ?.copyWith(fontWeight: FontWeight.w900),
        ),
        const SizedBox(height: 16),
        const Card(
          child: Padding(
            padding: EdgeInsets.all(16),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  'Version 0.3',
                  style: TextStyle(fontWeight: FontWeight.w800, fontSize: 17),
                ),
                SizedBox(height: 10),
                Text(
                  'MuscleTrack is a general workout log for recording training sessions, exercises, sets, repetitions, load, duration and notes. It also provides a training calendar, workout history and strength-progress summaries.',
                ),
                SizedBox(height: 12),
                Text(
                  '• Local device storage only\n'
                  '• Workout logging and editing\n'
                  '• Training calendar\n'
                  '• Sets, reps and load tracking\n'
                  '• Training-volume summaries\n'
                  '• Estimated 1RM for strength trends\n'
                  '• No cloud account\n'
                  '• No advertising or analytics in this version',
                ),
              ],
            ),
          ),
        ),
        const SizedBox(height: 12),
        Card(
          child: Padding(
            padding: const EdgeInsets.all(16),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  'Privacy',
                  style: Theme.of(context)
                      .textTheme
                      .titleMedium
                      ?.copyWith(fontWeight: FontWeight.w800),
                ),
                const SizedBox(height: 8),
                const Text(
                  'Workout records and your local profile are stored on this Android device. This version does not send workout records to the developer, does not use a developer-operated cloud database, and does not include advertising or analytics services.\n\n'
                  'If you upgraded from an older version of the app, older locally stored records may remain on the device until you delete all app data or uninstall the app. Those records are not uploaded by Version 0.3.\n\n'
                  'You can delete all locally stored app records using the control below.',
                ),
              ],
            ),
          ),
        ),
        const SizedBox(height: 22),
        OutlinedButton.icon(
          icon: const Icon(Icons.delete_forever_outlined),
          label: const Text('Delete all local app data'),
          onPressed: () async {
            final confirmed = await showDialog<bool>(
              context: context,
              builder: (context) => AlertDialog(
                title: const Text('Delete all data?'),
                content: const Text(
                  'This permanently removes locally stored MuscleTrack data from this device.',
                ),
                actions: [
                  TextButton(
                    onPressed: () => Navigator.pop(context, false),
                    child: const Text('Cancel'),
                  ),
                  FilledButton(
                    onPressed: () => Navigator.pop(context, true),
                    child: const Text('Delete'),
                  ),
                ],
              ),
            );
            if (confirmed == true) await store.reset();
          },
        ),
      ],
    );
  }
}
