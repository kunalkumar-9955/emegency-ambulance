import 'package:flutter/material.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'package:latlong2/latlong.dart';
import 'package:map_kit/map_kit.dart';

import '../core/config.dart';

/// Wires map_kit to patient app API + auth.
class PatientMapIntegration {
  static MapService? _service;

  static Future<MapService> create() async {
    if (_service != null) return _service!;
    await MapEnv.load(fileName: '.env');
    final token = await const FlutterSecureStorage().read(key: 'access_token');
    _service = MapService(
      apiBase: AppConfig.apiBase,
      wsBase: AppConfig.wsBase,
      authToken: token,
    );
    return _service!;
  }

  static void openMapScreen(BuildContext context) {
    create().then((svc) {
      if (!context.mounted) return;
      Navigator.of(context).push(
        MaterialPageRoute(builder: (_) => MapScreen(mapService: svc)),
      );
    });
  }

  static void openLiveTracking(
    BuildContext context, {
    required String emergencyId,
    required LatLng patient,
    LatLng? destination,
  }) {
    create().then((svc) {
      if (!context.mounted) return;
      Navigator.of(context).push(
        MaterialPageRoute(
          builder: (_) => LiveTrackingScreen(
            mapService: svc,
            emergencyId: emergencyId,
            patientLocation: patient,
            destinationLocation: destination,
          ),
        ),
      );
    });
  }
}
