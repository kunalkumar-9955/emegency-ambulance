import 'dart:convert';

import 'package:http/http.dart' as http;
import 'package:latlong2/latlong.dart';

import '../config/map_env.dart';
import '../models/map_models.dart';
import 'location_service.dart';
import 'map_websocket_service.dart';
import 'osm_tile_cache.dart';
import 'osrm_routing_service.dart';

/// Facade: OSM tiles + OSRM routes + Django APIs (unchanged).
class MapService {
  MapService({
    required this.apiBase,
    required this.wsBase,
    String? authToken,
  }) : _authToken = authToken;

  final String apiBase;
  final String wsBase;
  String? _authToken;

  final LocationService location = LocationService.instance;
  final OsrmRoutingService routing = OsrmRoutingService.instance;
  final MapWebSocketService websocket = MapWebSocketService();

  void setAuthToken(String? token) => _authToken = token;

  Map<String, String> get _headers => {
        'Content-Type': 'application/json',
        if (_authToken != null) 'Authorization': 'Bearer $_authToken',
      };

  Future<LatLng?> currentUserLocation() => location.getCurrentLatLng();

  Future<List<MapMarkerData>> fetchNearbyAmbulances(LatLng center) async {
    final markers = <MapMarkerData>[];
    try {
      final res = await http
          .get(Uri.parse('$apiBase/hospitals/'), headers: _headers)
          .timeout(const Duration(seconds: 10));
      if (res.statusCode == 200) {
        final body = jsonDecode(res.body);
        final items = body is Map && body.containsKey('results')
            ? body['results'] as List
            : body is List
                ? body
                : <dynamic>[];
        for (final h in items) {
          final lat = double.tryParse('${h['latitude']}');
          final lng = double.tryParse('${h['longitude']}');
          if (lat != null && lng != null) {
            final pos = LatLng(lat, lng);
            if (_withinRadius(center, pos, MapEnv.nearbyRadiusKm)) {
              markers.add(MapMarkerData(
                id: 'hospital_${h['id']}',
                position: pos,
                type: MapMarkerType.hospital,
                label: h['name']?.toString(),
              ));
            }
          }
        }
      }
    } catch (_) {}
    return markers;
  }

  bool _withinRadius(LatLng a, LatLng b, double km) {
    const dist = Distance();
    return dist.distance(a, b) <= km * 1000;
  }

  Future<RouteSegment?> buildEmergencyRoute({
    required LatLng source,
    required LatLng destination,
    LatLng? driver,
  }) async {
    final from = driver ?? source;
    return routing.getRoute(from: from, to: destination, emergencyHighlight: true);
  }

  Future<void> prefetchOfflineArea(LatLng center) async {
    const delta = 0.05;
    await OsmTileCache.warmCacheForBounds(
      south: center.latitude - delta,
      north: center.latitude + delta,
      west: center.longitude - delta,
      east: center.longitude + delta,
    );
  }
}
