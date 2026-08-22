import 'package:flutter/material.dart';

import 'app_database.dart';
import 'app_store.dart';
import 'screens/app_shell.dart';
import 'screens/onboarding_screen.dart';
import 'theme.dart';

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();
  final store = AppStore(AppDatabase());
  await store.load();
  runApp(MuscleTrackApp(store: store));
}

class MuscleTrackApp extends StatefulWidget {
  final AppStore store;
  const MuscleTrackApp({super.key, required this.store});

  @override
  State<MuscleTrackApp> createState() => _MuscleTrackAppState();
}

class _MuscleTrackAppState extends State<MuscleTrackApp> {
  @override
  void initState() {
    super.initState();
    widget.store.addListener(_refresh);
  }

  @override
  void dispose() {
    widget.store.removeListener(_refresh);
    super.dispose();
  }

  void _refresh() => setState(() {});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'MuscleTrack T2D',
      theme: buildAppTheme(),
      home: widget.store.loading
          ? const Scaffold(body: Center(child: CircularProgressIndicator()))
          : widget.store.profile == null
              ? OnboardingScreen(store: widget.store)
              : AppShell(store: widget.store),
    );
  }
}
