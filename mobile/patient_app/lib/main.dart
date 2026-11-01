import 'package:flutter/material.dart';
import 'package:map_kit/map_kit.dart';
import 'package:provider/provider.dart';
import 'core/config.dart';
import 'providers/auth_provider.dart';
import 'providers/emergency_provider.dart';
import 'screens/home_screen.dart';
import 'screens/login_screen.dart';
import 'services/ota_service.dart';
import 'package:firebase_core/firebase_core.dart';
import 'package:firebase_crashlytics/firebase_crashlytics.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();

  try {
    await Firebase.initializeApp();
    FlutterError.onError =
        FirebaseCrashlytics.instance.recordFlutterFatalError;
  } catch (_) {
    // Firebase optional for local builds without google-services
  }

  await MapEnv.load(fileName: '.env');

  await OtaService.checkForUpdates();

  runApp(const PatientApp());
}

class PatientApp extends StatelessWidget {
  const PatientApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MultiProvider(
      providers: [
        ChangeNotifierProvider(create: (_) => AuthProvider()),
        ChangeNotifierProvider(create: (_) => EmergencyProvider()),
      ],
      child: MaterialApp(
        title: AppConfig.appName,
        debugShowCheckedModeBanner: false,
        theme: ThemeData(
          colorScheme: ColorScheme.fromSeed(seedColor: const Color(0xFFDC2626), brightness: Brightness.light),
          useMaterial3: true,
        ),
        darkTheme: ThemeData(
          colorScheme: ColorScheme.fromSeed(seedColor: const Color(0xFFDC2626), brightness: Brightness.dark),
          useMaterial3: true,
        ),
        home: const AppEntry(),
      ),
    );
  }
}

class AppEntry extends StatelessWidget {
  const AppEntry({super.key});

  @override
  Widget build(BuildContext context) {
    final auth = context.watch<AuthProvider>();
    if (!auth.isReady) {
      return const Scaffold(body: Center(child: CircularProgressIndicator()));
    }
    return auth.isLoggedIn ? const HomeScreen() : const LoginScreen();
  }
}
