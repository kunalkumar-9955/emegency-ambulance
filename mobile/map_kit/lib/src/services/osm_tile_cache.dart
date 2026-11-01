import 'dart:math' as math;

import 'package:dio_cache_interceptor/dio_cache_interceptor.dart';
import 'package:flutter_map/flutter_map.dart';
import 'package:flutter_map_cache/flutter_map_cache.dart';
import 'package:http/http.dart' as http;
import '../config/map_env.dart';

/// OpenStreetMap tiles with disk cache (free, no API key).
class OsmTileCache {
  static MemCacheStore? _store;
  static CachedTileProvider? _cachedProvider;

  static TileLayer buildTileLayer({bool darkMode = false}) {
    _store ??= MemCacheStore();
    _cachedProvider ??= CachedTileProvider(
      store: _store!,
      cachePolicy: CachePolicy.forceCache,
    );

    final urlTemplate = darkMode ? MapEnv.osmDarkTileUrl : MapEnv.osmTileUrl;
    final subdomains = darkMode ? ['a', 'b', 'c', 'd'] : ['a', 'b', 'c'];

    return TileLayer(
      urlTemplate: urlTemplate,
      subdomains: subdomains,
      userAgentPackageName: 'com.emergencyambulance.app',
      tileProvider: _cachedProvider,
      maxZoom: 19,
      minZoom: 3,
      keepBuffer: 2,
      panBuffer: 1,
    );
  }

  static Future<void> warmCacheForBounds({
    required double south,
    required double west,
    required double north,
    required double east,
    int zoom = 14,
  }) async {
    final client = http.Client();
    try {
      for (var z = zoom - 1; z <= zoom; z++) {
        final xStart = _lonToTileX(west, z);
        final xEnd = _lonToTileX(east, z);
        final yStart = _latToTileY(north, z);
        final yEnd = _latToTileY(south, z);
        for (var x = xStart; x <= xEnd && x <= xStart + 3; x++) {
          for (var y = yStart; y <= yEnd && y <= yStart + 3; y++) {
            final url = MapEnv.osmTileUrl
                .replaceAll('{z}', '$z')
                .replaceAll('{x}', '$x')
                .replaceAll('{y}', '$y');
            await client.get(Uri.parse(url)).timeout(const Duration(seconds: 5));
          }
        }
      }
    } catch (_) {
      // Best-effort offline warm
    } finally {
      client.close();
    }
  }

  static int _lonToTileX(double lon, int z) =>
      ((lon + 180) / 360 * (1 << z)).floor();

  static int _latToTileY(double lat, int z) {
    final latRad = lat * math.pi / 180;
    return ((1 -
                (math.log(math.tan(latRad) + 1 / math.cos(latRad)) / math.pi)) /
            2 *
        (1 << z))
        .floor();
  }
}
