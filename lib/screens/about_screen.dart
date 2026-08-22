import 'package:flutter/material.dart';

import '../app_store.dart';
import '../widgets/common.dart';

class AboutScreen extends StatelessWidget {
  final AppStore store;
  const AboutScreen({super.key, required this.store});

  @override
  Widget build(BuildContext context) {
    return ListView(
      padding: const EdgeInsets.fromLTRB(16, 12, 16, 110),
      children: [
        Text('About & data', style: Theme.of(context).textTheme.headlineSmall?.copyWith(fontWeight: FontWeight.w900)),
        const SizedBox(height: 16),
        const MonitoringNotice(),
        const SizedBox(height: 12),
        const Card(
          child: Padding(
            padding: EdgeInsets.all(16),
            child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
              Text('Version 0.1', style: TextStyle(fontWeight: FontWeight.w800, fontSize: 17)),
              SizedBox(height: 8),
              Text('• Local device storage only\n• No diagnosis or treatment recommendations\n• No medication-change advice\n• No cloud account\n• No advertising or analytics\n• No smartwatch sync yet\n• No research upload yet'),
            ]),
          ),
        ),
        const SizedBox(height: 12),
        Card(
          child: Padding(
            padding: const EdgeInsets.all(16),
            child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
              Text('Privacy policy', style: Theme.of(context).textTheme.titleMedium?.copyWith(fontWeight: FontWeight.w800)),
              const SizedBox(height: 8),
              const Text(
                'MuscleTrack T2D is a monitoring and self-tracking app for adults. Users may enter profile information, weight and body-composition values, medication names and doses, physical activity, strength-training records and goals.\n\n'
                'Version 0.1 stores these entries locally in the app database on this Android device. It does not transmit these records to the developer, does not use a developer-operated cloud database, and does not include advertising or analytics services.\n\n'
                'Version 0.1 does not share user-entered health information with third parties. If a future version adds optional cloud sync, Health Connect, research export or another external-data feature, the privacy policy and in-app disclosures will be updated before that feature is released.\n\n'
                'Users can delete all locally stored app records using the control below. Uninstalling the app also removes app-specific local storage, subject to Android device backup and operating-system behaviour.\n\n'
                'The app is for monitoring and informational self-tracking only. It does not diagnose, treat, cure or prevent disease, does not prescribe exercise or nutrition, and does not recommend starting, stopping or changing medication. Medical decisions should be made with an appropriately qualified healthcare professional.'
              ),
              const SizedBox(height: 10),
              const Text('Privacy policy effective: 22 August 2026', style: TextStyle(fontWeight: FontWeight.w600)),
            ]),
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
                content: const Text('This permanently removes the local profile, weight, workout, goal and medication records from this app.'),
                actions: [
                  TextButton(onPressed: () => Navigator.pop(context, false), child: const Text('Cancel')),
                  FilledButton(onPressed: () => Navigator.pop(context, true), child: const Text('Delete')),
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
