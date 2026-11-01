import 'package:flutter_dotenv/flutter_dotenv.dart';

/// Free map configuration — OpenStreetMap tiles + OSRM routing only.
class MapEnv {
  static bool _loaded = false;

  static Future<void> load({String fileName = '.env'}) async {
    if (_loaded) return;
    try {
      await dotenv.load(fileName: fileName);
    } catch (_) {
      // Optional .env; defaults work without any API keys
    }
    _loaded = true;
  }

  /// OSRM route API base (self-host in production for heavy load).
  static String get osrmBaseUrl =>
      dotenv.env['OSRM_BASE_URL'] ??
      const String.fromEnvironment(
        'OSRM_BASE_URL',
        defaultValue: 'https://router.project-osrm.org',
      );

  static String get osmTileUrl =>
      dotenv.env['OSM_TILE_URL'] ?? 'https://tile.openstreetmap.org/{z}/{x}/{y}.png';

  static String get osmDarkTileUrl =>
      dotenv.env['OSM_DARK_TILE_URL'] ??
      'https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}.png';

  static int get routeRefreshSeconds =>
      int.tryParse(dotenv.env['ROUTE_REFRESH_SECONDS'] ?? '5') ?? 5;

  static double get nearbyRadiusKm =>
      double.tryParse(dotenv.env['NEARBY_AMBULANCE_RADIUS_KM'] ?? '15') ?? 15;

  /// Nominatim geocoding (free, rate-limited).
  static String get nominatimBaseUrl =>
      dotenv.env['NOMINATIM_BASE_URL'] ?? 'https://nominatim.openstreetmap.org';
}
