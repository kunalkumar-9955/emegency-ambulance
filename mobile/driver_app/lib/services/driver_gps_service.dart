import 'dart:async';
import 'dart:convert';

import 'package:http/http.dart' as http;
import 'package:latlong2/latlong.dart';
import 'package:map_kit/map_kit.dart';

import '../core/config.dart';

/// Posts driver GPS to Django API and streams position locally.
class DriverGpsService {
  DriverGpsService({
    required this.emergencyId,
    required this.authToken,
  });

  final String emergencyId;
  final String authToken;

  StreamSubscription<LatLng>? _sub;
  Timer? _heartbeat;

  void start() {
    _sub?.cancel();
    _sub = LocationService.instance.watchPosition(distanceFilterMeters: 8).listen(_postGps);
    _heartbeat = Timer.periodic(const Duration(seconds: 5), (_) async {
      final pos = LocationService.instance.lastPosition;
      if (pos != null) {
        await _postGps(LatLng(pos.latitude, pos.longitude));
      }
    });
  }

  Future<void> _postGps(LatLng pos) async {
    try {
      await http.post(
        Uri.parse('${DriverAppConfig.apiBase}/emergencies/$emergencyId/gps/'),
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer $authToken',
        },
        body: jsonEncode({
          'latitude': pos.latitude,
          'longitude': pos.longitude,
          'speed_kmh': LocationService.instance.lastPosition?.speed != null
              ? (LocationService.instance.lastPosition!.speed * 3.6)
              : null,
          'heading': LocationService.instance.lastPosition?.heading,
        }),
      );
    } catch (_) {}
  }

  void stop() {
    _sub?.cancel();
    _heartbeat?.cancel();
  }
}
