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
        Card(
          child: const Padding(
            padding: EdgeInsets.all(16),
            child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
              Text('Version 0.1', style: TextStyle(fontWeight: FontWeight.w800, fontSize: 17)),
              SizedBox(height: 8),
              Text('• Local device storage only\n• No diagnosis or treatment recommendations\n• No medication-change advice\n• No cloud account\n• No smartwatch sync yet\n• No research upload yet'),
            ]),
          ),
        ),
        const SizedBox(height: 12),
        Card(
          child: Padding(
            padding: const EdgeInsets.all(16),
            child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
              Text('Privacy in this MVP', style: Theme.of(context).textTheme.titleMedium?.copyWith(fontWeight: FontWeight.w800)),
              const SizedBox(height: 8),
              const Text('Entries are stored in the app database on this device. Version 0.1 does not send data to a server.'),
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
