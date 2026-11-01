import 'package:geolocator/geolocator.dart';
import 'package:latlong2/latlong.dart';
import 'package:permission_handler/permission_handler.dart';

/// Handles location permissions and current position (optimized: single stream).
class LocationService {
  static final LocationService instance = LocationService._();
  LocationService._();

  Position? _lastPosition;
  Stream<Position>? _positionStream;

  Position? get lastPosition => _lastPosition;

  Future<bool> ensurePermission() async {
    var status = await Permission.locationWhenInUse.status;
    if (status.isDenied) {
      status = await Permission.locationWhenInUse.request();
    }
    if (status.isPermanentlyDenied) return false;

    final serviceEnabled = await Geolocator.isLocationServiceEnabled();
    if (!serviceEnabled) return false;

    var geoPermission = await Geolocator.checkPermission();
    if (geoPermission == LocationPermission.denied) {
      geoPermission = await Geolocator.requestPermission();
    }
    return geoPermission == LocationPermission.always ||
        geoPermission == LocationPermission.whileInUse;
  }

  Future<LatLng?> getCurrentLatLng() async {
    if (!await ensurePermission()) return null;
    final pos = await Geolocator.getCurrentPosition(
      desiredAccuracy: LocationAccuracy.medium,
      timeLimit: const Duration(seconds: 12),
    );
    _lastPosition = pos;
    return LatLng(pos.latitude, pos.longitude);
  }

  /// Low-frequency stream for battery savings on low-end devices.
  Stream<LatLng> watchPosition({int distanceFilterMeters = 15}) async* {
    if (!await ensurePermission()) return;
    _positionStream ??= Geolocator.getPositionStream(
      locationSettings: LocationSettings(
        accuracy: LocationAccuracy.medium,
        distanceFilter: distanceFilterMeters,
      ),
    );
    await for (final pos in _positionStream!) {
      _lastPosition = pos;
      yield LatLng(pos.latitude, pos.longitude);
    }
  }

  void dispose() {
    _positionStream = null;
  }
}
