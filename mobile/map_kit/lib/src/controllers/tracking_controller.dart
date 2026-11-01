import 'dart:async';

import 'package:flutter/foundation.dart';
import 'package:latlong2/latlong.dart';

import '../config/map_env.dart';
import '../models/map_models.dart';
import '../services/map_service.dart';
import '../services/map_websocket_service.dart';
import 'map_controller.dart';

/// Live tracking: WebSocket driver GPS + OSRM route refresh (free).
class TrackingController extends ChangeNotifier {
  TrackingController({
    required MapService mapService,
    required EmergencyMapController mapController,
    required String emergencyId,
    LatLng? patientLocation,
    LatLng? destinationLocation,
  })  : _mapService = mapService,
        _mapController = mapController,
        _emergencyId = emergencyId {
    _state = LiveTrackingState(
      patient: patientLocation,
      destination: destinationLocation,
    );
  }

  final MapService _mapService;
  final EmergencyMapController _mapController;
  final String _emergencyId;

  LiveTrackingState _state = const LiveTrackingState();
  LiveTrackingState get state => _state;

  Timer? _routeRefreshTimer;
  StreamSubscription<DriverGpsUpdate>? _wsSub;
  StreamSubscription<Map<String, dynamic>>? _eventSub;

  Future<void> start() async {
    if (_state.patient != null && _state.destination != null) {
      _mapController.setSourceDestination(
        source: _state.patient!,
        destination: _state.destination!,
      );
      await _refreshRoute();
    }

    _mapService.websocket.connectEmergency(_mapService.wsBase, _emergencyId);
    _wsSub = _mapService.websocket.driverLocations.listen(_handleDriverGps);
    _eventSub = _mapService.websocket.emergencyEvents.listen(_handleEmergencyEvent);

    _routeRefreshTimer = Timer.periodic(
      Duration(seconds: MapEnv.routeRefreshSeconds),
      (_) => _refreshRoute(),
    );

    notifyListeners();
  }

  void _handleDriverGps(DriverGpsUpdate update) {
    _state = _state.copyWith(
      driver: update.position,
      etaMinutes: update.etaMinutes ?? _state.etaMinutes,
    );
    _mapController.addAmbulanceMarker(
      update.driverId ?? 'driver',
      update.position,
      label: 'Ambulance',
    );
    notifyListeners();
    _refreshRoute();
  }

  void _handleEmergencyEvent(Map<String, dynamic> data) {
    if (data['event'] == 'gps_update') {
      final lat = (data['lat'] as num?)?.toDouble();
      final lng = (data['lng'] as num?)?.toDouble();
      if (lat != null && lng != null) {
        _handleDriverGps(DriverGpsUpdate(
          position: LatLng(lat, lng),
          etaMinutes: (data['eta_minutes'] as num?)?.toInt(),
        ));
      }
    }
    if (data['eta'] != null || data['eta_minutes'] != null) {
      _state = _state.copyWith(
        etaMinutes: (data['eta'] ?? data['eta_minutes']) as int?,
      );
      notifyListeners();
    }
  }

  Future<void> _refreshRoute() async {
    final dest = _state.destination;
    final patient = _state.patient;
    if (dest == null || patient == null) return;

    await _mapController.drawRoute(patient, dest, driver: _state.driver);
    _state = _state.copyWith(route: _mapController.activeRoute);
    if (_mapController.activeRoute != null) {
      _state = _state.copyWith(
        etaMinutes: _mapController.activeRoute!.durationMinutes,
      );
    }
    notifyListeners();
  }

  @override
  void dispose() {
    _routeRefreshTimer?.cancel();
    _wsSub?.cancel();
    _eventSub?.cancel();
    _mapService.websocket.disconnect();
    super.dispose();
  }
}
