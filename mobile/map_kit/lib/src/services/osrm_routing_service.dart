import 'dart:convert';

import 'package:http/http.dart' as http;
import 'package:latlong2/latlong.dart';

import '../config/map_env.dart';
import '../models/map_models.dart';

/// Free routing via OSRM (Open Source Routing Machine).
class OsrmRoutingService {
  static final OsrmRoutingService instance = OsrmRoutingService._();
  OsrmRoutingService._();

  Future<RouteSegment?> getRoute({
    required LatLng from,
    required LatLng to,
    bool emergencyHighlight = true,
  }) async {
    final base = MapEnv.osrmBaseUrl.replaceAll(RegExp(r'/+$'), '');
    final coords =
        '${from.longitude},${from.latitude};${to.longitude},${to.latitude}';
    final uri = Uri.parse('$base/route/v1/driving/$coords').replace(
      queryParameters: {
        'overview': 'full',
        'geometries': 'geojson',
        'steps': 'false',
      },
    );

    try {
      final res = await http.get(uri).timeout(const Duration(seconds: 20));
      if (res.statusCode != 200) return _fallbackRoute(from, to, emergencyHighlight);

      final data = jsonDecode(res.body) as Map<String, dynamic>;
      if (data['code'] != 'Ok') return _fallbackRoute(from, to, emergencyHighlight);

      final routes = data['routes'] as List?;
      if (routes == null || routes.isEmpty) {
        return _fallbackRoute(from, to, emergencyHighlight);
      }

      final route = routes.first as Map<String, dynamic>;
      final geometry = route['geometry'] as Map<String, dynamic>?;
      final coordinates = geometry?['coordinates'] as List? ?? [];

      final points = coordinates
          .map((c) => LatLng((c[1] as num).toDouble(), (c[0] as num).toDouble()))
          .toList();

      if (points.length < 2) return _fallbackRoute(from, to, emergencyHighlight);

      final distanceM = (route['distance'] as num?)?.toDouble() ?? 0;
      final durationSec = (route['duration'] as num?)?.toDouble() ?? 0;

      return RouteSegment(
        points: points,
        distanceKm: distanceM / 1000,
        durationMinutes: (durationSec / 60).ceil().clamp(1, 999),
        isEmergency: emergencyHighlight,
      );
    } catch (_) {
      return _fallbackRoute(from, to, emergencyHighlight);
    }
  }

  RouteSegment _fallbackRoute(LatLng from, LatLng to, bool emergency) {
    return RouteSegment(
      points: [from, to],
      distanceKm: const Distance().distance(from, to) / 1000,
      durationMinutes: 10,
      isEmergency: emergency,
    );
  }
}
