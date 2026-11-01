import 'package:flutter/material.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'package:latlong2/latlong.dart';
import 'package:map_kit/map_kit.dart';

import '../core/config.dart';
import 'driver_gps_service.dart';

class DriverMapIntegration {
  static MapService? _service;
  static DriverGpsService? _gps;

  static Future<MapService> create() async {
    if (_service != null) return _service!;
    await MapEnv.load(fileName: '.env');
    final token = await const FlutterSecureStorage().read(key: 'access_token');
    _service = MapService(
      apiBase: DriverAppConfig.apiBase,
      wsBase: DriverAppConfig.wsBase,
      authToken: token,
    );
    return _service!;
  }

  static Future<void> openNavigation({
    required BuildContext context,
    required String emergencyId,
    required LatLng patientLocation,
    LatLng? hospitalLocation,
  }) async {
    final svc = await create();
    final token = await const FlutterSecureStorage().read(key: 'access_token') ?? '';

    _gps?.stop();
    _gps = DriverGpsService(emergencyId: emergencyId, authToken: token);
    _gps!.start();

    if (!context.mounted) return;
    Navigator.of(context).push(
      MaterialPageRoute(
        builder: (_) => LiveTrackingScreen(
          mapService: svc,
          emergencyId: emergencyId,
          patientLocation: patientLocation,
          destinationLocation: hospitalLocation ?? LatLng(
            patientLocation.latitude + 0.015,
            patientLocation.longitude + 0.015,
          ),
          onSendDriverGps: null,
        ),
      ),
    );
  }

  static void openFleetMap(BuildContext context) {
    create().then((svc) {
      if (!context.mounted) return;
      Navigator.of(context).push(
        MaterialPageRoute(builder: (_) => MapScreen(mapService: svc)),
      );
    });
  }

  static void stopGps() => _gps?.stop();
}
