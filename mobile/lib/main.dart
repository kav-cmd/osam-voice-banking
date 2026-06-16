import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'screens/voice_banking_screen.dart';

void main() {
  WidgetsFlutterBinding.ensureInitialized();
  SystemChrome.setPreferredOrientations([
    DeviceOrientation.portraitUp,
    DeviceOrientation.portraitDown,
  ]);
  runApp(const OSAMApp());
}

class OSAMApp extends StatelessWidget {
  const OSAMApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'OSAM Voice Banking',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        brightness: Brightness.dark,
        colorScheme: ColorScheme.dark(
          primary: const Color(0xFF6366F1),
          secondary: const Color(0xFF818CF8),
          surface: const Color(0xFF1E293B),
        ),
        scaffoldBackgroundColor: const Color(0xFF0F172A),
        useMaterial3: true,
      ),
      home: const VoiceBankingScreen(),
    );
  }
}
